import pandas as pd
from pathlib import Path
from datetime import date

# Configuration
ROOT = Path(__file__).parent
DATAFILE = ROOT / "suivi-des-objectifs_OBVFSJ.xlsx"
OUTDIR = ROOT / "docs"
OUTDIR.mkdir(parents=True, exist_ok=True)
today = date.today().strftime("%Y-%m-%d")

NAV_LINKS = [
    ("index.html", "Introduction"),
    ("orientation-1.html", "1. Qualité de l'eau"),
    ("orientation-2.html", "2. Eutrophisation des lacs"),
    ("orientation-3.html", "3. Espèces exotiques envahissantes"),
    ("orientation-4.html", "4. Habitats fauniques"),
    ("orientation-5.html", "5. Milieux humides et hydriques"),
]

ORIENTATIONS = {
    "1 - Éviter la dégradation de la qualité de l'eau": ("orientation-1.html", "💧🌊"),
    "2 - Ralentir l'eutrophisation des lacs": ("orientation-2.html", "🦠🏞️"),
    "3 - Limiter la prolifération des espèces exotiques envahissantes": ("orientation-3.html", "🌾🦪"),
    "4 - Freiner la perte d'habitat faunique": ("orientation-4.html", "🐟🦎"),
    "5 - Éviter la destruction ou la dégradation de la qualité des milieux humides et hydriques": ("orientation-5.html", "🌿🦆"),
}

BASE_CSS = """
body { font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; color: #222; margin: 18px; }
.header { display:flex; align-items:center; justify-content:space-between }
.header img { height:64px }
.nav { margin-top:12px; margin-bottom:20px }
.nav a { margin-right:12px; color:#0083cb; text-decoration:none; font-weight:600 }
.section-header { color:#0aa6b6; font-size:20px; font-weight:bold; margin-top:12px }
.card { border:1px solid #e6eef0; border-radius:6px; padding:12px; background:#fff; margin-bottom:18px }
.progress-bg { width:100%; background:#f0f0f0; height:12px; border-radius:4px; overflow:hidden }
.progress { height:100%; background:#0aa6b6; border-radius:4px }
.meta { color:#666; font-size:0.95rem }
"""


def nav_html(active_href):
    links = []
    for href, label in NAV_LINKS:
        cls = 'style="font-weight:700;"' if href == active_href else ''
        links.append(f'<a href="{href}" {cls}>{label}</a>')
    return '<div class="nav">' + '|  '.join(links) + '</div>'


def render_item(row):
    val = int(pd.to_numeric(row.get('atteinte_cible_pct', 0), errors='coerce') or 0)
    libelle = row.get('Libellé de l\'objectif', '')
    reference = row.get('Valeur(référence)', '')
    resultat = row.get('Résultat', '')
    date_resultat = row.get('Date du résultat', '')
    echeance = row.get('Échéance', '')
    cible = row.get('Cible - valeur numérique', '')

    html = f"""
    <div class="card">
      <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:6px;">
        <div style="font-weight:600">{libelle}</div>
        <div style="font-weight:600;color:#666">{val}%</div>
      </div>
      <div class="meta" style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:8px;"> 
        <div>Valeur de référence : {reference}</div>
        <div>Cible : {cible}</div>
        <div>Valeur au dernier suivi : {resultat}</div>
        <div>Suivi le : {date_resultat}</div>
        <div>Échéance : {echeance}</div>
      </div>
      <div class="progress-bg"><div class="progress" style="width:{val}%;"></div></div>
    </div>
    """
    return html


def build_page(title, body_html, active_href):
    return f"""
    <!doctype html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width,initial-scale=1">
      <title>{title}</title>
      <style>{BASE_CSS}</style>
    </head>
    <body>
      <div class="header">
        <div>
          <h1 style="margin:0">OBVFSJ - Suivi des objectifs du PDE 2024-2034</h1>
          <div class="meta">Dernière mise à jour : {today}</div>
        </div>
        <img src="https://obvfleuvestjean.com/wp-content/uploads/2026/01/LogoOBV_ContourBlanc.png" alt="Logo">
      </div>

      {nav_html(active_href)}

      <div>
        {body_html}
      </div>
    </body>
    </html>
    """


