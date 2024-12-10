# **📖 Utilisation des Scripts Python pour le Développement Web**

---

## **🌐 1. Broken_Links_Checker.py**

**Usage** : Vérifie les liens brisés dans un fichier HTML.

<details>
  <summary>🛠️ <strong>Exécution</strong></summary>
  - **Dans Visual Studio Code** : `Ctrl+Shift+P > Tasks: Run Task > Vérifier les liens brisés`.
  - **Entrez** le chemin du fichier HTML lorsque le script vous le demande.
</details>

**✔️ Résultat** : Liste des liens valides et brisés affichée dans la console.

---

## **🎨 2. Css_Cleaner.py**

**Usage** : Nettoie un fichier CSS en supprimant les classes non utilisées.

<details>
  <summary>🛠️ <strong>Exécution</strong></summary>
  - **Dans Visual Studio Code** : `Ctrl+Shift+P > Tasks: Run Task > Nettoyer les fichiers CSS inutilisés`.
  - **Fournissez** le fichier CSS et les fichiers HTML à analyser.
</details>

**✔️ Résultat** : Un fichier `cleaned.css` contenant uniquement les classes utilisées.

---

## **🎨 3. Css_Themes_Generator.py**

**Usage** : Génère plusieurs fichiers CSS pour des thèmes personnalisés.

<details>
  <summary>🛠️ <strong>Exécution</strong></summary>
  - **Dans Visual Studio Code** : `Ctrl+Shift+P > Tasks: Run Task > Générer des thèmes CSS`.
</details>

**✔️ Résultat** : Des fichiers CSS (ex. `theme_ocean.css`) créés avec des palettes de couleurs spécifiques.

---

## **📝 4. Form_Generator.py**

**Usage** : Génère un formulaire HTML avec des champs personnalisés.

<details>
  <summary>🛠️ <strong>Exécution</strong></summary>
  - **Dans Visual Studio Code** : `Ctrl+Shift+P > Tasks: Run Task > Générer un formulaire personnalisé`.
  - **Entrez** les noms des champs (ex. `nom,email,age`) lors de l'exécution.
</details>

**✔️ Résultat** : Un fichier `form.html` contenant un formulaire structuré.

---

## **🏗️ 5. generateur_projet.py**

**Usage** : Génère une structure complète pour un nouveau projet.

<details>
  <summary>🛠️ <strong>Exécution</strong></summary>
  - **Dans Visual Studio Code** : `Ctrl+Shift+P > Tasks: Run Task > Exécuter le générateur de projet`.
  - **Fournissez** un nom de projet et le chemin de destination.
</details>

**✔️ Résultat** : Une structure de projet avec les fichiers nécessaires (HTML, CSS, JS).

---

## **📂 6. Html_Template_Generator.py**

**Usage** : Génère des fichiers HTML basés sur des templates prédéfinis.

<details>
  <summary>🛠️ <strong>Exécution</strong></summary>
  - **Dans Visual Studio Code** : `Ctrl+Shift+P > Tasks: Run Task > Générer des templates HTML`.
</details>

**✔️ Résultat** : Des fichiers HTML (par ex. `index.html`, `about.html`) créés dans un dossier `templates`.

---

## **📦 7. library_manager.py**

**Usage** : Télécharge automatiquement des bibliothèques externes (Bootstrap, FontAwesome, etc.).

<details>
  <summary>🛠️ <strong>Exécution</strong></summary>
  - **Dans Visual Studio Code** : `Ctrl+Shift+P > Tasks: Run Task > Exécuter le gestionnaire de bibliothèques`.
  - **Indiquez** le dossier où les bibliothèques doivent être enregistrées.
</details>

**✔️ Résultat** : Les fichiers CSS/JS des bibliothèques téléchargés dans le dossier spécifié.

---

## **💻 8. local_Server.py**

**Usage** : Démarre un serveur local HTTP pour prévisualiser votre projet.

<details>
  <summary>🛠️ <strong>Exécution</strong></summary>
  - **Dans Visual Studio Code** : `Ctrl+Shift+P > Tasks: Run Task > Démarrer le serveur local`.
  - **Indiquez** un port (par défaut : 8000).
</details>

**✔️ Résultat** : Le serveur démarre, accessible via [http://localhost:8000](http://localhost:8000).

---

## **🧹 9. project_Cleaner.py**

**Usage** : Nettoie un projet en supprimant les fichiers inutiles (log, tmp) et en vidant les dossiers (build, dist).

<details>
  <summary>🛠️ <strong>Exécution</strong></summary>
  - **Dans Visual Studio Code** : `Ctrl+Shift+P > Tasks: Run Task > Nettoyer le projet`.
  - **Indiquez** le chemi
