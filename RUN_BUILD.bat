@echo off
title Production du Dashboard de suivi des objectifs du PDE de l'OBVFSJ
echo ============================================
echo   PRODUCTION DU DASHBOARD EN STRUCTURE HTML
echo ============================================
echo.
echo Tentative de création des fichiers dans le dossier /docs...
echo.

:: Lance le script build.py en utilisant l'exécutable Python par défaut
:: python build.py
"C:\Users\gchre\anaconda3\envs\suivi_objectifs_PDE_2024_2034\python.exe" export_static.py

echo.
echo ============================================
echo   TRAVAIL TERMINE !
echo ============================================
echo.
pause