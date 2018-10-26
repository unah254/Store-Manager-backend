
from flask_script import Manager

from app import create_app
# import user model
from app.api.v2.models import User, ProductItem

app = create_app('testing')

# for  running commands on terminal
manager = Manager(app)



# usage python manage.py migrate
@manager.command
def migrate():
    User().create()
    ProductItem().create()
@manager.command
def drop():
    """ drop test tables if they exist """

    User().drop()
    ProductItem().drop()

# usage python manage.py create_admin
@manager.command
def create_admin():
    """ add admin """
    user = User(email='unahgrace@gmail.com',
                password='Unah123', admin=True)
    user.add()
    


if __name__ == '__main__':
    manager.run()