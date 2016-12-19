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
    key = ''.join(random.choice(
        string.ascii_letters + string.digits + string.punctuation) 
        for _ in range(64))
    with open('.env', 'a') as env:
        env.write('SECRET_KEY=%s' % key)


if __name__ == '__main__':
    manager.run()

