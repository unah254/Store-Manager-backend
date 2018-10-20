import os

from app import create_app



#config_name = os.getenv('APP_SETTINGS')
app = create_app(os.getenv('APP_SETTINGS') or 'development')




if __name__ == '__main__':
    app.run(debug=True)