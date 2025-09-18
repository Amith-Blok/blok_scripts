import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Load environment variables from .env file
load_dotenv()


def aws_mail_send_with_attachment(path: str):
    SENDER = "noreply@bloksupplychain.com"
    RECIPIENT = "amitanil@bloksupplychain.com"
    AWS_REGION = os.getenv("AWS_DEFAULT_REGION")
    SUBJECT = "Amazon SES Test with Attachment"
    BODY_TEXT = "This email contains an attachment sent via Amazon SES using Boto3."
    BODY_HTML = """<html><body><h1>Amazon SES Test with Attachment</h1></body></html>"""
    ATTACHMENT_PATH = path

    # Create a new SES client
    client = boto3.client(
        "ses",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=AWS_REGION,
    )

    # Build the email
    msg = MIMEMultipart()
    msg["From"] = SENDER
    msg["To"] = RECIPIENT
    msg["Subject"] = SUBJECT

    # Add body parts
    msg.attach(MIMEText(BODY_TEXT, "plain"))
    msg.attach(MIMEText(BODY_HTML, "html"))

    # Add attachment
    try:
        with open(ATTACHMENT_PATH, "rb") as attachment:
            mime_base = MIMEBase("application", "octet-stream")
            mime_base.set_payload(attachment.read())
        encoders.encode_base64(mime_base)
        mime_base.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(ATTACHMENT_PATH)}",
        )
        msg.attach(mime_base)
    except FileNotFoundError:
        print(f"Attachment not found: {ATTACHMENT_PATH}")
        return

    # Send the email
    try:
        response = client.send_raw_email(
            Source=SENDER,
            Destinations=[RECIPIENT],
            RawMessage={"Data": msg.as_string()},
        )
    except ClientError as e:
        print("Error:", e.response["Error"]["Message"])
    else:
        print("Email sent with attachment! Message ID:", response["MessageId"])
