import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess

# Liste des scripts disponibles avec leurs descriptions
SCRIPTS = {
    "Broken_Links_Checker.py": "Vérifie les liens brisés dans un fichier HTML.",
    "Css_Cleaner.py": "Nettoie un fichier CSS en supprimant les classes inutilisées.",
    "Css_Themes_Generator.py": "Génère plusieurs fichiers CSS pour des thèmes personnalisés.",
    "Form_Generator.py": "Génère un formulaire HTML avec des champs personnalisés.",
    "generateur_projet.py": "Génère une structure complète pour un nouveau projet.",
    "Html_Template_Generator.py": "Génère des fichiers HTML basés sur des templates prédéfinis.",
    "library_manager.py": "Télécharge automatiquement des bibliothèques externes.",
    "local_Server.py": "Démarre un serveur local HTTP pour prévisualiser votre projet.",
    "project_Cleaner.py": "Nettoie un projet en supprimant les fichiers inutiles.",
    "setup_tailwind.py": "Installe et configure Tailwind CSS ou Bootstrap.",
    "Static_Site_Search.py": "Génère un fichier search.js pour un moteur de recherche simple."
}

# Fonction pour exécuter un ou plusieurs scripts
def execute_scripts(scripts, project_path):
    try:
        if not os.path.exists(project_path):
            messagebox.showerror("Erreur", f"Le dossier {project_path} n'existe pas.")
            return

        for script in scripts:
            script_path = os.path.join(os.getcwd(), script)
            if not os.path.exists(script_path):
                messagebox.showerror("Erreur", f"Le script {script} n'existe pas.")
                continue

            subprocess.run(["python", script_path], cwd=project_path, check=True)

        messagebox.showinfo("Succès", "Les scripts sélectionnés ont été exécutés avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'exécution des scripts : {e}")

# Interface utilisateur
class ScriptManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Scripts")
        self.root.geometry("500x400")

        # Chemin du projet
        self.project_path = tk.StringVar()

        tk.Label(root, text="Chemin du projet :").pack(pady=5)
        path_frame = tk.Frame(root)
        path_frame.pack(pady=5)

        tk.Entry(path_frame, textvariable=self.project_path, width=40).pack(side=tk.LEFT, padx=5)
        tk.Button(path_frame, text="Parcourir", command=self.browse_folder).pack(side=tk.LEFT)

        # Liste des scripts
        tk.Label(root, text="Sélectionnez les scripts à exécuter :").pack(pady=5)
        self.script_list = tk.Listbox(root, selectmode=tk.MULTIPLE, height=10, width=50)
        self.script_list.pack(pady=5)

        for script, description in SCRIPTS.items():
            self.script_list.insert(tk.END, f"{script} - {description}")

        # Bouton d'exécution
        tk.Button(root, text="Exécuter les scripts", command=self.run_selected_scripts).pack(pady=20)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.project_path.set(folder_selected)

    def run_selected_scripts(self):
        selected_indices = self.script_list.curselection()
        selected_scripts = [list(SCRIPTS.keys())[i] for i in selected_indices]
        project_path = self.project_path.get()

        if not selected_scripts:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner au moins un script.")
            return

        if not project_path:
            messagebox.showwarning("Avertissement", "Veuillez entrer ou sélectionner le chemin du projet.")
            return

        execute_scripts(selected_scripts, project_path)

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = ScriptManagerApp(root)
    root.mainloop()