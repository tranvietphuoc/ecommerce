import os
from flask import url_for, current_app, session
from ecommerce import mail
from flask_mail import Message
from PIL import Image
from ecommerce.models import User
import hashlib


# Save profile picture
def save_picture(form_picture, user_name):
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_name = hashlib.sha256(user_name.encode("utf-8")).hexdigest()[0:16] + file_ext
    picture_path = os.path.join(
        current_app.root_path, "static/assets/users", picture_name
    )
    output_size = (100, 100)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    return picture_name


def send_reset_token(user):
    token = user.get_reset_token()
    msg = Message(
        "Password reset request", sender="noreply@gmail.com", recipients=[user.email],
    )
    msg.body = f"""
    To reset your password, visit the following link:
    {url_for('users.reset_password', token=token, _external=True)}
    If you did not make this request, please ignore this email changes be made
    """
    mail.send(msg)
