# from flask import Blueprint, render_template
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, db


auth_blueprint = Blueprint('auth', __name__, template_folder='templates')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        name = request.form.get('name')  # Thêm dòng này để lấy giá trị tên từ form

        # Kiểm tra xác nhận mật khẩu và kiểm tra email đã tồn tại
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please use a different email.', 'error')
            return redirect(url_for('auth.register'))

        # Tạo một hash password và tạo một instance của User
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, hash_password=hashed_password, name=name)  # Thêm name vào đây

        # Thêm user mới vào cơ sở dữ liệu và chuyển hướng người dùng đến trang đăng nhập
        db.session.add(new_user)
        db.session.commit()
        flash('Registered successfully. You can now log in.', 'success')
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
