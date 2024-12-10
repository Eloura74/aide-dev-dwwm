import os

def normalize_path(path):
    """Convertir un chemin en format standard pour le système d'exploitation"""
    return os.path.abspath(path.replace("\\", "/"))

def create_file(path, content=""):
    """Créer un fichier avec un contenu donné"""
    with open(path, "w") as file:
        file.write(content)

def create_project_structure(base_path, project_name, use_tailwind=False, use_bootstrap=False):
    """Crée une structure de projet adaptée aux besoins."""

    # Normaliser le chemin
    base_path = normalize_path(base_path)

    # Définir la structure de base
    structure = {
        "css": ["style.css"],
        "js": ["app.js"],
        "img": [],
        "templates": ["index.html"],
    }

    # Ajouter des fichiers pour Tailwind ou Bootstrap si nécessaire
    if use_tailwind:
        structure["css"].append("tailwind.css")
        structure["config"] = ["tailwind.config.js"]
    if use_bootstrap:
        structure["css"].append("bootstrap.css")

    # Créer les dossiers et fichiers
    project_path = os.path.join(base_path, project_name)
    os.makedirs(project_path, exist_ok=True)
    for folder, files in structure.items():
        folder_path = os.path.join(project_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(folder_path, file)
            create_file(file_path)

    # Ajouter du contenu par défaut aux fichiers
    create_file(
        os.path.join(project_path, "templates", "index.html"),
        """<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <link rel=\"stylesheet\" href=\"../css/style.css\">
    <title>Mon Projet</title>
</head>
<body>
    <h1>Bienvenue dans Mon Projet</h1>
    <script src=\"../js/app.js\"></script>
</body>
</html>
""",
    )

    if use_tailwind:
        create_file(
            os.path.join(project_path, "config", "tailwind.config.js"),
            "module.exports = { content: ['./templates/**/*.html'], theme: { extend: {} }, plugins: [] };"
        )

    print(f"Structure du projet '{project_name}' créée avec succès dans '{base_path}' !")

# Interface utilisateur simplifiée pour personnaliser la création
if __name__ == "__main__":
    print("=== Générateur de Structure de Projet ===")
    project_name = input("Entrez le nom du projet : ").strip()
    base_path = input("Entrez le chemin où créer le projet (laisser vide pour le dossier actuel) : ").strip()
    if not base_path:
        base_path = os.getcwd()
    base_path = normalize_path(base_path)
    use_tailwind = input("Voulez-vous ajouter Tailwind CSS ? (o/n) : ").lower() == 'o'
    use_bootstrap = input("Voulez-vous ajouter Bootstrap ? (o/n) : ").lower() == 'o'

    create_project_structure(base_path, project_name, use_tailwind, use_bootstrap)
