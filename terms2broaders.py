import pandas as pd
import requests
import xml.etree.ElementTree as ET
import re
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tqdm import tqdm

# ---------- Functions ----------

def extract_aat_uri(uri_string):
    """Extracts a clean AAT URI from messy input (supports both /aat/ and /page/aat/)."""
    if not isinstance(uri_string, str):
        return None
    match = re.search(r'(https?://vocab\.getty\.edu(?:/page)?/aat/\d+)', uri_string)
    if match:
        return match.group(1)
    return None

def extract_aat_id(uri_string):
    """Extracts the AAT ID from a valid AAT URI."""
    clean_uri = extract_aat_uri(uri_string)
    if not clean_uri:
        return None
    match = re.search(r'/aat/(\d+)', clean_uri)
    return match.group(1) if match else None

def get_aat_parentstring(aat_id):
    if not aat_id:
        return ""
    url = f"http://vocabsservices.getty.edu/AATService.asmx/AATGetParents?subjectID={aat_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return ""
    try:
        root = ET.fromstring(response.content)
        parent_string_text_elem = root.find('.//Parent_String')
        if parent_string_text_elem is None or not parent_string_text_elem.text:
            return ""
        parent_string_text = parent_string_text_elem.text.strip()
        parents = []
        for item in parent_string_text.split(', '):
            match = re.match(r'(.+)\s\[(\d+)\]', item)
            if match:
                label = match.group(1)
                parent_id = match.group(2)
                uri = f"http://vocab.getty.edu/aat/{parent_id}"
                parents.append(f"{label}${uri}")
        return ', '.join(parents)
    except ET.ParseError:
        return ""

def match_first_broader_from_parentstring(parentstring, full_thesaurus):
    if pd.isna(parentstring) or not parentstring.strip():
        return None
    parents = [p.strip() for p in parentstring.split(', ')]
    for parent in parents:
        if '$' not in parent:
            continue
        label, uri = parent.split('$', 1)
        matching_rows = full_thesaurus.loc[full_thesaurus['URI'] == uri, ['recordnr', 'term']]
        if not matching_rows.empty:
            row = matching_rows.iloc[0]
            return f"{row['recordnr']}${row['term']}${uri}"
    return None

def build_complete_hierarchy(parentstring, full_thesaurus):
    if pd.isna(parentstring) or not parentstring.strip():
        return ""
    parents = [p.strip() for p in parentstring.split(', ')]
    matched_parents = []
    for parent in parents:
        if '$' not in parent:
            continue
        label, uri = parent.split('$', 1)
        matching_rows = full_thesaurus.loc[full_thesaurus['URI'] == uri, ['recordnr', 'term', 'URI']]
        if not matching_rows.empty:
            row = matching_rows.iloc[0]
            matched_parents.append(f"{row['recordnr']}${row['term']}${row['URI']}")
    return ', '.join(matched_parents)

def get_broader_domain(broader_str, full_thesaurus):
    """Return domain of the broader term from full thesaurus."""
    if pd.isna(broader_str):
        return None
    parts = broader_str.split('$')
    if len(parts) != 3:
        return None
    uri = parts[2]
    matching_row = full_thesaurus.loc[full_thesaurus['URI'] == uri, 'domain']
    if not matching_row.empty:
        return matching_row.iloc[0]
    return None

# ---------- Phase 1: Select source CSV ----------
Tk().withdraw()
source_file = askopenfilename(title="Select your source CSV (.csv) with AAT URIs", filetypes=[("CSV files", "*.csv")])
if not source_file:
    print("No file selected, script stops.")
    exit()

df = pd.read_csv(source_file, sep=';')
required_cols = ['recordnr', 'term', 'URI']
if not set(required_cols).issubset(df.columns):
    raise ValueError(f"CSV must contain columns: {required_cols}")

# Clean URIs and extract AAT IDs
df['Clean_URI'] = df['URI'].apply(extract_aat_uri)
df['AAT_ID'] = df['Clean_URI'].apply(extract_aat_id)

# ---------- Fetch AAT parent strings ----------
parent_strings = []
print("Fetching parent strings from AAT...")
for aat_id in tqdm(df['AAT_ID'], desc="Processing AAT IDs"):
    parent_strings.append(get_aat_parentstring(aat_id))
df['AAT-parentstring'] = parent_strings

create_hierarchy = df.copy()

# ---------- Phase 2: Select full thesaurus CSV ----------
full_file = askopenfilename(title="Select your full thesaurus CSV (.csv)", filetypes=[("CSV files", "*.csv")])
if not full_file:
    print("No file selected, script stops.")
    exit()

full_thesaurus = pd.read_csv(full_file, sep=';')
required_full_cols = ['recordnr', 'term', 'URI']
if not set(required_full_cols).issubset(full_thesaurus.columns):
    raise ValueError(f"CSV must contain columns: {required_full_cols}")

# Add 'domain' column if missing
if 'domain' not in full_thesaurus.columns:
    full_thesaurus['domain'] = None

# ---------- Match first broader term ----------
create_hierarchy['Broader_term'] = create_hierarchy['AAT-parentstring'].apply(
    lambda ps: match_first_broader_from_parentstring(ps, full_thesaurus)
)

# ---------- Add domain from matched broader ----------
create_hierarchy['domain'] = create_hierarchy['Broader_term'].apply(
    lambda x: get_broader_domain(x, full_thesaurus)
)

# ---------- Build complete hierarchy ----------
create_hierarchy['Complete_hierarchy'] = create_hierarchy['AAT-parentstring'].apply(
    lambda ps: build_complete_hierarchy(ps, full_thesaurus)
)

# ---------- Separate sheets ----------
base_cols = df.columns.tolist()
extra_cols = [c for c in create_hierarchy.columns if c not in base_cols]

# Matched broaders
matched_broaders_cols = base_cols + ['Broader_term', 'domain']
matched_broaders = create_hierarchy.loc[
    create_hierarchy['Broader_term'].notna(),
    [c for c in matched_broaders_cols if c in create_hierarchy.columns]
]

# No broader match (AAT only)
no_broader_cols = base_cols
No_broader_match = create_hierarchy.loc[
    (create_hierarchy['Broader_term'].isna()) &
    (create_hierarchy['Clean_URI'].notna()),
    [c for c in no_broader_cols if c in create_hierarchy.columns]
]

# No AAT URI — includes blanks, Wikidata, other vocabularies, or text
no_aat_cols = base_cols
No_AAT_URI = create_hierarchy.loc[
    (create_hierarchy['Clean_URI'].isna()) & (create_hierarchy['URI'].notna()),
    [c for c in no_aat_cols if c in create_hierarchy.columns]
]

# ---------- Export to Excel ----------
output_file = 'thesaurus_with_hierarchy.xlsx'
with pd.ExcelWriter(output_file) as writer:
    matched_broaders.to_excel(writer, sheet_name='matched_broaders', index=False)
    No_broader_match.to_excel(writer, sheet_name='No_broader_match', index=False)
    No_AAT_URI.to_excel(writer, sheet_name='No_AAT_URI', index=False)
    create_hierarchy.to_excel(writer, sheet_name='complete_hierarchy', index=False)

print(f"\n✅ Je thesaurus-hiërarchie is succesvol opgebouwd! Bestand opgeslagen als: {output_file}")
