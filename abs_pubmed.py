from Bio import Entrez
import pandas as pd
import os

# Set the file name
csv_file = "pubmed.csv"

# Set your email
my_email = "example@example.com"

# Read CSV
df = pd.read_csv(csv_file)
Entrez.email = my_email

def get_abstract(pmid):
    try:
        print(f"Fetching abstract for PMID {pmid}...")  # Progress message

        handle = Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="xml")  # Use "xml"
        record = Entrez.read(handle)  # Read the XML response
        handle.close()  # Close the handle

        # Extract abstract safely
        abstract_data = record["PubmedArticle"][0]["MedlineCitation"]["Article"].get("Abstract", {}).get("AbstractText", [""])
        abstract = abstract_data[0] if abstract_data else "No abstract available"

        print(f"✅ Abstract added for PMID {pmid}")  # Success message
        return abstract
    
    except Exception as e:
        print(f"❌ Error fetching abstract for PMID {pmid}: {e}")
        return None

# Apply function to fetch abstracts
df["Abstract"] = df["PMID"].apply(get_abstract)

# Save output file
filename, ext = os.path.splitext(csv_file)
new_filename = filename + "_with_abstracts" + ext
df.to_csv(new_filename, index=False)

print(f"\n🚀 Process completed! File saved as: {new_filename}")
