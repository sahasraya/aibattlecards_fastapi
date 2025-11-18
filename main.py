from asyncio.log import logger
import base64
from decimal import Decimal
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
import random 
import smtplib
import string 
from typing import Optional
from urllib.parse import urlparse
import uuid
import aiomysql 
from fastapi import Body, Depends, FastAPI, File, Form, Request,status, HTTPException, Query, UploadFile, requests
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse
 
from flask import jsonify
# from flask import jsonify, request
import httpx
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, datetime, timedelta 
from playwright.sync_api import sync_playwright
from pydantic import BaseModel
import requests
from dotenv import load_dotenv

load_dotenv()
 

app = FastAPI()


sync_db_config = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),  # No password
    'database': os.getenv("DB_DATABASE")
}

async_db_config = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),  # No password
    'db': os.getenv("DB_DATABASE"),
    'port': 3306,
    'minsize': 1,
    'maxsize': 10,
    'autocommit': True
    # 'ssl': {},  # Uncomment if SSL is needed
}

 

conn = mysql.connector.connect(**sync_db_config)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

pool = None

 
@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
 
    pool = await aiomysql.create_pool(**async_db_config)
    print("Database pool created.")
    await create_tables()
    try:
        
        yield
    finally:
  
        pool.terminate()
        await pool.wait_closed()
        print("Database pool terminated.")

 
app.router.lifespan_context = lifespan

# FASTAPI 


async def create_tables():
    try:
        async with aiomysql.create_pool(**async_db_config) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cursor:

                    
                    create_user_table_query = """
                    CREATE TABLE IF NOT EXISTS product (
                        id INT NOT NULL AUTO_INCREMENT,
                        userid VARCHAR(30) DEFAULT NULL,
                        productid VARCHAR(30) DEFAULT NULL,
                        productname VARCHAR(30) DEFAULT NULL,
                        productimage LONGBLOB DEFAULT NULL,
                        productcategory VARCHAR(30) DEFAULT NULL,
                        productlicense VARCHAR(30) DEFAULT NULL,
                        producttechnology VARCHAR(30) DEFAULT NULL,
                        productwebsite VARCHAR(300) DEFAULT NULL,
                        productfundingstage VARCHAR(30) DEFAULT NULL,
                        productusecaseid VARCHAR(30) DEFAULT NULL,
                        productfacebook VARCHAR(300) DEFAULT NULL,
                        productdocumentation VARCHAR(300) DEFAULT NULL,
                        productlinkedin VARCHAR(300) DEFAULT NULL,
                        productfounderid VARCHAR(30) DEFAULT NULL,
                        productdescription VARCHAR(300) DEFAULT NULL,
                        productbaseaimodelid VARCHAR(30) DEFAULT NULL,
                        productdeploymentid VARCHAR(30) DEFAULT NULL,
                        productrepositoryid VARCHAR(30) DEFAULT NULL,
                        productmediaid VARCHAR(30) DEFAULT NULL, 
                        rating TINYINT DEFAULT 0,
                        counts  VARCHAR(10) DEFAULT 0,
                        createddate DATETIME DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
                    """
                    await cursor.execute(create_user_table_query)
                    print("Table 'product' created successfully.")
                    
                    
                    
                    
                    
                    create_usecases_table_query = """
                    CREATE TABLE IF NOT EXISTS usecase (
                        id INT NOT NULL AUTO_INCREMENT,
                        userid VARCHAR(30) DEFAULT NULL,
                        productusecaseid VARCHAR(30) DEFAULT NULL, 
                        name VARCHAR(30) DEFAULT NULL, 
                        createddate DATETIME DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
                    """
                    await cursor.execute(create_usecases_table_query)
                    print("Table 'usecase' created successfully.")
                    
                    
                    
                    create_founders_table_query = """
                    CREATE TABLE IF NOT EXISTS founder (
                        id INT NOT NULL AUTO_INCREMENT,
                        userid VARCHAR(30) DEFAULT NULL,
                        productfounderid VARCHAR(30) DEFAULT NULL, 
                        name VARCHAR(30) DEFAULT NULL, 
                        createddate DATETIME DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
                    """
                    await cursor.execute(create_founders_table_query)
                    print("Table 'founder' created successfully.")
                    
                    
                    
                    create_baseaimodel_table_query = """
                    CREATE TABLE IF NOT EXISTS baseaimodel (
                        id INT NOT NULL AUTO_INCREMENT,
                        userid VARCHAR(30) DEFAULT NULL,
                        productbaseaimodelid VARCHAR(30) DEFAULT NULL, 
                        name VARCHAR(30) DEFAULT NULL, 
                        createddate DATETIME DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
                    """
                    await cursor.execute(create_baseaimodel_table_query)
                    print("Table 'baseaimodel' created successfully.")
                    
                    
                    
                    
                    create_deployment_table_query = """
                    CREATE TABLE IF NOT EXISTS deployment (
                        id INT NOT NULL AUTO_INCREMENT,
                        userid VARCHAR(30) DEFAULT NULL,
                        productdeploymentid VARCHAR(30) DEFAULT NULL, 
                        name VARCHAR(30) DEFAULT NULL, 
                        createddate DATETIME DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
                    """
                    await cursor.execute(create_deployment_table_query)
                    print("Table 'baseaimodel' created successfully.")
                    
                    
                    
                    create_repository_table_query = """
                    CREATE TABLE IF NOT EXISTS repository (
                        id INT NOT NULL AUTO_INCREMENT,
                        userid VARCHAR(30) DEFAULT NULL,
                        productrepositoryid VARCHAR(30) DEFAULT NULL, 
                        name TEXT DEFAULT NULL, 
                        createddate DATETIME DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
                    """
                    await cursor.execute(create_repository_table_query)
                    print("Table 'repository' created successfully.")

                    
                    
                    
                    
                    
                    
                    create_medeia_table_query = """
                    CREATE TABLE IF NOT EXISTS medeia (
                        id INT NOT NULL AUTO_INCREMENT,
                        userid VARCHAR(30) DEFAULT NULL,
                        productmediaid VARCHAR(30) DEFAULT NULL, 
                        name VARCHAR(200) DEFAULT NULL, 
                        createddate DATETIME DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
                    """
                    await cursor.execute(create_medeia_table_query)
                    print("Table 'medeia' created successfully.")
                    
                    
                    
                    
                    create_user_table_query = """
                    CREATE TABLE IF NOT EXISTS user (
                        id INT NOT NULL AUTO_INCREMENT,
                        userid VARCHAR(30) DEFAULT NULL,
                        username VARCHAR(30) DEFAULT NULL,
                        createddate DATETIME DEFAULT CURRENT_TIMESTAMP,
                        email VARCHAR(30) DEFAULT NULL,
                        password VARCHAR(30) DEFAULT NULL,
                        emailauth VARCHAR(5) DEFAULT NULL,
                        
                        linkedin VARCHAR(300) DEFAULT '',
                        facebook VARCHAR(300) DEFAULT '',
                        designation VARCHAR(100) DEFAULT '',
                        about VARCHAR(500) DEFAULT '',
                        
                        PRIMARY KEY (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
                    """
                    await cursor.execute(create_user_table_query)
                    print("Table 'user' created successfully.")
                    
                    
                    
                    
                    
                    
                    
                    
                    create_reset_table_query = """
                    CREATE TABLE IF NOT EXISTS reset (
                        id INT NOT NULL AUTO_INCREMENT,
                        resetid VARCHAR(30) DEFAULT NULL,
                        createddate DATETIME DEFAULT CURRENT_TIMESTAMP,
                        email VARCHAR(30) DEFAULT NULL, 
                        code VARCHAR(5) DEFAULT NULL, 
                        
                        PRIMARY KEY (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
                    """
                    await cursor.execute(create_reset_table_query)
                    print("Table 'reset' created successfully.")
                    
                    
                    
                    create_review_table_query = """
                    CREATE TABLE IF NOT EXISTS review (
                        id INT NOT NULL AUTO_INCREMENT,
                        reviewid VARCHAR(30) DEFAULT NULL,
                        userid VARCHAR(30) DEFAULT NULL,
                        productid VARCHAR(30) DEFAULT NULL,
                        username VARCHAR(30) DEFAULT NULL,
                        commercialorpersonal VARCHAR(5) DEFAULT NULL,
                        howlong VARCHAR(10) DEFAULT NULL,
                        experiencerate VARCHAR(4) DEFAULT NULL,
                        efficiencyrate VARCHAR(4) DEFAULT NULL,
                        documentationrate VARCHAR(4) DEFAULT NULL,
                        paidornot VARCHAR(4) DEFAULT NULL,
                        paidrate VARCHAR(4) DEFAULT NULL,
                        colorcode VARCHAR(10) DEFAULT NULL,
                        comment VARCHAR(500) DEFAULT NULL,
                        createddate DATETIME DEFAULT CURRENT_TIMESTAMP,
                        email VARCHAR(30) DEFAULT NULL, 
                        code VARCHAR(5) DEFAULT NULL, 
                        
                        PRIMARY KEY (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
                    """
                    await cursor.execute(create_review_table_query)
                    print("Table 'review' created successfully.")
     
              
                    
    except aiomysql.Error as e:
        print(f"Error creating tables: {e}")
        
        
   
   
   
   
   
        
        
def generate_random_id(length=30):
    if length < 1:
        raise ValueError("Length must be at least 1")
    
    first_digit = str(random.randint(1, 9))

    remaining_digits = ''.join(random.choices('0123456789', k=length - 1))

    random_id = first_digit + remaining_digits


    return random_id









