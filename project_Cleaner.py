# Exécute le script project_cleaner.py pour supprimer les fichiers
# inutiles et nettoyer les dossiers comme build ou dist.
# Ajoutez le fichier project_cleaner.py dans votre espace de travail.
# Exécutez la tâche via Visual Studio Code (Ctrl+Shift+P, puis Tasks: Run Task).
# Personnalisation :

# Vous pouvez ajouter d'autres extensions ou dossiers à nettoyer dans le script Python 
# en modifiant les listes extensions_to_delete et folders_to_clean.

# Résultat attendu :
# Suppression des fichiers temporaires (.tmp, .log).
# Vidage ou suppression des dossiers comme build et dist.
# Confirmation des fichiers et dossiers supprimés via des messages dans le terminal.

import os


def clean_project(directory):
    """Nettoie un projet en supprimant les fichiers inutiles et vidant certains dossiers."""
    extensions_to_delete = [".tmp", ".log"]
    folders_to_clean = ["build", "dist"]

    # Supprimer les fichiers inutiles
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions_to_delete):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Supprimé : {file_path}")

    # Vider les dossiers spécifiques
    for folder in folders_to_clean:
        folder_path = os.path.join(directory, folder)
        if os.path.exists(folder_path):
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print(f"Fichier supprimé : {file_path}")
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    os.rmdir(dir_path)
                    print(f"Dossier supprimé : {dir_path}")
            print(f"Nettoyage du dossier : {folder_path}")

if __name__ == "__main__":
    print("=== Nettoyeur de Projet ===")
    project_dir = input("Entrez le chemin du projet à nettoyer : ").strip()
    if not os.path.exists(project_dir):
        print(f"Le chemin '{project_dir}' n'existe pas.")
    else:
        clean_project(project_dir)
        print("Nettoyage terminé.")