import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class EmailService:
    def __init__(self):
        self.ses = boto3.client(
            "ses",
            region_name=os.getenv("AWS_SES_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
        )
        self.sender_email = os.getenv("AWS_SES_VERIFIED_MAIL")

    def send_email(self, to_email: str, subject: str, message: str):
        try:
            response = self.ses.send_email(
                Source=self.sender_email,
                Destination={"ToAddresses": [to_email]},
                Message={
                    "Subject": {"Data": subject},
                    "Body": {"Text": {"Data": message}},
                },
            )
            print(response["MessageId"])
            return response["MessageId"]
        except ClientError as e:
            raise Exception(f"Email sending failed: {str(e)}")

