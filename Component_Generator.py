import os
import argparse
from tkinter import messagebox

def generate_component(name, component_type, output_dir):
    """Génère un composant web réutilisable."""
    components = {
        "navbar": {
            "html": """
<nav class="navbar">
    <div class="navbar-brand">
        <a href="#" class="navbar-logo">Logo</a>
    </div>
    <div class="navbar-menu">
        <a href="#" class="navbar-item">Accueil</a>
        <a href="#" class="navbar-item">À propos</a>
        <a href="#" class="navbar-item">Services</a>
        <a href="#" class="navbar-item">Contact</a>
    </div>
</nav>""",
            "css": """
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background-color: var(--primary-color, #333);
    color: white;
}

.navbar-brand {
    font-size: 1.5rem;
}

.navbar-menu {
    display: flex;
    gap: 1rem;
}

.navbar-item {
    color: white;
    text-decoration: none;
    padding: 0.5rem;
}

.navbar-item:hover {
    background-color: rgba(255,255,255,0.1);
    border-radius: 4px;
}"""
        },
        "card": {
            "html": """
<div class="card">
    <div class="card-image">
        <img src="placeholder.jpg" alt="Image">
    </div>
    <div class="card-content">
        <h3 class="card-title">Titre de la carte</h3>
        <p class="card-text">Description de la carte</p>
    </div>
    <div class="card-footer">
        <button class="btn">En savoir plus</button>
    </div>
</div>""",
            "css": """
.card {
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    background: white;
    transition: transform 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
}

.card-image img {
    width: 100%;
    height: 200px;
    object-fit: cover;
}

.card-content {
    padding: 1rem;
}

.card-title {
    margin: 0 0 0.5rem 0;
    color: var(--primary-color, #333);
}

.card-footer {
    padding: 1rem;
    border-top: 1px solid #eee;
}"""
        },
        "footer": {
            "html": """
<footer class="footer">
    <div class="footer-content">
        <div class="footer-section">
            <h4>À propos</h4>
            <p>Description de votre entreprise ou projet.</p>
        </div>
        <div class="footer-section">
            <h4>Liens rapides</h4>
            <ul>
                <li><a href="#">Accueil</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Contact</a></li>
            </ul>
        </div>
        <div class="footer-section">
            <h4>Contact</h4>
            <p>Email: contact@example.com</p>
            <p>Tél: (123) 456-7890</p>
        </div>
    </div>
    <div class="footer-bottom">
        <p>&copy; 2024 Votre Entreprise. Tous droits réservés.</p>
    </div>
</footer>""",
            "css": """
.footer {
    background-color: var(--primary-color, #333);
    color: white;
    padding: 2rem 0;
}

.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
}

.footer-section h4 {
    color: white;
    margin-bottom: 1rem;
}

.footer-section ul {
    list-style: none;
    padding: 0;
}

.footer-section ul li {
    margin-bottom: 0.5rem;
}

.footer-section a {
    color: white;
    text-decoration: none;
}

.footer-bottom {
    text-align: center;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255,255,255,0.1);
}"""
        },
        "hero": {
            "html": """
<section class="hero">
    <div class="hero-content">
        <h1 class="hero-title">Titre principal</h1>
        <p class="hero-text">Une description captivante de votre projet ou service.</p>
        <div class="hero-buttons">
            <button class="btn btn-primary">Commencer</button>
            <button class="btn btn-secondary">En savoir plus</button>
        </div>
    </div>
</section>""",
            "css": """
.hero {
    background-color: var(--primary-color, #333);
    color: white;
    padding: 4rem 2rem;
    text-align: center;
    background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('hero-bg.jpg');
    background-size: cover;
    background-position: center;
}

.hero-content {
    max-width: 800px;
    margin: 0 auto;
}

.hero-title {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero-text {
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.hero-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
}"""
        }
    }

    if component_type not in components:
        raise ValueError(f"Type de composant non supporté. Types disponibles: {', '.join(components.keys())}")

    # Créer les dossiers nécessaires
    component_dir = os.path.join(output_dir, "components", name)
    os.makedirs(component_dir, exist_ok=True)

    # Générer les fichiers
    html_path = os.path.join(component_dir, f"{name}.html")
    css_path = os.path.join(component_dir, f"{name}.css")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(components[component_type]["html"])
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(components[component_type]["css"])

    return component_dir

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générateur de composants web")
    parser.add_argument("--name", required=True, help="Nom du composant")
    parser.add_argument("--type", required=True, choices=["navbar", "card", "footer", "hero"], help="Type de composant")
    parser.add_argument("--path", required=True, help="Chemin de destination")
    
    args = parser.parse_args()
    
    try:
        output_dir = generate_component(args.name, args.type, args.path)
        print(f"Composant généré avec succès dans: {output_dir}")
    except Exception as e:
        print(f"Erreur: {str(e)}")
