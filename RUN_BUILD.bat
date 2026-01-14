@echo off
title Exportation Dashboard OBVFSJ
echo ============================================
echo   EXPORTATION DU DASHBOARD (SHINYLIVE)
echo ============================================
echo.
echo Tentative d'exportation vers le dossier /docs...
echo.

:: Lance le script build.py en utilisant l'exécutable Python par défaut
:: python build.py
"C:\Users\gchre\anaconda3\envs\suivi_objectifs_PDE_2024_2034\python.exe" build.py

echo.
echo ============================================
echo   TRAVAIL TERMINE !
echo ============================================
echo.
pause