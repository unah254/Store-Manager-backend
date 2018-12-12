# module imports
import os

# local imports
from app.api.v2.models import User, ProductItem, SalesRecord

from app import create_app

app = create_app("testing")


def migrate():
    """ create test tables """
    User().create()
    ProductItem().create()
    SalesRecord().create()


def drop():
    """ drop test tables if they exist """

    User().drop()
    ProductItem().drop()
    SalesRecord().drop()


def create_admin():
    """ add default admin """
    user = User(email='unahgrace@gmail.com',
                password='Unah123', admin=True)
    user.add()
