import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import logging

# Configurer les logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_and_log_model():
    # Configuration MLflow
    mlflow.set_tracking_uri("http://35.188.13.90:5000")
    mlflow.set_experiment("iris_experiment")
    client = mlflow.tracking.MlflowClient()

    # Charger le dataset
    data = load_iris()
    X = data.data
    y = data.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entraîner le modèle
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)

    # Logger le modèle avec un tag
    with mlflow.start_run() as run:
        mlflow.log_param("n_estimators", 100)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(model, "model", registered_model_name="iris_model")

        # Vérifier les performances et promouvoir si nécessaire
        try:
            latest_version = client.get_latest_versions(name="iris_model", stages=["None"])[0].version
            production_model = client.get_latest_versions(name="iris_model", stages=["Production"])

            if production_model:
                production_version = production_model[0].version
                production_accuracy = client.get_run(production_model[0].run_id).data.metrics["accuracy"]

                if accuracy > production_accuracy:
                    logger.info("Nouveau modèle plus performant, promotion en Production.")
                    client.transition_model_version_stage(
                        name="iris_model",
                        version=latest_version,
                        stage="Production"
                    )
                else:
                    logger.info("Le modèle actuel est meilleur. Aucun changement.")
            else:
                logger.info("Aucun modèle en Production, promotion automatique.")
                client.transition_model_version_stage(
                    name="iris_model",
                    version=latest_version,
                    stage="Production"
                )
        except Exception as e:
            logger.error(f"Erreur lors de la promotion du modèle : {str(e)}")

if __name__ == "__main__":
    train_and_log_model()
