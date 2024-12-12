import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
import subprocess
import json
import sys
from datetime import datetime
from tkinter.scrolledtext import ScrolledText
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class ModernProjectManagerApp:
    def __init__(self, root):
        self.root = root
        self.setup_theme()
        self.root.title("✨ Gestionnaire de Projets Moderne")
        self.root.geometry("1200x800")
        
        # Variables
        self.project_name_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_projects)
        self.tailwind_var = tk.BooleanVar()
        self.bootstrap_var = tk.BooleanVar()
        self.target_folder = ""
        self.selected_fields = []
        
        self.load_config()
        self.create_menu()
        self.create_main_interface()
        self.load_history()

    def setup_theme(self):
        # Configuration du thème sombre moderne
        self.style = ttk.Style(theme="darkly")
        
    def create_menu(self):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # Menu Fichier
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Nouveau projet", command=self.new_project)
        file_menu.add_command(label="Ouvrir dossier", command=self.select_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit)

    def create_main_interface(self):
        # Création du conteneur principal avec Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Onglet Projets
        self.projects_tab = ttk.Frame(self.notebook)
        self.favorites_tab = ttk.Frame(self.notebook)
        self.history_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.projects_tab, text="Projets")
        self.notebook.add(self.favorites_tab, text="Favoris")
        self.notebook.add(self.history_tab, text="Historique")
        
        self.setup_projects_tab()
        self.setup_favorites_tab()
        self.setup_history_tab()

    def setup_projects_tab(self):
        # Frame gauche pour la liste des projets
        left_frame = ttk.Frame(self.projects_tab)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Boutons pour ajouter les scripts spécifiques
        scripts_frame = ttk.LabelFrame(left_frame, text="Scripts disponibles")
        scripts_frame.pack(fill=tk.X, padx=5, pady=5)

        # Générateurs
        ttk.Button(scripts_frame, text="Ajouter Générateur CSS", 
                  command=lambda: self.add_specific_script("Css_Themes_Generator.py")).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(scripts_frame, text="Ajouter Générateur de Formulaires", 
                  command=lambda: self.add_specific_script("Form_Generator.py")).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(scripts_frame, text="Ajouter Générateur de Projets", 
                  command=lambda: self.add_specific_script("generateur_projet.py")).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(scripts_frame, text="Ajouter Générateur de Composants", 
                  command=lambda: self.add_specific_script("Component_Generator.py")).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(scripts_frame, text="Ajouter Générateur de Layouts", 
                  command=lambda: self.add_specific_script("Layout_Generator.py")).pack(fill=tk.X, padx=5, pady=2)

        # Liste des projets avec scrollbar
        self.project_list = ttk.Treeview(left_frame, selectmode='extended', columns=("Type", "Date"), show="headings")
        self.project_list.heading("Type", text="Type")
        self.project_list.heading("Date", text="Date de modification")
        self.project_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.project_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.project_list.configure(yscrollcommand=scrollbar.set)

        # Frame droite pour les options
        right_frame = ttk.Frame(self.projects_tab)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Options du projet
        options_frame = ttk.LabelFrame(right_frame, text="Options du projet")
        options_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(options_frame, text="Nom du projet:").pack(anchor=tk.W, padx=5, pady=2)
        ttk.Entry(options_frame, textvariable=self.project_name_var).pack(fill=tk.X, padx=5, pady=2)

        ttk.Checkbutton(options_frame, text="Inclure Tailwind", variable=self.tailwind_var).pack(anchor=tk.W, padx=5)
        ttk.Checkbutton(options_frame, text="Inclure Bootstrap", variable=self.bootstrap_var).pack(anchor=tk.W, padx=5)

        # Actions
        actions_frame = ttk.LabelFrame(right_frame, text="Actions")
        actions_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(actions_frame, text="Nouveau Projet", 
                  command=self.new_project).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(actions_frame, text="Ajouter aux favoris", 
                  command=self.add_to_favorites).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(actions_frame, text="Exécuter", 
                  command=self.execute_selected).pack(fill=tk.X, padx=5, pady=2)

        # Prévisualisation
        preview_frame = ttk.LabelFrame(right_frame, text="Prévisualisation")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.preview_text = ScrolledText(preview_frame)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def setup_favorites_tab(self):
        self.favorites_list = ttk.Treeview(self.favorites_tab)
        self.favorites_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def setup_history_tab(self):
        self.history_list = ttk.Treeview(self.history_tab)
        self.history_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def load_config(self):
        self.config_file = "project_manager_config.json"
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        except:
            self.config = {
                "recent_projects": [],
                "favorites": [],
                "last_directory": "",
                "projects": []
            }
            self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def load_history(self):
        if "recent_projects" in self.config:
            for project in self.config["recent_projects"]:
                self.history_list.insert("", "end", text=project)

    def new_project(self):
        if not self.project_name_var.get().strip():
            messagebox.showwarning("Attention", "Veuillez entrer un nom de projet")
            return
        
        if not self.target_folder:
            self.target_folder = filedialog.askdirectory(title="Choisir le dossier de destination")
            if not self.target_folder:
                return

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.target_folder = folder

    def add_to_favorites(self):
        selected = self.project_list.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un projet")
            return
        
        for item in selected:
            project = self.project_list.item(item)["text"]
            if project not in self.config["favorites"]:
                self.config["favorites"].append(project)
                self.favorites_list.insert("", "end", text=project)
        
        self.save_config()

    def execute_selected(self):
        selected = self.project_list.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un projet")
            return
        
        for item in selected:
            project = self.project_list.item(item)["text"]
            try:
                self.run_project(project)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'exécution : {str(e)}")

    def run_project(self, project_name):
        project_path = os.path.join(os.path.dirname(__file__), project_name)
        
        if not os.path.exists(project_path):
            raise FileNotFoundError(f"Le fichier {project_path} n'existe pas.")

        command = ["python", project_path]
        
        if "Form_Generator.py" in project_name:
            self.setup_form_generator_dialog()
        elif "generateur_projet.py" in project_name:
            if not self.project_name_var.get().strip():
                messagebox.showwarning("Attention", "Veuillez entrer un nom de projet")
                return
            command.extend([
                "--path", self.target_folder,
                "--project-name", self.project_name_var.get().strip()
            ])
            if self.tailwind_var.get():
                command.append("--tailwind")
            if self.bootstrap_var.get():
                command.append("--bootstrap")

        if self.target_folder:
            command.extend(["--path", self.target_folder])
        
        try:
            result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                self.preview_text.delete('1.0', tk.END)
                self.preview_text.insert('1.0', result.stdout)
                messagebox.showinfo("Succès", "Projet généré avec succès !")
            else:
                messagebox.showerror("Erreur", f"Erreur lors de la génération : {result.stderr}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur : {str(e)}")

    def filter_projects(self, *args):
        search_term = self.search_var.get().lower()
        self.project_list.delete(*self.project_list.get_children())
        for project in self.config.get("projects", []):
            if search_term in project.lower():
                self.project_list.insert("", "end", text=project)

    def add_specific_script(self, script_name):
        script_path = os.path.join(os.path.dirname(__file__), script_name)
        if os.path.exists(script_path):
            if script_path not in self.config["projects"]:
                self.config["projects"].append(script_path)
                self.save_config()
            self.project_list.insert("", "end", text=script_name, values=("Script Python", datetime.now().strftime("%Y-%m-%d %H:%M")))
        else:
            messagebox.showerror("Erreur", f"Le script {script_name} n'existe pas dans le répertoire")

    def setup_form_generator_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Générateur de Formulaires")
        dialog.geometry("800x600")  # Agrandi pour la prévisualisation
        
        # Frame principale avec deux colonnes
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame gauche pour les options
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        ttk.Label(left_frame, text="Sélectionnez les champs :").pack(anchor=tk.W)
        
        # Dictionnaire des champs avec leurs descriptions
        self.fields_vars = {}  # Pour stocker les variables des checkboxes
        fields = [
            ("Texte", "text", "Champ texte simple (nom, titre, etc.)"),
            ("Email", "email", "Validation automatique du format email"),
            ("Mot de passe", "password", "Masque automatiquement les caractères"),
            ("Nombre", "number", "Accepte uniquement les chiffres"),
            ("Date", "date", "Sélecteur de date intégré"),
            ("Téléphone", "tel", "Format optimisé pour les numéros"),
            ("Zone de texte", "textarea", "Pour les textes longs"),
            ("Case à cocher", "checkbox", "Pour les choix oui/non"),
            ("Liste déroulante", "select", "Pour les choix multiples")
        ]
        
        # Frame pour les checkboxes avec scrollbar
        checkbox_frame = ttk.Frame(left_frame)
        checkbox_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(checkbox_frame)
        scrollbar = ttk.Scrollbar(checkbox_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Ajout des champs avec leurs descriptions
        for label, field_type, description in fields:
            frame = ttk.Frame(scrollable_frame)
            frame.pack(fill=tk.X, pady=2)
            
            var = tk.BooleanVar()
            self.fields_vars[field_type] = var
            cb = ttk.Checkbutton(frame, text=label, variable=var,
                               command=self.update_form_preview)
            cb.pack(side=tk.LEFT)
            
            ttk.Label(frame, text=description, foreground="gray").pack(side=tk.LEFT, padx=5)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame droite pour la prévisualisation
        right_frame = ttk.LabelFrame(main_frame, text="Prévisualisation en direct")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.preview_text = ScrolledText(right_frame, wrap=tk.WORD)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Boutons d'action
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(button_frame, text="Générer", 
                  command=lambda: self.generate_form(dialog)).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Annuler", 
                  command=dialog.destroy).pack(side=tk.RIGHT, padx=5)

    def update_form_preview(self):
        # Récupère les champs sélectionnés
        selected = [field_type for field_type, var in self.fields_vars.items() if var.get()]
        
        if not selected:
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert('1.0', "Sélectionnez des champs pour voir la prévisualisation")
            return
        
        # Génère le HTML de prévisualisation
        html = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulaire</title>
    <style>
        form { max-width: 500px; margin: 2rem auto; padding: 1rem; }
        .form-group { margin-bottom: 1rem; }
        label { display: block; margin-bottom: .5rem; }
        input, select, textarea {
            width: 100%;
            padding: .5rem;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="checkbox"] { width: auto; }
    </style>
