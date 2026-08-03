"""
Empaqueta el Teams Tab en un zip listo para subir al portal de Teams.

Uso:
    python teams/package.py https://mi-app.azurewebsites.net

El script reemplaza APP_URL y APP_DOMAIN en el manifest y genera:
    teams/onboarding-assistant.zip
"""

import argparse
import json
import os
import zipfile
from urllib.parse import urlparse


def main():
    parser = argparse.ArgumentParser(description="Empaqueta el Teams Tab")
    parser.add_argument("url", help="URL pública de la app (ej: https://mi-app.azurewebsites.net)")
    args = parser.parse_args()

    url = args.url.rstrip("/")
    domain = urlparse(url).netloc

    teams_dir = os.path.dirname(os.path.abspath(__file__))
    manifest_path = os.path.join(teams_dir, "manifest.json")

    with open(manifest_path) as f:
        manifest_text = f.read()

    manifest_text = manifest_text.replace("APP_URL", url)
    manifest_text = manifest_text.replace("APP_DOMAIN", domain)

    # Validar que el JSON resultante es correcto
    json.loads(manifest_text)

    zip_path = os.path.join(teams_dir, "onboarding-assistant.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("manifest.json", manifest_text)
        zf.write(os.path.join(teams_dir, "icon-color.png"), "icon-color.png")
        zf.write(os.path.join(teams_dir, "icon-outline.png"), "icon-outline.png")

    print(f"Zip generado: {zip_path}")
    print(f"URL configurada: {url}")
    print()
    print("Próximos pasos:")
    print("  1. Abrí Microsoft Teams")
    print("  2. Andá a Apps → Manage your apps → Upload an app")
    print("  3. Subí el archivo onboarding-assistant.zip")


if __name__ == "__main__":
    main()
