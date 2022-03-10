
import boto3
import os
from dotenv import load_dotenv
from post_functions import db_structure as connection
from urllib import parse

load_dotenv()

ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")
AWS_REGION = os.environ.get("AWS_REGION")

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY, region_name=AWS_REGION)

s3_connection = session.client('s3')
file_name = "test.pdf"
bucket_file_name = "test999.pdf"
file_uploaded = s3_connection.upload_file(f"downloads/{file_name}", "utilities-reception", bucket_file_name, ExtraArgs={'ContentType': 'application/pdf', "ContentDisposition": "inline"})

url = f"https://utilities-reception.s3.amazonaws.com/{bucket_file_name}"

print(url)
os.remove(f"downloads/{file_name}")