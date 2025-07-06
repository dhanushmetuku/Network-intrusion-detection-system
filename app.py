from flask import Flask, render_template, request
import pickle
import numpy as np
import random

app = Flask(__name__)

# Load the trained model
with open('trained_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the label encoder
with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# Updated attack mapping that matches your model's labels
attack_mapping = {
    'apache2': 'DoS',
    'back': 'DoS',
    'buffer_overflow': 'U2R',
    'ftp_write': 'R2L',
    'guess_passwd': 'R2L',
    'httptunnel': 'R2L',
    'imap': 'R2L',
    'ipsweep': 'Probe',
    'land': 'DoS',
    'loadmodule': 'U2R',
    'mailbomb': 'DoS',
    'mscan': 'Probe',
    'multihop': 'R2L',
    'named': 'R2L',
    'neptune': 'DoS',
    'nmap': 'Probe',
    'normal': 'Normal',
    'perl': 'U2R',
    'phf': 'R2L',
    'pod': 'DoS',
    'portsweep': 'Probe',
    'processtable': 'DoS',
    'ps': 'U2R',
    'rootkit': 'U2R',
    'saint': 'Probe',
    'satan': 'Probe',
    'sendmail': 'R2L',
    'smurf': 'DoS',
    'snmpgetattack': 'R2L',
    'snmpguess': 'R2L',
    'sqlattack': 'U2R',
    'teardrop': 'DoS',
    'udpstorm': 'DoS',
    'warezmaster': 'R2L',
    'worm': 'R2L',
    'xlock': 'R2L',
    'xsnoop': 'R2L',
    'xterm': 'U2R'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Generate more realistic features
    input_features = [0] * 41
    # Set some random spikes
    for i in random.sample(range(41), 5):
        input_features[i] = random.uniform(1, 100)
    
    features = np.array(input_features).reshape(1, -1)
    
    # Make prediction
    pred_encoded = model.predict(features)
    pred_label = label_encoder.inverse_transform(pred_encoded)[0]
    
    # Clean label by removing trailing dot and convert to lowercase
    clean_label = pred_label.rstrip('.').lower()
    attack_category = attack_mapping.get(clean_label, "Unknown")
    
    # Debug output
    print(f"\nPrediction Debug:")
    print(f"Raw prediction: {pred_label}")
    print(f"Clean label: {clean_label}")
    print(f"Category: {attack_category}")
    
    return render_template(
        'index.html',
        prediction_text=f'Detected Attack: {pred_label} (Category: {attack_category})'
    )

if __name__ == "__main__":
    app.run(debug=True)