@app.post("/user_log_in")
async def user_log_in(
    emailaddress: str = Form(...),
    password: str = Form(...),
    
):
    try: 
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # First check if user exists with this email
                await cursor.execute("SELECT userid, password, emailauth FROM user WHERE email = %s", (emailaddress,))
                result = await cursor.fetchone()

                if result is None:
                    return JSONResponse(content={"message": "No user found"}, status_code=200)

                userid_db, password_db, emailauth_db = result

                if emailauth_db == '0':
                    return JSONResponse(content={"message": "Please confirm the email"}, status_code=200)

                if password != password_db:
                    return JSONResponse(content={"message": "Invalid email or password"}, status_code=200)

                return JSONResponse(content={"message": "Login successful", "userid": userid_db}, status_code=200)

    except Exception as e:
        print(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")
    
    
    
    
    
    
    
    
    
    


@app.post("/sign_up")
async def sign_up(
    username: str = Form(...),
    emailaddress: str = Form(...),
    password: str = Form(...),
    reenterpassword: str = Form(...)
):
    if password != reenterpassword:
        return JSONResponse(content={"message": "Passwords do not match"}, status_code=400)
    
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # Check for existing email
                check_email_query = "SELECT COUNT(*) FROM user WHERE email = %s"
                await cursor.execute(check_email_query, (emailaddress,))
                result = await cursor.fetchone()
                if result[0] > 0:
                    return JSONResponse(content={"message": "Email already registered"}, status_code=200)
                
                user_id = generate_random_id()
                createddate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                insert_query = """
                INSERT INTO user (userid, username, email, password, createddate, emailauth)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                await cursor.execute(insert_query, (
                    user_id, username, emailaddress, password, createddate, "0"
                ))
                
                await conn.commit()
        
        # Send email with proper error handling
        email_sent = await send_email(emailaddress, user_id, username)
        
        if email_sent:
            return JSONResponse(content={"message": "registered", "userid": user_id}, status_code=200)
        else:
            return JSONResponse(content={"message": "registered_email_failed", "userid": user_id}, status_code=200)
    
    except Exception as e:
        logger.error(f"❌ Error during sign-up: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")

async def send_email(receiver_email: str, user_id: str, username: str):
    try:
        sender_email = "dilshanwickramaarachchi99@gmail.com"
        password = "lqtj loqv aiqz wsty"
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Welcome to STEPuP Ravoom - Please Confirm Your Email"
        message["From"] = f"STEPuP Ravoom <{sender_email}>"
        message["To"] = receiver_email
        
        # Professional HTML email template
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome to STEPuP Ravoom</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 0;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 30px 20px;
                    text-align: center;
                    color: white;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                    font-weight: 300;
                }}
                .content {{
                    padding: 40px 30px;
                }}
                .welcome-text {{
                    font-size: 24px;
                    color: #333;
                    margin-bottom: 20px;
                }}
                .message-text {{
                    font-size: 16px;
                    color: #666;
                    margin-bottom: 30px;
                    line-height: 1.8;
                }}
                .btn-container {{
                    text-align: center;
                    margin: 40px 0;
                }}
                .btn-confirm {{
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white !important;
                    padding: 15px 40px;
                    text-decoration: none;
                    border-radius: 50px;
                    font-size: 16px;
                    font-weight: 500;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                    transition: all 0.3s ease;
                }}
                .btn-confirm:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
                }}
                .info-box {{
                    background-color: #f8f9ff;
                    border-left: 4px solid #667eea;
                    padding: 20px;
                    margin: 30px 0;
                    border-radius: 4px;
                }}
                .footer {{
                    background-color: #f8f9fa;
                    padding: 30px;
                    text-align: center;
                    border-top: 1px solid #e9ecef;
                }}
                .footer p {{
                    margin: 5px 0;
                    color: #666;
                    font-size: 14px;
                }}
                .social-links {{
                    margin-top: 20px;
                }}
                .social-links a {{
                    display: inline-block;
                    margin: 0 10px;
                    color: #667eea;
                    text-decoration: none;
                }}
                @media (max-width: 600px) {{
                    .container {{
                        width: 100% !important;
                        margin: 0 !important;
                    }}
                    .content {{
                        padding: 30px 20px;
                    }}
                    .welcome-text {{
                        font-size: 20px;
                    }}
                    .btn-confirm {{
                        padding: 12px 30px;
                        font-size: 14px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>STEPuP Ravoom</h1>
                </div>
                
                <div class="content">
                    <h2 class="welcome-text">Welcome, {username}! 👋</h2>
                    
                    <p class="message-text">
                        Thank you for joining with Us! We're excited to have you as part of our community. 
                        To get started and secure your account, please confirm your email address by clicking the button below.
                    </p>
                    
                    <div class="btn-container">
                        <a href="http://localhost:4200/auth/authentication/{user_id}" class="btn-confirm">
                            Confirm Email Address
                        </a>
                    </div>
                    
                    <div class="info-box">
                        <p><strong>Why verify your email?</strong></p>
                        <ul style="margin: 10px 0; padding-left: 20px; color: #666;">
                            <li>Secure your account</li>
                            <li>Receive important updates</li>
                            <li>Reset your password if needed</li>
                            <li>Get the full experience</li>
                        </ul>
                    </div>
                    
                    <p class="message-text">
                        If the button doesn't work, you can also copy and paste this link into your browser:<br>
                        <a href="http://localhost:4200/auth/authentication/{user_id}" style="color: #667eea; word-break: break-all;">
                            http://localhost:4200/auth/authentication/{user_id}
                        </a>
                    </p>
                    
                    <p class="message-text">
                        If you didn't create an account with us, please ignore this email or contact our support team.
                    </p>
                </div>
                
                <div class="footer">
                    <p><strong>AI  Team Team</strong></p>
                    <p>Building better experiences, one step at a time</p>
                    <p style="margin-top: 20px; font-size: 12px; color: #999;">
                        This email was sent to {receiver_email}. If you have any questions, 
                        please contact us at stepupcare@stepupfitness.lk
                    </p>
                    
                    <div class="social-links">
                        <a href="#" style="color: #667eea;">Website</a>
                        <a href="#" style="color: #667eea;">Support</a>
                        <a href="#" style="color: #667eea;">Privacy Policy</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create plain text alternative
        text = f"""
        Welcome to STEPuP Ravoom, {username}!
        
        Thank you for joining our community. To complete your registration and secure your account, 
        please confirm your email address by visiting this link:
        
        http://localhost:4200/auth/email-auth/{user_id}
        
        Why verify your email?
        - Secure your account
        - Receive important updates  
        - Reset your password if needed
        - Get the full STEPuP Ravoom experience
        
        If you didn't create an account with us, please ignore this email.
        
        Best regards,
        STEPuP Ravoom Team
        stepupcare@stepupfitness.lk
        """
        
        # Attach both HTML and text versions
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        
        message.attach(part1)
        message.attach(part2)
        
        # Send email with better error handling
        logger.info(f"Attempting to send email to {receiver_email}")
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            logger.info(f"✅ Email sent successfully to {receiver_email}")
            return True
            
    except smtplib.SMTPException as e:
        logger.error(f"❌ SMTP Error sending email to {receiver_email}: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ General error sending email to {receiver_email}: {e}")
        return False
        
        
        
        




def generate_4digit_code():
    return ''.join(random.choices(string.digits, k=4))


class ResetPasswordRequest(BaseModel):
    emailaddress: str
    

@app.post("/send_code_reset_password")
async def send_code_reset_password(payload: ResetPasswordRequest):
    emailaddress = payload.emailaddress

    try:
        async with aiomysql.create_pool(**async_db_config) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    # Check if email exists
                    await cursor.execute("SELECT email FROM user WHERE email=%s", (emailaddress,))
                    user = await cursor.fetchone()
                    if not user:
                        return JSONResponse(content={"message": "no email"}, status_code=200)

                    # Generate code and resetid
                    code = generate_4digit_code()
                    resetid = generate_random_id()

                    # Insert into reset table
                    await cursor.execute(
                        "INSERT INTO reset (resetid, email, code, createddate) VALUES (%s,%s,%s,%s)",
                        (resetid, emailaddress, code, datetime.now())
                    )
                    await conn.commit()

                    # Send email
                    await send_email_password_reset(emailaddress, code)

        return JSONResponse(content={"message": "sent", "resetid": resetid,"code":code}, status_code=200)

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Server error")


class DeleteOtpRequest(BaseModel):
    resetid: str
    
@app.post("/delete_email_otp")
async def delete_email_otp(payload: DeleteOtpRequest):
    resetid = payload.resetid

    try:
        async with aiomysql.create_pool(**async_db_config) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("DELETE FROM reset WHERE resetid=%s", (resetid,))
                    await conn.commit()
        return JSONResponse(content={"message": "deleted"}, status_code=200)

    except Exception as e:
        print(f"Error deleting OTP: {e}")
        raise HTTPException(status_code=500, detail="Server error")


async def send_email_password_reset(receiver_email: str, code: str):
    try:
        sender_email = "dilshanwickramaarachchi99@gmail.com"
        password = "lqtj loqv aiqz wsty"
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Password Reset - STEPuP Ravoom"
        message["From"] = f"STEPuP Ravoom <{sender_email}>"
        message["To"] = receiver_email
        
        # Professional HTML email template with same color scheme
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Password Reset - STEPuP Ravoom</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 0;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 30px 20px;
                    text-align: center;
                    color: white;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                    font-weight: 300;
                }}
                .header .icon {{
                    font-size: 48px;
                    margin-bottom: 10px;
                }}
                .content {{
                    padding: 40px 30px;
                    text-align: center;
                }}
                .title {{
                    font-size: 24px;
                    color: #333;
                    margin-bottom: 20px;
                    font-weight: 300;
                }}
                .message-text {{
                    font-size: 16px;
                    color: #666;
                    margin-bottom: 30px;
                    line-height: 1.8;
                    text-align: left;
                }}
                .otp-container {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 15px;
                    padding: 30px;
                    margin: 30px 0;
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
                }}
                .otp-label {{
                    color: rgba(255,255,255,0.9);
                    font-size: 14px;
                    font-weight: 500;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    margin-bottom: 15px;
                }}
                .otp-code {{
                    color: white;
                    font-size: 48px;
                    font-weight: 700;
                    letter-spacing: 8px;
                    margin: 0;
                    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    font-family: 'Courier New', monospace;
                }}
                .security-box {{
                    background-color: #fff3cd;
                    border: 1px solid #ffeaa7;
                    border-radius: 8px;
                    padding: 20px;
                    margin: 30px 0;
                    text-align: left;
                }}
                .security-box .icon {{
                    color: #856404;
                    font-size: 20px;
                    margin-right: 10px;
                }}
                .security-title {{
                    color: #856404;
                    font-weight: 600;
                    margin-bottom: 10px;
                    display: flex;
                    align-items: center;
                }}
                .security-text {{
                    color: #856404;
                    font-size: 14px;
                    margin: 5px 0;
                }}
                .timer-box {{
                    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
                    color: white;
                    padding: 15px 25px;
                    border-radius: 50px;
                    display: inline-block;
                    margin: 20px 0;
                    font-weight: 500;
                    font-size: 14px;
                }}
                .timer-box .icon {{
                    margin-right: 8px;
                }}
                .help-section {{
                    background-color: #f8f9ff;
                    border-left: 4px solid #667eea;
                    padding: 20px;
                    margin: 30px 0;
                    border-radius: 4px;
                    text-align: left;
                }}
                .footer {{
                    background-color: #f8f9fa;
                    padding: 30px;
                    text-align: center;
                    border-top: 1px solid #e9ecef;
                }}
                .footer p {{
                    margin: 5px 0;
                    color: #666;
                    font-size: 14px;
                }}
                .contact-info {{
                    margin-top: 20px;
                    padding-top: 20px;
                    border-top: 1px solid #e9ecef;
                }}
                .contact-info a {{
                    color: #667eea;
                    text-decoration: none;
                }}
                @media (max-width: 600px) {{
                    .container {{
                        width: 100% !important;
                        margin: 0 !important;
                    }}
                    .content {{
                        padding: 30px 20px;
                    }}
                    .otp-code {{
                        font-size: 36px;
                        letter-spacing: 4px;
                    }}
                    .title {{
                        font-size: 20px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="icon">🔐</div>
                    <h1>AI Platform</h1>
                </div>
                
                <div class="content">
                    <h2 class="title">Password Reset Request</h2>
                    
                    <p class="message-text">
                        We received a request to reset the password for your account. 
                        To proceed with resetting your password, please use the verification code below:
                    </p>
                    
                    <div class="otp-container">
                        <div class="otp-label">Your Verification Code</div>
                        <div class="otp-code">{code}</div>
                    </div>
                    
                    <div class="timer-box">
                        <span class="icon">⏰</span>
                        This code expires in 60 minutes
                    </div>
                    
                    <div class="security-box">
                        <div class="security-title">
                            <span class="icon">⚠️</span>
                            Security Notice
                        </div>
                        <div class="security-text">
                            • Never share this code with anyone
                        </div>
                        <div class="security-text">
                            • We will never ask for this code via phone or email
                        </div>
                        <div class="security-text">
                            • If you didn't request this reset, please ignore this email
                        </div>
                    </div>
                    
                    <div class="help-section">
                        <p><strong>Need Help?</strong></p>
                        <p style="margin: 10px 0; color: #666; font-size: 14px;">
                            If you're having trouble with the password reset process or didn't request this change, 
                            please contact our support team immediately. We're here to help keep your account secure.
                        </p>
                    </div>
                    
                    <p class="message-text" style="text-align: center; margin-top: 30px;">
                        After entering this code, you'll be able to create a new password for your account.
                    </p>
                </div>
                
                <div class="footer">
                    <p><strong>AI Platform Security Team</strong></p>
                    <p>Keeping your account safe and secure</p>
                    
                    <div class="contact-info">
                        <p style="font-size: 12px; color: #999;">
                            This email was sent to {receiver_email} for security purposes.
                        </p>
                        <p style="font-size: 12px;">
                            Questions? Contact us at 
                            <a href="mailto:stepupcare@stepupfitness.lk">stepupcare@stepupfitness.lk</a>
                        </p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text alternative
        text = f"""
        STEPuP Ravoom - Password Reset Request
        
        We received a request to reset the password for your account.
        
        Your verification code is: {code}
        
        This code expires in 60 minutes.
        
        SECURITY NOTICE:
        - Never share this code with anyone
        - STEPuP Ravoom will never ask for this code via phone or email
        - If you didn't request this reset, please ignore this email
        
        After entering this code, you'll be able to create a new password for your account.
        
        Need help? Contact us at stepupcare@stepupfitness.lk
        
        Best regards,
        STEPuP Ravoom Security Team
        """
        
        # Attach both HTML and text versions
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        
        message.attach(part1)
        message.attach(part2)
        
        logger.info(f"Attempting to send password reset email to {receiver_email}")
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            logger.info(f"✅ Password reset email sent successfully to {receiver_email}")
            return True
            
    except smtplib.SMTPException as e:
        logger.error(f"❌ SMTP Error sending password reset email to {receiver_email}: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ General error sending password reset email to {receiver_email}: {e}")
        return False
        
        
        
        
        
        
        
        
        
        
        
           
    
     
    
    
    

    
    
    
    
    
    
    




# ----------------- Insert Product Endpoint -----------------

@app.post("/insert_product")
async def insert_product(request: Request, productImage: UploadFile = File(None)):
    try:
        form = await request.form()  # Get all FormData

        # Single fields
        name = form.get("name")
        type_ = form.get("type")
        license_ = form.get("license")
        technology = form.get("technology")
        website = form.get("website")
        fundingStage = form.get("fundingStage")
        userid = form.get("userid")
        productfb = form.get("productfb", "")
        productlinkedin = form.get("productlinkedin", "")
        productdescription = form.get("productdescription", "")
        productdocumentation = form.get("documentationlink", "")  # ✅ Documentation link

        # Arrays: manually collect fields like founders[0], repositories[0], etc.
        def get_array(prefix):
            return [v for k, v in form.items() if k.startswith(prefix)]

        founders = get_array("founders")
        useCases = get_array("useCases")
        baseModels = get_array("baseModels")
        deployments = get_array("deployments")
        mediaPreviews = get_array("mediaPreviews")
        repositories = get_array("repositories")  # ✅ Repository links

        # Generate unique IDs
        productid = generate_random_id(30)
        productusecaseid = generate_random_id(30)
        productfounderid = generate_random_id(30)
        productbaseaimodelid = generate_random_id(30)
        productdeploymentid = generate_random_id(30)
        productmediaid = generate_random_id(30)
        productrepositoryid = generate_random_id(30)  # ✅ Repository ID

        # Read image bytes
        image_bytes = await productImage.read() if productImage else None

        # Insert into database
        async with aiomysql.create_pool(**async_db_config) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cursor:

                    # ✅ Updated INSERT query to include productdocumentation & productrepositoryid
                    await cursor.execute("""
                        INSERT INTO product (
                            userid, productid, productname, productimage, productcategory,
                            productlicense, producttechnology, productwebsite, productfundingstage,
                            productusecaseid, productfacebook, productlinkedin, productdescription,
                            productfounderid, productbaseaimodelid, productdeploymentid, productmediaid,
                            productdocumentation, productrepositoryid
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (
                        userid, productid, name, image_bytes, type_, license_,
                        technology, website, fundingStage, productusecaseid,
                        productfb, productlinkedin, productdescription,
                        productfounderid, productbaseaimodelid, productdeploymentid, productmediaid,
                        productdocumentation, productrepositoryid
                    ))

                    # ✅ Insert related child data tables
                    for uc in useCases:
                        await cursor.execute(
                            "INSERT INTO usecase (userid, productusecaseid, name) VALUES (%s,%s,%s)",
                            (userid, productusecaseid, uc)
                        )
                    for f in founders:
                        await cursor.execute(
                            "INSERT INTO founder (userid, productfounderid, name) VALUES (%s,%s,%s)",
                            (userid, productfounderid, f)
                        )
                    for b in baseModels:
                        await cursor.execute(
                            "INSERT INTO baseaimodel (userid, productbaseaimodelid, name) VALUES (%s,%s,%s)",
                            (userid, productbaseaimodelid, b)
                        )
                    for d in deployments:
                        await cursor.execute(
                            "INSERT INTO deployment (userid, productdeploymentid, name) VALUES (%s,%s,%s)",
                            (userid, productdeploymentid, d)
                        )
                    for m in mediaPreviews:
                        await cursor.execute(
                            "INSERT INTO medeia (userid, productmediaid, name) VALUES (%s,%s,%s)",
                            (userid, productmediaid, m)
                        )
                    for r in repositories:  # ✅ Insert into repository table
                        await cursor.execute(
                            "INSERT INTO repository (userid, productrepositoryid, name) VALUES (%s,%s,%s)",
                            (userid, productrepositoryid, r)
                        )

                    await conn.commit()

        return JSONResponse(content={"message": "yes", "productid": productid})

    except Exception as e:
        print(f"Error inserting product: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while inserting product.")


@app.post("/get_all_product_details")
async def get_all_product_details(request: Request):
    try:
        data = await request.json()
        userid = data.get("userid")
        page = data.get("page", 1)
        limit = data.get("limit", 10)
        
        if not userid:
            raise HTTPException(status_code=400, detail="userid is required")

        # Validate pagination parameters
        if page < 1:
            page = 1
        if limit < 1 or limit > 100:  # Set maximum limit to prevent abuse
            limit = 10
            
        # Calculate offset
        offset = (page - 1) * limit

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                # Fetch paginated products for the given user
                await cursor.execute("""
                    SELECT productid, productimage, productname, productcategory, productusecaseid, userid
                    FROM product
                    WHERE userid = %s
                    ORDER BY productid DESC
                    LIMIT %s OFFSET %s
                """, (userid, limit, offset))
                
                products = await cursor.fetchall()

                if not products:
                    return JSONResponse(content={"message": "No product found", "products": []}, status_code=200)

                # For each product, fetch all related usecase names
                for prod in products:
                    if prod.get("productusecaseid"):
                        await cursor.execute(
                            "SELECT name FROM usecase WHERE productusecaseid = %s",
                            (prod["productusecaseid"],)
                        )
                        usecase_rows = await cursor.fetchall()
                        prod["usecasenames"] = [row["name"] for row in usecase_rows] if usecase_rows else []
                    else:
                        prod["usecasenames"] = []

                    # Convert product images to base64
                    if prod.get("productimage"):
                        prod["productimage"] = base64.b64encode(prod["productimage"]).decode('utf-8')

                return JSONResponse(content={"message": "yes", "products": products}, status_code=200)

    except Exception as e:
        print(f"❌ Error fetching product details: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching product details.")



















    
    
    
    
    
    
      




@app.post("/get_product_details_basedon_categoryname")
async def get_product_details_basedon_categoryname(request: Request):
    try:
        data = await request.json()
        newCategory = data.get("newCategory")
        if not newCategory:
            raise HTTPException(status_code=400, detail="newCategory is required")

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:

                # Fetch all product details for the given category
                await cursor.execute("""
                    SELECT *
                    FROM product
                    WHERE productcategory = %s
                """, (newCategory,))
                products = await cursor.fetchall()

                if not products:
                    return JSONResponse(content={"message": "No product found"}, status_code=200)

                # Convert product images to base64 + handle datetime serialization
                for prod in products:
                    if prod.get("productimage"):
                        prod["productimage"] = base64.b64encode(prod["productimage"]).decode("utf-8")

                    # Convert datetime/date fields to strings
                    for key, value in prod.items():
                        if isinstance(value, (datetime, date)):
                            prod[key] = value.strftime("%Y-%m-%d %H:%M:%S")

                # Collect all productusecaseids and productrepositoryids
                productusecaseids = [prod["productusecaseid"] for prod in products if prod.get("productusecaseid")]
                productrepositoryids = [prod["productrepositoryid"] for prod in products if prod.get("productrepositoryid")]

                # Fetch usecases if any
                if productusecaseids:
                    await cursor.execute(
                        f"""
                        SELECT productusecaseid, name 
                        FROM usecase 
                        WHERE productusecaseid IN ({','.join(['%s']*len(productusecaseids))})
                        """,
                        tuple(productusecaseids)
                    )
                    usecases = await cursor.fetchall()

                    # Organize usecases by productusecaseid
                    usecase_map = {}
                    for uc in usecases:
                        usecase_map.setdefault(uc["productusecaseid"], []).append(uc["name"])

                    # Attach useCases to products
                    for prod in products:
                        prod["useCases"] = usecase_map.get(prod["productusecaseid"], [])
                else:
                    for prod in products:
                        prod["useCases"] = []

                # Fetch repositories if any
                if productrepositoryids:
                    await cursor.execute(
                        f"""
                        SELECT productrepositoryid, name 
                        FROM repository 
                        WHERE productrepositoryid IN ({','.join(['%s']*len(productrepositoryids))})
                        """,
                        tuple(productrepositoryids)
                    )
                    repositories = await cursor.fetchall()

                    # Organize repositories by productrepositoryid
                    repository_map = {}
                    for repo in repositories:
                        repository_map.setdefault(repo["productrepositoryid"], []).append(repo["name"])

                    # Attach repositories to products
                    for prod in products:
                        prod["repositories"] = repository_map.get(prod["productrepositoryid"], [])
                else:
                    for prod in products:
                        prod["repositories"] = []

                return JSONResponse(content={"message": "yes", "products": products}, status_code=200)

    except Exception as e:
        print(f"❌ Error fetching product details: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching product details.")

    
    
    
    
    
    
    
    
    
    
    
    
    












@app.post("/get_product_details_basedon_usecase")
async def get_product_details_basedon_usecase(request: Request):
    try:
        data = await request.json()
        newCategory = data.get("newCategory")
        if not newCategory:
            raise HTTPException(status_code=400, detail="newCategory is required")

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:

                # 1. Fetch all matching usecases
                await cursor.execute(
                    "SELECT productusecaseid, name FROM usecase WHERE name = %s",
                    (newCategory,)
                )
                usecases = await cursor.fetchall()

                if not usecases:
                    return JSONResponse(content={"message": "No product found"}, status_code=200)

                products = []

                # 2. For each usecase, fetch its products
                for usecase in usecases:
                    productusecaseid = usecase["productusecaseid"]

                    await cursor.execute("""
                        SELECT productid, productimage, productname, productcategory, productusecaseid,userid
                        FROM product
                        WHERE productusecaseid = %s
                    """, (productusecaseid,))

                    prod_list = await cursor.fetchall()

                    for prod in prod_list:
                        if prod.get("productimage"):
                            prod["productimage"] = base64.b64encode(prod["productimage"]).decode("utf-8")
                        prod["useCases"] = [usecase["name"]]  # attach the usecase name
                        products.append(prod)

                if not products:
                    return JSONResponse(content={"message": "No product found"}, status_code=200)

                return JSONResponse(content={"message": "yes", "products": products}, status_code=200)

    except Exception as e:
        print(f"Error fetching product details: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching product details.")

    
    
    
    








@app.post("/get_all_product_details_all")
async def get_all_product_details_all(request: Request):
    try:
        # Parse request body to get pagination parameters
        body = await request.json()
        page = body.get("page", 1)
        limit = body.get("limit", 10)
        
        # Validate pagination parameters
        if page < 1:
            page = 1
        if limit < 1 or limit > 100:  # Set maximum limit to prevent abuse
            limit = 10
            
        # Calculate offset
        offset = (page - 1) * limit
        
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                # Get paginated products in random order
                # Note: For consistent pagination with random order, you might want to use a seed
                # or consider ordering by a fixed field like productid for better performance
                await cursor.execute("""
                    SELECT productid, productimage, productname, productcategory, productusecaseid, userid
                    FROM product 
                    ORDER BY productid  -- Changed from RAND() for better pagination performance
                    LIMIT %s OFFSET %s
                """, (limit, offset))
                
                products = await cursor.fetchall()

                if not products:
                    return JSONResponse(content={"message": "No product found", "products": []}, status_code=200)

                # For each product, fetch all related usecase names
                for prod in products:
                    if prod.get("productusecaseid"):
                        await cursor.execute(
                            "SELECT name FROM usecase WHERE productusecaseid = %s",
                            (prod["productusecaseid"],)
                        )
                        usecase_rows = await cursor.fetchall()
                        prod["usecasenames"] = [row["name"] for row in usecase_rows] if usecase_rows else []
                    else:
                        prod["usecasenames"] = []

                    # Convert product images to base64
                    if prod.get("productimage"):
                        prod["productimage"] = base64.b64encode(prod["productimage"]).decode("utf-8")

                return JSONResponse(content={"message": "yes", "products": products}, status_code=200)

    except Exception as e:
        print(f"❌ Error fetching product details: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching product details.")





@app.post("/get_all_product_details_all_new")
async def get_all_product_details_all_new(request: Request):
    try:
        # Parse request body to get pagination parameters
        body = await request.json()
        page = body.get("page", 1)
        limit = body.get("limit", 10)
        
        # Calculate offset
        offset = (page - 1) * limit
        
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                # Get products with LIMIT and OFFSET for pagination
                await cursor.execute("""
                    SELECT productid, productimage, productname, productcategory, productusecaseid
                    FROM product 
                    ORDER BY createddate DESC
                    LIMIT %s OFFSET %s
                """, (limit, offset))
                products = await cursor.fetchall()

                if not products:
                    return JSONResponse(content={"message": "No product found"}, status_code=200)

                # For each product, fetch the usecase name
                for prod in products:
                    if prod.get("productusecaseid"):
                        await cursor.execute(
                            "SELECT name FROM usecase WHERE productusecaseid = %s",
                            (prod["productusecaseid"],)
                        )
                        usecase_rows = await cursor.fetchall()
                        prod["usecasenames"] = [row["name"] for row in usecase_rows] if usecase_rows else []

                    # Convert product images to base64
                    if prod.get("productimage"):
                        prod["productimage"] = base64.b64encode(prod["productimage"]).decode("utf-8")

                return JSONResponse(content={"message": "yes", "products": products}, status_code=200)

    except Exception as e:
        print(f"❌ Error fetching new product details: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching new product details.")
   
    
    
    
    
    
    








@app.post("/get_all_product_details_all_most_viewed")
async def get_all_product_details_all_most_viewed(request: Request):
    try:
        # Parse request body to get pagination parameters
        body = await request.json()
        page = body.get("page", 1)
        limit = body.get("limit", 10)
        
        # Calculate offset
        offset = (page - 1) * limit
        
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                # Get products with LIMIT and OFFSET for pagination
                await cursor.execute("""
                    SELECT productid, productimage, productname, productcategory, productusecaseid
                    FROM product 
                    ORDER BY counts DESC
                    LIMIT %s OFFSET %s
                """, (limit, offset))
                products = await cursor.fetchall()

                if not products:
                    return JSONResponse(content={"message": "No product found"}, status_code=200)

                # For each product, fetch the usecase name
                for prod in products:
                    if prod.get("productusecaseid"):
                        await cursor.execute(
                            "SELECT name FROM usecase WHERE productusecaseid = %s",
                            (prod["productusecaseid"],)
                        )
                        usecase_rows = await cursor.fetchall()
                        prod["usecasenames"] = [row["name"] for row in usecase_rows] if usecase_rows else []

                    # Convert product images to base64
                    if prod.get("productimage"):
                        prod["productimage"] = base64.b64encode(prod["productimage"]).decode("utf-8")

                return JSONResponse(content={"message": "yes", "products": products}, status_code=200)

    except Exception as e:
        print(f"❌ Error fetching most viewed product details: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching most viewed product details.")
    
    
    
    
    
    
    
    
    
    
    
    
    










@app.post("/search_filter")
async def search_filter(request: Request):
    try:
        data = await request.json()
        typing_text = data.get("typpingtext", "").strip()
        
        if not typing_text:
            raise HTTPException(status_code=400, detail="typing text is required")
        
        if len(typing_text) < 2:
            return JSONResponse(content={"message": "no", "products": []}, status_code=200)

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                
                # Dictionary to store unique products by productid
                unique_products = {}
                
                # 1. Search in products table (productname and productdescription)
                product_search_query = """
                    SELECT productid, productimage, productname, productcategory, 
                           productdescription, userid
                    FROM product 
                    WHERE productname LIKE %s OR productdescription LIKE %s
                """
                
                search_pattern = f"%{typing_text}%"
                await cursor.execute(product_search_query, (search_pattern, search_pattern))
                direct_products = await cursor.fetchall()
                
                # Process direct product matches
                for prod in direct_products:
                    product_id = prod["productid"]
                    
                    # Get usecases for this product
                    usecase_query = """
                        SELECT u.name 
                        FROM usecase u 
                        INNER JOIN product p ON u.productusecaseid = p.productusecaseid 
                        WHERE p.productid = %s
                    """
                    await cursor.execute(usecase_query, (product_id,))
                    usecases = await cursor.fetchall()
                    
                    # Process product image
                    if prod.get("productimage"):
                        prod["productimage"] = base64.b64encode(prod["productimage"]).decode("utf-8")
                    else:
                        prod["productimage"] = None
                    
                    # Add usecases to product
                    prod["useCases"] = [uc["name"] for uc in usecases] if usecases else []
                    
                    # Store in unique products dictionary
                    unique_products[product_id] = prod
                
                # 2. Search in usecase table and get related products
                usecase_search_query = """
                    SELECT productusecaseid, name 
                    FROM usecase 
                    WHERE name LIKE %s
                """
                
                await cursor.execute(usecase_search_query, (search_pattern,))
                matching_usecases = await cursor.fetchall()
                
                # For each matching usecase, get its products
                for usecase in matching_usecases:
                    productusecaseid = usecase["productusecaseid"]
                    usecase_name = usecase["name"]
                    
                    # Get products for this usecase
                    products_by_usecase_query = """
                        SELECT productid, productimage, productname, productcategory, 
                               productdescription, userid
                        FROM product 
                        WHERE productusecaseid = %s
                    """
                    
                    await cursor.execute(products_by_usecase_query, (productusecaseid,))
                    usecase_products = await cursor.fetchall()
                    
                    for prod in usecase_products:
                        product_id = prod["productid"]
                        
                        # If product already exists, just add the usecase
                        if product_id in unique_products:
                            if usecase_name not in unique_products[product_id]["useCases"]:
                                unique_products[product_id]["useCases"].append(usecase_name)
                        else:
                            # New product, get all its usecases
                            all_usecases_query = """
                                SELECT u.name 
                                FROM usecase u 
                                INNER JOIN product p ON u.productusecaseid = p.productusecaseid 
                                WHERE p.productid = %s
                            """
                            await cursor.execute(all_usecases_query, (product_id,))
                            all_usecases = await cursor.fetchall()
                            
                            # Process product image
                            if prod.get("productimage"):
                                prod["productimage"] = base64.b64encode(prod["productimage"]).decode("utf-8")
                            else:
                                prod["productimage"] = None
                            
                            # Add all usecases to product
                            prod["useCases"] = [uc["name"] for uc in all_usecases] if all_usecases else []
                            
                            # Store in unique products dictionary
                            unique_products[product_id] = prod
                
                # Convert dictionary values to list
                products = list(unique_products.values())
                
                if not products:
                    return JSONResponse(content={"message": "no", "products": []}, status_code=200)
                
                # Sort products by relevance (exact matches first, then partial matches)
                def sort_key(product):
                    name_exact = typing_text.lower() == product["productname"].lower()
                    name_starts = product["productname"].lower().startswith(typing_text.lower())
                    usecase_exact = any(typing_text.lower() == uc.lower() for uc in product["useCases"])
                    
                    # Priority: exact name match, exact usecase match, name starts with, others
                    if name_exact:
                        return 0
                    elif usecase_exact:
                        return 1
                    elif name_starts:
                        return 2
                    else:
                        return 3
                
                products.sort(key=sort_key)
                
                # Limit results to prevent overwhelming the UI
                products = products[:20]  # Limit to 20 results
                
                return JSONResponse(
                    content={"message": "yes", "products": products}, 
                    status_code=200
                )

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error in search_filter: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while searching products."
        )

    
    
    
    
    
    

