def main():
    # Load data exactly as the app does
    df = pd.read_excel(DATAFILE, sheet_name=1, header=1)
    df['atteinte_cible_pct'] = df['Pourcentage d\'atteinte de la cible'].astype(str).str.replace('%','', regex=False)
    df['atteinte_cible_pct'] = pd.to_numeric(df['atteinte_cible_pct'], errors='coerce').fillna(0)
    df['cible_pct'] = df['Cible en %'].astype(str).str.replace('%','', regex=False)

    # Index (Introduction)
    intro_html = """
    <hr><p>Bienvenue sur l'outil de suivi des objectifs du PDE 2024-2034 de l'<strong>Organisme de bassin versant du fleuve Saint-Jean</strong>. Ce tableau de bord présente l'état d'avancement des <strong>47 objectifs</strong> du PDE à travers les <strong>5 orientations</strong> qui ont été définies en concertation avec les acteurs de l'eau de la zone de gestion intégrée de l'eau du bassin versant du fleuve Saint-Jean.</p>
    <p>Pour de plus amples informations sur le territoire couvert par notre action collective, consultez la page suivante : <a href="https://obvfleuvestjean.com/un-bassin-versant-transfrontalier/">obvfleuvestjean.com/un-bassin-versant-transfrontalier/</a>.</p><hr>

    <div class="card">
      <h2 style="text-align:center;margin-top:0">Mission de l'OBVFSJ</h2>
      <p style="text-align:center;color:#555"><em>« Dans le bassin versant du fleuve Saint-Jean, le maintien d'écosystèmes intègres, source d'une excellente qualité d'eau, constitue la base d'un héritage bâti sur de saines relations transfrontalières »</em></p>
    </div>
    """

    (OUTDIR / 'index.html').write_text(build_page('Introduction', intro_html, 'index.html'), encoding='utf-8')

    # Build orientation pages
    for orientation, (filename, icon) in ORIENTATIONS.items():
        df_o = df[df['Orientation'] == orientation].copy()
        df_o['atteinte_cible_pct'] = pd.to_numeric(df_o['atteinte_cible_pct'], errors='coerce').fillna(0)
        moyenne = int(df_o['atteinte_cible_pct'].mean()) if len(df_o)>0 else 0

        body = f"<hr><div class=\"section-header\">{icon} Moyenne d'atteinte des objectifs pour cette orientation : {moyenne} %</div>"
        if moyenne > 70:
            body += "<p>✅ Les objectifs sont en bonne voie d'être atteints.</p>"
        elif moyenne > 30:
            body += "<p>⚠️ Des efforts constants sont encore requis.</p>"
        else:
            body += "<p>🚨 Priorité élevée : phase de planification.</p>"

        body += '<hr><h4><u>Progression par objectif :</u></h4>'
        for _, row in df_o.iterrows():
            body += render_item(row)

        (OUTDIR / filename).write_text(build_page(filename.replace('.html',''), body, filename), encoding='utf-8')

    # README with publish instructions
    readme = """
    # PDE static export

    Files generated in this folder are suitable for publishing with GitHub Pages (put the containing `pde-static/` folder in `docs/` or serve the whole `docs/`).

    To embed on your site (iframe):

    <iframe src="https://<your-github-username>.github.io/<repo-name>/pde-static/index.html" width="100%" height="900" frameborder="0"></iframe>

    Regenerate these files after you update `suivi-des-objectifs_OBVFSJ.xlsx` by running `python export_static.py`.
    """

    (OUTDIR / 'README.md').write_text(readme, encoding='utf-8')


if __name__ == '__main__':
    main()
