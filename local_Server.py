# fichier tasks.json mis à jour pour inclure le serveur local intégré, 
# vous permettant de prévisualiser vos fichiers HTML directement depuis Visual Studio Code.

# Exécute le script local_server.py pour démarrer un serveur HTTP local.
# Permet de prévisualiser les fichiers HTML sur http://localhost:8000.

# Utilisation :

# Placez local_server.py dans votre espace de travail.
# Ouvrez Visual Studio Code et exécutez la tâche via Ctrl+Shift+P > Tasks: Run Task.
# Résultat attendu :

# Le terminal de VSCode affiche l'URL du serveur (par exemple : http://localhost:8000).
# Vous pouvez ouvrir cette URL dans votre navigateur pour visualiser les fichiers.


import http.server
import socketserver

def start_server(port=8000):
    """Démarre un serveur HTTP local pour prévisualiser des fichiers."""
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serveur démarré sur le port {port}. Accédez à http://localhost:{port}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nArrêt du serveur...")
            httpd.server_close()

if __name__ == "__main__":
    print("=== Serveur Local Intégré ===")
    port = input("Entrez le port pour le serveur (par défaut : 8000) : ").strip()
    if not port.isdigit():
        port = 8000
    else:
        port = int(port)
    start_server(port)
    
    
    