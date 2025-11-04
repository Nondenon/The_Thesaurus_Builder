## *Voor Nederlands [klik hier](#thesaurus-hierarchiebouwer)*

# Thesaurus Hierarchy Builder

This Python script (terms2broaders.py) automatically builds a hierarchical thesaurus. It enriches your terms by fetching broader terms from the Art & Architecture Thesaurus (AAT) using your existing term database. The script works in two steps: first, you provide a subset of terms for which you want broader terms; then, you provide your full thesaurus to match these broader terms against. Each term in the output is assigned one broader term, ensuring a clean, hierarchical structure.
The script uses the URI's to match the data so it will work on terms in *any language*, as long as they are matched with their respective AAT entity.


## Requirements
- A database or spreadsheet with your thesaurus terms, each with a unique record number or ID.
- These terms must be aligned with the Art & Architecture Thesaurus (https://www.getty.edu/research/tools/vocabularies/aat/)
- Python 3.6 or higher installed.
- Python libraries:
   ```bash
   pip install requests pandas openpyxl tqdm
   ```
   Or, if you are using a corporate laptop with restrictions, you can install the libraries locally with:
   ```bash
   python -m pip install requests pandas openpyxl tqdm
   ```
- Ability to export your terms from the database to a CSV file (semicolon ;-separated).
- Internet connection (to fetch broader terms from the AAT service).

### What is Python?

- Python is a programming language.
- The Python interpreter is the program that reads and executes Python code.
- Python can run:
  - **Interactively**: typing commands line by line.
  - **Scripts**: files (`.py`) containing multiple commands executed all at once.

The **terminal (Command Prompt, PowerShell, or Mac/Linux Terminal)** is how you communicate with Python. It tells Python to run commands or scripts.

## Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/). Make sure to download **the standalone version**
2. During installation, **make sure to check "Add Python to PATH"** (Windows) so you can run Python from any terminal. The easiest folder to install Python in (especially when working from a corporate machine) is C:\Users\*<Your.Name>*\AppData\Local\Programs\Python\
3. Run Python in a command window: Windows: Navigate to the folder where your Python script is saved, Shift + Right-click → “Open PowerShell window here” or “Open Command Prompt here”. MacOS/Linux: Open Terminal and navigate to the folder containing your script using cd /path/to/folder.
4. Verify the installation:
   ```bash
   python --version

## Step 2: Prepare your CSV files

### CSV 1: Source thesaurus (terms with AAT URIs)
It is recommended to export a subset of your terms that need broaders instead of the full set. In this example a subset of terms related to materials was used. 

- Columns required are **recordnr, term, URI**
- You can add more columns to the .CSV, like, for instance, *domain* (if the term is a material, technique, objecttype etc). which, if also added to the full thesaurus .CSV file, can be useful if you want to check if the AAT URI's you have previously assigned to the terms are actually in the correct facet.
- Example of required columns:

| recordnr | term       | URI                               |
|-------------|-----------|----------------------------------|
| 16          | painting  | http://vocab.getty.edu/aat/300177435 |
| 117         | tableware | http://vocab.getty.edu/aat/300236054 |

- Example of required + optional columns:

| recordnr | term       | URI                               | domain |
|-------------|-----------|----------------------------------|-------------------|
| 16          | painting  | http://vocab.getty.edu/aat/300177435 | object_name |
| 117         | tableware | http://vocab.getty.edu/aat/300236054 | object_name |

- Make sure the first 3 columns are named `recordnr`, `term` and `URI` like in the example above.
- Make sure there are *only* AAT-URI's in the URI column. If you also use other URI's in your souce system, please remove them from the .csv file before starting the Python script, otherwise it will return an error.
- Save as **semicolon-separated CSV** (`.csv`) and UTF-8 encoded.
### CSV 2: Full thesaurus
- Columns required are **recordnr, term, URI**
- You can add optional columns like domains.
- Make sure there are *only* AAT-URI's in the URI column.
- Can include **all terms**, including the ones in CSV 1.  
- Save as **semicolon-separated CSV** (`.csv`) and UTF-8 encoded.
- Keep your CSV files in a known location.

## Step 3: Run the Python script and install the required libraries automatically
- Download [run_terms2broaders.bat](https://github.com/Nondenon/The_Thesaurus_Builder/blob/main/run_terms2broaders.bat) and [terms2broaders.py](https://github.com/Nondenon/The_Thesaurus_Builder/blob/main/terms2broaders.py) from this Github repository and place them into *any* folder you like.
- Double click `run_terms2broaders.bat` to automatically install the required Python libraries and run the script.
- Once the libraries are installed the .bat will only check if they are there and then run the script.
- **This is the easiest way to do run this script, so if you are still a beginner with Python, or not interested in code at all, this is the file for you!**

## Step 4: Operating the script
File picker windows will appear to ask for your .CSV-file. Now Select your **subset CSV** with a subset of the terms and URIs you want broader terms for. Once you have selected that file a progress bar will show how many IDs have been processed. The script will fetch AAT parent strings directly from the AAT service, for each term. Once it reaches 100% a new window will open:  

Now select your **full thesaurus CSV**. The script will match the **first broader term in order** that exists in your full thesaurus.

## Step 5: Output

After running the script, an Excel file will be created in the same folder as your Python script:

It contains **four sheets**:

1. **matched_broaders** – Your terms with one broader term matched **from your own thesaurus, based on the AAT hierarchy**.  
2. **No_broader_match** – Terms that have an AAT URI but **no matching broader term** in your full thesaurus.  
3. **No_AAT_URI** – Terms that **don’t have an AAT URI**.
4. **complete_hierarchy** - Your terms matched with more than one broader term from your own thesaurus. They are in the correct hierarchical order, in alignment with the AAT hierarchy.

## Additional Notes

- **Network Connection:** A stable internet connection is required to fetch data from the AAT service.  
- **Processing Time:** Depends on the number of terms and network speed, hence the suggestion to use a subset of terms instead of your full list.
- **Error Handling:** Terms without valid AAT URIs are handled accordingly and reported in the `No_AAT_URI` sheet.  
- **CSV Format:** Ensure your CSV files are semicolon-separated (`;`) and UTF-8 encoded.

*Nederlandse versie:*

# Thesaurus Hierarchiebouwer

Dit Python-script (terms2broaders.py) bouwt automatisch een hiërarchische thesaurus. Het verrijkt je termen door bredere termen op te halen uit de Art & Architecture Thesaurus (AAT) met behulp van je bestaande termendatabase. Het script werkt in twee stappen: eerst geef je een subset van termen op waarvoor je bredere termen wilt; daarna geef je je volledige thesaurus om deze bredere termen tegen te matchen. Elke term in de output krijgt één bredere term toegewezen, wat zorgt voor een nette hiërarchische structuur.
Het script gebruikt de URI's om de data te matchen, dus het werkt voor termen in *elke taal*, zolang ze gekoppeld zijn aan de juiste AAT-entiteit.

## Vereisten
- Een database of spreadsheet met je thesaurustermen, elk met een uniek recordnummer of ID.
- Deze termen moeten afgestemd zijn op de Art & Architecture Thesaurus (https://www.getty.edu/research/tools/vocabularies/aat/)
- Python 3.6 of hoger geïnstalleerd.
- Mogelijkheid om je termen uit de database te exporteren naar een CSV-bestand (puntkomma ;-gescheiden).
- Internetverbinding (om bredere termen op te halen van de AAT-service).

### Wat is Python?

- Python is een programmeertaal.
- De Python-interpreter is het programma dat Python-code leest en uitvoert.
- Python kan draaien:
  - **Interactief**: commando’s regel voor regel typen.
  - **Scripts**: bestanden (`.py`) met meerdere commando’s die in één keer uitgevoerd worden.

De **terminal (Command Prompt, PowerShell, of Mac/Linux Terminal)** is hoe je communiceert met Python. Hiermee geef je Python opdrachten of laat je scripts uitvoeren.

## Stap 1: Installeer Python

1. Download Python van [python.org](https://www.python.org/downloads/).
2. Vink tijdens de installatie **"Add Python to PATH"** aan (Windows), zodat je Python vanuit elke terminal kunt draaien. De makkelijkste map om Python in te installeren (vooral op een werkcomputer) is C:\Users\*<Je.Naam>*\AppData\Local\Programs\Python\
3. Start Python in een commandovenster: Windows: Navigeer naar de map waar je Python-script is opgeslagen, Shift + Rechtsklik → “Open PowerShell window here” of “Open Command Prompt here”. MacOS/Linux: Open Terminal en navigeer naar de map met je script met cd /pad/naar/map.
4. Controleer de installatie:
   ```bash
   python --version
   ```
### Nu kun je ofwel de vereiste Python-libraries handmatig installeren *of* gewoon [run_terms2broaders.bat](https://github.com/Nondenon/The_Thesaurus_Builder/blob/main/run_terms2broaders.bat) uitvoeren om ze automatisch te installeren. Meer info [hier](#stap-31-voer-het-python-script-uit-en-installeer-de-vereiste-libraries-automatisch)

5.1 **Installeer de vereiste Python-libraries handmatig**  
   Installeer ze met pip:  
   ```bash
   pip install requests pandas openpyxl tqdm
   ```
   Als je een werk-laptop met restricties gebruikt, kun je de libraries lokaal installeren met:
   ```bash
   python -m pip install requests pandas openpyxl tqdm
   ```

5.2 **Voer het .bat-bestand uit en installeer de libraries automatisch**
Ga [hier voor meer info](#stap-31-voer-het-python-script-uit-en-installeer-de-vereiste-libraries-automatisch).

## Stap 2: Bereid je CSV-bestanden voor

### CSV 1: Bron-thesaurus (termen met AAT-URI's)
Het is aanbevolen om een subset van je termen te exporteren waarvoor je bredere termen nodig hebt in plaats van de volledige set. In dit voorbeeld werd een subset van termen gerelateerd aan materialen gebruikt. 

- Vereiste kolommen zijn **recordnr, term, URI**
- Je kunt meer kolommen toevoegen aan de .CSV, bijvoorbeeld *domain* (als de term een materiaal, techniek, objecttype etc. is). Als deze ook in de volledige thesaurus .CSV aanwezig is, kan dit handig zijn om te controleren of de AAT-URI's die je eerder aan de termen hebt gekoppeld daadwerkelijk in de juiste categorie vallen.
- Voorbeeld van vereiste kolommen:

| recordnr | term       | URI                               |
|-------------|-----------|----------------------------------|
| 16          | painting  | http://vocab.getty.edu/aat/300177435 |
| 117         | tableware | http://vocab.getty.edu/aat/300236054 |

- Voorbeeld van vereiste + optionele kolommen:

| recordnr | term       | URI                               | domain |
|-------------|-----------|----------------------------------|-------------------|
| 16          | painting  | http://vocab.getty.edu/aat/300177435 | object_name |
| 117         | tableware | http://vocab.getty.edu/aat/300236054 | object_name |

- Zorg dat de eerste 3 kolommen `recordnr`, `term` en `URI` heten zoals in het voorbeeld hierboven.
- Zorg dat er *alleen* AAT-URI's in de URI-kolom staan. Als je ook andere URI's in je bronbestand gebruikt, verwijder deze dan uit de .csv voordat je het Python-script start, anders geeft het script een foutmelding.
- Sla op als **puntkomma-gescheiden CSV** (`.csv`) en UTF-8 gecodeerd.
### CSV 2: Volledige thesaurus
- Vereiste kolommen zijn **recordnr, term, URI**
- Je kunt optionele kolommen toevoegen, zoals domains.
- Zorg dat er *alleen* AAT-URI's in de URI-kolom staan.
- Kan **alle termen** bevatten, inclusief de termen uit CSV 1.  
- Sla op als **puntkomma-gescheiden CSV** (`.csv`) en UTF-8 gecodeerd.
- Bewaar je CSV-bestanden op een bekende locatie.

## Stap 3.1: Voer het Python-script uit en installeer de vereiste libraries automatisch
- Download [run_terms2broaders.bat](https://github.com/Nondenon/The_Thesaurus_Builder/blob/main/run_terms2broaders.bat) en [terms2broaders.py](https://github.com/Nondenon/The_Thesaurus_Builder/blob/main/terms2broaders.py) uit deze Github-repository en plaats ze in *een* map naar keuze.
- Dubbelklik op `run_terms2broaders.bat` om automatisch de vereiste Python-libraries te installeren en het script uit te voeren.
- Zodra de libraries geïnstalleerd zijn, zal het .bat-bestand alleen controleren of ze aanwezig zijn en het script uitvoeren.
- **Dit is de makkelijkste manier om het script uit te voeren. Als je nog een beginner bent met Python of helemaal geen interesse hebt in code, is dit het bestand voor jou!**

## Stap 3.2: Voer het script zelf uit vanuit de command prompt
- Sla `terms2broaders.py` op in de map waar je Python-applicatie is geïnstalleerd.
- Navigeer naar de map met `terms2broaders.py`
- Open een terminal (Windows) of terminal/command prompt (Mac/Linux) en typ het volgende commando om het script uit te voeren: 
   ```bash
   python terms2broaders.py
   ```
## Stap 4: Het script gebruiken
Er verschijnen vensters om je .CSV-bestand te selecteren. Kies nu je **subset CSV** met de subset van termen en URI's waarvoor je bredere termen wilt. Zodra je dat bestand hebt geselecteerd, verschijnt een voortgangsbalk die laat zien hoeveel ID's zijn verwerkt. Het script haalt voor elke term direct de AAT-parentstrings op van de AAT-service. Zodra het 100% bereikt, opent er een nieuw venster:  

Selecteer nu je **volledige thesaurus CSV**. Het script matcht de **eerste bredere term in volgorde** die in je volledige thesaurus voorkomt.

## Stap 5: Output

Na het uitvoeren van het script wordt een Excel-bestand aangemaakt in dezelfde map als je Python-script:

Het bevat **vier sheets**:

1. **matched_broaders** – Je termen met één bredere term gematcht **vanuit je eigen thesaurus, op basis van de AAT-hiërarchie**.  
2. **No_broader_match** – Termen die een AAT-URI hebben maar **geen overeenkomende bredere term** in je volledige thesaurus.  
3. **No_AAT_URI** – Termen die **geen AAT-URI** hebben.
4. **complete_hierarchy** - Je termen gematcht met meer dan één bredere term vanuit je eigen thesaurus. Ze staan in de juiste hiërarchische volgorde, in lijn met de AAT-hiërarchie.

## Extra opmerkingen

- **Netwerkverbinding:** Een stabiele internetverbinding is nodig om gegevens op te halen van de AAT-service.  
- **Verwerkingstijd:** Afhankelijk van het aantal termen en de netwerksnelheid, vandaar de aanbeveling om een subset van termen te gebruiken in plaats van de volledige lijst.
- **Foutafhandeling:** Termen zonder geldige AAT-URI's worden correct afgehandeld en gerapporteerd in de sheet `No_AAT_URI`.  
- **CSV-formaat:** Zorg dat je CSV-bestanden puntkomma-gescheiden (`;`) en UTF-8 gecodeerd zijn.

