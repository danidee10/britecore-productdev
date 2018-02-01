from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .models import db, Risk


admin = Admin(name='atmfinda', url='/admin', template_mode='bootstrap3')


admin.add_view(ModelView(Risk, db.session))
