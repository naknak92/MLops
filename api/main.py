import mlflow
import mlflow.pyfunc
from flask import Flask, request, jsonify
from prometheus_client import Counter, generate_latest, REGISTRY

app = Flask(__name__)

# Configuration du serveur de tracking MLflow
mlflow.set_tracking_uri("http://34.170.123.233:5000")  # Remplace avec l'IP de ton serveur MLflow

# Charger le modèle MLflow depuis le Model Registry
MODEL_URI = "models:/iris_model/1"
model = mlflow.pyfunc.load_model(MODEL_URI)

# Créer un compteur pour suivre les requêtes
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests')

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Incrémenter le compteur à chaque requête
        REQUEST_COUNT.inc()

        # Récupérer les données d'entrée
        data = request.get_json()

        # Vérifier si la clé "features" existe
        if "features" not in data:
            return jsonify({"error": "'features' key is missing"}), 400

        features = data["features"]
        
        # Log ou afficher les features reçues pour déboguer
        print(f"Features received: {features}")

        # Faire la prédiction
        prediction = model.predict([features])
        
        # Retourner la prédiction
        return jsonify({"prediction": prediction.tolist()})

    except Exception as e:
        # Afficher l'erreur dans les logs pour aider à déboguer
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route("/metrics", methods=["GET"])
def metrics():
    """Expose les métriques pour Prometheus"""
    return generate_latest(REGISTRY)

if __name__ == "__main__":
    # Lancer le serveur Flask sur le port 5001
    app.run(host="0.0.0.0", port=5001)
