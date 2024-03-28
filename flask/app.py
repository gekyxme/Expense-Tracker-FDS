from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load trained model and vectorizer
with open('../models/exp_classifier.pkl', 'rb') as f:
    classifier = pickle.load(f)

with open('../models/tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

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
