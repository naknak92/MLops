
# MLOps Project

## Description

Ce projet vise à mettre en place une chaîne complète **MLOps** intégrant des pratiques **DevOps** et des outils spécifiques au **Machine Learning**. Le projet utilise une approche **Infrastructure as Code (IaC)** et de **CI/CD** avec un suivi de modèle via **MLflow**, une API Flask pour l'inférence, **Prometheus** et **Grafana** pour le monitoring, et **Terraform** pour l'automatisation de l'infrastructure sur Google Cloud.

## Technologies utilisées

- **Conteneurisation** : Docker
- **Infrastructure as Code (IaC)** : Terraform
- **Configuration** : Ansible
- **Cloud** : Google Cloud Platform (GCP)
- **ML Tracking** : MLflow
- **CI/CD** : GitHub Actions
- **Monitoring** : Prometheus + Grafana
- **API** : Flask
- **Test** : Pytest + unittest

## Prérequis

### Local

1. **Python 3.10+**
2. **Docker** et **Docker Compose**
3. **Google Cloud SDK** pour gérer les ressources GCP
4. **Git** pour la gestion de version

### Installations requises

1. Clonez le projet :

```bash
git clone https://github.com/naknak92/projet-devops.git
cd projet-devops
```

2. Installez les dépendances nécessaires :

```bash
pip install -r api/requirements.txt
```

3. Pour les tests :

```bash
pip install -r requirements-dev.txt
```

## Architecture du projet

Le projet est organisé comme suit :

```
.
├── MLflow
│   ├── pipeline.py      # Entraînement du modèle et log avec MLflow
│   └── train.py         # Entraînement initial du modèle
├── README.md
├── ansible
│   └── setup.yml        # Playbook Ansible pour configurer les instances
├── api
│   ├── main.py          # API Flask pour l'inférence
│   └── requirements.txt # Dépendances de l'API
├── dockerfile           # Dockerfile pour construire l'image Docker de l'API
├── terraform
│   ├── main.tf          # Configuration de l'infrastructure GCP avec Terraform
│   ├── ml_instance_key.pem  # Clé privée SSH pour GCP
│   ├── terraform.tfstate    # État de l'infrastructure Terraform
│   └── terraform.tfstate.backup
└── test
    ├── main_test.py     # Tests unitaires pour l'API
    └── pipeline_test.py # Tests unitaires pour la pipeline
```

## Étapes du projet

### 1. **Infrastructure (Terraform + Ansible)**

1. **Configurer l'infrastructure sur GCP** :
   - Utilisation de **Terraform** pour déployer les instances sur GCP (avec les configurations appropriées pour les serveurs, le réseau, etc.).
   - Utilisation de **Ansible** pour la configuration des serveurs.

2. **Instance GCP** :
   - Une instance GCP est déployée et configurée pour héberger l'API Flask et les services de monitoring.

### 2. **Modèle ML (MLflow)**

1. **Entraînement du modèle** :
   - Utilisation de **MLflow** pour l'entraînement et le suivi des modèles.
   - Le modèle est un **Random Forest** entraîné sur le dataset Iris.
   
2. **Versioning des modèles** :
   - Les modèles sont enregistrés et versionnés via **MLflow Model Registry**.

### 3. **API Flask**

1. **API Flask pour l'inférence** :
   - Une API Flask est utilisée pour effectuer des prédictions via les modèles enregistrés dans **MLflow**.
   - L'API expose un endpoint `/predict` pour recevoir des requêtes avec les caractéristiques à prédire et retourne les résultats.

2. **Métriques pour Prometheus** :
   - Des métriques sont exposées pour surveiller les requêtes HTTP via **Prometheus**. L'endpoint `/metrics` est utilisé pour exposer les données nécessaires à la surveillance.

### 4. **CI/CD (GitHub Actions)**

1. **Pipeline CI/CD** :
   - **GitHub Actions** est utilisé pour automatiser l'entraînement, le déploiement et la mise à jour des modèles via un pipeline.
   - Les tests unitaires sont également intégrés au pipeline pour assurer la validité du code et des modèles.

### 5. **Monitoring (Prometheus + Grafana)**

1. **Prometheus** :
   - **Prometheus** est utilisé pour scraper les métriques de l'API Flask.
   - La configuration de **Prometheus** est définie dans le fichier `prometheus.yml`.

2. **Grafana** :
   - **Grafana** est utilisé pour visualiser les métriques collectées par **Prometheus** via des dashboards.

## Instructions d'exécution

1. **Démarrer les services Docker** :
   - Lancez Prometheus, Grafana et l'API Flask en utilisant Docker :
   
   ```bash
   docker-compose up -d
   ```

2. **Accéder aux services** :
   - **Grafana** : `http://<INSTANCE_IP>:3000`
     - Identifiants par défaut : `admin` / `admin`
   - **Prometheus** : `http://<INSTANCE_IP>:9090`
   - **API Flask** : `http://<INSTANCE_IP>:5001/predict`

3. **Démarrer le serveur** :
   - Vous pouvez également démarrer le serveur Flask manuellement :
   
   ```bash
   python3 api/main.py
   ```

## Tests

### Lancer les tests unitaires :

```bash
python3 -m unittest test/main_test.py
python3 -m unittest test/pipeline_test.py
```

### Tests avec `pytest` :

```bash
pytest test/pipeline_test.py
```

## Conclusion

Ce projet permet d'automatiser la chaîne MLOps en utilisant des technologies comme **Terraform**, **MLflow**, **Docker**, **Prometheus**, **Grafana** et **GitHub Actions**. Il couvre l'ensemble des étapes du cycle de vie des modèles, de l'entraînement à la mise en production, tout en intégrant un système de monitoring complet.