@app.post("/get_products_using_search_enter")
async def get_products_using_search_enter(request: Request):
    try:
        data = await request.json()
        typing_text = data.get("typpingtext", "").strip()
        
        if not typing_text:
            raise HTTPException(status_code=400, detail="typing text is required")
        
        if len(typing_text) < 2:
            return JSONResponse(content={"message": "no", "products": []}, status_code=200)

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                
                # Dictionary to store unique products by productid
                unique_products = {}
                
                # 1. Search in products table (productname and productdescription)
                product_search_query = """
                    SELECT productid, productimage, productname, productcategory, 
                           productdescription, userid
                    FROM product 
                    WHERE productname LIKE %s OR productdescription LIKE %s
                """
                
                search_pattern = f"%{typing_text}%"
                await cursor.execute(product_search_query, (search_pattern, search_pattern))
                direct_products = await cursor.fetchall()
                
                print(f"Direct products found: {len(direct_products)}")
                
                # Process direct product matches
                for prod in direct_products:
                    product_id = prod["productid"]
                    
                    # Get usecases for this product
                    usecase_query = """
                        SELECT u.name 
                        FROM usecase u 
                        INNER JOIN product p ON u.productusecaseid = p.productusecaseid 
                        WHERE p.productid = %s
                    """
                    await cursor.execute(usecase_query, (product_id,))
                    usecases = await cursor.fetchall()
                    
                    # Process product image
                    if prod.get("productimage"):
                        prod["productimage"] = base64.b64encode(prod["productimage"]).decode("utf-8")
                    else:
                        prod["productimage"] = None
                    
                    # Add usecases to product
                    prod["useCases"] = [uc["name"] for uc in usecases] if usecases else []
                    
                    # Store in unique products dictionary
                    unique_products[product_id] = prod
                
                # 2. Search in usecase table and get related products
                usecase_search_query = """
                    SELECT productusecaseid, name 
                    FROM usecase 
                    WHERE name LIKE %s
                """
                
                await cursor.execute(usecase_search_query, (search_pattern,))
                matching_usecases = await cursor.fetchall()
                
                print(f"Matching usecases found: {len(matching_usecases)}")
                
                # For each matching usecase, get its products
                for usecase in matching_usecases:
                    productusecaseid = usecase["productusecaseid"]
                    usecase_name = usecase["name"]
                    
                    # Get products for this usecase
                    products_by_usecase_query = """
                        SELECT productid, productimage, productname, productcategory, 
                               productdescription, userid
                        FROM product 
                        WHERE productusecaseid = %s
                    """
                    
                    await cursor.execute(products_by_usecase_query, (productusecaseid,))
                    usecase_products = await cursor.fetchall()
                    
                    for prod in usecase_products:
                        product_id = prod["productid"]
                        
                        # If product already exists, just add the usecase
                        if product_id in unique_products:
                            if usecase_name not in unique_products[product_id]["useCases"]:
                                unique_products[product_id]["useCases"].append(usecase_name)
                        else:
                            # New product, get all its usecases
                            all_usecases_query = """
                                SELECT u.name 
                                FROM usecase u 
                                INNER JOIN product p ON u.productusecaseid = p.productusecaseid 
                                WHERE p.productid = %s
                            """
                            await cursor.execute(all_usecases_query, (product_id,))
                            all_usecases = await cursor.fetchall()
                            
                            # Process product image
                            if prod.get("productimage"):
                                prod["productimage"] = base64.b64encode(prod["productimage"]).decode("utf-8")
                            else:
                                prod["productimage"] = None
                            
                            # Add all usecases to product
                            prod["useCases"] = [uc["name"] for uc in all_usecases] if all_usecases else []
                            
                            # Store in unique products dictionary
                            unique_products[product_id] = prod
                
                # Convert dictionary values to list
                products = list(unique_products.values())
                
                print(f"Total unique products found: {len(products)}")
                print(f"Search term: '{typing_text}'")
                
                if not products:
                    print("No products found - returning empty result")
                    return JSONResponse(content={"message": "no", "products": []}, status_code=200)
                
                # Sort products by relevance (exact matches first, then partial matches)
                def sort_key(product):
                    name_exact = typing_text.lower() == product["productname"].lower()
                    name_starts = product["productname"].lower().startswith(typing_text.lower())
                    usecase_exact = any(typing_text.lower() == uc.lower() for uc in product["useCases"])
                    desc_contains = product.get("productdescription", "").lower().find(typing_text.lower()) != -1
                    
                    # Priority: exact name match, exact usecase match, name starts with, description contains, others
                    if name_exact:
                        return 0
                    elif usecase_exact:
                        return 1
                    elif name_starts:
                        return 2
                    elif desc_contains:
                        return 3
                    else:
                        return 4
                
                products.sort(key=sort_key)
                
                print(f"Returning {len(products)} products")
                for i, prod in enumerate(products[:5]):  # Print first 5 for debugging
                    print(f"Product {i+1}: {prod['productname']} - UseCases: {prod['useCases']}")
                
                return JSONResponse(
                    content={"message": "yes", "products": products}, 
                    status_code=200
                )

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error in get_products_using_search_enter: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while searching products."
        )
        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
    
    
     
    
    
     
    
    
