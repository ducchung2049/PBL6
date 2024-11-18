from bson import ObjectId
from flask import Blueprint, jsonify, request
import cloudinary
import cloudinary.uploader
from app.models.user import User

api_user_profile_bp = Blueprint('api_user_profile', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_user_profile_bp.route('/', methods=['PUT'])
def update():
    data = request.form
    file = request.files.get('image')
    user = User.objects.get(id=ObjectId(data['id']))

    if data.get('name'):
        user.name = data['name']
    if data.get('email'):
        user.email = data['email']
    if data.get('username'):
        user.username = data['username']
    if data.get('date_of_birth'):
        user.date_of_birth = data['date_of_birth']
    if data.get('bio'):
        user.bio = data['bio']

    public_id = f"user_{str(user.id)}_avatar"

    if file and allowed_file(file.filename):
        try:
            response = cloudinary.uploader.upload(
                file,
                resource_type="image",
                public_id=public_id,
                overwrite=True,
                transformation=[
                    {
                        'width': 212,
                        'height': 212,
                        'crop': 'fill',
                        'gravity': 'face',
                        'quality': 'auto',
                        'fetch_format': 'auto'
                    }
                ]
            )
            avatar_url = response['secure_url']
        except Exception as e:
            print(f"Cloudinary upload error: {e}")
            return jsonify({'error': 'Image upload failed'}), 500
    else:
        avatar_url = None
    if avatar_url:
        user.avatar_url = avatar_url
    user.save()
    return jsonify({'message': 'User profile updated successfully'}), 200
