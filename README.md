# Time Capsule Messenger - WhatsApp Edition 🕰️📱


A futuristic web application that allows users to write messages today and receive them automatically on WhatsApp at a specific date and time in the future.

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Architecture and Tech Stack](#architecture-and-tech-stack)
4. [Prerequisites](#prerequisites)
5. [Installation & Setup](#installation--setup)
6. [Environment Variables](#environment-variables)
7. [Running the Application](#running-the-application)
8. [Usage Guide](#usage-guide)
9. [Project Structure](#project-structure)

---

## Overview
**Time Capsule Messenger** is a full-stack Flask application designed with a sleek, modern glassmorphism UI. Users can log in using their WhatsApp number, create digital "Time Capsules" containing text messages, and schedule them for future delivery. The backend utilizes `APScheduler` to continuously monitor pending capsules and dispatches them via the **Twilio WhatsApp API** when their delivery time arrives.

## Features
* **WhatsApp OTP Authentication**: Secure login mechanism requiring a WhatsApp number and an OTP (One-Time Password) for verification.
* **Schedule Future Messages**: Select the exact date and local time for a message to be delivered.
* **Custom Recipients**: Send a time capsule to yourself or specify another recipient's WhatsApp number.
* **Privacy Controls**: 
  * **Private**: Only delivered to the specified WhatsApp number.
  * **Public**: Appears on the application's global "Messages from the Past" public feed once the delivery date has passed.
* **Secret Capsules (Password Protected)**: Add a password constraint. The recipient will receive a notification that a locked capsule awaits them.
* **AI Inspiration**: Get pseudo-AI generated motivational quotes and reflections when creating a capsule.
* **Dashboard Management**: View all your scheduled and delivered capsules. Delete pending capsules if you change your mind.
* **Futuristic Glassmorphism UI**: Beautifully crafted frontend using Tailwind CSS for a premium user experience.

## Architecture and Tech Stack
* **Frontend:** HTML5, CSS3, JavaScript, TailwindCSS (CDN), Flatpickr (Date/Time UI)
* **Backend:** Python 3, Flask framework, Flask-SQLAlchemy, Werkzeug (Security)
* **Database:** PostgreSQL (Neon Serverless Postgres recommended) or SQLite (fallback)
* **Task Scheduler:** APScheduler (Background task running every minute)
* **Messaging API:** Twilio API for WhatsApp

## Prerequisites
Before you begin, ensure you have the following installed and set up:
* **Python 3.8+**
* Let pip manage packages: `pip install -r requirements.txt`
* A **Twilio Account** (with the WhatsApp Sandbox configured)
* A **PostgreSQL Database** (e.g., via Neon.tech)

## Installation & Setup

1. **Clone the repository or navigate to the project folder:**
   ```bash
   cd "Time Capsule Messenger"
   ```

2. **Install necessary Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the Database:**
   Ensure your database connection string is set up (see Environment Variables). Then run the application once to automatically build the necessary tables via SQLAlchemy's `db.create_all()`.

## Environment Variables
The application relies on a `.env` file situated in the project's root directory. Create a file named `.env` and configure the following variables (do not wrap values in quotes):

```env
# Flask Configuration
SECRET_KEY=your_secure_random_secret_key_here

# Database Configuration (PostgreSQL URI)
# Example: postgresql://user:password@hostname/dbname
DATABASE_URL=your_postgresql_database_url_here

# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_WHATSAPP_NUMBER=your_twilio_whatsapp_number_here

# Note for Twilio Sandbox: 
# The TWILIO_WHATSAPP_NUMBER format usually looks like: whatsapp:+14155238886
# User numbers must also be formatted with the 'whatsapp:' prefix internally.
```

**Security Warning**: Never commit your `.env` file to public version control (e.g., GitHub).

## Running the Application

To start the Flask development server and the background scheduler simultaneously, run:

```bash
python app.py
```

You should see terminal output indicating that the Application is starting, Database tables have been verified, the APScheduler has started, and Flask is serving on `http://127.0.0.1:5000`.

## Usage Guide

1. **Twilio Sandbox Opt-in**: If you are using the Twilio Sandbox for evaluation, ensure you and any recipients have joined the sandbox by messaging the designated Twilio join code (e.g., "join your-sandbox-word") to your Twilio WhatsApp number.
2. **Access the App**: Navigate to `http://127.0.0.1:5000` in your web browser.
3. **Login**: Enter your Name and WhatsApp Number (including the country code, e.g., +1234567890).
4. **OTP Verification**: For local development, if Twilio is not fully configured, check your server console/terminal—the OTP will be printed there. Enter the code in the UI.
5. **Create a Capsule**:
   - Navigate to **Create**.
   - Type your message.
   - Pick a **Delivery Date** and **Delivery Time** using the popup calendar/clock UI.
   - (Optional) Provide a **Recipient WhatsApp Number**. 
   - Select the privacy settings.
   - Click **Lock Capsule & Schedule**.
6. **Wait for Delivery**: Keep the Flask server (`app.py`) running. The background scheduler checks everything minute. Once the system clock passes the selected delivery time, the WhatsApp message will be dispatched!

## Project Structure

```text
Time Capsule Messenger/
│
├── .env                        # Environment variables (Credentials - Do NOT share)
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── app.py                      # Main Flask application and entry point
├── config.py                   # Configuration loader for Flask and DB
├── add_recipient_column.py     # Schema migration script (utility)
│
├── database/                   # Database related logic
│   ├── __init__.py
│   └── models.py               # SQLAlchemy Database Models (User, Capsule)
│
├── routes/                     # Application routing controllers
│   ├── __init__.py
│   ├── auth.py                 # Login, OTP generation, and session logic
│   └── capsule.py              # Creation, Dashboard, Deletion, and Public feed
│
├── services/                   # Core backend services
│   ├── __init__.py
│   ├── scheduler.py            # APScheduler background job implementation
│   └── whatsapp_service.py     # Twilio API integration and message formatting
│
├── static/                     # Public static assets
│   ├── css/
│   │   └── styles.css          # Core visual styling, glassmorphism UI rules
│   └── images/                 # Image assets (if applicable)
│
└── templates/                  # HTML templates (Jinja2)
    ├── base.html               # Main application layout and navigation
    ├── index.html              # Landing page
    ├── login.html              # WhatsApp number entry UI
    ├── verify_otp.html         # OTP verification UI
    ├── dashboard.html          # User's personal scheduled capsules list
    ├── create_capsule.html     # Form to schedule a new capsule
    └── public.html             # Global view of public delivered capsules
```

---
*Time Capsule Messenger - Building connections across time.*
