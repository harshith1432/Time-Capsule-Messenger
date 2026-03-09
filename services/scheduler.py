import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from services.whatsapp_service import send_capsule_message

logger = logging.getLogger(__name__)

def check_pending_capsules(app):
    # We must run this inside the application context to access the database
    with app.app_context():
        from database.models import db, Capsule, User
        logger.info("Scheduler running: Checking for pending capsules...")
        
        # Find all capsules that are pending and their delivery time has passed
        # Get current local time
        now = datetime.now()
        due_capsules = Capsule.query.filter(
            Capsule.status == 'pending',
            Capsule.delivery_time <= now
        ).all()
        
        for capsule in due_capsules:
            try:
                # Format the message
                user = User.query.get(capsule.user_id)
                target_number = capsule.recipient_number if capsule.recipient_number else user.whatsapp_number
                send_capsule_message(target_number, capsule, user.name)
                
                # Update status
                capsule.status = 'delivered'
                db.session.commit()
                logger.info(f"Successfully delivered capsule {capsule.id} to {user.whatsapp_number}")
            except Exception as e:
                logger.error(f"Failed to deliver capsule {capsule.id}: {str(e)}")
                # Depending on requirement, we could set status to 'failed' or keep pending for retry
                # capsule.status = 'failed'
                # db.session.commit()

def init_scheduler(app):
    scheduler = BackgroundScheduler()
    # Check every minute
    scheduler.add_job(func=check_pending_capsules, args=[app], trigger="interval", seconds=60)
    scheduler.start()
    logger.info("APScheduler started")
    return scheduler
