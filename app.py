from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import joblib
import re
import pyrebase
import datetime

load_dotenv()

firebaseConfig = {
    'apiKey': os.getenv('FIREBASE_API_KEY'),
    'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
    'databaseURL': os.getenv('FIREBASE_DATABASE_URL'),
    'projectId': os.getenv('FIREBASE_PROJECT_ID'),
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
    'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    'appId': os.getenv('FIREBASE_APP_ID'),
    'measurementId': os.getenv('FIREBASE_MEASUREMENT_ID')
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

def unix_time():
    presentDate = datetime.datetime.now()
    unix_timestamp = datetime.datetime.timestamp(presentDate)*1000
    round_unix_time = round(unix_timestamp)
    return str(round_unix_time)

def pushExp(intent, amount):
    unixTime = unix_time()
    data = {
        "intent": intent,
        "amount": amount
    }
    db.child("Expenses").child(unixTime).set(data)
    return "Expense pushed successfully!"

# Regular expression pattern to match expenses in the format "<amount> Rs" or "Rs <amount>"
expense_pattern = r'(?i)(?:Rs\.?|rs\.?)? (\d+(?:\.\d+)?)|(?:\d+(?:\.\d+)?) (?i)(?:Rs\.?|rs\.?)'

# Function to extract expenses from input text
def extract_expense(input_text):
    match = re.search(expense_pattern, input_text)
    if match:
        # Find the matched group that contains the expense amount
        for group in match.groups():
            if group:
                return float(group)
    return None

app = Flask(__name__)
CORS(app)

# Load trained model and vectorizer
classifier = joblib.load('./models/exp_classifier.joblib')
vectorizer = joblib.load('./models/tfidf_vectorizer.joblib')

@app.route('/')
def index():
    return 'ExpTracker Backend!'

@app.route('/classify', methods=['POST'])
def classify_text():
    data = request.get_json()
    input_text = data['text']
    
    # Preprocess and vectorize input text
    text_vector = vectorizer.transform([input_text])
    
    # Extract Expense
    extracted_exp = extract_expense(input_text)

    # Classify input text
    predicted_label = classifier.predict(text_vector)[0]

    # Push to Firebase
    pushExp(predicted_label, extracted_exp)
    
    return jsonify({'predicted_label': predicted_label, 'expense': extracted_exp})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
