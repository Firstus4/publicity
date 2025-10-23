from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory, session
from werkzeug.utils import secure_filename
from models import db, Student
from forms import RegistrationForm
import os, json

public_bp = Blueprint('public', __name__)

ALLOWED_EXT = {'png','jpg','jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT

def save_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        count, base, ext = 1, *os.path.splitext(filename)
        while os.path.exists(filepath):
            filename = f"{base}_{count}{ext}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            count += 1
        file.save(filepath)
        return filename
    return None

@public_bp.route('/')
@public_bp.route('/home', methods=['GET', 'POST'])
def home():
    """Session control"""
    if not session.get('register'):
        return render_template('home.html')
    else:
        if request.method == 'POST':
            return render_template('home.html')
        return render_template('home.html')

@public_bp.route('/started')
def started():
    """Redirect to registration"""
    return redirect(url_for('public.register'))

@public_bp.route('/register', methods=['GET','POST'])
def register():
    with open('data/states_lgas.json') as f:
        states_lgas = json.load(f)
    with open('data/schools.json') as f:
        schools = json.load(f)
    with open('data/country_codes.json') as f:
        country_codes = json.load(f)
    with open('data/units.json') as f:
        units = json.load(f)

    form = RegistrationForm()
    form.state.choices = [('', 'Select')] + [(s,s) for s in sorted(states_lgas.keys())]
    form.school.choices = [('', 'Select')] + [(sch['name'], f"{sch['name']}") for sch in schools] + [('Other', 'Other (Specify below)')]
    form.country_code.choices = [('', 'Select Country Code')] + [(cc['code'], f"{cc['code']} ({cc['name']})") for cc in country_codes]
    form.unit.choices = [(unit['name'], unit['name']) for unit in units]

    # Populate LGA choices based on selected state
    if request.method == 'POST' and form.state.data:
        form.lga.choices = [(lga, lga) for lga in states_lgas.get(form.state.data, [])]

    if request.method == 'POST' and form.validate_on_submit():
        photo_file = request.files.get('photo')
        photo_filename = save_file(photo_file)
        
        # Handle multiple units - store as comma-separated string
        selected_units = form.unit.data
        units_str = ','.join(selected_units) if selected_units else ""
        
        student = Student(
            first_name=(form.first_name.data or "").strip(),
            middle_name=(form.middle_name.data or "").strip(),
            last_name=(form.last_name.data or "").strip(),
            sex=form.sex.data or "",
            state=form.state.data or "",
            lga=form.lga.data or "",
            dob=form.dob.data.strftime('%m-%d') if form.dob.data else "",
            email=(form.email.data or "").strip(),
            phone=f"{form.country_code.data or ''}{(form.phone.data or '').strip()}",
            ppa=(form.ppa.data or "").strip(),
            school=form.school.data or "",
            unit=units_str,
            room_allocated=(form.room_allocated.data or "").strip(),
            photo_filename=photo_filename
        )
        db.session.add(student)
        db.session.commit()
        flash(f'Registration successful! Welcome {student.first_name}!', 'success')
        # Stay on registration page to show success message
        # Create a new form instance to reset the form
        form = RegistrationForm()
        form.state.choices = [('', 'Select')] + [(s,s) for s in sorted(states_lgas.keys())]
        form.school.choices = [('', 'Select')] + [(sch['name'], f"{sch['name']}") for sch in schools] + [('Other', 'Other (Specify below)')]
        form.country_code.choices = [('', 'Select Country Code')] + [(cc['code'], f"{cc['code']} ({cc['name']})") for cc in country_codes]
        form.unit.choices = [(unit['name'], unit['name']) for unit in units]
    
    # If form validation failed and it was a POST request, show errors
    if request.method == 'POST':
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')

    return render_template('register.html', form=form, states_lgas=states_lgas)

@public_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@public_bp.route('/profile/<int:student_id>')
def profile(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student_profile.html', student=student)