@app.post("/get_product_details")
async def get_product_details(request: Request):
    try:
        data = await request.json()
        productid = data.get("productid")
        if not productid:
            raise HTTPException(status_code=400, detail="productid is required")

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                # Fetch main product
                await cursor.execute("""
                    SELECT productid, productimage, productname, productcategory,
                           productlicense, producttechnology, productwebsite, productfundingstage,
                           productfacebook, productlinkedin,productdocumentation,
                           productusecaseid, productfounderid, productbaseaimodelid, productdeploymentid, productmediaid,productrepositoryid,
                           rating, productdescription, userid, counts
                    FROM product
                    WHERE productid = %s
                """, (productid,))
                
                product = await cursor.fetchone()
                if not product:
                    return JSONResponse(content={"message": "No product found"}, status_code=200)

                # Convert image to base64 if exists
                if product.get("productimage"):
                    import base64
                    product["productimage"] = base64.b64encode(product["productimage"]).decode('utf-8')

                # Fetch related data
                child_ids = {
                    "useCases": ("usecase", "productusecaseid"),
                    "founders": ("founder", "productfounderid"),
                    "baseModels": ("baseaimodel", "productbaseaimodelid"),
                    "deployments": ("deployment", "productdeploymentid"),
                    "mediaPreviews": ("medeia", "productmediaid"),
                    "repositories": ("repository", "productrepositoryid"),
                }

                response_children = {}
                for key, (table, column) in child_ids.items():
                    await cursor.execute(f"SELECT name FROM {table} WHERE {column} = %s", (product[column],))
                    response_children[key] = [row["name"] for row in await cursor.fetchall()]

                # ✅ Increment counts column by 1
                await cursor.execute("""
                    UPDATE product
                    SET counts = CAST(counts AS UNSIGNED) + 1
                    WHERE productid = %s
                """, (productid,))
                await conn.commit()

                # Combine all data
                response_data = {
                    "product": product,
                    **response_children,
                    "message": "yes"
                }

                return JSONResponse(content=response_data, status_code=200)

    except Exception as e:
        print(f"Error fetching product details: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching product details.")






















