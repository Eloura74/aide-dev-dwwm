import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import subprocess
import json
from datetime import datetime
import webbrowser
from tkinter.scrolledtext import ScrolledText

class ModernProjectManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Projets Moderne")
        self.root.geometry("1200x800")
        
        # Configuration et états
        self.load_config()
        self.selected_projects = []
        self.target_folder = None
        self.history = []
        self.favorites = set()

        # Création de l'interface
        self.setup_styles()
        self.create_menu()
        self.create_main_interface()
        self.load_history()

    def load_config(self):
        self.config_file = "project_manager_config.json"
        self.default_config = {
            "theme": "light",
            "recent_projects": [],
            "favorites": [],
            "last_directory": "",
            "projects": [
                os.path.abspath("generateur_projet.py"),
                os.path.abspath("Form_Generator.py"),
                os.path.abspath("Html_Template_Generator.py"),
                os.path.abspath("Css_Themes_Generator.py"),
                os.path.abspath("library_manager.py"),
                os.path.abspath("project_Cleaner.py"),
                os.path.abspath("setup_tailwind.py"),
                os.path.abspath("Static_Site_Search.py"),
            ]
        }
        
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        except:
            self.config = self.default_config
            self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configuration des styles
        style.configure('Modern.TButton', padding=10, font=('Helvetica', 10))
        style.configure('Modern.TFrame', background='#f0f0f0')
        style.configure('Modern.TLabel', font=('Helvetica', 10))
        style.configure('Favorites.TButton', background='gold')

    def create_menu(self):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # Menu Fichier
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Nouveau Projet", command=self.new_project)
        file_menu.add_command(label="Ouvrir Projet", command=self.open_project)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit)

        # Menu Outils
        tools_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Outils", menu=tools_menu)
        tools_menu.add_command(label="Générateur CSS", command=lambda: self.launch_tool("Css_Themes_Generator.py"))
        tools_menu.add_command(label="Générateur de Formulaires", command=lambda: self.launch_tool("Form_Generator.py"))
        tools_menu.add_command(label="Générateur de Projets", command=lambda: self.launch_tool("generateur_projet.py"))

        # Menu Aide
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
        help_menu.add_command(label="À propos", command=self.show_about)

    def create_main_interface(self):
        # Création du conteneur principal avec Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Onglet Projets
        self.projects_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.projects_tab, text="Projets")
        self.setup_projects_tab()

        # Onglet Favoris
        self.favorites_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.favorites_tab, text="Favoris")
        self.setup_favorites_tab()

        # Onglet Historique
        self.history_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.history_tab, text="Historique")
        self.setup_history_tab()

        # Barre d'état
        self.status_bar = ttk.Label(self.root, text="Prêt", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_projects_tab(self):
        # Frame gauche pour la liste des projets
        left_frame = ttk.Frame(self.projects_tab)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Boutons pour ajouter les scripts spécifiques
        scripts_frame = ttk.LabelFrame(left_frame, text="Scripts disponibles")
        scripts_frame.pack(fill=tk.X, padx=5, pady=5)

        # Générateurs de base
        ttk.Button(scripts_frame, text="Ajouter Générateur CSS", 
                  command=lambda: self.add_specific_script("Css_Themes_Generator.py")).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(scripts_frame, text="Ajouter Générateur de Formulaires", 
                  command=lambda: self.add_specific_script("Form_Generator.py")).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(scripts_frame, text="Ajouter Générateur de Projets", 
                  command=lambda: self.add_specific_script("generateur_projet.py")).pack(fill=tk.X, padx=5, pady=2)

        # Nouveaux générateurs
        ttk.Separator(scripts_frame, orient='horizontal').pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(scripts_frame, text="Ajouter Générateur de Composants", 
                  command=lambda: self.add_specific_script("Component_Generator.py")).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(scripts_frame, text="Ajouter Générateur de Layouts", 
                  command=lambda: self.add_specific_script("Layout_Generator.py")).pack(fill=tk.X, padx=5, pady=2)

        # Liste des projets avec scrollbar
        self.project_list = ttk.Treeview(left_frame, selectmode='extended')
        self.project_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.project_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.project_list.configure(yscrollcommand=scrollbar.set)
        self.project_list["columns"] = ("type", "date")
        self.project_list.column("#0", width=200)
        self.project_list.column("type", width=100)
        self.project_list.column("date", width=150)
        
        self.project_list.heading("#0", text="Nom du Projet")
        self.project_list.heading("type", text="Type")
        self.project_list.heading("date", text="Date de modification")

        # Frame droite pour les options et actions
        right_frame = ttk.Frame(self.projects_tab)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)

        # Options de projet
        options_frame = ttk.LabelFrame(right_frame, text="Options du projet")
        options_frame.pack(fill=tk.X, padx=5, pady=5)

        self.project_name_var = tk.StringVar()
        ttk.Label(options_frame, text="Nom du projet:").pack(anchor=tk.W, padx=5, pady=2)
        ttk.Entry(options_frame, textvariable=self.project_name_var).pack(fill=tk.X, padx=5, pady=2)

        # Options supplémentaires
        self.tailwind_var = tk.BooleanVar()
        self.bootstrap_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Inclure Tailwind", variable=self.tailwind_var).pack(anchor=tk.W, padx=5)
        ttk.Checkbutton(options_frame, text="Inclure Bootstrap", variable=self.bootstrap_var).pack(anchor=tk.W, padx=5)

        # Boutons d'action
        actions_frame = ttk.LabelFrame(right_frame, text="Actions")
        actions_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(actions_frame, text="Nouveau Projet", command=self.new_project).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(actions_frame, text="Ajouter aux favoris", command=self.add_to_favorites).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(actions_frame, text="Exécuter", command=self.execute_project).pack(fill=tk.X, padx=5, pady=2)

        # Prévisualisation
        preview_frame = ttk.LabelFrame(right_frame, text="Prévisualisation")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.preview_text = ScrolledText(preview_frame, height=10)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def setup_favorites_tab(self):
        self.favorites_list = ttk.Treeview(self.favorites_tab)
        self.favorites_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configuration similaire à la liste des projets
        self.favorites_list["columns"] = ("type", "date")
        self.favorites_list.column("#0", width=200)
        self.favorites_list.column("type", width=100)
        self.favorites_list.column("date", width=150)
        
        self.favorites_list.heading("#0", text="Projet Favori")
        self.favorites_list.heading("type", text="Type")
        self.favorites_list.heading("date", text="Ajouté le")

    def setup_history_tab(self):
        self.history_list = ttk.Treeview(self.history_tab)
        self.history_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.history_list["columns"] = ("status", "date")
        self.history_list.column("#0", width=200)
        self.history_list.column("status", width=100)
        self.history_list.column("date", width=150)
        
        self.history_list.heading("#0", text="Action")
        self.history_list.heading("status", text="Statut")
        self.history_list.heading("date", text="Date")

    def new_project(self):
        project_name = simpledialog.askstring("Nouveau Projet", "Nom du projet:")
        if project_name:
            self.project_name_var.set(project_name)
            self.select_target_folder()

    def open_project(self):
        file_path = filedialog.askopenfilename(
            title="Ouvrir un projet",
            filetypes=[("Fichiers Python", "*.py"), ("Tous les fichiers", "*.*")]
        )
        if file_path:
            self.add_to_project_list(file_path)

    def add_to_project_list(self, file_path):
        file_name = os.path.basename(file_path)
        file_type = os.path.splitext(file_name)[1]
        mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M')
        
        self.project_list.insert("", "end", text=file_name, values=(file_type, mod_time))

    def add_to_favorites(self):
        selected = self.project_list.selection()
        if selected:
            for item in selected:
                project = self.project_list.item(item)
                if project["text"] not in self.favorites:
                    self.favorites.add(project["text"])
                    self.favorites_list.insert("", "end", text=project["text"], 
                                            values=(project["values"][0], datetime.now().strftime('%Y-%m-%d %H:%M')))

    def execute_project(self):
        selected = self.project_list.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un projet à exécuter.")
            return

        if not self.target_folder:
            self.select_target_folder()
            if not self.target_folder:
                return

        for item in selected:
            project = self.project_list.item(item)["text"]
            try:
                self.run_project(project)
                self.add_to_history(project, "Succès")
            except Exception as e:
                self.add_to_history(project, "Échec")
                messagebox.showerror("Erreur", f"Erreur lors de l'exécution de {project}: {str(e)}")

    def run_project(self, project_name):
        project_path = os.path.join(os.path.dirname(__file__), project_name)
        
        if not os.path.exists(project_path):
            raise FileNotFoundError(f"Le fichier {project_path} n'existe pas.")

        command = ["python", project_path]
        
        # Ajout des options spécifiques selon le type de projet
        if "Form_Generator.py" in project_name:
            fields = simpledialog.askstring("Champs", "Entrez les champs (séparés par des virgules):")
            if fields:
                command.extend(["--fields", fields])
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
        elif "Component_Generator.py" in project_name:
            choices = ["navbar", "card", "footer", "hero"]
            component_type = simpledialog.askstring("Type de composant", 
                f"Choisissez le type de composant ({', '.join(choices)}):")
            if not component_type or component_type.lower() not in choices:
                messagebox.showerror("Erreur", f"Le type doit être l'un des suivants : {', '.join(choices)}")
                return
            if not self.project_name_var.get().strip():
                messagebox.showwarning("Attention", "Veuillez entrer un nom de composant")
                return
            command.extend([
                "--type", component_type.lower(),
                "--name", self.project_name_var.get().strip()
            ])
        elif "Layout_Generator.py" in project_name:
            choices = ["grid", "flex"]
            layout_type = simpledialog.askstring("Type de layout", 
                f"Choisissez le type de layout ({', '.join(choices)}):")
            if not layout_type or layout_type.lower() not in choices:
                messagebox.showerror("Erreur", f"Le type doit être l'un des suivants : {', '.join(choices)}")
                return
            if not self.project_name_var.get().strip():
                messagebox.showwarning("Attention", "Veuillez entrer un nom pour le layout")
                return
            command.extend([
                "--type", layout_type.lower(),
                "--name", self.project_name_var.get().strip()
            ])

        if self.target_folder:
            command.extend(["--path", self.target_folder])
        
        try:
            # Utilisation de subprocess avec encoding spécifié
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8',
                errors='replace',
                universal_newlines=True
            )
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                raise Exception(stderr)

            self.preview_text.delete(1.0, tk.END)
            if stdout:
                self.preview_text.insert(tk.END, stdout)
            self.add_to_history(project_name, "Succès")
            messagebox.showinfo("Succès", f"Le script {project_name} a été exécuté avec succès")
        except Exception as e:
            self.add_to_history(project_name, "Échec")
            messagebox.showerror("Erreur", f"Erreur lors de l'exécution de {project_name}: {str(e)}")

    def select_target_folder(self):
        folder = filedialog.askdirectory(title="Sélectionner le dossier de destination")
        if folder:
            self.target_folder = folder
            self.status_bar.config(text=f"Dossier sélectionné: {folder}")

    def add_to_history(self, action, status):
        self.history_list.insert("", 0, text=action, 
                               values=(status, datetime.now().strftime('%Y-%m-%d %H:%M')))

    def show_documentation(self):
        # Ouvrir la documentation dans le navigateur par défaut
        doc_path = os.path.join(os.path.dirname(__file__), "documentation.html")
        if os.path.exists(doc_path):
            webbrowser.open(doc_path)
        else:
            messagebox.showinfo("Documentation", 
                              "La documentation complète est disponible dans le fichier README.md")

    def show_about(self):
        about_text = """Gestionnaire de Projets Moderne
Version 2.0
Créé par l'équipe Codeium

Un outil puissant pour gérer vos projets de développement.
"""
        messagebox.showinfo("À propos", about_text)

    def load_history(self):
        # Charger l'historique depuis le fichier de configuration
        if "history" in self.config:
            for entry in self.config["history"]:
                self.history_list.insert("", "end", text=entry["action"],
                                       values=(entry["status"], entry["date"]))

    def add_specific_script(self, script_name):
        script_path = os.path.join(os.path.dirname(__file__), script_name)
        if os.path.exists(script_path):
            # Vérifier si le script n'est pas déjà dans la liste
            for item in self.project_list.get_children():
                if self.project_list.item(item)["text"] == script_name:
                    messagebox.showinfo("Information", f"{script_name} est déjà dans la liste")
                    return
                
            # Ajouter le script à la liste
            file_type = "Script Python"
            mod_time = datetime.fromtimestamp(os.path.getmtime(script_path)).strftime('%Y-%m-%d %H:%M')
            self.project_list.insert("", "end", text=script_name, values=(file_type, mod_time))
            
            # Mettre à jour la configuration
            if script_path not in self.config["projects"]:
                self.config["projects"].append(script_path)
                self.save_config()
                
            messagebox.showinfo("Succès", f"{script_name} a été ajouté à la liste des projets")
        else:
            messagebox.showerror("Erreur", f"Le script {script_name} n'existe pas dans le répertoire")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernProjectManagerApp(root)
    root.mainloop()
