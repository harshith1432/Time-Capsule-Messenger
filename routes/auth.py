from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.models import db, User
from services.whatsapp_service import send_otp
import random

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        number = request.form.get('whatsapp_number')
        
        if not name or not number:
            flash("Name and WhatsApp number are required.")
            return redirect(url_for('auth.login'))
            
        # Clean number (basic)
        number = number.strip().replace(' ', '')
        
        user = User.query.filter_by(whatsapp_number=number).first()
        if not user:
            user = User(name=name, whatsapp_number=number)
            db.session.add(user)
            db.session.commit()
            
        # Generate OTP
        otp = str(random.randint(100000, 999999))
        session['otp'] = otp
        session['temp_user_id'] = user.id
        
        success, msg = send_otp(number, otp)
        if success:
            flash("OTP sent to your WhatsApp.")
            return redirect(url_for('auth.verify_otp'))
        else:
            flash("Failed to send OTP. Try again.")
            return redirect(url_for('auth.login'))
            
    return render_template('login.html')

@auth_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if 'temp_user_id' not in session:
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        user_otp = request.form.get('otp')
        if user_otp == session.get('otp'):
            user = User.query.get(session['temp_user_id'])
            user.otp_verified = True
            db.session.commit()
            
            session['user_id'] = user.id
            session.pop('otp', None)
            session.pop('temp_user_id', None)
            
            flash("Successfully logged in!")
            return redirect(url_for('capsule_bp.dashboard'))
        else:
            flash("Invalid OTP.")
            
    return render_template('verify_otp.html') # A small template for OTP form

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('auth.login'))