@app.post("/update_product_details")
async def update_product_details(request: Request):
    try:
        data = await request.json()
        productid = data.get("productid")
        userid = data.get("userid")
        
        if not productid or not userid:
            raise HTTPException(status_code=400, detail="productid and userid are required")

        # Extract product data
        productname = data.get("productname", "")
        productcategory = data.get("productcategory", "")
        productlicense = data.get("productlicense", "")
        producttechnology = data.get("producttechnology", "")
        productwebsite = data.get("productwebsite", "")
        productfundingstage = data.get("productfundingstage", "")
        productdescription = data.get("productdescription", "")
        productfacebook = data.get("productfacebook", "")
        productlinkedin = data.get("productlinkedin", "")
        productimage = data.get("productimage")  # Base64 encoded image
        
        # Extract array data
        founders = data.get("founders", [])
        baseModels = data.get("baseModels", [])
        deployments = data.get("deployments", [])
        mediaPreviews = data.get("mediaPreviews", [])
        useCases = data.get("useCases", [])

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                # Verify product belongs to user
                await cursor.execute("""
                    SELECT productid FROM product 
                    WHERE productid = %s AND userid = %s
                """, (productid, userid))
                
                existing_product = await cursor.fetchone()
                if not existing_product:
                    return JSONResponse(content={"message": "Product not found or unauthorized"}, status_code=404)

                # Get existing related IDs
                await cursor.execute("""
                    SELECT productusecaseid, productfounderid, productbaseaimodelid, 
                           productdeploymentid, productmediaid
                    FROM product WHERE productid = %s
                """, (productid,))
                existing_ids = await cursor.fetchone()

                # Helper function to update related tables
                async def update_related_table(table_name, items, existing_id, id_column):
                    if not items:
                        return existing_id
                    
                    # Delete existing entries
                    if existing_id:
                        await cursor.execute(f"DELETE FROM {table_name} WHERE {id_column} = %s", (existing_id,))
                    
                    # Generate new ID
                    import random
                    new_id = str(random.randint(100000000000000000000000000000, 999999999999999999999999999999))
                    
                    # Insert new entries
                    for item in items:
                        if item and item.strip():  # Only insert non-empty items
                            await cursor.execute(
                                f"INSERT INTO {table_name} ({id_column}, name) VALUES (%s, %s)",
                                (new_id, item.strip())
                            )
                    
                    return new_id

                # Update related tables
                new_usecase_id = await update_related_table(
                    "usecase", useCases, existing_ids.get("productusecaseid"), "productusecaseid"
                ) if useCases else existing_ids.get("productusecaseid")

                new_founder_id = await update_related_table(
                    "founder", founders, existing_ids.get("productfounderid"), "productfounderid"
                ) if founders else existing_ids.get("productfounderid")

                new_basemodel_id = await update_related_table(
                    "baseaimodel", baseModels, existing_ids.get("productbaseaimodelid"), "productbaseaimodelid"
                ) if baseModels else existing_ids.get("productbaseaimodelid")

                new_deployment_id = await update_related_table(
                    "deployment", deployments, existing_ids.get("productdeploymentid"), "productdeploymentid"
                ) if deployments else existing_ids.get("productdeploymentid")

                new_media_id = await update_related_table(
                    "medeia", mediaPreviews, existing_ids.get("productmediaid"), "productmediaid"
                ) if mediaPreviews else existing_ids.get("productmediaid")

                # Handle image update
                image_data = None
                if productimage:
                    try:
                        import base64
                        image_data = base64.b64decode(productimage)
                    except Exception as e:
                        print(f"Error decoding image: {e}")

                # Update main product table
                if image_data:
                    await cursor.execute("""
                        UPDATE product SET 
                            productname = %s, productcategory = %s, productlicense = %s,
                            producttechnology = %s, productwebsite = %s, productfundingstage = %s,
                            productdescription = %s, productfacebook = %s, productlinkedin = %s,
                            productimage = %s, productusecaseid = %s, productfounderid = %s,
                            productbaseaimodelid = %s, productdeploymentid = %s, productmediaid = %s
                        WHERE productid = %s AND userid = %s
                    """, (
                        productname, productcategory, productlicense, producttechnology,
                        productwebsite, productfundingstage, productdescription,
                        productfacebook, productlinkedin, image_data,
                        new_usecase_id, new_founder_id, new_basemodel_id,
                        new_deployment_id, new_media_id, productid, userid
                    ))
                else:
                    # Update without changing image
                    await cursor.execute("""
                        UPDATE product SET 
                            productname = %s, productcategory = %s, productlicense = %s,
                            producttechnology = %s, productwebsite = %s, productfundingstage = %s,
                            productdescription = %s, productfacebook = %s, productlinkedin = %s,
                            productusecaseid = %s, productfounderid = %s,
                            productbaseaimodelid = %s, productdeploymentid = %s, productmediaid = %s
                        WHERE productid = %s AND userid = %s
                    """, (
                        productname, productcategory, productlicense, producttechnology,
                        productwebsite, productfundingstage, productdescription,
                        productfacebook, productlinkedin,
                        new_usecase_id, new_founder_id, new_basemodel_id,
                        new_deployment_id, new_media_id, productid, userid
                    ))

                # Check if update was successful
                if cursor.rowcount > 0:
                    await conn.commit()
                    return JSONResponse(content={"message": "success"}, status_code=200)
                else:
                    return JSONResponse(content={"message": "No changes made"}, status_code=400)

    except Exception as e:
        print(f"Error updating product details: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating product details.")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


    
    
    
    
     

        
