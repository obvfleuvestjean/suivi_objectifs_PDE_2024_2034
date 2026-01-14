import pandas as pd
import numpy as np
from datetime import date
from shiny import App, Inputs, Outputs, Session, render
from shiny.types import ImgData
from shiny.express import ui, input
import shinylive
import os

# Configuration du thème personnalisé
theme_obv = (
    ui.Theme("shiny")
    .add_defaults(
        primary="#0083cb",
        info="#0aa6b6",
        success="#c3d700",
        bg="#ffffff",
        fg="#000000",
    )
)

today = date.today().strftime("%Y-%m-%d")


# Chargement et travail des données (Excel + retrait des symboles de % sur les deux colonnes pertinentes)
df = pd.read_excel("suivi-des-objectifs_OBVFSJ.xlsx", sheet_name=1, header=1)
df["atteinte_cible_pct"] = df["Pourcentage d'atteinte de la cible"].str.replace('%', '').astype(float)
df["cible_pct"] = df["Cible en %"].str.replace('%', '').astype(float)
#df["numero_objectif"] = df["Numéro d'objectif"].astype(str) + " — " + df["Libellé de l'objectif"].astype(str)

# Colonnes importantes du Excel :
    # Objectif = "numero_objectif"
    # Échéance = "Échéance"
    # Cible = "Cible - valeur numérique"
    # Progression = "Résultat"
    # Date de mise à jour = "Date du résultat"

# Valeurs possibles "Orientation" :
    # 1 - Éviter la dégradation de la qualité de l'eau
    # 2 - Ralentir l'eutrophisation des lacs
    # 3 - Limiter la prolifération des espèces exotiques envahissantes
    # 4 - Freiner la perte d'habitat faunique
    # 5 - Éviter la destruction ou la dégradation de la qualité des milieux humides et hydriques

# Configuration de la page
ui.page_opts(theme=theme_obv, fillable=True)

# Ajout de CSS personnalisé pour forcer le style des barres de navigation et boutons
ui.head_content(
    ui.tags.style(f"""
        /* Active pill: blue background with white text for contrast */
        .nav-pills .nav-link.active, .nav-pills .nav-link.active:focus, .nav-pills .nav-link.active:hover {{
            background-color: #0083cb !important;
            color: #ffffff !important;
        }}
        /* Inactive links keep the brand blue */
        .nav-pills .nav-link {{ color: #0083cb; }}
        .nav-link {{ color: #0083cb; }}
        .card-header {{ background-color: #f8f9fa; border-bottom: 2px solid #0aa6b6; }}
        .app-header {{ display:flex; align-items:center; gap:12px; margin-bottom: 12px; }}
        .app-header img {{ height:80px; }}
        .app-header .meta {{ color:#666; font-size:14px; margin-top:4px; }}
        .section-header {{ color:#0aa6b6; margin-bottom:0px; font-size:24px; font-weight:bold;}}
    """)
)

# Header avec logo + titre + date
ui.HTML(f'''
    <div class="app-header">
      <div>
         <h1 style="margin:0">OBVFSJ - Suivi des objectifs du PDE 2024-2034</h1>
         <div class="meta">Dernière mise à jour : {today}</div>
      </div>
      <img src="https://obvfleuvestjean.com/wp-content/uploads/2026/01/LogoOBV_ContourBlanc.png" alt="Logo OBVFSJ">
    </div>
''')

