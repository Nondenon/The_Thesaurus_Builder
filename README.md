# Thesaurus Hierarchy Builder

This Python script (terms2broaders.py) automatically builds a hierarchical thesaurus. It enriches your terms by fetching broader terms from the Art & Architecture Thesaurus (AAT) using your existing term database. The script works in two steps: first, you provide a subset of terms for which you want broader terms; then, you provide your full thesaurus to match these broader terms against. Each term in the output is assigned one broader term, ensuring a clean, hierarchical structure.
Note that all the example data is in Dutch but the script uses the URI's to match the data so it will work on terms in any language, as long as they are matched with their respective AAT entity.


## Requirements
- A database or spreadsheet with your thesaurus terms, each with a unique record number or ID.
- These terms must be aligned with the Art & Architecture Thesaurus (https://www.getty.edu/research/tools/vocabularies/aat/)
- Python 3.6 or higher installed.
- Ability to export your terms from the database to a CSV file (semicolon ;-separated).
- Internet connection (to fetch broader terms from the AAT service).
- Python libraries: requests, pandas, openpyxl, tqdm.

### What is Python?

- Python is a programming language.
- The Python interpreter is the program that reads and executes Python code.
- Python can run:
  - **Interactively**: typing commands line by line.
  - **Scripts**: files (`.py`) containing multiple commands executed all at once.

The **terminal (Command Prompt, PowerShell, or Mac/Linux Terminal)** is how you communicate with Python. It tells Python to run commands or scripts.

## Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/).
2. During installation, **make sure to check "Add Python to PATH"** (Windows) so you can run Python from any terminal.
3. Run Python in a command window: Windows: Navigate to the folder where your Python script is saved, Shift + Right-click → “Open PowerShell window here” or “Open Command Prompt here”. MacOS/Linux: Open Terminal and navigate to the folder containing your script using cd /path/to/folder.
4. Verify the installation:
   ```bash
   python --version

3. **Required Python libraries**  
   Install them with pip:  
   ```bash
   pip install requests pandas openpyxl tqdm

## Step 2: Prepare your CSV files

### CSV 1: Source thesaurus (terms with AAT URIs)
It is recommended to export a subset of your terms that need broaders instead of the full set. In this example a subset of terms related to materials was used. 

- Columns required are **recordnr, term, URI**
- Example:

| recordnr | term       | URI                               |
|-------------|-----------|----------------------------------|
| 16          | painting  | http://vocab.getty.edu/aat/300177435 |
| 117         | tableware | http://vocab.getty.edu/aat/300236054 |

- Save as **semicolon-separated CSV** (`.csv`) and UTF-8 encoded.
### CSV 2: Full thesaurus
- Columns required are **recordnr, term, URI**
- Can include **all terms**, including the ones in CSV 1.  
- Save as **semicolon-separated CSV** (`.csv`) and UTF-8 encoded.

## Step 3: Place the Python script

1. Save `terms2broaders.py` in a folder you can easily access, e.g.:  
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

1. **full_hierarchy** – Your terms with one broader term matched **from your own thesaurus, based on the AAT hierarchy**.  
2. **No_broader_match** – Terms that have an AAT URI but **no matching broader term** in your full thesaurus.  
3. **No_AAT_URI** – Terms that **don’t have an AAT URI**.
4. **complete_hierarchy** - Your terms matched with more than one broader term from your own thesaurus. They are in the correct hierarchical order, in alignment with the AAT hierarchy.

## Additional Notes

- **Network Connection:** A stable internet connection is required to fetch data from the AAT service.  
- **Processing Time:** Depends on the number of terms and network speed, hence the suggestion to use a subset of terms instead of your full list.
- **Error Handling:** Terms without valid AAT URIs are handled accordingly and reported in the `No_AAT_URI` sheet.  
- **CSV Format:** Ensure your CSV files are semicolon-separated (`;`) and UTF-8 encoded.