@app.post("/user_log_in")
async def user_log_in(
    emailaddress: str = Form(...),
    password: str = Form(...),
    
):
    try: 
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # First check if user exists with this email
                await cursor.execute("SELECT userid, password, emailauth FROM user WHERE email = %s", (emailaddress,))
                result = await cursor.fetchone()

                if result is None:
                    return JSONResponse(content={"message": "No user found"}, status_code=200)

                userid_db, password_db, emailauth_db = result

                if emailauth_db == '0':
                    return JSONResponse(content={"message": "Please confirm the email"}, status_code=200)

                if password != password_db:
                    return JSONResponse(content={"message": "Invalid email or password"}, status_code=200)

                return JSONResponse(content={"message": "Login successful", "userid": userid_db}, status_code=200)

    except Exception as e:
        print(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")
    
    
    
    
    
    






@app.post("/update_email_auth")
async def update_email_auth(userid: str = Form(...)):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # Update query: set emailauth = 1 where userid matches
                await cursor.execute(
                    "UPDATE user SET emailauth = %s WHERE userid = %s",
                    (1, userid)
                )
                await conn.commit()

                if cursor.rowcount == 0:
                    return JSONResponse(content={"message": "No user found"}, status_code=200)

                return JSONResponse(content={"message": "updated", "userid": userid}, status_code=200)

    except Exception as e:
        print(f"❌ Error during update_email_auth: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")
    
    
    
    
    
    
    
    
    
    
    
      
    
    


@app.post("/get_user_details")
async def get_user_details(request: Request):
    try:
        data = await request.json()
        userid = data.get("userid")

        if not userid:
            raise HTTPException(status_code=400, detail="userid is required")

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("SELECT * FROM user WHERE userid = %s", (userid,))
                result = await cursor.fetchone()

                if result is None:
                    return JSONResponse(content={"message": "No user found"}, status_code=200)

                # Convert datetime/date to string (if any field is datetime)
                for key, value in result.items():
                    if isinstance(value, (datetime, date)):
                        result[key] = value.isoformat()

                # Convert blob image to base64 (if you have profile image in DB)
                if "profileimage" in result and result["profileimage"]:
                    result["profileimage"] = base64.b64encode(result["profileimage"]).decode("utf-8")

                return JSONResponse(content={"message": "yes", "user": result}, status_code=200)

    except Exception as e:
        print(f"Error fetching user details: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching user details.")
    
    
    
    
    
    
    

    







@app.post("/update_user_details")
async def update_user_details(request: Request):
    try:
        data = await request.json()
        userid = data.get("userid")
        username = data.get("username")
        email = data.get("email")
        linkedin = data.get("linkedin")
        facebook = data.get("facebook")
        designation = data.get("designation")
        about = data.get("about")

        if not userid:
            raise HTTPException(status_code=400, detail="userid is required")

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                update_query = """
                    UPDATE user
                    SET username = %s,
                        email = %s,
                        linkedin = %s,
                        facebook = %s,
                        designation = %s,
                        about = %s
                    WHERE userid = %s
                """
                await cursor.execute(update_query, (
                    username, email, linkedin, facebook, designation, about, userid
                ))
                await conn.commit()

                if cursor.rowcount == 0:
                    return JSONResponse(content={"message": "No user found"}, status_code=200)

                return JSONResponse(content={"message": "updated"}, status_code=200)

    except Exception as e:
        print(f"❌ Error updating user details: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating user details.")

    
    
    
    
    
    
    
    
    
    



@app.post("/update_password")
async def update_password(request: Request):
    try:
        data = await request.json()
        confirmPassword = data.get("confirmPassword")
        emailaddress = data.get("emailaddress")

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                update_query = """
                    UPDATE user
                    SET password = %s
                    WHERE email = %s
                """
                await cursor.execute(update_query, (confirmPassword, emailaddress))
                await conn.commit()

                if cursor.rowcount == 0:
                    return JSONResponse(content={"message": "no email"}, status_code=200)

                return JSONResponse(content={"message": "updated"}, status_code=200)

    except Exception as e:
        print(f"❌ Error updating user details: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating user details.")

    
    
    
    
    
    
    
    
    
    
 


@app.post("/email_auth_admin_click_email_confirmation")
async def email_auth_admin_click_email_confirmation(adminid: str = Form(...)):
    try: 
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("UPDATE user SET emailauth = %s WHERE userid = %s", ('1', adminid))
                await conn.commit()  # Make sure changes are saved

        return JSONResponse(content={"message": "Email is authenticated"}, status_code=200)

    except Exception as e:
        print(f"Error during email confirmation: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")

    
 
    
@app.post("/get_booking_dates_details_user_end")
async def get_booking_dates_details_user_end(bookingid: str = Form(...)):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                select_query = "SELECT * FROM bookingdate WHERE bookingid = %s"
                await cursor.execute(select_query, (bookingid,))
                bookings = await cursor.fetchall()

                if not bookings:
                    return JSONResponse(content={"message": "no bookings found", "data": []}, status_code=200)

                # ✅ Convert datetime fields to string
                for booking in bookings:
                    for key, value in booking.items():
                        if isinstance(value, datetime):
                            booking[key] = value.isoformat()  # or strftime('%Y-%m-%d %H:%M:%S')

                return JSONResponse(content={"message": "yes", "data": bookings}, status_code=200)

    except Exception as e:
        print(f"Error fetching booking list: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching booking data.")
    
    
    
    
    
    
    
    
    
    
    
    
    
@app.post("/delete_product")
async def delete_product(payload: dict = Body(...)):
    try:
        productid = payload.get("productid")
        if not productid:
            raise HTTPException(status_code=400, detail="productid is required")

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                delete_query = "DELETE FROM product WHERE productid = %s"
                await cursor.execute(delete_query, (productid,))
                await conn.commit()

                return JSONResponse(content={"message": "deleted"}, status_code=200)

    except Exception as e:
        print(f"❌ Error deleting product: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while deleting the product."
        )








    
@app.post("/delete_review")
async def delete_review(payload: dict = Body(...)):
    try:
        userid = payload.get("userid")
        reviewid = payload.get("reviewid")

        if not userid or not reviewid:
            raise HTTPException(status_code=400, detail="userid and reviewid are required")

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                delete_query = "DELETE FROM review WHERE userid = %s AND reviewid = %s"
                await cursor.execute(delete_query, (userid, reviewid))
                await conn.commit()

                return JSONResponse(content={"message": "deleted"}, status_code=200)

    except Exception as e:
        print(f"❌ Error deleting review: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while deleting the review."
        )
        
        
        
        
        



@app.post("/add_review")
async def add_review(payload: dict = Body(...)):
    try:
        # Extract data from payload
        productid = payload.get("productid")
        userid = payload.get("userid")
        ispaidtogglecommercialorpersonal = payload.get("ispaidtogglecommercialorpersonal")
        usageDuration = payload.get("usageDuration")
        experienceRating = payload.get("experienceRating")
        efficiencyRating = payload.get("efficiencyRating")
        documentationRating = payload.get("documentationRating")
        isPaid = payload.get("isPaid")
        paidVersionRating = payload.get("paidVersionRating")
        additionalComments = payload.get("additionalComments")
        
        # Validate required fields
        if not productid or not userid:
            raise HTTPException(status_code=400, detail="productid and userid are required")
        
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                # CHECK IF REVIEW ALREADY EXISTS
                existing_review_query = """
                SELECT reviewid, commercialorpersonal, howlong, experiencerate, 
                       efficiencyrate, documentationrate, paidornot, paidrate, comment
                FROM review 
                WHERE userid = %s AND productid = %s
                """
                await cursor.execute(existing_review_query, (userid, productid))
                existing_review = await cursor.fetchone()
                
                if existing_review:
                    # Return existing review data for frontend to handle
                    return JSONResponse(content={
                        "message": "review_exists",
                        "existing_review": {
                            "reviewid": existing_review['reviewid'],
                            "ispaidtogglecommercialorpersonal": existing_review['commercialorpersonal'],
                            "usageDuration": existing_review['howlong'],
                            "experienceRating": int(existing_review['experiencerate']) if existing_review['experiencerate'] else 1,
                            "efficiencyRating": int(existing_review['efficiencyrate']) if existing_review['efficiencyrate'] else 1,
                            "documentationRating": int(existing_review['documentationrate']) if existing_review['documentationrate'] else 1,
                            "isPaid": existing_review['paidornot'],
                            "paidVersionRating": int(existing_review['paidrate']) if existing_review['paidrate'] else 1,
                            "additionalComments": existing_review['comment'] or ""
                        }
                    }, status_code=200)
                
                # Get username from users table
                user_query = "SELECT username, email FROM user WHERE userid = %s"
                await cursor.execute(user_query, (userid,))
                user_result = await cursor.fetchone()
                
                if not user_result:
                    raise HTTPException(status_code=404, detail="User not found")
                
                username = user_result['username']
                email = user_result.get('email', '')
                
                # Generate unique review ID and color code
                reviewid = generate_random_id()
                colorcode = generate_dark_color()
                createddate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Insert new review into database
                insert_query = """
                INSERT INTO review (
                    reviewid, userid, productid, commercialorpersonal, howlong, 
                    experiencerate, comment, efficiencyrate, documentationrate, 
                    paidornot, paidrate, colorcode, username, createddate, email, code
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                await cursor.execute(insert_query, (
                    reviewid,
                    userid,
                    productid,
                    ispaidtogglecommercialorpersonal,
                    usageDuration,
                    str(experienceRating),
                    additionalComments or "",
                    str(efficiencyRating),
                    str(documentationRating),
                    isPaid,
                    str(paidVersionRating) if paidVersionRating else None,
                    colorcode,
                    username,
                    createddate,
                    email,
                    "REV01"
                ))
                
                await conn.commit()
                
                # Auto-calculate and update product rating
                rating_query = """
                SELECT experiencerate, efficiencyrate, documentationrate, 
                       paidornot, paidrate
                FROM review 
                WHERE productid = %s
                """
                
                await cursor.execute(rating_query, (productid,))
                rating_results = await cursor.fetchall()
                
                # Initialize rating_data with default values
                rating_data = {"weighted_rating": 0.0}
                
                if rating_results:
                    # Get global average for better calculation
                    global_avg_query = """
                    SELECT AVG((CAST(experiencerate AS DECIMAL) + CAST(efficiencyrate AS DECIMAL) + CAST(documentationrate AS DECIMAL)) / 3) as global_avg
                    FROM review 
                    WHERE experiencerate IS NOT NULL 
                    AND efficiencyrate IS NOT NULL 
                    AND documentationrate IS NOT NULL
                    """
                    
                    await cursor.execute(global_avg_query)
                    global_result = await cursor.fetchone()
                    global_avg = float(global_result['global_avg']) if global_result and global_result['global_avg'] else 4.0
                    
                    # Calculate rating with dynamic global average
                    rating_data = calculate_rating_from_reviews(rating_results, m=10, global_avg=global_avg)
                    
                    # Update product rating
                    update_query = "UPDATE product SET rating = %s WHERE productid = %s"
                    await cursor.execute(update_query, (rating_data["weighted_rating"], productid))
                    await conn.commit()
                
                return JSONResponse(content={
                    "message": "added", 
                    "reviewid": reviewid,
                    "new_rating": rating_data["weighted_rating"]
                }, status_code=200)
                
    except Exception as e:
        print(f"❌ Error adding review: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while adding the review."
        )

@app.post("/update_review")
async def update_review(payload: dict = Body(...)):
    try:
        # Extract data from payload
        reviewid = payload.get("reviewid")
        productid = payload.get("productid")
        userid = payload.get("userid")
        ispaidtogglecommercialorpersonal = payload.get("ispaidtogglecommercialorpersonal")
        usageDuration = payload.get("usageDuration")
        experienceRating = payload.get("experienceRating")
        efficiencyRating = payload.get("efficiencyRating")
        documentationRating = payload.get("documentationRating")
        isPaid = payload.get("isPaid")
        paidVersionRating = payload.get("paidVersionRating")
        additionalComments = payload.get("additionalComments")
        
        # Validate required fields
        if not reviewid or not productid or not userid:
            raise HTTPException(status_code=400, detail="reviewid, productid and userid are required")
        
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                # Verify the review belongs to the user
                verify_query = "SELECT reviewid FROM review WHERE reviewid = %s AND userid = %s AND productid = %s"
                await cursor.execute(verify_query, (reviewid, userid, productid))
                verify_result = await cursor.fetchone()
                
                if not verify_result:
                    raise HTTPException(status_code=404, detail="Review not found or you don't have permission to update it")
                
                # Update the review
                update_query = """
                UPDATE review SET 
                    commercialorpersonal = %s,
                    howlong = %s,
                    experiencerate = %s,
                    comment = %s,
                    efficiencyrate = %s,
                    documentationrate = %s,
                    paidornot = %s,
                    paidrate = %s
                WHERE reviewid = %s AND userid = %s AND productid = %s
                """
                
                await cursor.execute(update_query, (
                    ispaidtogglecommercialorpersonal,
                    usageDuration,
                    str(experienceRating),
                    additionalComments or "",
                    str(efficiencyRating),
                    str(documentationRating),
                    isPaid,
                    str(paidVersionRating) if paidVersionRating else None,
                    reviewid,
                    userid,
                    productid
                ))
                
                await conn.commit()
                
                # Auto-calculate and update product rating
                rating_query = """
                SELECT experiencerate, efficiencyrate, documentationrate, 
                       paidornot, paidrate
                FROM review 
                WHERE productid = %s
                """
                
                await cursor.execute(rating_query, (productid,))
                rating_results = await cursor.fetchall()
                
                # Initialize rating_data with default values
                rating_data = {"weighted_rating": 0.0}
                
                if rating_results:
                    # Get global average for better calculation
                    global_avg_query = """
                    SELECT AVG((CAST(experiencerate AS DECIMAL) + CAST(efficiencyrate AS DECIMAL) + CAST(documentationrate AS DECIMAL)) / 3) as global_avg
                    FROM review 
                    WHERE experiencerate IS NOT NULL 
                    AND efficiencyrate IS NOT NULL 
                    AND documentationrate IS NOT NULL
                    """
                    
                    await cursor.execute(global_avg_query)
                    global_result = await cursor.fetchone()
                    global_avg = float(global_result['global_avg']) if global_result and global_result['global_avg'] else 4.0
                    
                    # Calculate rating with dynamic global average
                    rating_data = calculate_rating_from_reviews(rating_results, m=10, global_avg=global_avg)
                    
                    # Update product rating
                    update_product_query = "UPDATE product SET rating = %s WHERE productid = %s"
                    await cursor.execute(update_product_query, (rating_data["weighted_rating"], productid))
                    await conn.commit()
                
                return JSONResponse(content={
                    "message": "updated", 
                    "reviewid": reviewid,
                    "new_rating": rating_data["weighted_rating"]
                }, status_code=200)
                
    except Exception as e:
        print(f"❌ Error updating review: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while updating the review."
        )

@app.post("/check_existing_review")
async def check_existing_review(payload: dict = Body(...)):
    try:
        productid = payload.get("productid")
        userid = payload.get("userid")
        
        # Validate required fields
        if not productid or not userid:
            raise HTTPException(status_code=400, detail="productid and userid are required")
        
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                # Check if review exists
                query = """
                SELECT reviewid, commercialorpersonal, howlong, experiencerate, 
                       efficiencyrate, documentationrate, paidornot, paidrate, comment
                FROM review 
                WHERE userid = %s AND productid = %s
                """
                
                await cursor.execute(query, (userid, productid))
                result = await cursor.fetchone()
                
                if result:
                    return JSONResponse(content={
                        "message": "found",
                        "review": {
                            "reviewid": result['reviewid'],
                            "ispaidtogglecommercialorpersonal": result['commercialorpersonal'],
                            "usageDuration": result['howlong'],
                            "experienceRating": int(result['experiencerate']) if result['experiencerate'] else 1,
                            "efficiencyRating": int(result['efficiencyrate']) if result['efficiencyrate'] else 1,
                            "documentationRating": int(result['documentationrate']) if result['documentationrate'] else 1,
                            "isPaid": result['paidornot'],
                            "paidVersionRating": int(result['paidrate']) if result['paidrate'] else 1,
                            "additionalComments": result['comment'] or ""
                        }
                    }, status_code=200)
                else:
                    return JSONResponse(content={
                        "message": "not_found"
                    }, status_code=200)
                
    except Exception as e:
        print(f"❌ Error checking existing review: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while checking for existing review."
        )

@app.post("/get_reviews")
async def get_reviews(payload: dict = Body(...)):
    try:
        productid = payload.get("productid")
        offset = payload.get("offset", 0)  # Default to 0 if not provided
        limit = payload.get("limit", 5)    # Default to 5 reviews per request
        
        if not productid:
            raise HTTPException(status_code=400, detail="productid is required")
        
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                # Get total count of reviews for this product
                count_query = "SELECT COUNT(*) as total FROM review WHERE productid = %s"
                await cursor.execute(count_query, (productid,))
                count_result = await cursor.fetchone()
                total_reviews = count_result['total'] if count_result else 0
                
                # Get reviews with pagination
                query = """
                SELECT id, reviewid, userid, productid, commercialorpersonal, howlong, 
                       experiencerate, comment, efficiencyrate, documentationrate, 
                       paidornot, paidrate, colorcode, username, createddate, email
                FROM review 
                WHERE productid = %s 
                ORDER BY createddate DESC
                LIMIT %s OFFSET %s
                """
                
                await cursor.execute(query, (productid, limit, offset))
                results = await cursor.fetchall()
                
                reviews = []
                for row in results:
                    review = {
                        "id": row['id'],
                        "reviewid": row['reviewid'],
                        "userid": row['userid'],
                        "productid": row['productid'],
                        "commercialorpersonal": row['commercialorpersonal'],
                        "howlong": row['howlong'],
                        "experiencerate": row['experiencerate'],
                        "comment": row['comment'],
                        "efficiencyrate": row['efficiencyrate'],
                        "documentationrate": row['documentationrate'],
                        "paidornot": row['paidornot'],
                        "paidrate": row['paidrate'],
                        "colorcode": row['colorcode'],
                        "username": row['username'],
                        "createddate": row['createddate'].strftime('%Y-%m-%d %H:%M:%S') if row['createddate'] else '',
                        "email": row['email']
                    }
                    reviews.append(review)
                
                # Calculate if there are more reviews to load
                has_more = (offset + limit) < total_reviews
                
                return JSONResponse(content={
                    "message": "found", 
                    "reviews": reviews,
                    "total_reviews": total_reviews,
                    "has_more": has_more,
                    "current_offset": offset,
                    "limit": limit
                }, status_code=200)
                
    except Exception as e:
        print(f"❌ Error fetching reviews: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while fetching reviews."
        )




@app.post("/calculate_product_rating")
async def calculate_product_rating(payload: dict = Body(...)):
    try:
        productid = payload.get("productid")
        if not productid:
            raise HTTPException(status_code=400, detail="productid is required")
        
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                # Get global average first
                global_avg_query = """
                SELECT AVG((CAST(experiencerate AS DECIMAL) + CAST(efficiencyrate AS DECIMAL) + CAST(documentationrate AS DECIMAL)) / 3) as global_avg
                FROM review 
                WHERE experiencerate IS NOT NULL 
                AND efficiencyrate IS NOT NULL 
                AND documentationrate IS NOT NULL
                """
                
                await cursor.execute(global_avg_query)
                global_result = await cursor.fetchone()
                global_avg = float(global_result['global_avg']) if global_result and global_result['global_avg'] else 4.0
                
                # Get all reviews for the specific product
                query = """
                SELECT experiencerate, efficiencyrate, documentationrate, 
                       paidornot, paidrate
                FROM review 
                WHERE productid = %s
                """
                
                await cursor.execute(query, (productid,))
                results = await cursor.fetchall()
                
                if not results:
                    return JSONResponse(content={
                        "message": "no_reviews", 
                        "rating": 0.0,
                        "core_avg": 0.0,
                        "paid_support_avg": None,
                        "overall_score": 0.0,
                        "weighted_rating": 0.0,
                        "num_reviews": 0,
                        "global_average_used": global_avg
                    }, status_code=200)
                
                # Calculate rating using dynamic global average
                rating_data = calculate_rating_from_reviews(results, m=10, global_avg=global_avg)
                
                # Update the product table with the new rating
                update_query = "UPDATE product SET rating = %s WHERE productid = %s"
                await cursor.execute(update_query, (rating_data["weighted_rating"], productid))
                await conn.commit()
                
                return JSONResponse(content={
                    "message": "calculated",
                    "rating": rating_data["weighted_rating"],
                    "core_avg": rating_data["core_avg"],
                    "paid_support_avg": rating_data["paid_support_avg"],
                    "overall_score": rating_data["overall_score"],
                    "weighted_rating": rating_data["weighted_rating"],
                    "num_reviews": rating_data["num_reviews"],
                    "global_average_used": global_avg
                }, status_code=200)
                
    except Exception as e:
        print(f"❌ Error calculating product rating: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while calculating the rating."
        )

@app.get("/get_global_average")
async def get_global_average():
    try:
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                # Calculate global average from all reviews
                query = """
                SELECT AVG((CAST(experiencerate AS DECIMAL) + CAST(efficiencyrate AS DECIMAL) + CAST(documentationrate AS DECIMAL)) / 3) as global_avg
                FROM review 
                WHERE experiencerate IS NOT NULL 
                AND efficiencyrate IS NOT NULL 
                AND documentationrate IS NOT NULL
                """
                
                await cursor.execute(query)
                result = await cursor.fetchone()
                
                global_avg = float(result['global_avg']) if result and result['global_avg'] else 4.0
                
                return JSONResponse(content={
                    "message": "calculated",
                    "global_average": round(global_avg, 2)
                }, status_code=200)
                
    except Exception as e:
        print(f"❌ Error calculating global average: {e}")
        # Return default global average if calculation fails
        return JSONResponse(content={
            "message": "default",
            "global_average": 4.0
        }, status_code=200)

def calculate_rating_from_reviews(reviews_data, m=10, global_avg=4.0):
    
    num_reviews = len(reviews_data)
    
    if num_reviews == 0:
        return {
            "core_avg": 0.0,
            "paid_support_avg": None,
            "overall_score": 0.0,
            "weighted_rating": 0.0,
            "num_reviews": 0
        }
    
    try:
        # Step 1: Core averages (experience, efficiency, documentation)
        experience_sum = sum(int(r["experiencerate"]) for r in reviews_data if r["experiencerate"])
        efficiency_sum = sum(int(r["efficiencyrate"]) for r in reviews_data if r["efficiencyrate"])
        docs_sum = sum(int(r["documentationrate"]) for r in reviews_data if r["documentationrate"])
        
        experience_avg = experience_sum / num_reviews
        efficiency_avg = efficiency_sum / num_reviews
        docs_avg = docs_sum / num_reviews
        
        core_avg = (experience_avg + efficiency_avg + docs_avg) / 3
        
        # Step 2: Paid support average (if paid users exist)
        paid_ratings = []
        for r in reviews_data:
            if r["paidornot"] == "yes" and r.get("paidrate") is not None and r["paidrate"]:
                paid_ratings.append(int(r["paidrate"]))
        
        paid_support_avg = sum(paid_ratings) / len(paid_ratings) if paid_ratings else None
        
        # Step 3: Weighted overall score (70% core, 30% paid support if available)
        if paid_support_avg is not None:
            overall_score = 0.7 * core_avg + 0.3 * paid_support_avg
        else:
            overall_score = core_avg
        
        # Step 4: Confidence-adjusted Weighted Rating (WR)
        v = num_reviews
        R = overall_score
        C = global_avg
        
        weighted_rating = (v / (v + m)) * R + (m / (v + m)) * C
        
        return {
            "core_avg": round(core_avg, 2),
            "paid_support_avg": round(paid_support_avg, 2) if paid_support_avg else None,
            "overall_score": round(overall_score, 2),
            "weighted_rating": round(weighted_rating, 2),
            "num_reviews": num_reviews
        }
        
    except Exception as e:
        print(f"❌ Error in calculate_rating_from_reviews: {e}")
        return {
            "core_avg": 0.0,
            "paid_support_avg": None,
            "overall_score": 0.0,
            "weighted_rating": 0.0,
            "num_reviews": num_reviews
        }

def generate_dark_color():
    """Generate a random dark color in hex format"""
    import random
    # Generate darker colors by keeping RGB values below 128
    r = random.randint(0, 127)
    g = random.randint(0, 127)
    b = random.randint(0, 127)
    return f"#{r:02x}{g:02x}{b:02x}"








@app.post("/get_user_reviews_page")
async def get_user_reviews_page(payload: dict = Body(...)):
    try:
        userid = payload.get("userid")
        offset = payload.get("offset", 0)  # Default to 0 if not provided
        limit = payload.get("limit", 5)    # Default to 5 reviews per request

        if not userid:
            raise HTTPException(status_code=200, detail="userid is required")

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                # Get total count of reviews for this user
                count_query = "SELECT COUNT(*) as total FROM review WHERE userid = %s"
                await cursor.execute(count_query, (userid,))
                count_result = await cursor.fetchone()
                total_reviews = count_result['total'] if count_result else 0

                # Get reviews with pagination
                query = """
                SELECT id, reviewid, userid, productid, commercialorpersonal, howlong, 
                       experiencerate, comment, efficiencyrate, documentationrate, 
                       paidornot, paidrate, colorcode, username, createddate, email
                FROM review 
                WHERE userid = %s 
                ORDER BY createddate DESC
                LIMIT %s OFFSET %s
                """
                await cursor.execute(query, (userid, limit, offset))
                results = await cursor.fetchall()

                reviews = []
                for row in results:
                    review = {
                        "id": row['id'],
                        "reviewid": row['reviewid'],
                        "userid": row['userid'],
                        "productid": row['productid'],
                        "commercialorpersonal": row['commercialorpersonal'],
                        "howlong": row['howlong'],
                        "experiencerate": row['experiencerate'],
                        "comment": row['comment'],
                        "efficiencyrate": row['efficiencyrate'],
                        "documentationrate": row['documentationrate'],
                        "paidornot": row['paidornot'],
                        "paidrate": row['paidrate'],
                        "colorcode": row['colorcode'],
                        "username": row['username'],
                        "createddate": row['createddate'].strftime('%Y-%m-%d %H:%M:%S') if row['createddate'] else '',
                        "email": row['email']
                    }
                    reviews.append(review)

                # Calculate if there are more reviews to load
                has_more = (offset + limit) < total_reviews

                return JSONResponse(content={
                    "message": "found",
                    "reviews": reviews,
                    "total_reviews": total_reviews,
                    "has_more": has_more,
                    "current_offset": offset,
                    "limit": limit
                }, status_code=200)

    except Exception as e:
        print(f"❌ Error fetching user reviews: {e}")
        raise HTTPException(
            status_code=200,
            detail="An error occurred while fetching user reviews."
        )
        
        
        
        
        




@app.post("/product_comparison_review_count")
async def product_comparison_review_count(payload: dict = Body(...)):
    try:
        product_ids = payload.get("product_ids", [])
        
        if not product_ids:
            return {
                "message": "error",
                "detail": "product_ids list is required"
            }
        
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                # Create placeholders for SQL IN clause
                placeholders = ', '.join(['%s'] * len(product_ids))
                
                query = f"""
                    SELECT 
                        productid, 
                        COUNT(*) as count 
                    FROM review 
                    WHERE productid IN ({placeholders})
                    GROUP BY productid
                """
                
                await cursor.execute(query, product_ids)
                results = await cursor.fetchall()
                
                # Create a dictionary with all product IDs (including those with 0 reviews)
                review_counts = {pid: 0 for pid in product_ids}
                
                # Update with actual counts
                for row in results:
                    review_counts[row['productid']] = row['count']
                
                # Convert to list format
                review_counts_list = [
                    {"productid": pid, "count": count} 
                    for pid, count in review_counts.items()
                ]
                
                return {
                    "message": "success",
                    "review_counts": review_counts_list
                }
                
    except Exception as e:
        print(f"❌ Error in product_comparison_review_count: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    



