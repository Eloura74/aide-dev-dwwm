import os
import subprocess
import shutil

if shutil.which("npm") is None:
    print("Erreur : npm n'est pas installé ou n'est pas dans le PATH.")
else:
    print("npm est installé.")

def setup_tailwind_or_bootstrap(base_path, project_name, use_tailwind=False, use_bootstrap=False):
    """Configure Tailwind CSS ou Bootstrap pour un projet."""

    # Définir les chemins absolus de npm et npx
    npm_path = r"C:\Program Files\nodejs\npm.cmd"
    npx_path = r"C:\Program Files\nodejs\npx.cmd"

    # Créer le dossier du projet si nécessaire
    project_path = os.path.join(base_path, project_name)
    os.makedirs(project_path, exist_ok=True)
    os.chdir(project_path)

    # Initialiser npm
    subprocess.run([npm_path, "init", "-y"], check=True)

    # Configurer Tailwind CSS
    if use_tailwind:
        subprocess.run([npm_path, "install", "-D", "tailwindcss", "postcss", "autoprefixer"], check=True)
        subprocess.run([npx_path, "tailwindcss", "init"], check=True)
        print(f"Tailwind CSS configuré dans le projet '{project_name}'.")

    # Configurer Bootstrap
    if use_bootstrap:
        subprocess.run([npm_path, "install", "bootstrap"], check=True)
        print(f"Bootstrap configuré dans le projet '{project_name}'.")

    print(f"Configuration terminée pour le projet '{project_name}' dans '{base_path}'.")

# Interface utilisateur simplifiée
if __name__ == "__main__":
    print("=== Configuration Tailwind CSS ou Bootstrap ===")
    project_name = input("Entrez le nom du projet : ").strip()
    base_path = input("Entrez le chemin où créer le projet (laisser vide pour le dossier actuel) : ").strip()
    if not base_path:
        base_path = os.getcwd()
    base_path = os.path.abspath(base_path)
    use_tailwind = input("Voulez-vous configurer Tailwind CSS ? (o/n) : ").lower() == 'o'
    use_bootstrap = input("Voulez-vous configurer Bootstrap ? (o/n) : ").lower() == 'o'

    setup_tailwind_or_bootstrap(base_path, project_name, use_tailwind, use_bootstrap)
