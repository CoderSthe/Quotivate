import json
import random
import os
import smtplib
import sys
from typing import Dict

from config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT
from inspirational_emails.validate_email import validate_email


def load_quotes(data: str) -> Dict:
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        raise ValueError("Failed to load quotes. Please ensure JSON data is valid.")


def get_random_quote(data: Dict) -> str:
    quotes = data.get("quotes", [])
    if not quotes:
        raise ValueError("No quotes found in the data.")
    random_quote = random.choice(quotes)
    return f'"{random_quote.get("quote", "Unknown quote")}" - {random_quote.get("author", "Unknown author")}'


def send_email(subject: str, body: str, recipient: str) -> None:
    if not validate_email(recipient):
        raise ValueError("The provided email address is not valid.")

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        msg = f"Subject: {subject}\n\n{body}"
        try:
            smtp.sendmail(EMAIL_ADDRESS, recipient, msg)
        except smtplib.SMTPException:
            raise ValueError("Failed to send email.")


def main():
    if len(sys.argv) <= 1:
        raise ValueError("No email recipient found. Please provide a recipient email as an argument.")
    
    recipient = sys.argv[1]

    file_path = os.path.join(os.path.dirname(__file__), "random_quotes.json")
    with open(file_path, "r") as file:
        json_data = json.load(file)

    data = load_quotes(json.dumps(json_data))
    random_quote = get_random_quote(data)

    subject = "Motivational Quote of the Day"
    body = random_quote

    send_email(subject, body, recipient)
    print(f"Email successfully sent to {recipient}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
