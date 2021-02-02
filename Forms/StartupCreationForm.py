from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class StartupCreationForm(FlaskForm):
	name = StringField('Название', validators=[DataRequired()])
	description = StringField('Описание', validators=[DataRequired()])
	submit = SubmitField('Создать')