import csv
import requests
import sys

CSV_FILE = 'data/bioeco_list.csv'

# this is not working, URLs are giving SSL CERTIFICATE_VERIFY_FAILED errors e.g. bioecoocean.org
def check_urls(rows):
    bad_urls = []
    for row in rows:
        url = row['URL']
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print(f"URL returned status {response.status_code}: {url}")
                bad_urls.append(url)
            else:
                print(f"URL OK: {url}")
        except Exception as e:
            print(f"URL error: {url} ({e})")
            bad_urls.append(url)
    return bad_urls

def check_duplicates(rows, field):
    seen = set()
    dups = set()
    for row in rows:
        val = row[field]
        if val in seen:
            dups.add(val)
        else:
            seen.add(val)
    return dups

if __name__ == "__main__":
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Check for duplicate names and URLs
    dup_names = check_duplicates(rows, 'Project Name')
    dup_urls = check_duplicates(rows, 'URL')

    if dup_names:
        print("Duplicate Project Names found:")
        for name in dup_names:
            print(f"  {name}")

    if dup_urls:
        print("Duplicate URLs found:")
        for url in dup_urls:
            print(f"  {url}")

    # Check URLs
    #bad_urls = check_urls(rows)

    # Fail if any problems found
    if dup_names or dup_urls: #or bad_urls:
        with open("gh_alert.txt", "w", encoding="utf-8") as alert:
            alert.write("## :warning: Metadata List Issues Detected\n")
            if dup_names:
                alert.write("### Duplicate Project Names:\n")
                for name in dup_names:
                    alert.write(f"- {name}\n")
            if dup_urls:
                alert.write("### Duplicate URLs:\n")
                for url in dup_urls:
                    alert.write(f"- {url}\n")
            # if bad_urls:
            #     alert.write("### Bad URLs:\n")
            #     for url in bad_urls:
            #         alert.write(f"- {url}\n")
            alert.write("\n/cc @EliLawrence\n") 
        sys.exit(1)
    
