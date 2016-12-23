"""A simple management script."""
import os
import random
import string


if os.path.exists('.env'):
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


from flask_script import Manager
from app import create_app
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


@manager.command
def genkey():
    "Generates flask secret key."
    keys = []
    secret = ''.join(random.choice(string.ascii_letters + string.digits)
        for _ in range(64))
    with open('.env') as env:
        for line in env.readlines():
            if 'SECRET_KEY' not in line:
                keys.append(line)
    with open('.env', 'w') as env:
        for key in keys:
            env.write(key)
        env.write('SECRET_KEY=%s' % secret)


if __name__ == '__main__':
    manager.run()

