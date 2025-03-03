# The Thesaurus Builder
Building a thesaurus from pre-existing terms in your database.



- The Thesaurus Builder
  - [Build from existing terms](#build-from-existing-terms)
  - [Fix domains](#fix-domains)
  - [Terms without a broader but with AAT URI]
  - [Terms without a broader without AAT URI]

 ## Build from existing terms

How does it work?
Have an excel document. In Sheet1, in column F there are multiple concepts and URI's in one cell. They correspond to the value in the same row in column B. The concepts and URI's in the cells in column F are seperated by a [$]. Individual concepts and their URI's are seperated by a [ ,] (comma and space) 
Example: paintings by form$http://vocab.getty.edu/aat/300033638, paintings (visual works)$http://vocab.getty.edu/aat/300033618, etc etc. 

In Sheet2 I have a list of terms in column B and a list of URI's in column C. 

terms2broaders.py is a Python script that creates a new Excel document where columns A to F from Sheet1 are in, and the URI's from column F in Sheet1 are matched with the URI's in column C from Sheet2. If there is a match it must be returned in column G in the new Excel. If there is more than one match a new column must be added for each match.

THIS Needs 1 workbook named terms_need_broaders.xslx, which is the result of an OpenRefine action to obtain the parentsXML from the AAT URI attached to terms (Sheet1) and a Collections export (Sheet2). Sheet1, columns A-F (contain A; priref, B; term C; AAT-URI, D; AAT-ID only, E; Full AAT-parentXML, F; parsed XML to human readable form), Sheet2 columns A-C (A; priref, B; term, C; AAT-URI. Keep in mind that export must be of terms + URI with exact match only)

 ## Fix domains

 SOMETHING SOMETHING

 ## Terms with minus Broader but plus AAT URI

  SOMETHING SOMETHING

 ## Terms with minus Broader and minus AAT URI

  SOMETHING SOMETHING
