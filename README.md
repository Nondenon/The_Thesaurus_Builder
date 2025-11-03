## *Voor Nederlands [klik hier](#thesaurus-hierarchie-bouwer)*

# Thesaurus Hierarchy Builder

This Python script (terms2broaders.py) automatically builds a hierarchical thesaurus. It enriches your terms by fetching broader terms from the Art & Architecture Thesaurus (AAT) using your existing term database. The script works in two steps: first, you provide a subset of terms for which you want broader terms; then, you provide your full thesaurus to match these broader terms against. Each term in the output is assigned one broader term, ensuring a clean, hierarchical structure.
Note that all the example data is in Dutch but the script uses the URI's to match the data so it will work on terms in any language, as long as they are matched with their respective AAT entity.


## Requirements
- A database or spreadsheet with your thesaurus terms, each with a unique record number or ID.
- These terms must be aligned with the Art & Architecture Thesaurus (https://www.getty.edu/research/tools/vocabularies/aat/)
- Python 3.6 or higher installed.
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

1. Download Python from [python.org](https://www.python.org/downloads/).
2. During installation, **make sure to check "Add Python to PATH"** (Windows) so you can run Python from any terminal. The easiest folder to install Python in (especially when working from a corporate machine) is C:\Users\*<Your.Name>*\AppData\Local\Programs\Python\
3. Run Python in a command window: Windows: Navigate to the folder where your Python script is saved, Shift + Right-click → “Open PowerShell window here” or “Open Command Prompt here”. MacOS/Linux: Open Terminal and navigate to the folder containing your script using cd /path/to/folder.
4. Verify the installation:
   ```bash
   python --version

3.1 **Run .bat file and install the libraries automatically**
Download [run_terms2broaders.bat](https://github.com/Nondenon/The_Thesaurus_Builder/blob/main/run_terms2broaders.bat) and [terms2broaders.py](https://github.com/Nondenon/The_Thesaurus_Builder/blob/main/terms2broaders.py) from this Github repository and place them into *any* folder you like.
Double click `run_terms2broaders.bat` to automatically install the required Python libraries and run the script. Once the libraries are installed the .bat will only check if they are there and then run the script. This is the easiest way to do run this script, so if you are still a beginner with Python, or not interested in code at all, this is the file for you!

3.2 **Required Python libraries**  
   Install them with pip:  
   ```bash
   pip install requests pandas openpyxl tqdm
   ```
   If you are using a corporate laptop with restrictions, you can install the libraries locally with:
   ```bash
   python -m pip install requests pandas openpyxl tqdm
   ```


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

## Step 3: Place the Python script

1. Save `terms2broaders.py` in the folder where you installed you Python application in. 
2. Keep your CSV files in a known location.

## Step 4: Run the script

1. Navigate to the folder containing `terms2broaders.py`
2. Open a terminal (Windows) or terminal/command prompt (Mac/Linux) and type in the following command: 
   ```bash
   python terms2broaders.py

4. File picker windows will appear:

Select your **subset CSV** with a subset of the terms and URIs you want broader terms for. Once you have selected that file a progress bar will show how many IDs have been processed. The script will fetch AAT parent strings directly from the AAT service, for each term. Once it reaches 100% a new window will open:  

5. Now select your **full thesaurus CSV**. The script will match the **first broader term in order** that exists in your full thesaurus.


## Step 5: Output

The script creates an Excel file that you can find in your Python folder:

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

# Thesaurus Hierarchie Bouwer

Dit Python-script (terms2broaders.py) bouwt automatisch een hiërarchische thesaurus. Het verrijkt je termen door bredere termen op te halen uit de Art & Architecture Thesaurus (AAT) met behulp van je bestaande termendatabase. Het script werkt in twee stappen: eerst geef je een subset van termen waarvoor je bredere termen wilt; daarna geef je je volledige thesaurus om deze bredere termen tegen te matchen. Elke term in de output krijgt één bredere term toegewezen, zodat een schone hiërarchische structuur ontstaat.

Let op: alle voorbeeldgegevens zijn in het Nederlands, maar het script gebruikt de URI’s om te matchen. Het werkt dus met termen in elke taal, zolang ze gekoppeld zijn aan hun respectieve AAT-entiteit.

## Vereisten
- Een database of spreadsheet met je thesaurustermen, elk met een uniek recordnummer of ID.
- Deze termen moeten overeenkomen met de Art & Architecture Thesaurus (https://www.getty.edu/research/tools/vocabularies/aat/)
- Python 3.6 of hoger geïnstalleerd.
- Mogelijkheid om je termen vanuit de database naar een CSV-bestand te exporteren (gescheiden door een puntkomma ;).
- Internetverbinding (om bredere termen op te halen via de AAT-service).

### Wat is Python?
- Python is een programmeertaal.
- De Python-interpreter is het programma dat Python-code leest en uitvoert.
- Python kan draaien:
  - Interactief: commando’s regel voor regel typen.
  - Scripts: bestanden (.py) met meerdere commando’s die tegelijk worden uitgevoerd.

De terminal (Command Prompt, PowerShell of Mac/Linux Terminal) is hoe je met Python communiceert. Het vertelt Python welke commando’s of scripts uitgevoerd moeten worden.

## Stap 1: Python installeren
1. Download Python van https://www.python.org/downloads/.  
2. Tijdens de installatie, **zorg dat "Add Python to PATH" aangevinkt is** (Windows), zodat je Python vanaf elke terminal kunt starten.  
   De makkelijkste map om Python in te installeren (zeker op een werk-laptop) is C:\Users\*<Jouw.Naam>*\AppData\Local\Programs\Python\
3. Start Python in een commandovenster:  
   - Windows: navigeer naar de map waar je Python-script staat, Shift + Rechtsklik → “Open PowerShell window here” of “Open Command Prompt here”.  
   - MacOS/Linux: open Terminal en navigeer naar de map met je script met cd /pad/naar/map.
4. Controleer de installatie:
   ```bash
   python --version

3.1 **.bat-bestand uitvoeren en bibliotheken automatisch installeren**
Download [run_terms2broaders.bat](https://github.com/Nondenon/The_Thesaurus_Builder/blob/main/run_terms2broaders.bat) en [terms2broaders.py](https://github.com/Nondenon/The_Thesaurus_Builder/blob/main/terms2broaders.py) van deze Github-repository en plaats ze in *elke* map die je wilt.
Dubbelklik op `run_terms2broaders.bat` om automatisch de benodigde Python-bibliotheken te installeren en het script uit te voeren. Zodra de bibliotheken zijn geïnstalleerd, controleert de .bat alleen of ze aanwezig zijn en voert daarna het script uit. Dit is de gemakkelijkste manier om dit script te gebruiken, dus als je nog een beginner bent met Python, of helemaal niet in code geïnteresseerd bent, is dit het bestand voor jou!

3.2 **Benodigde Python-bibliotheken**  
   Installeer ze met pip:  
   ```bash
   pip install requests pandas openpyxl tqdm
   ```
   Als je een werk-laptop met beperkingen gebruikt, kun je de bibliotheken lokaal installeren met:
   ```bash
   python -m pip install requests pandas openpyxl tqdm
   ```

## Stap 2: Bereid je CSV-bestanden voor

### CSV 1: Bron-thesaurus (termen met AAT URI's)
Het is aanbevolen een subset van je termen te exporteren waarvoor je bredere termen wilt, in plaats van de volledige set. In dit voorbeeld is een subset van termen gerelateerd aan materialen gebruikt. 

- Vereiste kolommen zijn **recordnr, term, URI**  
- Je kunt extra kolommen toevoegen aan de .CSV, zoals bijvoorbeeld *domain* (als de term een materiaal, techniek, objecttype etc. is). Als deze ook in de volledige thesaurus .CSV worden toegevoegd, kan dit handig zijn om te controleren of de AAT-URI's die je eerder aan de termen hebt toegewezen daadwerkelijk in de juiste categorie/facet zitten.  
- Voorbeeld van vereiste kolommen:

| recordnr | term       | URI                               |
|-------------|-----------|----------------------------------|
| 16          | schilderij  | http://vocab.getty.edu/aat/300177435 |
| 117         | serviesgoed | http://vocab.getty.edu/aat/300236054 |

- Voorbeeld van vereiste + optionele kolommen:

| recordnr | term       | URI                               | domain |
|-------------|-----------|----------------------------------|-------------------|
| 16          | schilderij | http://vocab.getty.edu/aat/300177435 | objectnaam |
| 117         | serviesgoed | http://vocab.getty.edu/aat/300236054 | objectnaam |

- Zorg dat de eerste 3 kolommen `recordnr`, `term` en `URI` heten zoals in het voorbeeld hierboven.
- Zorg dat er *alleen* AAT-URI's in de URI-kolom staan. Als je ook andere URI's in je bronsysteem gebruikt, verwijder deze dan uit het .csv-bestand voordat je het Python-script start, anders geeft het een foutmelding.  
- Opslaan als **puntkomma-gescheiden CSV** (`.csv`) en UTF-8 gecodeerd.

### CSV 2: Volledige thesaurus
- Vereiste kolommen zijn **recordnr, term, URI**  
- Optionele kolommen zoals domain kun je toevoegen.  
- Zorg dat er *alleen* AAT-URI's in de URI-kolom staan.  
- Kan **alle termen** bevatten, inclusief de termen in CSV 1.  
- Opslaan als **puntkomma-gescheiden CSV** (`.csv`) en UTF-8 gecodeerd.

## Stap 3: Plaats het Python-script

1. Sla `terms2broaders.py` op in de map waarin je Python hebt geïnstalleerd.  
2. Bewaar je CSV-bestanden op een bekende locatie.

## Stap 4: Voer het script uit

1. Navigeer naar de map waarin `terms2broaders.py` staat  
2. Open een terminal (Windows) of terminal/command prompt (Mac/Linux) en typ het volgende commando:  
   ```bash
   python terms2broaders.py
   ```

3. Er verschijnen vensters om bestanden te kiezen:

Selecteer je **subset CSV** met de subset van termen en URI's waarvoor je bredere termen wilt. Zodra je het bestand hebt geselecteerd, verschijnt een voortgangsbalk die laat zien hoeveel IDs zijn verwerkt. Het script haalt direct AAT-parentstrings op van de AAT-service voor elke term. Zodra 100% is bereikt, opent er een nieuw venster.  

4. Selecteer nu je **volledige thesaurus CSV**. Het script matcht de **eerste bredere term in volgorde** die bestaat in je volledige thesaurus.

## Stap 5: Output

Het script maakt een Excel-bestand aan dat je kunt vinden in je Python-map:

Het bestand bevat **vier tabbladen**:

1. **matched_broaders** – Je termen met één bredere term gematcht **vanuit je eigen thesaurus, op basis van de AAT-hiërarchie**.  
2. **No_broader_match** – Termen met een AAT-URI maar **zonder bijpassende bredere term** in je volledige thesaurus.  
3. **No_AAT_URI** – Termen die **geen AAT-URI** hebben.  
4. **complete_hierarchy** – Je termen gematcht met meer dan één bredere term vanuit je eigen thesaurus. Ze staan in de correcte hiërarchische volgorde, in lijn met de AAT-hiërarchie.

## Aanvullende opmerkingen

- **Netwerkverbinding:** Een stabiele internetverbinding is vereist om gegevens van de AAT-service op te halen.  
- **Verwerkingstijd:** Afhankelijk van het aantal termen en de netwerksnelheid, daarom het advies om een subset van termen te gebruiken in plaats van je volledige lijst.  
- **Foutafhandeling:** Termen zonder geldige AAT-URI's worden correct verwerkt en gerapporteerd in het tabblad `No_AAT_URI`.  
- **CSV-formaat:** Zorg dat je CSV-bestanden puntkomma-gescheiden (`;`) en UTF-8 gecodeerd zijn.

