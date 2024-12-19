import unittest
from unittest.mock import patch
from api.main import app  # Assurez-vous que le chemin vers app est correct

class TestAPI(unittest.TestCase):

    @patch("api.main.model.predict")  # Modifier le chemin
    def test_predict(self, mock_predict):
        # Mock la prédiction du modèle
        mock_predict.return_value = [0]  # Simuler une prédiction

        with app.test_client() as client:
            response = client.post("/predict", json={"features": [5.1, 3.5, 1.4, 0.2]})
            data = response.get_json()

            # Assurer que le statut de la réponse est 200
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["prediction"], [0])

if __name__ == "__main__":
    unittest.main()
