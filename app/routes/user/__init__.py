from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity

from app.decorators import login_required
from app.models.user import User

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    current_user_id = get_jwt_identity()
    user = User.objects(id=current_user_id).first()
    if user:
        return jsonify({
            "username": user.username,
            "email": user.email
        }), 200
    return jsonify({"message": "User not found"}), 404

# @user_bp.route('/update', methods=['POST'])
# @login_required
# def update_profile():
#     current_user_id = get_jwt_identity()
#     user = User.objects(id=current_user_id).first()
