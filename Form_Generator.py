from tkinter import Tk, simpledialog, filedialog, messagebox
import os

def generate_form(fields, output_dir):
    """Génère un fichier HTML contenant un formulaire personnalisé."""
    form = "<form action='#' method='POST'>\n"
    for field in fields:
        field_id = field.replace(" ", "_").lower()
        form += f'    <label for="{field_id}">{field.title()} :</label><br>\n'
        form += f'    <input type="text" id="{field_id}" name="{field_id}" placeholder="Entrez votre {field.lower()}"><br><br>\n'
    form += '    <input type="submit" value="Soumettre">\n</form>'

    # Écrire dans un fichier HTML dans le dossier sélectionné
    output_file = os.path.join(output_dir, "form.html")
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(form)
    messagebox.showinfo("Succès", f"Formulaire HTML généré avec succès dans '{output_file}'.")

if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # Masquer la fenêtre principale

    # Récupérer le nom du projet depuis l'entrée utilisateur du GUI
    project_name = simpledialog.askstring(
        "Nom du Projet", 
        "Entrez le nom du projet où le formulaire sera enregistré :"
    )

    if not project_name:
        messagebox.showwarning("Avertissement", "Aucun nom de projet fourni.")
        exit()

    # Sélectionner le dossier de destination
    output_dir = filedialog.askdirectory(
        title="Sélectionner le dossier de destination pour le projet"
    )

    if not output_dir:
        messagebox.showwarning("Avertissement", "Aucun dossier de destination sélectionné.")
        exit()

    full_path = os.path.join(output_dir, project_name)
    os.makedirs(full_path, exist_ok=True)

    # Demander les champs du formulaire
    fields_input = simpledialog.askstring(
        "Champs du Formulaire", 
        "Entrez les noms des champs du formulaire (séparés par des virgules, ex: nom, email, téléphone) :"
    )

    if fields_input:
        fields = [field.strip() for field in fields_input.split(",")]
        if fields:
            generate_form(fields, full_path)
        else:
            messagebox.showwarning("Avertissement", "Aucun champ valide fourni.")
    else:
        messagebox.showwarning("Avertissement", "Aucun champ fourni.")

# Instructions pour l'utiliser :
# Depuis le GUI :
# - Lancer le script dans un environnement où Tkinter est installé.
# - Une fenêtre apparaîtra pour demander le nom du projet, le dossier de destination et les champs du formulaire.
# - Les champs doivent être fournis sous la forme de noms séparés par des virgules (par exemple : nom, email, téléphone).
# - Le script générera un fichier HTML nommé 'form.html' dans le dossier sélectionné et organisé dans un sous-dossier portant le nom du projet.
# Depuis Visual Studio Code :
# - Placez ce script dans votre espace de travail.
# - Ajoutez une tâche dans votre fichier tasks.json pour exécuter le script :
#   {
#     "label": "Générer un formulaire personnalisé",
#     "type": "shell",
#     "command": "python",
#     "args": ["${workspaceFolder}/form_generator_gui.py"],
#     "problemMatcher": []
#   }
# - Lancez la tâche avec Ctrl+Shift+P > Tasks: Run Task > Générer un formulaire personnalisé.
# Résultat :
# - Un fichier HTML sera généré dans un sous-dossier portant le nom du projet dans le dossier sélectionné.
