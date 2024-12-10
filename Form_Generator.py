# Lancez Visual Studio Code.
# Appuyez sur Ctrl+Shift+P, recherchez Tasks: Run Task, et sélectionnez "Générer un formulaire personnalisé".
# Résultat attendu :

# Le script génèrera un fichier form.html dans votre dossier de travail contenant un formulaire HTML basé sur
# les champs que vous aurez spécifiés.

def generate_form(fields):
    """Génère un fichier HTML contenant un formulaire personnalisé."""
    form = "<form action='#' method='POST'>\n"
    for field in fields:
        field_id = field.replace(" ", "_").lower()
        form += f'    <label for="{field_id}">{field.title()} :</label><br>\n'
        form += f'    <input type="text" id="{field_id}" name="{field_id}" placeholder="Entrez votre {field.lower()}"><br><br>\n'
    form += '    <input type="submit" value="Soumettre">\n</form>'

    # Écrire dans un fichier HTML
    with open("form.html", "w", encoding="utf-8") as file:
        file.write(form)
    print("Formulaire HTML généré avec succès dans 'form.html'.")

if __name__ == "__main__":
    print("=== Générateur de Formulaire Personnalisé ===")
    fields = input("Entrez les noms des champs du formulaire (séparés par des virgules) : ").strip().split(",")
    fields = [field.strip() for field in fields]
    generate_form(fields)