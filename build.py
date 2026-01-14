import subprocess
import os
import shutil
import sys
from pathlib import Path

def exporter_dashboard():
    # 1. Chemins des dossiers
    dossier_source = Path(__file__).parent
    dossier_sortie = dossier_source / "docs"

    # 2. Localiser l'exécutable shinylive
    # On cherche dans le dossier 'Scripts' de votre installation Python
    python_bin_dir = Path(sys.executable).parent
    shinylive_exe = python_bin_dir / "Scripts" / "shinylive.exe"
    
    # Si non trouvé (ex: environnement virtuel), on cherche au même niveau que python.exe
    if not shinylive_exe.exists():
        shinylive_exe = python_bin_dir / "shinylive"

    print(f"--- Tentative d'exportation ---")
    
    # Nettoyage
    if dossier_sortie.exists():
        shutil.rmtree(dossier_sortie)

    try:
        # 3. Exécution avec le chemin complet
        subprocess.run(
            [str(shinylive_exe), "export", str(dossier_source), str(dossier_sortie)],
            check=True,
            shell=True
        )
        print(f"\n✅ Succès ! Le dossier 'docs' a été créé à : {dossier_sortie}")
        
    except Exception as e:
        print(f"\n❌ Erreur persistante : {e}")
        print("\nAlternative de dernier recours :")
        print(f"Tapez manuellement ceci dans votre terminal VS Code :")
        print(f"python -m shinylive export . docs")

if __name__ == "__main__":
    exporter_dashboard()