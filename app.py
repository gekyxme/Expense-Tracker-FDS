from flask import Flask, request, jsonify
import joblib

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
    
    # Classify input text
    predicted_label = classifier.predict(text_vector)[0]
    
    return jsonify({'predicted_label': predicted_label})

if __name__ == '__main__':
    app.run(debug=True)
