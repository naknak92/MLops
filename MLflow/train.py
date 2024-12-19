import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Connexion au serveur MLflow
mlflow.set_tracking_uri("http://35.188.13.90:5000")  # Remplace par ton IP
mlflow.set_experiment("iris_experiment")

# Charger les données
data = load_iris()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraîner le modèle
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Log du modèle et enregistrement dans le Model Registry
with mlflow.start_run():
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", model.score(X_test, y_test))
    mlflow.sklearn.log_model(model, artifact_path="model", registered_model_name="iris_experiment")
