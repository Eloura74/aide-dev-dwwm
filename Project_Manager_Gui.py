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
        self.target_folder = None
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

        # Utiliser Text au lieu de ScrolledText pour éviter l'erreur
        self.preview_text = tk.Text(preview_frame, wrap=tk.WORD)
        preview_scrollbar = ttk.Scrollbar(preview_frame, orient="vertical", command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=preview_scrollbar.set)
        
        self.preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

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

        # S'assurer que le nom du projet est défini
        if not self.project_name_var.get().strip():
            messagebox.showwarning("Attention", "Veuillez entrer un nom de projet")
            return
            
        # S'assurer que le dossier cible est sélectionné
        if not self.target_folder:
            self.target_folder = filedialog.askdirectory(title="Choisir le dossier de destination")
            if not self.target_folder:
                return

        try:
            if "Form_Generator.py" in project_name:
                self.setup_form_generator_dialog()
            elif "Css_Themes_Generator.py" in project_name:
                self.setup_css_generator_dialog()
            elif "Component_Generator.py" in project_name:
                self.setup_component_generator_dialog()
            elif "Layout_Generator.py" in project_name:
                self.setup_layout_generator_dialog()
            elif "generateur_projet.py" in project_name:
                # Créer le dossier du projet s'il n'existe pas
                project_folder = os.path.join(self.target_folder, self.project_name_var.get().strip())
                os.makedirs(project_folder, exist_ok=True)
                
                # Exécuter le générateur de projet
                command = [
                    sys.executable,  # Utiliser le chemin Python actuel
                    project_path,
                    "--path", self.target_folder,
                    "--project-name", self.project_name_var.get().strip()
                ]
                
                if self.tailwind_var.get():
                    command.append("--tailwind")
                if self.bootstrap_var.get():
                    command.append("--bootstrap")
                
                # Exécuter la commande et capturer la sortie
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=os.path.dirname(project_path)
                )
                
                stdout, stderr = process.communicate()
                
                if process.returncode == 0:
                    messagebox.showinfo("Succès", f"Projet '{self.project_name_var.get().strip()}' créé avec succès !")
                    # Mettre à jour la prévisualisation si possible
                    if hasattr(self, 'preview_text'):
                        self.preview_text.delete('1.0', tk.END)
                        self.preview_text.insert('1.0', f"Projet créé avec succès dans :\n{project_folder}\n\nStructure :\n{stdout}")
                else:
                    messagebox.showerror("Erreur", f"Erreur lors de la génération du projet :\n{stderr}")
                
                # Réinitialiser le dossier cible
                self.target_folder = None
                
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
            
            # Déterminer le type spécifique du script
            script_type = ""
            if "Css_Themes_Generator.py" in script_name:
                script_type = "Générateur CSS"
            elif "Form_Generator.py" in script_name:
                script_type = "Générateur de Formulaires"
            elif "generateur_projet.py" in script_name:
                script_type = "Générateur de Projets"
            elif "Component_Generator.py" in script_name:
                script_type = "Générateur de Composants"
            elif "Layout_Generator.py" in script_name:
                script_type = "Générateur de Layouts"
            
            self.project_list.insert("", "end", text=script_name, values=(script_type, datetime.now().strftime("%Y-%m-%d %H:%M")))
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
        
        self.preview_text = ScrolledText(right_frame)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Boutons d'action
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(button_frame, text="Générer", 
                  command=lambda: self.generate_form(dialog)).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Annuler", 
                  command=dialog.destroy).pack(side=tk.RIGHT, padx=5)

    def setup_css_generator_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Générateur de Thèmes CSS")
        dialog.geometry("800x600")
        
        # Frame principale avec deux colonnes
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame gauche pour les options
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        ttk.Label(left_frame, text="Sélectionnez les composants :").pack(anchor=tk.W)
        
        # Dictionnaire des options avec leurs descriptions
        self.css_vars = {}
        css_options = [
            ("Thème Sombre", "dark", "Style sombre élégant avec accents colorés"),
            ("Thème Clair", "light", "Design épuré et minimaliste"),
            ("Thème Corporate", "corporate", "Style professionnel pour entreprises"),
            ("Variables CSS", "variables", "Définition des couleurs et espacements"),
            ("Reset CSS", "reset", "Réinitialisation des styles par défaut"),
            ("Utilitaires", "utilities", "Classes utilitaires (marges, padding...)"),
            ("Animations", "animations", "Effets de transition et animations"),
            ("Media Queries", "media", "Styles responsives pour tous écrans"),
            ("Print Styles", "print", "Styles optimisés pour l'impression")
        ]
        
        # Frame scrollable pour les options
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
        
        # Ajout des options avec leurs descriptions
        for label, option_type, description in css_options:
            frame = ttk.Frame(scrollable_frame)
            frame.pack(fill=tk.X, pady=2)
            
            var = tk.BooleanVar()
            self.css_vars[option_type] = var
            cb = ttk.Checkbutton(frame, text=label, variable=var,
                               command=self.update_css_preview)
            cb.pack(side=tk.LEFT)
            
            ttk.Label(frame, text=description, foreground="gray").pack(side=tk.LEFT, padx=5)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame droite pour la prévisualisation
        right_frame = ttk.LabelFrame(main_frame, text="Prévisualisation en direct")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.preview_text = ScrolledText(right_frame)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Boutons d'action
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(button_frame, text="Générer", 
                  command=lambda: self.generate_css(dialog)).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Annuler", 
                  command=dialog.destroy).pack(side=tk.RIGHT, padx=5)

    def setup_component_generator_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Générateur de Composants")
        dialog.geometry("800x600")
        
        # Frame principale avec deux colonnes
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame gauche pour les options
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        ttk.Label(left_frame, text="Sélectionnez les composants :").pack(anchor=tk.W)
        
        # Dictionnaire des composants avec leurs descriptions
        self.component_vars = {}
        components = [
            ("Barre de Navigation", "navbar", "Barre de navigation responsive"),
            ("Carte", "card", "Composant carte pour afficher du contenu"),
            ("Pied de Page", "footer", "Footer avec liens et copyright"),
            ("Section Hero", "hero", "Section d'en-tête avec image et texte")
        ]
        
        # Frame scrollable pour les composants
        checkbox_frame = ttk.Frame(left_frame)
        checkbox_frame.pack(fill=tk.BOTH, expand=True)
        
        for label, comp_type, description in components:
            frame = ttk.Frame(checkbox_frame)
            frame.pack(fill=tk.X, pady=2)
            
            var = tk.BooleanVar()
            self.component_vars[comp_type] = var
            cb = ttk.Checkbutton(frame, text=label, variable=var,
                               command=self.update_component_preview)
            cb.pack(side=tk.LEFT)
            
            ttk.Label(frame, text=description, foreground="gray").pack(side=tk.LEFT, padx=5)
        
        # Frame droite pour la prévisualisation
        right_frame = ttk.LabelFrame(main_frame, text="Prévisualisation en direct")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.preview_text = tk.Text(right_frame, wrap=tk.WORD)
        preview_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=preview_scrollbar.set)
        
        self.preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Boutons d'action
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(button_frame, text="Générer", 
                  command=lambda: self.generate_component(dialog)).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Annuler", 
                  command=dialog.destroy).pack(side=tk.RIGHT, padx=5)

    def setup_layout_generator_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Générateur de Layouts")
        dialog.geometry("800x600")
        
        # Frame principale avec deux colonnes
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame gauche pour les options
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        ttk.Label(left_frame, text="Sélectionnez le type de layout :").pack(anchor=tk.W)
        
        # Dictionnaire des layouts avec leurs descriptions
        self.layout_vars = {}
        layouts = [
            ("Grid Layout", "grid", "Mise en page basée sur CSS Grid"),
            ("Flex Layout", "flex", "Mise en page basée sur Flexbox")
        ]
        
        # Frame pour les layouts
        layout_frame = ttk.Frame(left_frame)
        layout_frame.pack(fill=tk.BOTH, expand=True)
        
        for label, layout_type, description in layouts:
            frame = ttk.Frame(layout_frame)
            frame.pack(fill=tk.X, pady=2)
            
            var = tk.BooleanVar()
            self.layout_vars[layout_type] = var
            cb = ttk.Checkbutton(frame, text=label, variable=var,
                               command=self.update_layout_preview)
            cb.pack(side=tk.LEFT)
            
            ttk.Label(frame, text=description, foreground="gray").pack(side=tk.LEFT, padx=5)
        
        # Frame droite pour la prévisualisation
        right_frame = ttk.LabelFrame(main_frame, text="Prévisualisation en direct")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.preview_text = tk.Text(right_frame, wrap=tk.WORD)
        preview_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=preview_scrollbar.set)
        
        self.preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Boutons d'action
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(button_frame, text="Générer", 
                  command=lambda: self.generate_layout(dialog)).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Annuler", 
                  command=dialog.destroy).pack(side=tk.RIGHT, padx=5)

    def update_css_preview(self):
        selected = [opt for opt, var in self.css_vars.items() if var.get()]
        if not selected:
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert('1.0', "Sélectionnez des options pour voir la prévisualisation")
            return
        
        preview = """/* Style CSS généré */\n\n"""
        
        for opt in selected:
            if opt == "dark":
                preview += """:root {
    --bg-color: #1a1a1a;
    --text-color: #ffffff;
    --primary-color: #00b4d8;
}

body {
    background-color: var(--bg-color);
    color: var(--text-color);
}\n\n"""
            elif opt == "light":
                preview += """:root {
    --bg-color: #ffffff;
    --text-color: #333333;
    --primary-color: #0066cc;
}

body {
    background-color: var(--bg-color);
    color: var(--text-color);
}\n\n"""
            # Ajoutez d'autres prévisualisations pour les autres options
        
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', preview)

    def update_component_preview(self):
        selected = [comp for comp, var in self.component_vars.items() if var.get()]
        if not selected:
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert('1.0', "Sélectionnez des composants pour voir la prévisualisation")
            return
        
        preview = """<!-- Composants HTML générés -->\n\n"""
        
        for comp in selected:
            if comp == "navbar":
                preview += """<nav class="navbar">
    <div class="brand">Logo</div>
    <ul class="nav-links">
        <li><a href="#">Accueil</a></li>
        <li><a href="#">Services</a></li>
        <li><a href="#">Contact</a></li>
    </ul>
</nav>\n\n"""
            elif comp == "hero":
                preview += """<section class="hero">
    <h1>Titre Principal</h1>
    <p>Description accrocheuse</p>
    <button>Call to Action</button>
</section>\n\n"""
            # Ajoutez d'autres prévisualisations pour les autres composants
        
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', preview)

    def update_layout_preview(self):
        selected = [layout for layout, var in self.layout_vars.items() if var.get()]
        if not selected:
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert('1.0', "Sélectionnez des layouts pour voir la prévisualisation")
            return
        
        preview = """<!-- Layout HTML généré -->\n\n"""
        
        for layout in selected:
            if layout == "grid":
                preview += """<div class="grid-container">
    <div class="grid-item">1</div>
    <div class="grid-item">2</div>
    <div class="grid-item">3</div>
    <div class="grid-item">4</div>
</div>

<style>
.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    padding: 1rem;
}
</style>\n\n"""
            elif layout == "flex":
                preview += """<div class="flex-container">
    <div class="flex-item">1</div>
    <div class="flex-item">2</div>
    <div class="flex-item">3</div>
</div>

<style>
.flex-container {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
    padding: 1rem;
}
</style>\n\n"""
            # Ajoutez d'autres prévisualisations pour les autres layouts
        
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', preview)

    def generate_css(self, dialog):
        selected_options = [opt for opt, var in self.css_vars.items() if var.get()]
        if not selected_options:
            messagebox.showwarning("Attention", "Veuillez sélectionner au moins une option")
            return
            
        if not self.target_folder:
            self.target_folder = filedialog.askdirectory(title="Choisir le dossier de destination")
            if not self.target_folder:
                return

        try:
            script_path = os.path.join(os.path.dirname(__file__), "Css_Themes_Generator.py")
            command = [
                "python",
                script_path,
                "--path", self.target_folder,
                "--options", ",".join(selected_options)
            ]
            
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("Succès", "CSS généré avec succès !")
                dialog.destroy()
            else:
                messagebox.showerror("Erreur", f"Erreur lors de la génération : {result.stderr}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur : {str(e)}")

    def generate_form(self, dialog):
        selected_fields = [field for field, var in self.fields_vars.items() if var.get()]
        if not selected_fields:
            messagebox.showwarning("Attention", "Veuillez sélectionner au moins un champ")
            return
            
        if not self.project_name_var.get().strip():
            messagebox.showwarning("Attention", "Veuillez entrer un nom de projet")
            return
            
        if not self.target_folder:
            self.target_folder = filedialog.askdirectory(title="Choisir le dossier de destination")
            if not self.target_folder:
                return

        try:
            script_path = os.path.join(os.path.dirname(__file__), "Form_Generator.py")
            command = [
                "python",
                script_path,
                "--path", os.path.join(self.target_folder, self.project_name_var.get().strip()),
                "--fields", ",".join(selected_fields),
                "--name", "form"
            ]
            
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("Succès", "Formulaire généré avec succès !")
                dialog.destroy()
            else:
                messagebox.showerror("Erreur", f"Erreur lors de la génération : {result.stderr}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur : {str(e)}")

    def generate_component(self, dialog):
        selected_components = [comp for comp, var in self.component_vars.items() if var.get()]
        if not selected_components:
            messagebox.showwarning("Attention", "Veuillez sélectionner au moins un composant")
            return
            
        if not self.project_name_var.get().strip():
            messagebox.showwarning("Attention", "Veuillez entrer un nom de projet")
            return
            
        if not self.target_folder:
            self.target_folder = filedialog.askdirectory(title="Choisir le dossier de destination")
            if not self.target_folder:
                return

        try:
            for component_type in selected_components:
                script_path = os.path.join(os.path.dirname(__file__), "Component_Generator.py")
                command = [
                    sys.executable,
                    script_path,
                    "--name", self.project_name_var.get().strip(),
                    "--type", component_type,
                    "--path", self.target_folder
                ]
                
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                stdout, stderr = process.communicate()
                
                if process.returncode != 0:
                    messagebox.showerror("Erreur", f"Erreur lors de la génération du composant {component_type}:\n{stderr}")
                    return
            
            messagebox.showinfo("Succès", "Composants générés avec succès !")
            dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur : {str(e)}")

    def generate_layout(self, dialog):
        selected_layouts = [layout for layout, var in self.layout_vars.items() if var.get()]
        if not selected_layouts:
            messagebox.showwarning("Attention", "Veuillez sélectionner au moins un type de layout")
            return
            
        if not self.project_name_var.get().strip():
            messagebox.showwarning("Attention", "Veuillez entrer un nom de projet")
            return
            
        if not self.target_folder:
            self.target_folder = filedialog.askdirectory(title="Choisir le dossier de destination")
            if not self.target_folder:
                return

        try:
            for layout_type in selected_layouts:
                script_path = os.path.join(os.path.dirname(__file__), "Layout_Generator.py")
                command = [
                    sys.executable,
                    script_path,
                    "--name", self.project_name_var.get().strip(),
                    "--type", layout_type,
                    "--path", self.target_folder
                ]
                
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                stdout, stderr = process.communicate()
                
                if process.returncode != 0:
                    messagebox.showerror("Erreur", f"Erreur lors de la génération du layout {layout_type}:\n{stderr}")
                    return
            
            messagebox.showinfo("Succès", "Layouts générés avec succès !")
            dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur : {str(e)}")

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

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = ModernProjectManagerApp(root)
    root.mainloop()
