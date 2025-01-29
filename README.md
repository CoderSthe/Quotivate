# Quotivate

## Overview
This project sends a randomly selected motivational quote via email. It features functionalities to:
- Load and validate JSON data containing inspirational quotes.
- Randomly select a quote from the data.
- Send the selected quote to a recipient's email address.

The project uses `unittest` for unit testing along with mocks for external dependencies such as email validation and SMTP operations.

---

## Features
1. **Load Quotes**: Parses JSON data to retrieve a collection of quotes.
2. **Random Quote Generator**: Selects a random quote and formats it with the author's name.
3. **Email Sending**: Sends the selected quote via email, ensuring the recipient's address is validated.

---

## Requirements
- Python 3.8 or later
- SMTP configuration (e.g., Gmail SMTP server)
- Modules:
  - `smtplib`
  - `unittest`
  - `random`
  - `json`

---

## Installation
1. Clone the repository:
```bash
git clone git@github.com:CoderSthe/Quotivate.git
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the configuration:
- Export the following environment variables in your shell or add them to a `.env` file in the project root (if using a tool like `python-dotenv`):
```bash
export SMTP_LOGIN="your_email@example.com"
export SMTP_PASSWORD="your_password"
export SMTP_SERVER="smtp.example.com"
export SMTP_PORT=587
```

---

## Usage
1. Run the script with the recipient's email address as an argument:
```bash
python inspirational_emails/send_inspiration.py recipient@example.com
```

2. The script will:

- Load quotes from a predefined JSON data source.
- Randomly select a quote.
- Send the quote via email.

---

## Testing
The project includes a comprehensive test suite to validate its functionalities. To run the tests:

```bash
python -m unittest discover tests
```
---

## Example Output

### Command Line
```bash
python inspirational_emails/send_inspiration.py recipient@example.com
```

### Output:
```bash
Email successfully sent to recipient@example.com
```

## On Error
If an error occurs (e.g., invalid recipient email), the script will print:
```bash
The provided email address is not valid.
```

---

## Project Structure

```graphql
Quotivate/
├── inspirational_emails/
│   ├── send_inspiration.py
│   ├── validate_email.py
│   └── random_quotes.py  
├── tests/
│   └── test_send_inspiration.py
│
├── .gitignore
├── config.py
├── setup.py
├── requirements.txt
└── README.md
```
