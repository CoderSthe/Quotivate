import unittest
from unittest.mock import patch, MagicMock
import smtplib

from config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_PORT, SMTP_SERVER
from inspirational_emails.send_inspiration import (
    get_random_quote,
    load_quotes,
    send_email,
    validate_email,
)


class TestSendInspiration(unittest.TestCase):
    def test_load_quotes_valid(self):
        valid_json = '{"quotes": [{"quote": "Stay positive.", "author": "Author A"}]}'
        data = load_quotes(valid_json)
        self.assertIn("quotes", data)
        self.assertEqual(data["quotes"][0]["quote"], "Stay positive.")

    def test_load_quotes_invalid(self):
        invalid_json = "{invalid_json}"
        with self.assertRaises(ValueError) as context:
            load_quotes(invalid_json)
        self.assertEqual(
            str(context.exception),
            "Failed to load quotes. Please ensure JSON data is valid.",
        )

    def test_get_random_quote_valid(self):
        data = {
            "quotes": [
                {"quote": "Be yourself.", "author": "Author B"},
                {"quote": "Keep going.", "author": "Author C"},
            ]
        }
        quote = get_random_quote(data)
        self.assertTrue(quote.startswith('"'))
        self.assertIn("- Author", quote)

    def test_get_random_quote_empty(self):
        data = {"quotes": []}
        with self.assertRaises(ValueError) as context:
            get_random_quote(data)
        self.assertEqual(str(context.exception), "No quotes found in the data.")

    @patch("inspirational_emails.send_inspiration.validate_email", return_value=True)
    @patch("inspirational_emails.send_inspiration.smtplib.SMTP")
    def test_send_email_success(self, mock_smtp, mock_validate_email):
        mock_server_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server_instance

        with patch.dict(
            "inspirational_emails.send_inspiration.__dict__",
            {
                "EMAIL_ADDRESS": "mock_email@example.com",
                "EMAIL_PASSWORD": "mock_password",
                "SMTP_SERVER": "mock_smtp_server",
                "SMTP_PORT": 587,
            },
        ):
            send_email("Test Subject", "Test Body", "test@example.com")

        mock_validate_email.assert_called_once_with("test@example.com")
        mock_server_instance.sendmail.assert_called_once()

    @patch("inspirational_emails.send_inspiration.validate_email", return_value=False)
    def test_send_email_invalid_recipient(self, mock_validate_email):
        with self.assertRaises(ValueError) as context:
            send_email("Test Subject", "Test Body", "invalid-email")
        self.assertEqual(
            str(context.exception), "The provided email address is not valid."
        )

    def test_valid_emails(self):
        valid_emails = [
            "test@example.com",
            "sithembiso.mdhluli@umuzi.org",
            "employee@company.co.za",
            "student-123@university.org.za",
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email), f"Failed for {email}")

    def test_invalid_emails(self):
        invalid_emails = [
            "employee21",
            "@company.org",
            "test@@example.com",
            "student-123.university.com",
        ]
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(validate_email(email), f"Failed for {email}")

    def test_config_values(self):
        with patch.dict(
            "inspirational_emails.send_inspiration.__dict__",
            {
                "EMAIL_ADDRESS": "mock_email@example.com",
                "EMAIL_PASSWORD": "mock_password",
                "SMTP_SERVER": "mock_smtp_server",
                "SMTP_PORT": 587,
            },
        ):
            self.assertTrue(EMAIL_ADDRESS.strip(), "EMAIL_ADDRESS is empty.")
            self.assertTrue(EMAIL_PASSWORD.strip(), "EMAIL_PASSWORD is empty.")
            self.assertTrue(SMTP_SERVER.strip(), "SMTP_SERVER is empty.")
            self.assertTrue(SMTP_PORT, "SMTP_PORT is empty.")

    @patch("smtplib.SMTP")
    def test_smtp_connection(self, mock_smtp):
        with patch.dict(
            "inspirational_emails.send_inspiration.__dict__",
            {
                "EMAIL_ADDRESS": "mock_email@example.com",
                "EMAIL_PASSWORD": "mock_password",
                "SMTP_SERVER": "mock_smtp_server",
                "SMTP_PORT": 587,
            },
        ):
            mock_instance = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_instance

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            mock_smtp.assert_called_with(SMTP_SERVER, SMTP_PORT)
            mock_instance.ehlo.assert_called_once()
            mock_instance.starttls.assert_called_once()
            mock_instance.login.assert_called_once_with(EMAIL_ADDRESS, EMAIL_PASSWORD)