with ui.navset_card_pill(id="tabs"):
    
    ### SECTION 0. INTRODUCTION ###
    with ui.nav_panel("Introduction"):
        ui.markdown("""
        ## Démarche de suivi du Plan directeur de l'eau (PDE)
        Bienvenue sur l'outil de suivi des objectifs du PDE de l'**Organisme de bassin versant du fleuve Saint-Jean** (OBVFSJ).
        Ce tableau de bord présente l'état d'avancement des **47 objectifs** du PDE 2024-2034 à travers les **5 orientations**.
        <br><br>
        """)
        with ui.value_box(theme="primary", value=None, max_height="250px"):
            ui.HTML(f'''
                <div>
                    <h2 style="margin:0.5em ; color:#ffffff ; text-align:center">Mission de l'OBVFSJ</h2>
                </div>
                <div>
                    <p style="padding-left:15% ; padding-right:15% ; color:#ffffff ; text-align:center"><i>«&nbspDans le bassin versant du fleuve Saint-Jean, le maintien d'écosystèmes intègres, source d'une  excellente qualité d'eau, constitue la base d'un héritage bâti sur de saines relations transfrontalières&nbsp»</i></p>
                </div>
            ''')

    ### SECTION 1. QUALITÉ DE L'EAU ###
    with ui.nav_panel("1. Qualité de l'eau"):
        df_qualite_eau = df[df["Orientation"] == "1 - Éviter la dégradation de la qualité de l'eau"].copy()
        df_qualite_eau["atteinte_cible_pct"] = pd.to_numeric(df_qualite_eau["atteinte_cible_pct"], errors="coerce").fillna(0)
        icone_qualite_eau = "💧🌊"
        moyenne_qualite_eau = int(df_qualite_eau["atteinte_cible_pct"].mean())
        
        ui.HTML(f'''
            <div class="section-header">
            <br>
                <h2><b>{icone_qualite_eau} Moyenne d'atteinte des objectifs pour cette orientation : {moyenne_qualite_eau} %</b></h2>
            </div>
        ''')
        
        if moyenne_qualite_eau > 70:
            ui.p("✅ Les objectifs sont en bonne voie d'être atteints.")
        elif moyenne_qualite_eau > 30:
            ui.p("⚠️ Des efforts constants sont encore requis.")
        else:
            ui.p("🚨 Priorité élevée : phase de planification.")  
        
        ui.hr()
        ui.h4("Progression par objectif :", style="color: #0083cb; margin-bottom: 20px;")
        
        for _, row in df_qualite_eau.iterrows():
            val = int(row["atteinte_cible_pct"])
            libelle = row["Libellé de l'objectif"]
            reference = row["Valeur(référence)"]
            resultat = row["Résultat"]
            date_resultat = row["Date du résultat"]
            echeance = row["Échéance"]
            cible = row["Cible - valeur numérique"]
            
            # Conteneur pour un seul objectif
            with ui.div(style="margin-bottom: 45px; padding: 0 10px;"):
                
                # Ligne supérieure : Libellé à gauche, Valeur à droite
                with ui.div(style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2.5px;"):
                    ui.span(libelle, style="font-weight: 600; color: #333; font-size: 0.95rem;")
                    ui.span(f"{val}%", style="font-weight: 600; color: #666; font-size: 0.9rem;")

                # Ligne médiane : Cible, dernier résultat et date du dernier résultat en valeur absolue
                with ui.div(style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 5px;color: rgba(0, 0, 0, 0.6);font-size: 0.9em;line-height: 1.2;"):
                    ui.span(f"Valeur de référence : {reference}")
                    ui.span(f"Cible : {cible}")
                    ui.span(f"Valeur au dernier suivi : {resultat}")
                    ui.span(f"Suivi le : {date_resultat}")
                    ui.span(f"Échéance : {echeance}")
                
                # Ligne inférieure : La barre de progression fine
                with ui.div(style="width: 100%; background-color: #f0f0f0; height: 12px; border-radius: 4px; overflow: hidden;"):
                    ui.div(style=f"""
                        width: {val}%; 
                        background-color: #0aa6b6; 
                        height: 100%; 
                        border-radius: 4px;
                        transition: width 1s ease-in-out;
                    """)                

    ### SECTION 2. EUTROPHISATION DES LACS ###
    with ui.nav_panel("2. Eutrophisation des lacs"):
        df_eutrophisation = df[df["Orientation"] == "2 - Ralentir l'eutrophisation des lacs"].copy()
        df_eutrophisation["atteinte_cible_pct"] = pd.to_numeric(df_eutrophisation["atteinte_cible_pct"], errors="coerce").fillna(0)
        icone_eutrophisation = "🦠🏞️"
        moyenne_eutrophisation = int(df_eutrophisation["atteinte_cible_pct"].mean())
        
        ui.HTML(f'''
            <div class="section-header">
            <br>
                <h2><b>{icone_eutrophisation} Moyenne d'atteinte des objectifs pour cette orientation : {moyenne_eutrophisation} %</b></h2>
            </div>
        ''')
        
        if moyenne_eutrophisation > 70:
            ui.p("✅ Les objectifs sont en bonne voie d'être atteints.")
        elif moyenne_eutrophisation > 30:
            ui.p("⚠️ Des efforts constants sont encore requis.")
        else:
            ui.p("🚨 Priorité élevée : phase de planification.")  
        
        ui.hr()
        ui.h4("Progression par objectif :", style="color: #0083cb; margin-bottom: 20px;")
        
        for _, row in df_eutrophisation.iterrows():
            val = int(row["atteinte_cible_pct"])
            libelle = row["Libellé de l'objectif"]
            reference = row["Valeur(référence)"]
            resultat = row["Résultat"]
            date_resultat = row["Date du résultat"]
            echeance = row["Échéance"]
            cible = row["Cible - valeur numérique"]
            
            # Conteneur pour un seul objectif
            with ui.div(style="margin-bottom: 45px; padding: 0 10px;"):
                
                # Ligne supérieure : Libellé à gauche, Valeur à droite
                with ui.div(style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2.5px;"):
                    ui.span(libelle, style="font-weight: 600; color: #333; font-size: 0.95rem;")
                    ui.span(f"{val}%", style="font-weight: 600; color: #666; font-size: 0.9rem;")

                # Ligne médiane : Cible, dernier résultat et date du dernier résultat en valeur absolue
                with ui.div(style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 5px;color: rgba(0, 0, 0, 0.6);font-size: 0.9em;line-height: 1.2;"):
                    ui.span(f"Valeur de référence : {reference}")
                    ui.span(f"Cible : {cible}")
                    ui.span(f"Valeur au dernier suivi : {resultat}")
                    ui.span(f"Suivi le : {date_resultat}")
                    ui.span(f"Échéance : {echeance}")
                
                # Ligne inférieure : La barre de progression fine
                with ui.div(style="width: 100%; background-color: #f0f0f0; height: 12px; border-radius: 4px; overflow: hidden;"):
                    ui.div(style=f"""
                        width: {val}%; 
                        background-color: #0aa6b6; 
                        height: 100%; 
                        border-radius: 4px;
                        transition: width 1s ease-in-out;
                    """)   

    ### SECTION 3. ESPÈCES EXOTIQUES ENVAHISSANTES ###
    with ui.nav_panel("3. Espèces exotiques envahissantes"):
        df_EEE = df[df["Orientation"] == "3 - Limiter la prolifération des espèces exotiques envahissantes"].copy()
        df_EEE["atteinte_cible_pct"] = pd.to_numeric(df_EEE["atteinte_cible_pct"], errors="coerce").fillna(0)
        icone_EEE = "🌾🦪"
        moyenne_EEE = int(df_EEE["atteinte_cible_pct"].mean())
        
        ui.HTML(f'''
            <div class="section-header">
            <br>
                <h2><b>{icone_EEE} Moyenne d'atteinte des objectifs pour cette orientation : {moyenne_EEE} %</b></h2>
            </div>
        ''')
        
        if moyenne_EEE > 70:
            ui.p("✅ Les objectifs sont en bonne voie d'être atteints.")
        elif moyenne_EEE > 30:
            ui.p("⚠️ Des efforts constants sont encore requis.")
        else:
            ui.p("🚨 Priorité élevée : phase de planification.")  
        
        ui.hr()
        ui.h4("Progression par objectif :", style="color: #0083cb; margin-bottom: 20px;")
        
        for _, row in df_EEE.iterrows():
            val = int(row["atteinte_cible_pct"])
            libelle = row["Libellé de l'objectif"]
            reference = row["Valeur(référence)"]
            resultat = row["Résultat"]
            date_resultat = row["Date du résultat"]
            echeance = row["Échéance"]
            cible = row["Cible - valeur numérique"]
            
            # Conteneur pour un seul objectif
            with ui.div(style="margin-bottom: 45px; padding: 0 10px;"):
                
                # Ligne supérieure : Libellé à gauche, Valeur à droite
                with ui.div(style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2.5px;"):
                    ui.span(libelle, style="font-weight: 600; color: #333; font-size: 0.95rem;")
                    ui.span(f"{val}%", style="font-weight: 600; color: #666; font-size: 0.9rem;")

                # Ligne médiane : Cible, dernier résultat et date du dernier résultat en valeur absolue
                with ui.div(style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 5px;color: rgba(0, 0, 0, 0.6);font-size: 0.9em;line-height: 1.2;"):
                    ui.span(f"Valeur de référence : {reference}")
                    ui.span(f"Cible : {cible}")
                    ui.span(f"Valeur au dernier suivi : {resultat}")
                    ui.span(f"Suivi le : {date_resultat}")
                    ui.span(f"Échéance : {echeance}")
                
                # Ligne inférieure : La barre de progression fine
                with ui.div(style="width: 100%; background-color: #f0f0f0; height: 12px; border-radius: 4px; overflow: hidden;"):
                    ui.div(style=f"""
                        width: {val}%; 
                        background-color: #0aa6b6; 
                        height: 100%; 
                        border-radius: 4px;
                        transition: width 1s ease-in-out;
                    """)  

    ### SECTION 4. HABITATS FAUNIQUES ###
    with ui.nav_panel("4. Habitats fauniques"):
        df_habitats_fauniques = df[df["Orientation"] == "4 - Freiner la perte d'habitat faunique"].copy()
        df_habitats_fauniques["atteinte_cible_pct"] = pd.to_numeric(df_habitats_fauniques["atteinte_cible_pct"], errors="coerce").fillna(0)
        icone_habitats_fauniques = "🐟🦎"
        moyenne_habitats_fauniques = int(df_habitats_fauniques["atteinte_cible_pct"].mean())
        
        ui.HTML(f'''
            <div class="section-header">
            <br>
                <h2><b>{icone_habitats_fauniques} Moyenne d'atteinte des objectifs pour cette orientation : {moyenne_habitats_fauniques} %</b></h2>
            </div>
        ''')
        
        if moyenne_habitats_fauniques > 70:
            ui.p("✅ Les objectifs sont en bonne voie d'être atteints.")
        elif moyenne_habitats_fauniques > 30:
            ui.p("⚠️ Des efforts constants sont encore requis.")
        else:
            ui.p("🚨 Priorité élevée : phase de planification.")  
        
        ui.hr()
        ui.h4("Progression par objectif :", style="color: #0083cb; margin-bottom: 20px;")
        
        for _, row in df_habitats_fauniques.iterrows():
            val = int(row["atteinte_cible_pct"])
            libelle = row["Libellé de l'objectif"]
            reference = row["Valeur(référence)"]
            resultat = row["Résultat"]
            date_resultat = row["Date du résultat"]
            echeance = row["Échéance"]
            cible = row["Cible - valeur numérique"]
            
            # Conteneur pour un seul objectif
            with ui.div(style="margin-bottom: 45px; padding: 0 10px;"):
                
                # Ligne supérieure : Libellé à gauche, Valeur à droite
                with ui.div(style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2.5px;"):
                    ui.span(libelle, style="font-weight: 600; color: #333; font-size: 0.95rem;")
                    ui.span(f"{val}%", style="font-weight: 600; color: #666; font-size: 0.9rem;")

                # Ligne médiane : Cible, dernier résultat et date du dernier résultat en valeur absolue
                with ui.div(style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 5px;color: rgba(0, 0, 0, 0.6);font-size: 0.9em;line-height: 1.2;"):
                    ui.span(f"Valeur de référence : {reference}")
                    ui.span(f"Cible : {cible}")
                    ui.span(f"Valeur au dernier suivi : {resultat}")
                    ui.span(f"Suivi le : {date_resultat}")
                    ui.span(f"Échéance : {echeance}")
                
                # Ligne inférieure : La barre de progression fine
                with ui.div(style="width: 100%; background-color: #f0f0f0; height: 12px; border-radius: 4px; overflow: hidden;"):
                    ui.div(style=f"""
                        width: {val}%; 
                        background-color: #0aa6b6; 
                        height: 100%; 
                        border-radius: 4px;
                        transition: width 1s ease-in-out;
                    """)  

    ### SECTION 5. MILIEUX HUMIDES ET HYDRIQUES ###
    with ui.nav_panel("5. Milieux humides et hydriques"):
        df_MHH = df[df["Orientation"] == "5 - Éviter la destruction ou la dégradation de la qualité des milieux humides et hydriques"].copy()
        df_MHH["atteinte_cible_pct"] = pd.to_numeric(df_MHH["atteinte_cible_pct"], errors="coerce").fillna(0)
        icone_MHH = "🌿🦆"
        moyenne_MHH = int(df_MHH["atteinte_cible_pct"].mean())
        
        ui.HTML(f'''
            <div class="section-header">
            <br>
                <h2><b>{icone_MHH} Moyenne d'atteinte des objectifs pour cette orientation : {moyenne_MHH} %</b></h2>
            </div>
        ''')
        
        if moyenne_MHH > 70:
            ui.p("✅ Les objectifs sont en bonne voie d'être atteints.")
        elif moyenne_MHH > 30:
            ui.p("⚠️ Des efforts constants sont encore requis.")
        else:
            ui.p("🚨 Priorité élevée : phase de planification.")  
        
        ui.hr()
        ui.h4("Progression par objectif :", style="color: #0083cb; margin-bottom: 20px;")
        
        for _, row in df_MHH.iterrows():
            val = int(row["atteinte_cible_pct"])
            libelle = row["Libellé de l'objectif"]
            reference = row["Valeur(référence)"]
            resultat = row["Résultat"]
            date_resultat = row["Date du résultat"]
            echeance = row["Échéance"]
            cible = row["Cible - valeur numérique"]
            
            # Conteneur pour un seul objectif
            with ui.div(style="margin-bottom: 45px; padding: 0 10px;"):
                
                # Ligne supérieure : Libellé à gauche, Valeur à droite
                with ui.div(style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2.5px;"):
                    ui.span(libelle, style="font-weight: 600; color: #333; font-size: 0.95rem;")
                    ui.span(f"{val}%", style="font-weight: 600; color: #666; font-size: 0.9rem;")

                # Ligne médiane : Cible, dernier résultat et date du dernier résultat en valeur absolue
                with ui.div(style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 5px;color: rgba(0, 0, 0, 0.6);font-size: 0.9em;line-height: 1.2;"):
                    ui.span(f"Valeur de référence : {reference}")
                    ui.span(f"Cible : {cible}")
                    ui.span(f"Valeur au dernier suivi : {resultat}")
                    ui.span(f"Suivi le : {date_resultat}")
                    ui.span(f"Échéance : {echeance}")
                
                # Ligne inférieure : La barre de progression fine
                with ui.div(style="width: 100%; background-color: #f0f0f0; height: 12px; border-radius: 4px; overflow: hidden;"):
                    ui.div(style=f"""
                        width: {val}%; 
                        background-color: #0aa6b6; 
                        height: 100%; 
                        border-radius: 4px;
                        transition: width 1s ease-in-out;
                    """) 

