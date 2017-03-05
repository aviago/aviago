from app import manager, app
from urllib.parse import unquote


@manager.command
def seed_db():
    print('DB seeded successfully')
    return


@manager.command
def list_routes():
    """Lists all routes known to this application"""
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        output.append(line)
    for line in sorted(output):
        print(line)
