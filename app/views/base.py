from flask_classful import FlaskView
from app.decorators import login_required, global_variables


class BaseView(FlaskView):
    decorators = [login_required(admin_only=True), global_variables]
    trailing_slash = False


class BaseUserView(FlaskView):
    decorators = [login_required(admin_only=False), global_variables]
    trailing_slash = False
