from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from buyacar import app
from datetime import datetime, timezone
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_admin.model.form import InlineFormAdmin
from flask_login import UserMixin, LoginManager, current_user
from flask import render_template

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return render_template('error_pages/403.html')
    
class LogoutMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated

db = SQLAlchemy(app)
migrate = Migrate(app, db)
admin = Admin(app, index_view=MyAdminIndexView())
#admin.add_view(ModelView(Car))
login_manager = LoginManager()
login_manager.init_app(app)
# Tells users what view to go to when they need to login.
login_manager.login_view = "admin.login"

# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Defines models
class Car(db.Model):

    # Create a table in the db
    __tablename__ = 'car'

    carIndex = db.Column(db.Integer, primary_key=True, default=None)
    make = db.Column(db.String(10), default=None)
    model = db.Column(db.String(15), default=None)
    reg = db.Column(db.String(2), default=None)
    colour = db.Column(db.String(10), default=None)
    miles = db.Column(db.String(6), default=None)
    price= db.Column(db.Integer, default=None)
    dealer = db.Column(db.String(50), default=None)
    town = db.Column(db.String(20), default=None)
    telephone = db.Column(db.String(15), default=None)
    description = db.Column(db.String(30), default=None)
    region = db.Column(db.String(10), default=None)
    picture = db.Column(db.String(128), nullable=True)
    # Foreign key to reference the Car that the owner has purchased
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)

    def __str__(self):
        return f'Car {self.carIndex} {self.make} {self.model} {self.dealer} {self.town} {self.telephone} {self.price}'
    
class Client(db.Model):

    # Create a table in the db
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(30), nullable=False)
    town = db.Column(db.String(20), nullable=False)
    postcode = db.Column(db.String(7), nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    
    # Relationship to link owners to their cars
    cars = db.relationship('Car', backref='owner', lazy=True)    

    def __str__(self):
        return f'Owner {self.name} {self.surname} {self.email} {self.phone}'
    
class User(UserMixin ,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(20), unique=True)      
    password = db.Column(db.String(20))

    def __repr__(self):
        return f'User {self.name}'
    
class CarModelView(ModelView):
    column_list = ('carIndex','make', 'model', 'reg', 'colour', 'miles', 'price', 'dealer', 'town', 'telephone', 'description', 'region', 'picture', 'owner')
    form_columns = ('carIndex','make', 'model', 'reg', 'colour', 'miles', 'price', 'dealer', 'town', 'telephone', 'description', 'region', 'picture', 'client_id')
    column_searchable_list = ('carIndex', 'make', 'model', 'client_id')
    
    
class CarInlineModelForm(InlineFormAdmin):
    form_columns = ('carIndex','make', 'model', 'reg', 'colour', 'miles', 'price', 'dealer', 'town', 'telephone', 'description', 'region', 'picture')   
    

class ClientModelView(ModelView):
    column_list = ('name', 'surname', 'email', 'phone', 'address', 'town', 'postcode', 'purchase_date', 'cars')
    inline_models = (CarInlineModelForm(Car),)

    
admin.add_view(CarModelView(Car, db.session))
admin.add_view(ClientModelView(Client, db.session))
admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))

    
        