</head>
<body>
    <form>
"""
        
        # Ajoute chaque champ sélectionné
        for field_type in selected:
            html += '        <div class="form-group">\n'
            label = next(label for label, type_, _ in [
                ("Texte", "text", "Champ texte simple (nom, titre, etc.)"),
                ("Email", "email", "Validation automatique du format email"),
                ("Mot de passe", "password", "Masque automatiquement les caractères"),
                ("Nombre", "number", "Accepte uniquement les chiffres"),
                ("Date", "date", "Sélecteur de date intégré"),
                ("Téléphone", "tel", "Format optimisé pour les numéros"),
                ("Zone de texte", "textarea", "Pour les textes longs"),
                ("Case à cocher", "checkbox", "Pour les choix oui/non"),
                ("Liste déroulante", "select", "Pour les choix multiples")
            ] if type_ == field_type)
            
            if field_type == "checkbox":
                html += f'            <label><input type="checkbox"> {label}</label>\n'
            elif field_type == "textarea":
                html += f'            <label>{label}</label>\n'
                html += f'            <textarea rows="4"></textarea>\n'
            elif field_type == "select":
                html += f'            <label>{label}</label>\n'
                html += '            <select>\n'
                html += '                <option>Option 1</option>\n'
                html += '                <option>Option 2</option>\n'
                html += '                <option>Option 3</option>\n'
                html += '            </select>\n'
            else:
                html += f'            <label>{label}</label>\n'
                html += f'            <input type="{field_type}">\n'
            
            html += '        </div>\n'
        
        html += """    </form>
</body>
</html>
"""
        
        # Affiche la prévisualisation
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', html)

    def generate_form(self, dialog):
        # Récupère les champs sélectionnés
        selected = [field_type for field_type, var in self.fields_vars.items() if var.get()]
        
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner au moins un champ")
            return
        
        # Ferme la fenêtre de dialogue
        dialog.destroy()
        
        # Sélectionne le dossier de destination si pas encore fait
        if not self.target_folder:
            self.target_folder = filedialog.askdirectory(title="Choisir le dossier de destination")
            if not self.target_folder:
                return
        
        # Prépare la commande
        fields_str = ",".join(selected)
        command = [
            "python",
            "Form_Generator.py",
            "--fields", fields_str,
            "--path", self.target_folder
        ]
        
        try:
            result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                self.preview_text.delete('1.0', tk.END)
                self.preview_text.insert('1.0', result.stdout)
                messagebox.showinfo("Succès", "Formulaire généré avec succès !")
            else:
                messagebox.showerror("Erreur", f"Erreur lors de la génération : {result.stderr}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur : {str(e)}")

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = ModernProjectManagerApp(root)
    root.mainloop()
