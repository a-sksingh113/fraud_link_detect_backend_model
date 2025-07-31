import re
import string
import pandas as pd
import pickle
from pathlib import Path

# Optional: enable logging instead of print
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Suspicious keywords that often appear in spam URLs
suspicious_keywords = [
    'login', 'signin', 'verify', 'update', 'banking',
    'account', 'secure', 'ebay', 'paypal'
]

# Load the trained model (.pkl file)
model_path = Path(__file__).parent.parent / "model" / "link prediction model.pkl"
with open(model_path, "rb") as f:
    model = pickle.load(f)

# Feature extraction function
def extract_features(url):
    features = {}

    features['url_length'] = len(url)
    features['num_digits'] = sum(c.isdigit() for c in url)
    features['num_special_chars'] = sum(c in string.punctuation for c in url)
    features['num_subdomains'] = url.count('.') - 1
    features['has_ip'] = int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', url)))
    features['has_https'] = int('https' in url.lower())
    features['num_params'] = url.count('?')
    features['num_fragments'] = url.count('#')
    features['num_slashes'] = url.count('/')
    features['has_suspicious_words'] = int(any(word in url.lower() for word in suspicious_keywords))

    tld = url.split('.')[-1]
    features['tld_length'] = len(tld)
    features['is_common_tld'] = int(tld in ['com', 'org', 'net', 'edu', 'gov'])
    features['has_hex'] = int(bool(re.search(r'%[0-9a-fA-F]{2}', url)))
    features['repeated_chars'] = int(bool(re.search(r'(.)\1{3,}', url)))

    return pd.Series(features)

# Prediction function with logging
def predict_from_url(url: str) -> int:
    features_series = extract_features(url)

    logging.info(f"\n📦 Extracted features for URL: {url}")
    for key, value in features_series.items():
        logging.info(f"  {key}: {value}")

    df = pd.DataFrame([features_series])
    prediction = model.predict(df)[0]

    logging.info(f"🔮 Prediction: {prediction} (1 = spam, 0 = safe)\n")
    return int(prediction)

# Optional: quick test
if __name__ == "__main__":
    test_url = "https://www.google.com"
    predict_from_url(test_url)
