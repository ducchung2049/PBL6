from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, Email

class RegisterGoogleForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Họ và Tên', validators=[DataRequired()])
    date_of_birth = DateField('Ngày sinh', validators=[DataRequired()])
    submit = SubmitField('Tạo tài khoản')