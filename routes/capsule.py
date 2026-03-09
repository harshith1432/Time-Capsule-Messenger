from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.models import db, Capsule, User
from datetime import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

capsule_bp = Blueprint('capsule_bp', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in first.")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@capsule_bp.route('/')
def index():
    return render_template('index.html')

@capsule_bp.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    capsules = Capsule.query.filter_by(user_id=user.id).order_by(Capsule.created_at.desc()).all()
    return render_template('dashboard.html', capsules=capsules, user=user)

@capsule_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_capsule():
    if request.method == 'POST':
        message = request.form.get('message')
        delivery_date = request.form.get('delivery_date') # YYYY-MM-DD
        delivery_time = request.form.get('delivery_time') # HH:MM
        privacy_type = request.form.get('privacy_type', 'private')
        password = request.form.get('password')
        
        recipient_number = request.form.get('recipient_number')
        
        try:
            dt_str = f"{delivery_date} {delivery_time}"
            delivery_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        except Exception:
            flash("Invalid date or time format.")
            return redirect(url_for('capsule_bp.create_capsule'))
            
        if delivery_dt <= datetime.now():
            flash("Delivery time must be in the future.")
            return redirect(url_for('capsule_bp.create_capsule'))
            
        capsule = Capsule(
            user_id=session['user_id'],
            message=message,
            delivery_time=delivery_dt,
            privacy_type=privacy_type,
            recipient_number=recipient_number,
            status='pending'
        )
        
        if password:
            capsule.password_hash = generate_password_hash(password)
            
        db.session.add(capsule)
        db.session.commit()
        flash("Capsule created and scheduled successfully!")
        return redirect(url_for('capsule_bp.dashboard'))
        
    return render_template('create_capsule.html', datetime=datetime)

@capsule_bp.route('/public')
def public_capsules():
    # Show public messages that have already been delivered
    capsules = Capsule.query.filter_by(
        privacy_type='public', 
        status='delivered'
    ).order_by(Capsule.delivery_time.desc()).all()
    return render_template('public.html', capsules=capsules)

@capsule_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_capsule(id):
    capsule = Capsule.query.get_or_404(id)
    if capsule.user_id == session['user_id']:
        db.session.delete(capsule)
        db.session.commit()
        flash("Capsule deleted.")
    return redirect(url_for('capsule_bp.dashboard'))
