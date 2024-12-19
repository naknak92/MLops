# Étape 1 : Choisir une image de base légère
FROM python:3.10-slim

# Étape 2 : Définir le répertoire de travail
WORKDIR /app

# Étape 3 : Copier les fichiers nécessaires
COPY ./MLflow/train.py ./train.py
COPY ./api/main.py ./main.py
COPY ./api/requirements.txt ./requirements.txt

# Étape 4 : Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : Ajouter un utilisateur non-root pour renforcer la sécurité
RUN useradd -m appuser

# Étape 6 : Créer le répertoire mlruns avec les bonnes permissions
RUN mkdir -p /app/mlruns && chown -R appuser:appuser /app/mlruns

# Étape 7 : Exposer le port pour Flask
EXPOSE 5000

# Étape 8 : Exécuter en tant qu'utilisateur non-root
USER appuser

# Étape 9 : Démarrer l'API Flask
CMD ["python", "main.py"]
