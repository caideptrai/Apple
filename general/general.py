from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from utils.tools import MessageType
# from models import Games, Platform, User, Orders
from models import Games, User, Orders

general_blueprint = Blueprint('general', __name__, template_folder='templates', static_folder='static', static_url_path='/assets')

@general_blueprint.route('/', methods=["POST", "GET"])
def index():
    game_hero_section = Games.query.filter_by(name='Rocket League').first()
    games_best_seller = Games.query.order_by(Games.purchase_number).limit(10).all()
    games_by_price = Games.query.order_by(Games.price).all()

    # Kiểm tra xem có session người dùng nào đang tồn tại hay không
    if 'user_id' not in session:
        # Nếu không, đăng nhập với người dùng có id là 1
        user = User.query.get(1)
        session['user_id'] = user.id
        session['current_user'] = {
            'username': user.username,
            'name': user.name,
            'budget': user.budget
        }

    curr_user = User.query.get(session['user_id'])

    cart_length = Orders.query.filter_by(customer_id=curr_user.id).count()
    session['subtotal'] = 0
    session['cart'] = []
    for order in curr_user.orders:
        game_order_obj = {
            'image': order.game.image,
            'name': order.game.name,
            'price': order.game.price
        }
        session['cart'].append(game_order_obj)
        session['subtotal'] += order.game.price

    session['cart_length'] = cart_length
    session['current_user'] = {
        'username': curr_user.username,
        'name': curr_user.name,
        'budget': curr_user.budget
    }

    return render_template('general/index.html', games_best_seller=games_best_seller, game_hero_section=game_hero_section)