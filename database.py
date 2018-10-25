# module imports
import os

# local imports
from app.api.v2.models import User

from app import create_app

app = create_app("testing")


def migrate():
    """ create test tables """

    User().create()
    


def drop():
    """ drop test tables if they exist """

    User().drop()
    


def create_admin():
    """ add default admin """
    user = User(email='unahgrace@gmail.com',
                password='Unah123',admin=True)
    user.add()
