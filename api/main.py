import mlflow
import mlflow.pyfunc
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuration du serveur de tracking MLflow
mlflow.set_tracking_uri("http://34.170.123.233:5000")  # Remplace avec l'IP de ton serveur MLflow

# Charger le modèle MLflow depuis le Model Registry
MODEL_URI = "models:/iris_model/1"
model = mlflow.pyfunc.load_model(MODEL_URI)

@app.route("/predict", methods=["POST"])
def predict():
    try:
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
        return jsonify({"prediction": prediction})
    
    except Exception as e:
        # Afficher l'erreur dans les logs pour aider à déboguer
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    # Lancer le serveur Flask sur le port 5001
    app.run(host="0.0.0.0", port=5001)
