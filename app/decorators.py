from flask import g, session, redirect, url_for, render_template, flash
from app.models.user import User
from app import app, release_date, release_version
from functools import wraps
from datetime import datetime, timedelta


def global_variables(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.release = {
            'version': release_version,
            'date': release_date,
        }
        try:
            from app.globals import setup_custom_globals
            c = setup_custom_globals()
            if not c[0]:
                raise Exception('Error {0} raised, Cannot continue'.format(c[1]))
        except ImportError:
            raise Exception('Missing custom globals file, Application configuration error')
        return f(*args, **kwargs)
    return decorated_function


def login_required(admin_only=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                app.logger.debug('No user session found, Redirecting to login')
                return redirect(url_for('Auth:index'))

            user_id = session['user_id']

            app.logger.debug('Retrieved {0} from session'.format(user_id))
            user = User.query.filter_by(audit_is_deleted=False, id=user_id).first()
            if not user:
                return redirect(url_for('Auth:index'))

            app.logger.debug('User determined to be {0}'.format(user.username))
            if user.last_seen and user.last_seen < datetime.utcnow() - timedelta(minutes=3600):
                app.logger.debug('User session older than 3600 minutes ago, Redirecting to login')
                del session['user_id']
                return redirect(url_for('Auth:index'))

            if admin_only and not user.account.is_admin:
                flash('Admin privileges required', 'error')
                return render_template('403.html')
            # Update our last seen & add to our globals
            g.user = user
            g.account = user.account
            g.user.last_seen = datetime.utcnow()
            g.user.update()

            app.logger.debug('User authenticated successfully, Allowing through')

            return f(*args, **kwargs)
        return decorated_function
    return decorator
