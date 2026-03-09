import os
from app import app, db
from sqlalchemy import text
import traceback

with app.app_context():
    try:
        db.session.execute(text('ALTER TABLE capsules ADD COLUMN recipient_number VARCHAR(20)'))
        db.session.commit()
        print("Successfully added recipient_number column to capsules")
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
