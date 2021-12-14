# ORCID Lookup Tool

### A very quick and dirty tool to see if email addresses are publicly associated with an ORCID

Steps to run script:
1. Clone/download repository
2. Navigate to folder
3. (Optionally) configure virtual env
`python3 -m venv env`
4. `pip install -r requirements.txt`
5. `python3 orcid_lookup.py email_list.csv`

The file `email_list.csv` should be a csv/text file, with one email address per row.
