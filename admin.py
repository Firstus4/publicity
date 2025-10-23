import os
from flask import Blueprint, render_template, redirect, url_for, flash, request 
from flask_login import login_user, login_required, logout_user, current_user
from models import db, Admin, Student
from forms import AdminLoginForm, AdminRegistrationForm, RegistrationForm
from decorator import super_admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET','POST'])
def login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data.strip()).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            flash('Logged in as admin.', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('Invalid credentials.', 'danger')
    return render_template('admin_login.html', form=form)

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    students = Student.query.order_by(Student.id.desc()).all()
    admins = Admin.query.all()
    return render_template('admin_dashboard.html', students=students, admins=admins, current_user=current_user)

@admin_bp.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    
    import json
    with open('data/states_lgas.json') as f:
        states_lgas = json.load(f)
    with open('data/schools.json') as f:
        schools = json.load(f)
    with open('data/country_codes.json') as f:
        country_codes = json.load(f)
    with open('data/units.json') as f:
        units = json.load(f)

    form = RegistrationForm()
    form.state.choices = [('', 'Select')] + [(s,s) for s in sorted(states_lgas.keys())] # type: ignore
    form.school.choices = [('', 'Select')] + [(sch['name'], f"{sch['name']}") for sch in schools] + [('Other', 'Other (Specify below)')] # pyright: ignore[reportAttributeAccessIssue]
    form.country_code.choices = [('', 'Select Country Code')] + [(cc['code'], f"{cc['code']} ({cc['name']})") for cc in country_codes] # pyright: ignore[reportAttributeAccessIssue]
    form.unit.choices = [(unit['name'], unit['name']) for unit in units]
    
    if request.method == 'POST' and form.state.data:
        form.lga.choices = [('', 'Select')] + [(lga, lga) for lga in states_lgas.get(form.state.data, [])] # pyright: ignore[reportAttributeAccessIssue]
    
    if request.method == 'POST' and form.validate_on_submit():
    
        student.first_name = form.first_name.data.strip()# type: ignore
        student.middle_name = (form.middle_name.data or "").strip()
        student.last_name = form.last_name.data.strip() # type: ignore
        student.sex = form.sex.data
        student.state = form.state.data
        student.lga = form.lga.data
        student.dob = form.dob.data.strftime('%m-%d') # pyright: ignore[reportOptionalMemberAccess]
        student.email = form.email.data.strip() # type: ignore

        phone_data = form.phone.data.strip() # type: ignore
        if not phone_data.startswith('+'):
            student.phone = f"{form.country_code.data}{phone_data}"
        else:
            student.phone = phone_data
        student.ppa = form.ppa.data.strip() # type: ignore
        student.school = form.school.data
        
        selected_units = form.unit.data
        student.unit = ','.join(selected_units) if selected_units else ""
        
        student.room_allocated = form.room_allocated.data.strip()# type: ignore
        
        db.session.commit()
        flash('Student information updated successfully.', 'success')
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'GET':
        form.first_name.data = student.first_name
        form.middle_name.data = student.middle_name
        form.last_name.data = student.last_name
        form.sex.data = student.sex
        form.state.data = student.state
        form.lga.data = student.lga
        
        if student.dob:
            try:
                from datetime import datetime
                form.dob.data = datetime.strptime(f"2024-{student.dob}", '%Y-%m-%d').date()
            except:
                pass
        form.email.data = student.email
    
        if student.phone:
            for cc in country_codes:
                if student.phone.startswith(cc['code']):
                    form.country_code.data = cc['code']
                    form.phone.data = student.phone[len(cc['code']):]
                    break
        form.ppa.data = student.ppa
        form.school.data = student.school
        
        if student.unit:
            form.unit.data = student.unit.split(',')
        
        form.room_allocated.data = student.room_allocated
        
        if student.state:
            form.lga.choices = [('', 'Select')] + [(lga, lga) for lga in states_lgas.get(student.state, [])] # pyright: ignore[reportAttributeAccessIssue]
    
    return render_template('edit_student.html', form=form, student=student, states_lgas=states_lgas)

@admin_bp.route('/delete_student/<int:student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash(f'Student {student.first_name} {student.last_name} has been deleted successfully.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/add_admin', methods=['GET', 'POST'])
@login_required
@super_admin_required
def add_admin():  # renamed
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        email = form.email.data.strip()
        password = form.password.data.strip()

        if Admin.query.filter_by(email=email).first():
            flash('Admin with this email already exists.', 'warning')
            return redirect(url_for('admin.add_admin'))
        
        new_admin = Admin(email=email)
        new_admin.set_password(password)
        db.session.add(new_admin)
        db.session.commit()

        flash(f'New admin ({email}) added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('add_admin.html', form=form)


@admin_bp.route('/delete_admin/<int:admin_id>', methods=['POST'])
@login_required
@super_admin_required
def delete_admin(admin_id):
    admin_to_delete = Admin.query.get_or_404(admin_id)
    if admin_to_delete.role == 'super_admin':
        flash('You cannot delete the super admin.', 'danger')
        return redirect(url_for('admin.dashboard'))

    db.session.delete(admin_to_delete)
    db.session.commit()
    flash('Admin deleted successfully.', 'success')
    return redirect(url_for('admin.dashboard'))