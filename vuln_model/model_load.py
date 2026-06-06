# Carga de modelo
import joblib

model_path = 'vuln_model/vulnerability_detector.pkl'

saved = joblib.load(model_path)

vectorizer = saved['vectorizer']
model = saved['model']

# Ejecución individual de código
## Ingresar su propio código para comprobarlo
code = """
Path = os.path.basename(filename);
open(os.path.join(upload_dir, path), 'rb');
"""

X = vectorizer.transform([code])

prediction = model.predict(X)[0]
probability = model.predict_proba(X)[0]

print("Vulnerable:", prediction)
print("Probabilidades:", probability)
