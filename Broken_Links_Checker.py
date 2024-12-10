

# Copiez ce bloc et ajoutez-le dans la section "tasks" de votre fichier tasks.json.
# Placez le script broken_links_checker.py dans votre espace de travail.
# Exécutez cette tâche dans Visual Studio Code via Ctrl+Shift+P > Tasks: Run Task > Vérifier les liens brisés.
import requests
from bs4 import BeautifulSoup
import os

def check_links(html_file):
    """Vérifie les liens dans un fichier HTML pour s'assurer qu'ils fonctionnent."""
    if not os.path.exists(html_file):
        print(f"Erreur : Le fichier {html_file} n'existe pas.")
        return

    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    for link in soup.find_all("a", href=True):
        url = link["href"]
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"Lien valide : {url}")
            else:
                print(f"Lien brisé : {url} - Code HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erreur avec le lien {url} : {e}")

if __name__ == "__main__":
    print("=== Vérificateur de Liens Brisés ===")
    html_file = input("Entrez le nom du fichier HTML à vérifier : ").strip()
    check_links(html_file)


# Copiez ce bloc et ajoutez-le dans la section "tasks" de votre fichier tasks.json.
# Placez le script broken_links_checker.py dans votre espace de travail.
# Exécutez cette tâche dans Visual Studio Code via Ctrl+Shift+P > Tasks: Run Task > Vérifier les liens brisés.
import requests
from bs4 import BeautifulSoup
import os
import argparse

def check_links(html_file):
    """Vérifie les liens dans un fichier HTML pour s'assurer qu'ils fonctionnent."""
    if not os.path.exists(html_file):
        print(f"Erreur : Le fichier {html_file} n'existe pas.")
        return

    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    for link in soup.find_all("a", href=True):
        url = link["href"]
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"Lien valide : {url}")
            else:
                print(f"Lien brisé : {url} - Code HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erreur avec le lien {url} : {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vérificateur de liens brisés.")
    parser.add_argument("--html-file", required=True, help="Chemin du fichier HTML à vérifier.")

    args = parser.parse_args()

    check_links(args.html_file)

