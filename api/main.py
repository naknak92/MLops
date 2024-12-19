import mlflow
import mlflow.pyfunc
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuration du serveur de tracking MLflow
mlflow.set_tracking_uri("http://34.170.123.233:5000")  # Remplace avec l'IP de ton serveur MLflow

# Charger le modèle MLflow depuis le Model Registry
MODEL_URI = "models:/iris_model/1"
  # Nom du modèle et version
model = mlflow.pyfunc.load_model(MODEL_URI)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Récupérer les données d'entrée
        data = request.get_json()
        features = data["features"]  # Attendre une liste de features
        prediction = model.predict([features])
        
        # Retourner la prédiction
        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    # Lancer le serveur Flask sur le port 5000
    app.run(host="0.0.0.0", port=5001)
