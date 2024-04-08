from flask import Flask
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
# Ensures the flag is set to False initially
#app.config['DATA_LOADED'] = False

# This code is necessary only once for the very first app launch
# Ensures that csv file is imported only once during the lifetime of app
#if not app.config.get('DATA_LOADED', False):
    #with app.app_context():        
        #from buyacar.import_csv import load_csv_data
        #load_csv_data()
    #app.config['DATA_LOADED'] = True 
# Routes
from buyacar.core.views import core
from buyacar.error_pages.handlers import error_pages
from buyacar.user.views import users

app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)