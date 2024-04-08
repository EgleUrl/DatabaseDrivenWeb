from flask import render_template, request, Blueprint, session, redirect, url_for, jsonify
from buyacar.models import db, Car, Client

from buyacar.core.forms import PurchaseForm
import json
import stripe

# This is your test secret API key.
stripe.api_key = 'sk_test_51Oyfo6P7tQOhIrsaoqV41g2YaSDc2cAB6Qjt4tXoKWfVkQ6eAhRqatbYrHxKhi71AbiAOgV4y3HL0TfL3Myjl82I003C2UEtc4'

# Creates blueprint for core
core = Blueprint('core', __name__)

# Function to load data from CSV, to be called only once
#@app.before_first_request

@core.route('/')
def index():    
    return render_template('index.html')

# Route for displaying all cars without any filters
@core.route('/cars')
def cars():
    page = request.args.get('page', 1, type=int)
    filters = {}
    priceFilters = {}
    # Loads distinct values for all filters
    makes = Car.query.with_entities(Car.make).distinct().all()
    models = Car.query.with_entities(Car.model).distinct().all()
    towns = Car.query.with_entities(Car.town).distinct().all()
    regions = Car.query.with_entities(Car.region).distinct().all()
    # Query to get all cars
    query = Car.query
    cars = query.paginate(page=page, per_page=6)
    return render_template('cars.html', cars=cars, filters=filters, priceFilters=priceFilters, makes=makes, models=models, towns=towns, regions=regions)

@core.route('/filtered-cars', methods=['GET', 'POST'])
def filtered_cars():
    page = request.args.get('page', 1, type=int)

    # Defines filters dictionary
    if request.method == 'POST':
        # Updates session with form data for each filter
        session['make'] = request.form.get('make')
        session['model'] = request.form.get('model')
        session['town'] = request.form.get('town')
        session['region'] = request.form.get('region')
        session['minPrice'] = request.form.get('minPrice')
        session['maxPrice'] = request.form.get('maxPrice')

    # Checks for GET request and updates session (for images in index.html)
    if request.method == 'GET':
        session['make'] = request.args.get('make')
        session['model'] = request.args.get('model')

        
    # Loads distinct values for all filters
    makes = Car.query.with_entities(Car.make).distinct().all()
    models = Car.query.with_entities(Car.model).distinct().all()
    towns = Car.query.with_entities(Car.town).distinct().all()
    regions = Car.query.with_entities(Car.region).distinct().all()

    # Retrieves session data to maintain filter state and stores in a dictionary
    filters = {
        'make': session.get('make'),
        'model': session.get('model'),
        'town': session.get('town'),
        'region': session.get('region')
    }
    # Retrieves min and max price from session and stores into a separate dictionary
    priceFilters = {
        'minPrice': session.get('minPrice'),
        'maxPrice': session.get('maxPrice')
    }
    # Builds query based on session filters
    query = Car.query
    for key, value in filters.items():
        if value:
            query = query.filter(getattr(Car, key) == value)    

    # Filters by price range if both min and max prices are provided    
    if priceFilters['minPrice'] and priceFilters['maxPrice']:
        query = query.filter(Car.price.between(priceFilters['minPrice'], priceFilters['maxPrice']))
    elif priceFilters['minPrice']:
        query = query.filter(Car.price >= priceFilters['minPrice'])
    elif priceFilters['maxPrice']:
        query = query.filter(Car.price <= priceFilters['maxPrice'])    

    # Execute the query and paginate results
    cars = query.paginate(page=page, per_page=6)
    return render_template('cars.html', cars=cars, filters=filters, priceFilters=priceFilters, makes=makes, models=models, towns=towns, regions=regions)
 
@core.route('/clear-filters')
def clear_filters():
    # List of filter keys to clear from the session
    filter_keys = ['make', 'model', 'town', 'region', 'colour', 'miles', 'price_min', 'price_max']
    # Clear each filter key from the session
    for key in filter_keys:
        session.pop(key, None)
    # Redirects back to the cars page
    return redirect(url_for('core.cars'))

# Handles AJAX request and returns models for a selected make
@core.route('/get-models/<make>')
def get_models(make):
    models = Car.query.filter_by(make=make).with_entities(Car.model).distinct().all()
    model_list = [model[0] for model in models]  # Converts to a simple list
    return jsonify(model_list)

# Handles AJAX request and returns towns for a selected model
@core.route('/get-towns/<model>')
def get_towns(model):
    towns = Car.query.filter_by(model=model).with_entities(Car.town).distinct().all()
    town_list = [town[0] for town in towns]  # Converts to a simple list
    return jsonify(town_list)

# Handles AJAX request and returns regions for a selected model
@core.route('/get-regions/<model>')
def get_regions(model):
    regions = Car.query.filter_by(model=model).with_entities(Car.region).distinct().all()
    region_list = [region[0] for region in regions]  # Converts to a simple list
    return jsonify(region_list)

@core.route('/carform/<int:car_id>', methods=['GET','POST'])
def carform(car_id):
    car = Car.query.filter_by(carIndex=car_id).first()
    form = PurchaseForm()
    if form.validate_on_submit():
        client = Client(name=form.name.data,
                        surname=form.surname.data,
                        email=form.email.data,
                        phone=form.telephone.data,
                        address=form.address.data,
                        town=form.town.data,
                        postcode=form.postcode.data                        
                    )        
        db.session.add(client)
        db.session.commit() 
        car.client_id = client.id
        db.session.add(car)
        db.session.commit()      
        return redirect(url_for('core.checkout', car_id=car.carIndex))    
    return render_template('carform.html', car=car, form=form)

@core.route('/checkout/<int:car_id>')
def checkout(car_id):
    car = Car.query.get(car_id) 
       
    return render_template('checkout.html', car=car)

@core.route('/create-payment-intent/<car_price>', methods=['GET', 'POST'])
def create_payment(car_price):
    # Convert car_price to an integer
    try:
        data = json.loads(request.data)
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=car_price,
            currency='gbp',
            # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
            automatic_payment_methods={
                'enabled': True,
            },
        )
        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403

@core.route('/thankyou/<car_id>')
def thankyou(car_id):
    car = Car.query.get(car_id) 
    
    return render_template('thankyou.html', car=car)
    


