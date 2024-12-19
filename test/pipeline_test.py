import unittest
from unittest.mock import patch
import mlflow
from MLflow.pipeline import train_and_log_model
  

class TestModelTraining(unittest.TestCase):

    @patch("mlflow.sklearn.log_model")
    @patch("mlflow.log_metric")
    @patch("mlflow.log_param")
    def test_train_and_log_model(self, mock_log_param, mock_log_metric, mock_log_model):
        # Simuler l'exécution de la fonction
        train_and_log_model()

        # Vérifier que les paramètres sont bien loggés
        mock_log_param.assert_called_with("n_estimators", 100)
        mock_log_metric.assert_called()
        mock_log_model.assert_called()

if __name__ == "__main__":
    unittest.main()
