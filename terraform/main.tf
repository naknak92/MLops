provider "google" {
  project     = "devopsproject-65235"
  region      = "us-central1"
  credentials = file("/Users/rafael/Downloads/devopsproject-65235-63f22bae9ef1.json")
}

# Génération de clé SSH
resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "local_file" "ssh_key" {
  content  = tls_private_key.ssh_key.private_key_pem
  filename = "${path.module}/ml_instance_key.pem"
}

# Règle de pare-feu pour autoriser le port 5000
resource "google_compute_firewall" "allow_mlflow" {
  name    = "allow-mlflow"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["5000"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["ml-instance"]
  description   = "Allow access to MLflow on port 5000"
}

# Création d'une VM avec GCP
resource "google_compute_instance" "ml_instance" {
  name         = "ml-instance-new"
  machine_type = "e2-small"
  zone         = "us-central1-a"

  allow_stopping_for_update = true  # Autoriser l'arrêt temporaire

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }

  tags = ["ml-instance"]

  metadata = {
    ssh-keys = "debian:${tls_private_key.ssh_key.public_key_openssh}"
  }

  metadata_startup_script = <<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get install -y docker.io python3-pip
    systemctl start docker
    systemctl enable docker
    pip3 install mlflow
    nohup mlflow server --backend-store-uri sqlite:///mlflow.db --host 0.0.0.0 --port 5000 &
  EOF
}

output "instance_ip" {
  value = google_compute_instance.ml_instance.network_interface[0].access_config[0].nat_ip
}

output "ssh_key_location" {
  value = local_file.ssh_key.filename
}
