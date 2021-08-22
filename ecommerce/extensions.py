from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_migrate import Migrate
from flask_login import LoginManager


# mail
mail = Mail()
# babel
babel = Babel()
# sqlalchemy
db = SQLAlchemy()
# migrate
migrate = Migrate()
# login manager
login_manager = LoginManager()

