import csv
from random import randint
from time import sleep
import chardet
import locale

import requests
import untangle


def guess_file_encoding(input_file, verbose=False):
    with open(input_file, "rb") as f:
        rawdata = f.read()
        enc = chardet.detect(rawdata)
        if verbose:
            print(f'Guess on encoding of {input_file}: {enc["encoding"]}')
    return enc["encoding"]


input_file = "emails.csv"

emails = []
enc = guess_file_encoding(input_file)
with open(input_file, "r", encoding=enc) as emf:
    for r in csv.reader(emf):
        emails.append(r[0])

# TODO: check emails for: 1) spaces, 2) quotation marks, 3) new lines

url = "https://pub.orcid.org/v3.0/search/?q=email:"

print(f"Checking {len(emails)} email addresses for ORCIDs.")

with open("matches.csv", "a+", encoding=locale.getpreferredencoding()) as mf, open(
    "not_matched.csv", "a+", encoding=locale.getpreferredencoding()
) as nmf:
    mw = csv.writer(mf)
    nmw = csv.writer(nmf)

    count = 0
    for email in emails:
        print(f"Checking {email}...")
        r_url = url + email
        r = requests.get(r_url)
        obj = untangle.parse(r.text)

        try:
            obj.search_search["num-found"]
        except:
            print(r.text)
            break

        if int(obj.search_search["num-found"]) > 0:
            orcid = (
                obj.search_search.search_result.common_orcid_identifier.common_path.cdata
            )
            mw.writerow((email, orcid))
            mf.flush()
            print("\tORCID found.")
        else:
            nmw.writerow([email])

        sleep(0.1)
        count += 1
        if (count % 100) == 0:
            print()
            print(
                f"Checked {count} email addresses. {round(count/len(emails)*100,2)}% complete."
            )
            print()

print("Complete")
print(f"Checked {count} emails")
