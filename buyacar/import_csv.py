import pandas as pd
from buyacar.models import db, Car

# Function to load data from CSV
def load_csv_data():
    db.drop_all()
    db.create_all()    
    csv_file_path = 'buyacar/static/DDW Data.csv'  # Declares path to file stored location
    df = pd.read_csv(csv_file_path)
    for _, row in df.iterrows():
        car = Car(carIndex=row['carIndex'], make=row['make'], model=row['model'], reg=row['reg'], colour=row['colour'], miles=row['miles'],
        price=row['price'], dealer=row['dealer'], town=row['town'], telephone=row['telephone'], description=row['description'], region=row['region'])
        db.session.add(car)
    db.session.commit()

