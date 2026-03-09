import os
import logging
from twilio.rest import Client

logger = logging.getLogger(__name__)

def get_twilio_client():
    sid = os.environ.get('TWILIO_ACCOUNT_SID')
    token = os.environ.get('TWILIO_AUTH_TOKEN')
    if not sid or not token:
        logger.warning("Twilio credentials not fully set. WhatsApp messages will only be logged.")
        return None
    return Client(sid, token)

def send_whatsapp_message(to_number, body):
    client = get_twilio_client()
    from_number = os.environ.get('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
    
    if not to_number.startswith('whatsapp:'):
        to_number = f"whatsapp:{to_number}"
        
    try:
        if client:
            message = client.messages.create(
                from_=from_number,
                body=body,
                to=to_number
            )
            logger.info(f"Sent WhatsApp message to {to_number}. SID: {message.sid}")
            return True, message.sid
        else:
            logger.info(f"[MOCK WHATSAPP] To: {to_number} | Body: {body}")
            return True, "mock_sid"
    except Exception as e:
        logger.error(f"Failed to send WhatsApp message: {str(e)}")
        return False, str(e)

def send_otp(to_number, otp):
    message = f"Your Time Capsule Messenger OTP is: {otp}\nDo not share this code with anyone."
    return send_whatsapp_message(to_number, message)

def send_capsule_message(to_number, capsule, user_name):
    created_date = capsule.created_at.strftime('%d %B %Y')
    
    message = (
        f"⏳ *Hello from your past self, {user_name}* ⏳\n\n"
        f"This message was written on: {created_date}\n\n"
        f"Your message:\n"
        f"\"{capsule.message}\"\n\n"
        f"Time Capsule Messenger"
    )
    
    return send_whatsapp_message(to_number, message)
