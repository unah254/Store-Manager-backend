import os

import click

from app import create_app

# from app.api.v2.models import User, ProductItem

#config_name = os.getenv('APP_SETTINGS')
app = create_app(os.getenv('APP_SETTINGS', 'development') )
# @app.cli.command()
# def migrate():
#     """ create test tables """

#     User().create()
#     ProductItem().create()


# @app.cli.command()
# def drop():
#     """ drop test tables if they exist """

#     User().drop()
#     ProductItem().drop()

# # add admin to db
# @app.cli.command()
# def create_admin():
#     """ add default admin """
#     user = User(email='unahgrace@gmail.com',
#                 password='Unah123', admin=True)
#     user.add()



if __name__ == '__main__':
    app.run(debug=True)