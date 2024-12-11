import re
import os
from tkinter import Tk, filedialog, messagebox

def clean_css(css_file, html_files):
    """Nettoie un fichier CSS en supprimant les classes non utilisées dans les fichiers HTML."""
    if not os.path.exists(css_file):
        messagebox.showerror("Erreur", f"Le fichier CSS '{css_file}' n'existe pas.")
        return

    with open(css_file, "r", encoding="utf-8") as css:
        css_content = css.read()

    used_classes = set()
    for html_file in html_files:
        if os.path.exists(html_file):
            with open(html_file, "r", encoding="utf-8") as html:
                # Trouver toutes les classes utilisées dans les fichiers HTML
                used_classes.update(re.findall(r'class="(.*?)"', html.read()))
        else:
            messagebox.showwarning("Avertissement", f"Le fichier HTML '{html_file}' n'existe pas et sera ignoré.")

    # Filtrer le CSS pour ne garder que les classes utilisées
    cleaned_css = "\n".join([
        line for line in css_content.splitlines()
        if any(cls in line for cls in used_classes)
    ])

    # Écrire le CSS nettoyé dans un nouveau fichier
    output_file = os.path.join(os.path.dirname(css_file), "cleaned.css")
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(cleaned_css)

    messagebox.showinfo("Succès", f"CSS nettoyé avec succès dans '{output_file}'.")

if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # Masquer la fenêtre principale

    messagebox.showinfo("Nettoyeur CSS", "Sélectionnez le fichier CSS à nettoyer.")
    css_file = filedialog.askopenfilename(
        title="Sélectionner un fichier CSS",
        filetypes=[("Fichiers CSS", "*.css")]
    )

    if not css_file:
        messagebox.showwarning("Avertissement", "Aucun fichier CSS sélectionné.")
        exit()

    messagebox.showinfo("Nettoyeur CSS", "Sélectionnez les fichiers HTML associés.")
    html_files = filedialog.askopenfilenames(
        title="Sélectionner des fichiers HTML",
        filetypes=[("Fichiers HTML", "*.html")]
    )

    if not html_files:
        messagebox.showwarning("Avertissement", "Aucun fichier HTML sélectionné.")
        exit()

    clean_css(css_file, html_files)

# Instructions pour l'utiliser :
# Depuis le GUI :
# - Lancer le script dans un environnement où Tkinter est installé.
# - Une fenêtre apparaîtra pour permettre à l'utilisateur de sélectionner un fichier CSS et les fichiers HTML associés.
# Depuis Visual Studio Code :
# - Placez ce script dans votre espace de travail.
# - Ajoutez une tâche dans votre fichier tasks.json pour exécuter le script :
#   {
#     "label": "Nettoyer les fichiers CSS inutilisés",
#     "type": "shell",
#     "command": "python",
#     "args": ["${workspaceFolder}/css_cleaner_gui.py"],
#     "problemMatcher": []
#   }
# - Lancez la tâche avec Ctrl+Shift+P > Tasks: Run Task > Nettoyer les fichiers CSS inutilisés.
# Résultat :
# - Un fichier cleaned.css sera généré dans le même répertoire que le fichier CSS d'origine, contenant uniquement les classes utilisées.
