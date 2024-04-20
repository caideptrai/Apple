from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Lấy thông tin từ form
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        budget = request.form.get('budget')

        # Kiểm tra xem có bất kỳ trường nào trống không
        if not (username and email and password and name and phone_number and budget):
            error_message = 'Please fill in all fields.'
            return render_template('register.html', error_message=error_message)

        # Kiểm tra xem email đã được sử dụng chưa
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            error_message = 'Email already exists. Please use a different email.'
            return render_template('register.html', error_message=error_message)

        # Tạo hash password
        hashed_password = generate_password_hash(password)

        # Tạo user mới
        new_user = User(
            username=username,
            email=email,
            hash_password=hashed_password,
            role='customer',
            name=name,
            phone_number=phone_number,
            budget=budget
        )

        # Thêm user mới vào cơ sở dữ liệu
        db.session.add(new_user)
        db.session.commit()

        # Đăng ký thành công, chuyển hướng đến trang đăng nhập
        return redirect(url_for('auth.login'))

    return render_template('register.html')



@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # # Tìm người dùng trong cơ sở dữ liệu dựa trên email
        user = User.query.filter_by(email=email).first()

        # if user and check_password_hash(user.hash_password, password):
        if user and check_password_hash(user.hash_password, password):
            # Xác thực thành công, đặt thông tin người dùng vào session
            session['user_id'] = user.id
            # return render_template('general/index.html')
            return redirect(url_for('general.index'))
        else:
            # Xác thực thất bại, hiển thị thông báo lỗi
            error_message = "Invalid email or password. Please try again."
            return render_template('login.html', error_message=error_message, password = password, email = email)

        # if user:
        #     if check_password_hash(user.password, password):
        #         flash('Logged in successfully!', category='success')
        #         login_user(user, remember=True)
        #         return redirect(url_for('views.home'))
        #     else:
        #         flash('Incorrect password, try again.', category='error')
        # else:
        #     flash('Email does not exist.', category='error')
    return render_template('login.html')
