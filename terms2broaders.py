import pandas as pd

#Needs 1 workbook named terms_need_broaders.xslx, which is the result of an OpenRefine action to obtain the parentsXML from the AAT URI attached to terms (Sheet1) and a Collections export (Sheet2). Sheet1, columns A-F (contain A; priref, B; term C; AAT-URI, D; AAT-ID only, E; Full AAT-parentXML, F; parsed XML to human readable form), Sheet2 columns A-C (A; priref, B; term, C; AAT-URI. Keep in mind that export must be of terms + URI with exact match only)

# Load the workbook and sheets
def process_excel(base_excel):
    # Read both sheets into dataframe
    sheet1 = pd.read_excel(base_excel, sheet_name='Sheet1')
    sheet2 = pd.read_excel(base_excel, sheet_name='Sheet2')

    # Ensure necessary columns exist
    required_sheet1_cols = {'B', 'F'}
    required_sheet2_cols = {'A', 'B', 'C'}
    
    if not required_sheet1_cols.issubset(sheet1.columns):
        raise ValueError("Sheet1 must contain columns B and F.")
    if not required_sheet2_cols.issubset(sheet2.columns):
        raise ValueError("Sheet2 must contain columns A, B, and C.")

    # Extract URIs from Sheet1 Column F
    def extract_uris(cell):
        if pd.isna(cell):
            return []
        return [entry.split('$')[1] for entry in cell.split(', ') if '$' in entry]

    sheet1['URIs'] = sheet1['F'].apply(extract_uris)

    # Match URIs exactly and include all matching terms from Sheet2
    def match_uris(uris):
        matches = []
        for uri in uris:
            matching_rows = sheet2.loc[sheet2['C'] == uri, ['A', 'B']]
            matches.extend([f"{row['A']}${row['B']}${uri}" for _, row in matching_rows.iterrows()])
        return matches

    sheet1['Matches'] = sheet1['URIs'].apply(match_uris)

    # Expand matches into separate columns
    max_matches = sheet1['Matches'].apply(len).max()
    for i in range(max_matches):
        sheet1[f'Match_{i+1}'] = sheet1['Matches'].apply(lambda x: x[i] if i < len(x) else None)

    # Drop intermediate columns and save the resulting dataframe
    result = sheet1.drop(columns=['URIs', 'Matches'])
    output_file = 'terms_with_matches.xlsx'
    result.to_excel(output_file, index=False)
    print(f"You've succesfully build a thesaurus! Output saved to {output_file}")

# Run the function
process_excel('terms_need_broaders.xlsx')
