# Carga de modelo
import joblib

class Model:
  def __init__(self, model_path):
    saved = joblib.load(model_path)

    self.vectorizer = saved['vectorizer']
    self.model = saved['model']

  def predict_code(self, code):
    X = self.vectorizer.transform([code])

    return self.model.predict(X)[0], self.model.predict_proba(X)[0]
