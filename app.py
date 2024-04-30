from flask import Flask, request, jsonify
import joblib
import re

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
    
    return jsonify({'predicted_label': predicted_label, 'expense': extracted_exp})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
