# The Thesaurus Builder
Building a thesaurus from pre-existing terms in your database.



- The Thesaurus Builder
  - [Build from existing terms](#build-from-existing-terms) _using terms2broaders.py_ 
  - [Fix domains](#fix-domains)
  - [Terms without a broader but with AAT URI]
  - [Terms without a broader without AAT URI]
  - [Resolve a hierarchy...] with resolve_hierarchy.py
  - [Validate domains] with validate_domains.py

 ## Build from existing terms
You need:
- database with list of terms + their AAT URI's
- OpenRefine
- Python
- Excel

### Why use this?
If you manage a list of terms in a database management system—such as a museum collection management system—you might have enriched these terms with URIs from the [Art & Architecture Thesaurus (AAT)](https://vocab.getty.edu/sparql). However, your database may not include the hierarchical relationships between these terms.  

The script **terms2broaders.py** helps reconstruct these relationships by identifying broader terms already present in your database. Here’s how it works:  

1. **Extracting Parent URIs from AAT**  
   - Using OpenRefine, you have resolved your existing AAT URIs to retrieve their broader terms from the AAT hierarchy.  
   - Each term now has a corresponding list of broader term URIs extracted from AAT.  

2. **Matching Broader Terms to Your Existing Database**  
   - The script compares these broader term URIs to the URIs already stored in your database.  
   - If a match is found, the corresponding broader term is suggested as a hierarchical parent.  

### Why is this useful?  
- It helps **rebuild thesaurus relationships** using only the terms already in your system.  
- You don’t need to **add new terms manually**—instead, you can link existing ones.  
- It ensures your database remains **consistent and structured** without introducing unnecessary duplicates.  

In short, **terms2broaders.py** identifies and assigns broader terms to existing terms in your database, saving time and improving thesaurus integration.  

### How does it work?
To start you have to have a list of terms that are already aligned with the [Art & Architecture Thesaurus](https://vocab.getty.edu/sparql). Just a list of terms + their URI is enough. Keep in mind that you want to export a recordnumber/documentnumber/priref/whatever from you database in order to later be able to import the broader terms.

Run the list through OpenRefine to resolve the broader terms. Make sure to have a column with the *ID ONLY* (exclude the prefix). Use this GREL on that column (Add column by fetching URL's):

`'http://vocabsservices.getty.edu/AATService.asmx/AATGetParents?subjectID='+value`

Depending on the amount of terms this may take a while. It will return a XML with all the parents, grandparents, great-grandparents etc. that are above the term ID that you used to resolve these parents (so; there are no children here...)
Turn it into something human readable with Add column based on this column, GREL must be:

`value.parseXml().select('Preferred_Parent')[0].select('Parent_String')[0].ownText()`

Export to .xslx
The last column with the human-readable parent structure must be changed from (example):

```sets (groups) [300133146], object groupings by general context [300241508], object groupings [300241507], Object Groupings and Systems (hierarchy name) [300241489], Objects Facet [300264092]```

into:

```sets (groups)$http://vocab.getty.edu/aat/300133146, object groupings by general context$http://vocab.getty.edu/aat/300241508, object groupings$http://vocab.getty.edu/aat/300241507, Object Groupings and Systems (hierarchy name)$http://vocab.getty.edu/aat/300241489, Objects Facet$http://vocab.getty.edu/aat/300264092```

So be sure to have the full URI there, with the prefix and use [$] as a seperator between term and URI and [, ] (comma space) as a seperator between parents.

Now you have an excel document. In Sheet1 must be the result of your OpenRefine action. Must hold columns A-F (see example below) in column F there are multiple concepts and URI's in one cell. They are the parents to the value in the same row in column B. The concepts and URI's in the cells in column F are seperated by a [$]. Individual concepts and their URI's are seperated by a [ ,] (comma and space) 
Example: 
```paintings by form$http://vocab.getty.edu/aat/300033638, paintings (visual works)$http://vocab.getty.edu/aat/300033618, etc etc.```

Now make an export of the entire list of terms + their AAT URI's from your database. Export recordnumber, term, AAT-URI. (3 columns). Name them A-B-C. Place these in the same Excel workbook in Sheet2. URI's must be in column C. 

You now have 1 Excel workbook with 2 Sheets. Name this workbook **terms_need_broaders.xslx**

So, to conclude, this action requires 1 workbook named terms_need_broaders.xslx, which is the result of an OpenRefine action to obtain the parentsXML from the AAT URI attached to terms (Sheet1) and a Collections export (Sheet2). Sheet1, columns A-F (contain A; priref, B; term C; AAT-URI, D; AAT-ID only, E; Full AAT-parentXML, F; parsed XML to human readable form), Sheet2 columns A-C (A; priref, B; term, C; AAT-URI. Keep in mind that export must be of terms + URI with exact match only)

*terms2broaders.py* is a Python script that creates a new Excel document where all the URI's from column F in Sheet1 are compared to all the URI's in column C from Sheet2 ([Sheet1]F:F => [Sheet2]C:C [<- that is not an Excel formula]). If there is a match it must be returned in column G in the new Excel that the Python script will create. In cell F of Sheet1 there will me more than 1 URI, so it is likely that more than 1 match will come from this action. If so a new column is added. This is your hierarchical tree structure that is created from terms that you allready had in your database. Thus it automatically creates a thesaurus. 

The example terms here are in Dutch but this works on ANY LANGUAGE(!) because it only looks at the URI's to match, not the strings.

Example Sheet1
| A | B | C | D | E | F |
|----------|----------|----------|----------|----------|----------|
| 16   | schilderij  | http://vocab.getty.edu/aat/300177435   | 300177435   | XML export from OpenRefine   | paintings by form$http://vocab.getty.edu/aat/300033638, paintings (visual works)$http://vocab.getty.edu/aat/300033618, visual works by material or technique$http://vocab.getty.edu/aat/300191091, visual works (works)$http://vocab.getty.edu/aat/300191086, Visual Works (hierarchy name)$http://vocab.getty.edu/aat/300179869, Visual and Verbal Communication (hierarchy name)$http://vocab.getty.edu/aat/300264552, Objects Facet$http://vocab.getty.edu/aat/300264092   |
| 117   | serviesgoed   | http://vocab.getty.edu/aat/300236054   | 300236054   | XML export from OpenRefine   | sets (groups)$http://vocab.getty.edu/aat/300133146, object groupings by general context$http://vocab.getty.edu/aat/300241508, object groupings$http://vocab.getty.edu/aat/300241507, Object Groupings and Systems (hierarchy name)$http://vocab.getty.edu/aat/300241489, Objects Facet$http://vocab.getty.edu/aat/300264092   |
| 154   | persoonlijk object   | http://vocab.getty.edu/aat/300238982   | 300238982   | XML export from OpenRefine   | equipment by context$http://vocab.getty.edu/aat/300239170, equipment$http://vocab.getty.edu/aat/300122241, Tools and Equipment (hierarchy name)$http://vocab.getty.edu/aat/300022238, Furnishings and Equipment (hierarchy name)$http://vocab.getty.edu/aat/300264551, Objects Facet$http://vocab.getty.edu/aat/300264092   |
| 155   | servetring   | http://vocab.getty.edu/aat/300043085   | 300043085   | XML export from OpenRefine   | accessory containers for food service$http://vocab.getty.edu/aat/300198761, containers for serving and consuming food$http://vocab.getty.edu/aat/300198760, culinary containers$http://vocab.getty.edu/aat/300197577, containers by function or context$http://vocab.getty.edu/aat/300197200, containers (receptacles)$http://vocab.getty.edu/aat/300197197, Containers (hierarchy name)$http://vocab.getty.edu/aat/300045611, Furnishings and Equipment (hierarchy name)$http://vocab.getty.edu/aat/300264551, Objects Facet$http://vocab.getty.edu/aat/300264092   |

Example Sheet2
| A | B | C |
|----------|----------|----------|
| 1   | bord  | http://vocab.getty.edu/aat/300042991   |
| 6   | diepte   | http://vocab.getty.edu/aat/300072633   |
| 13   | schenking   | http://vocab.getty.edu/aat/300138913   |
| 16   | schilderij   | http://vocab.getty.edu/aat/300177435   |



 ## Fix domains

 SOMETHING SOMETHING

 ## Terms with minus Broader but plus AAT URI

  SOMETHING SOMETHING

 ## Terms with minus Broader and minus AAT URI

  SOMETHING SOMETHING
