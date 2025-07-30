import joblib
import os

# --- Load the trained model ---
# Construct the path to the model file relative to this script's location
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'contract_classifier_model.joblib')

try:
    model = joblib.load(MODEL_PATH)
    print("Contract classifier model loaded successfully.")
except FileNotFoundError:
    print(f"Error: Model file not found at {MODEL_PATH}")
    model = None
except Exception as e:
    print(f"An error occurred while loading the model: {e}")
    model = None


def classify_contract(text: str) -> str:
    """
    Classifies the contract type using the pre-trained machine learning model.
    """
    if model is None:
        return "Model not loaded"

    try:
        # The model expects a list of texts, so we wrap our text in a list.
        # The prediction will also be a list, so we take the first element.
        prediction = model.predict([text])
        return prediction[0]
    except Exception as e:
        print(f"Error during classification: {e}")
        return "Classification failed"
