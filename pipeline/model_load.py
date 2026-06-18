# Carga de modelo
import joblib

VULNERABLE_THRESHOLD = 0.66

class Model:
  def __init__(self, model_path):
    saved = joblib.load(model_path)

    self.vectorizer = saved['vectorizer']
    self.model = saved['model']

  def predict_code(self, code):
    X = self.vectorizer.transform([code])
    probs = self.model.predict_proba(X)[0]

    is_vulnerable = probs[1] >= VULNERABLE_THRESHOLD

    return is_vulnerable, probs
