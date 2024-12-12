import os
import argparse

def generate_form_field(field_type, label):
    """Génère le HTML pour un champ de formulaire spécifique."""
    field_id = label.lower().replace(" ", "_")
    html = f'    <div class="form-group">\n'
    html += f'        <label for="{field_id}">{label}</label>\n'
    
    if field_type == "text":
        html += f'        <input type="text" id="{field_id}" name="{field_id}" class="form-control">\n'
    elif field_type == "email":
        html += f'        <input type="email" id="{field_id}" name="{field_id}" class="form-control">\n'
    elif field_type == "password":
        html += f'        <input type="password" id="{field_id}" name="{field_id}" class="form-control">\n'
    elif field_type == "number":
        html += f'        <input type="number" id="{field_id}" name="{field_id}" class="form-control">\n'
    elif field_type == "date":
        html += f'        <input type="date" id="{field_id}" name="{field_id}" class="form-control">\n'
    elif field_type == "tel":
        html += f'        <input type="tel" id="{field_id}" name="{field_id}" class="form-control">\n'
    elif field_type == "textarea":
        html += f'        <textarea id="{field_id}" name="{field_id}" class="form-control"></textarea>\n'
    elif field_type == "checkbox":
        html += f'        <input type="checkbox" id="{field_id}" name="{field_id}" class="form-check-input">\n'
    elif field_type == "select":
        html += f'        <select id="{field_id}" name="{field_id}" class="form-control">\n'
        html += '            <option value="">Sélectionnez une option</option>\n'
        html += '        </select>\n'
    
    html += '    </div>\n'
    return html

def generate_form(fields, output_dir, name="form"):
    """Génère un fichier HTML contenant un formulaire personnalisé."""
    html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulaire</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { padding: 2rem; }
        .form-group { margin-bottom: 1rem; }
    </style>
</head>
<body>
    <div class="container">
        <h2 class="mb-4">Formulaire</h2>
        <form action="#" method="POST" class="needs-validation" novalidate>
"""
    
    # Génération des champs
    for field_type in fields:
        label = field_type.replace("_", " ").title()
        html += generate_form_field(field_type, label)
    
    html += """            <button type="submit" class="btn btn-primary">Envoyer</button>
        </form>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Validation des formulaires Bootstrap
        (function () {
            'use strict'
            var forms = document.querySelectorAll('.needs-validation')
            Array.prototype.slice.call(forms).forEach(function (form) {
                form.addEventListener('submit', function (event) {
                    if (!form.checkValidity()) {
                        event.preventDefault()
                        event.stopPropagation()
                    }
                    form.classList.add('was-validated')
                }, false)
            })
        })()
    </script>
</body>
</html>"""

    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)
    
    # Écrire le fichier HTML
    output_file = os.path.join(output_dir, f"{name}.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Formulaire généré avec succès : {output_file}")
    return output_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générateur de formulaires HTML")
    parser.add_argument("--path", required=True, help="Chemin de destination du formulaire")
    parser.add_argument("--fields", required=True, help="Liste des champs séparés par des virgules")
    parser.add_argument("--name", default="form", help="Nom du fichier de sortie (sans extension)")
    
    args = parser.parse_args()
    
    # Convertir la chaîne de champs en liste
    fields = [field.strip() for field in args.fields.split(",")]
    
    # Générer le formulaire
    generate_form(fields, args.path, args.name)
