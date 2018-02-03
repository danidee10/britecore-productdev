from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .models import db, Insurer, RiskClient, RiskTemplate


admin = Admin(name='atmfinda', url='/admin', template_mode='bootstrap3')


admin.add_view(ModelView(Insurer, db.session))
admin.add_view(ModelView(RiskClient, db.session))
admin.add_view(ModelView(RiskTemplate, db.session))
