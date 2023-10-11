"""
Tímhle skriptem se vytvoří základní jazyky pro Slovník.
Nevytvoří to duplicitní system_names
"""

languages = [
    {"system_name": "czech", "display_name": "Čeština"},
    {"system_name": "german", "display_name": "Deutsch"},
    {"system_name": "english", "display_name": "English"},
    {"system_name": "french", "display_name": "Français"},
    {"system_name": "spanish", "display_name": "Español"},
    {"system_name": "italian", "display_name": "Italiano"},
    {"system_name": "portuguese", "display_name": "Português"},
    {"system_name": "dutch", "display_name": "Nederlands"},
    {"system_name": "polish", "display_name": "Polski"},
    {"system_name": "hungarian", "display_name": "Magyar"},
    {"system_name": "romanian", "display_name": "Română"},
    {"system_name": "greek", "display_name": "Ελληνικά"},
    {"system_name": "turkish", "display_name": "Türkçe"},
    {"system_name": "croatian", "display_name": "Hrvatski"},
    {"system_name": "slovak", "display_name": "Slovenčina"},
    {"system_name": "slovenian", "display_name": "Slovenščina"},
    {"system_name": "serbian", "display_name": "Српски"},
    {"system_name": "latin", "display_name": "Latina"},
    {"system_name": "dane", "display_name": "Dansk"},
    {"system_name": "swedish", "display_name": "Svenska"}
]


from website import create_app
from website.models.language import Language


app = create_app()
with app.app_context():
    for l in languages:
        if not Language.get_by_system_name(l["system_name"]):
            la = Language(system_name = l["system_name"], display_name = l["display_name"])
            la.update()
        else:
            print(f"Skipping {l}")
    
    print("done!")