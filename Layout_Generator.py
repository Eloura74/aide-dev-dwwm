import os
import argparse
from tkinter import messagebox

def generate_layout(name, layout_type, output_dir):
    """Génère une mise en page web."""
    layouts = {
        "grid": {
            "html": """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grid Layout</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="grid-container">
        <header class="header">Header</header>
        <nav class="sidebar">Sidebar</nav>
        <main class="main-content">
            <h1>Contenu Principal</h1>
            <div class="grid">
                <div class="grid-item">1</div>
                <div class="grid-item">2</div>
                <div class="grid-item">3</div>
                <div class="grid-item">4</div>
            </div>
        </main>
        <aside class="sidebar-right">Sidebar Right</aside>
        <footer class="footer">Footer</footer>
    </div>
</body>
</html>""",
            "css": """
.grid-container {
    display: grid;
    grid-template-areas:
        "header header header header"
        "nav main main sidebar"
        "footer footer footer footer";
    grid-template-rows: auto 1fr auto;
    min-height: 100vh;
    gap: 1rem;
    padding: 1rem;
}

.header {
    grid-area: header;
    background: var(--primary-color, #333);
    color: white;
    padding: 1rem;
}

.sidebar {
    grid-area: nav;
    background: #f5f5f5;
    padding: 1rem;
}

.main-content {
    grid-area: main;
    padding: 1rem;
}

.sidebar-right {
    grid-area: sidebar;
    background: #f5f5f5;
    padding: 1rem;
}

.footer {
    grid-area: footer;
    background: var(--primary-color, #333);
    color: white;
    padding: 1rem;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    padding: 1rem;
}

.grid-item {
    background: #f0f0f0;
    padding: 1rem;
    text-align: center;
    border-radius: 4px;
}

@media (max-width: 768px) {
    .grid-container {
        grid-template-areas:
            "header"
            "nav"
            "main"
            "sidebar"
            "footer";
    }
}"""
        },
        "flex": {
            "html": """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flex Layout</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="flex-container">
        <header class="header">
            <h1>Header</h1>
        </header>
        
        <div class="content-wrapper">
            <nav class="sidebar">
                <h2>Navigation</h2>
                <ul>
                    <li><a href="#">Lien 1</a></li>
                    <li><a href="#">Lien 2</a></li>
                    <li><a href="#">Lien 3</a></li>
                </ul>
            </nav>
            
            <main class="main-content">
                <h2>Contenu Principal</h2>
                <div class="flex-grid">
                    <div class="flex-item">1</div>
                    <div class="flex-item">2</div>
                    <div class="flex-item">3</div>
                    <div class="flex-item">4</div>
                </div>
            </main>
        </div>
        
        <footer class="footer">
            <p>Footer</p>
        </footer>
    </div>
</body>
</html>""",
            "css": """
.flex-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

.header {
    background: var(--primary-color, #333);
    color: white;
    padding: 1rem;
}

.content-wrapper {
    display: flex;
    flex: 1;
}

.sidebar {
    width: 200px;
    background: #f5f5f5;
    padding: 1rem;
}

.main-content {
    flex: 1;
    padding: 1rem;
}

.flex-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    padding: 1rem;
}

.flex-item {
    flex: 1 1 200px;
    background: #f0f0f0;
    padding: 1rem;
    text-align: center;
    border-radius: 4px;
}

.footer {
    background: var(--primary-color, #333);
    color: white;
    padding: 1rem;
    text-align: center;
}

@media (max-width: 768px) {
    .content-wrapper {
        flex-direction: column;
    }
    
    .sidebar {
        width: 100%;
    }
}"""
        }
    }

    if layout_type not in layouts:
        raise ValueError(f"Type de mise en page non supporté. Types disponibles: {', '.join(layouts.keys())}")

    # Créer le dossier de mise en page
    layout_dir = os.path.join(output_dir, "layouts", name)
    os.makedirs(layout_dir, exist_ok=True)

    # Générer les fichiers
    html_path = os.path.join(layout_dir, "index.html")
    css_path = os.path.join(layout_dir, "style.css")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(layouts[layout_type]["html"])
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(layouts[layout_type]["css"])

    return layout_dir

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générateur de mises en page")
    parser.add_argument("--name", required=True, help="Nom de la mise en page")
    parser.add_argument("--type", required=True, choices=["grid", "flex"], help="Type de mise en page")
    parser.add_argument("--path", required=True, help="Chemin de destination")
    
    args = parser.parse_args()
    
    try:
        output_dir = generate_layout(args.name, args.type, args.path)
        print(f"Mise en page générée avec succès dans: {output_dir}")
    except Exception as e:
        print(f"Erreur: {str(e)}")
