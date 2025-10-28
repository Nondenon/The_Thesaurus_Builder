import pandas as pd
import requests
import xml.etree.ElementTree as ET
import re
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tqdm import tqdm

# ---------- Functions ----------

def extract_aat_id(uri):
    if pd.isna(uri):
        return None
    parts = uri.split('/aat/')
    return parts[1] if len(parts) == 2 else None


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
    """Return the first matching broader term (recordnr, term, URI) from ordered parent string."""
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
    """Return all matching parents in order as a single string."""
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

# ---------- Fetch AAT parent strings ----------
df['AAT_ID'] = df['URI'].apply(extract_aat_id)
parent_strings = []
print("Fetching parent strings from AAT...")
for aat_id in tqdm(df['AAT_ID'], desc="Processing AAT IDs"):
    parent_strings.append(get_aat_parentstring(aat_id))
df['AAT-parentstring'] = parent_strings

# Keep copy for hierarchy processing
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

# ---------- Match first broader term ----------
create_hierarchy['Broader_term'] = create_hierarchy['AAT-parentstring'].apply(
    lambda ps: match_first_broader_from_parentstring(ps, full_thesaurus)
)

# ---------- Build complete hierarchy ----------
create_hierarchy['Complete_hierarchy'] = create_hierarchy['AAT-parentstring'].apply(
    lambda ps: build_complete_hierarchy(ps, full_thesaurus)
)

# ---------- Separate sheets ----------
# Only show relevant columns for the main hierarchy sheet
full_hierarchy = create_hierarchy.loc[
    create_hierarchy['Broader_term'].notna(),
    ['recordnr', 'term', 'URI', 'AAT_ID', 'AAT-parentstring', 'Broader_term']
]

No_broader_match = create_hierarchy[
    (create_hierarchy['Broader_term'].isna()) &
    (create_hierarchy['URI'].str.startswith("http://vocab.getty.edu/aat/", na=False))
]

No_AAT_URI = create_hierarchy[
    create_hierarchy['URI'].isna() |
    (~create_hierarchy['URI'].str.startswith("http://vocab.getty.edu/aat/", na=False))
]

# ---------- Export to Excel ----------
output_file = 'thesaurus_with_hierarchy.xlsx'
with pd.ExcelWriter(output_file) as writer:
    full_hierarchy.to_excel(writer, sheet_name='full_hierarchy', index=False)
    No_broader_match.to_excel(writer, sheet_name='No_broader_match', index=False)
    No_AAT_URI.to_excel(writer, sheet_name='No_AAT_URI', index=False)
    create_hierarchy[['recordnr','term','URI','Complete_hierarchy']].to_excel(writer, sheet_name='complete_hierarchy', index=False)

print(f"\nYour thesaurus hierarchy has been built successfully! Output saved as {output_file}")
