import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import subprocess

class ProjectManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Projets")

        # Liste des projets existants (chemins complets)
        self.projects = [
            os.path.abspath("generateur_projet.py"),
            os.path.abspath("Form_Generator.py"),
            os.path.abspath("Html_Template_Generator.py"),
            os.path.abspath("library_manager.py"),
            os.path.abspath("project_Cleaner.py"),
            os.path.abspath("setup_tailwind.py"),
            os.path.abspath("Static_Site_Search.py"),
            os.path.abspath("Broken_Links_Checker.py"),
            os.path.abspath("Css_Cleaner.py"),
            os.path.abspath("Css_Themes_Generator.py"),
            os.path.abspath("form_generator.py")  # Ajout du script pour les formulaires
        ]

        self.selected_projects = []  # Projets sélectionnés
        self.target_folder = None  # Dossier cible pour le projet
        self.options = {"tailwind": False, "bootstrap": False, "project_name": ""}  # Options de configuration

        # Interface graphique
        self.create_widgets()

    def create_widgets(self):
        # Liste des projets
        self.project_frame = tk.Frame(self.root)
        self.project_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.project_list_label = tk.Label(self.project_frame, text="Projets disponibles :")
        self.project_list_label.pack(anchor="w")

        self.project_listbox = tk.Listbox(
            self.project_frame, selectmode=tk.MULTIPLE, height=15, activestyle="dotbox"
        )
        for project in self.projects:
            self.project_listbox.insert(tk.END, os.path.basename(project))
        self.project_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

        # Ajouter un bouton pour parcourir et ajouter un projet
        self.browse_button = tk.Button(self.project_frame, text="Ajouter un Projet", command=self.add_project)
        self.browse_button.pack(pady=5)

        # Ajouter un bouton pour créer un nouveau dossier
        self.create_folder_button = tk.Button(self.project_frame, text="Créer/Sélectionner un Dossier de Projet", command=self.select_target_folder)
        self.create_folder_button.pack(pady=5)

        # Options spécifiques
        self.options_frame = tk.Frame(self.root)
        self.options_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.options_label = tk.Label(self.options_frame, text="Options supplémentaires :")
        self.options_label.pack(anchor="w")

        self.tailwind_var = tk.BooleanVar()
        self.bootstrap_var = tk.BooleanVar()

        self.tailwind_check = tk.Checkbutton(self.options_frame, text="Inclure Tailwind CSS", variable=self.tailwind_var)
        self.tailwind_check.pack(anchor="w")

        self.bootstrap_check = tk.Checkbutton(self.options_frame, text="Inclure Bootstrap", variable=self.bootstrap_var)
        self.bootstrap_check.pack(anchor="w")

        self.project_name_label = tk.Label(self.options_frame, text="Nom du projet :")
        self.project_name_label.pack(anchor="w")
        self.project_name_entry = tk.Entry(self.options_frame)
        self.project_name_entry.pack(fill=tk.X, pady=5)

        # Boutons d'action
        self.action_frame = tk.Frame(self.root)
        self.action_frame.pack(fill=tk.X, padx=10, pady=10)

        self.run_button = tk.Button(self.action_frame, text="Exécuter", command=self.execute_projects)
        self.run_button.pack(side=tk.RIGHT, padx=5)

        self.quit_button = tk.Button(self.action_frame, text="Quitter", command=self.root.quit)
        self.quit_button.pack(side=tk.RIGHT, padx=5)

    def add_project(self):
        file_path = filedialog.askopenfilename(
            title="Sélectionner un script Python",
            filetypes=[("Fichiers Python", "*.py")]
        )
        if file_path:
            if not os.path.exists(file_path):
                messagebox.showerror("Erreur", f"Le fichier {file_path} n'existe pas.")
                return

            if file_path not in self.projects:
                self.projects.append(file_path)
                self.project_listbox.insert(tk.END, os.path.basename(file_path))
                messagebox.showinfo("Projet ajouté", f"{os.path.basename(file_path)} a été ajouté à la liste des projets.")
            else:
                messagebox.showwarning("Déjà existant", f"{os.path.basename(file_path)} est déjà dans la liste.")

    def select_target_folder(self):
        folder_path = filedialog.askdirectory(title="Créer/Sélectionner un dossier de projet")
        if folder_path:
            if not os.path.exists(folder_path):
                try:
                    os.makedirs(folder_path)
                    messagebox.showinfo("Dossier créé", f"Le dossier {folder_path} a été créé avec succès.")
                except Exception as e:
                    messagebox.showerror("Erreur", f"Impossible de créer le dossier : {e}")
            self.target_folder = folder_path
            messagebox.showinfo("Dossier sélectionné", f"Le dossier de destination est : {self.target_folder}")

    def execute_projects(self):
        selected_indices = self.project_listbox.curselection()
        self.selected_projects = [self.projects[i] for i in selected_indices]

        if not self.selected_projects:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner au moins un projet.")
            return

        if not self.target_folder:
            messagebox.showwarning("Dossier non défini", "Veuillez sélectionner un dossier de destination.")
            return

        for project in self.selected_projects:
            if not os.path.exists(project):
                messagebox.showerror("Erreur", f"Le fichier {project} n'existe pas.")
                return

            try:
                if "Form_Generator.py" in project or "form_generator.py" in project:
                    fields = simpledialog.askstring(
                        title="Champs du formulaire",
                        prompt="Entrez les champs du formulaire, séparés par des virgules :"
                    )
                    if not fields:
                        messagebox.showwarning("Champs manquants", "Veuillez entrer des champs pour le formulaire.")
                        return
                    fields_list = [field.strip() for field in fields.split(",")]
                    command = ["python", project, "--fields", ",".join(fields_list), "--path", self.target_folder]
                elif "generateur_projet.py" in project:
                    command = ["python", project, "--path", self.target_folder, "--project-name", self.project_name_entry.get().strip()]
                    if self.tailwind_var.get():
                        command.append("--tailwind")
                    if self.bootstrap_var.get():
                        command.append("--bootstrap")
                elif "Html_Template_Generator.py" in project or "html_template_generator.py" in project:
                    command = ["python", project, "--path", self.target_folder]
                else:
                    messagebox.showerror("Script non pris en charge", f"Le script {project} n'est pas configuré pour ce GUI.")
                    return

                subprocess.run(command, check=True)
                print(f"Exécution réussie de {project} avec les options : {command}")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'exécution de {project} : {e}")
                return

        messagebox.showinfo("Exécution terminée", "Les scripts sélectionnés ont été exécutés avec succès.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectManagerApp(root)
    root.mainloop()
