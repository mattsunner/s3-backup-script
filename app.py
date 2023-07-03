"""
app.py - Script to upload folder contents to S3


Author: Matthew Sunner, 2023
"""

import os

import boto3
from dotenv import load_dotenv


# Import env variables from .env (not in git)
load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')


# Define Function to Connect to S3 Bucket

def service_conn(aws_access_key_id, aws_secret_access_key, service):
    """
    service_conn - Connect to an AWS service using Boto3 using .env credentials

    args:
        aws_access_key_id - string access key setup in IAM
        aws_secret_access_key - sting secret setup in IAM
        service - service being accessed in AWS (i.e. S3, EC2, DynamoDB, etc..)

    """
    client = boto3.client(
        service,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    return client


def upload_folder(folder_path, client):
    """
    upload_folder - Function to upload folder and subfolder content to s3 bucket

    args:
        folder_path - string of relative path to folder being uploaded
        client - client object for boto3

    return:
        None

    """
    for subdir, dirs, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(subdir, file)
            
            client.upload_file(full_path, S3_BUCKET_NAME, full_path)
    
    return None


if __name__ == '__main__':
    client = service_conn(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, 's3')
    drive = 'data' # Change this to the drive name for uploading to s3

    upload_folder(drive, client)