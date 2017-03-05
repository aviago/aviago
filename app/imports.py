def import_routes(flask_app):

    from app.views.auth import Auth
    Auth.register(flask_app)

    from app.views.dashboard import Dashboard
    Dashboard.register(flask_app)
    return
