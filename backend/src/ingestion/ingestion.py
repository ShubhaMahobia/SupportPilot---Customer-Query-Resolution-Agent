from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from dotenv import load_dotenv
load_dotenv()
import re
import unicodedata
import unicodedata

import os

ARTIFACT_DIR = "./src/ingestion/artifacts"

os.makedirs(ARTIFACT_DIR, exist_ok=True)


def extract_text_from_url():

    try:

        loader = FireCrawlLoader(
            url="https://www.flipkart.com/pages/terms"
        )

        docs = loader.load()

        with open(
            f"{ARTIFACT_DIR}/raw_terms.txt",
            "w",
            encoding="utf-8"
        ) as f:

            for doc in docs:
                f.write(doc.page_content)
                f.write("\n")

        print("Terms and Condition extracted successfully")

    except Exception as e:
        print("Got an Error while fetching from internet")
        print("Error:", e)

def clean_text():

    try:
        text = ""

        with open(f"{ARTIFACT_DIR}/raw_terms.txt", "r", encoding="utf-8") as f:
            text = f.read()


        # Unicode normalization
        text = unicodedata.normalize("NFKC", text)

        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', '[LINK]', text)

        # Remove escaped slashes like \\\[
        text = re.sub(r'\\+', '', text)

        # Fix OCR hyphenation
        text = re.sub(r'-\n', '', text)

        # Normalize spaces/tabs
        text = re.sub(r'[ \t]+', ' ', text)

        # Reduce excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Remove trailing spaces
        text = re.sub(r' +\n', '\n', text)

        
        with open(f"{ARTIFACT_DIR}/clean.txt", "w", encoding="utf-8") as f:
            f.write(text)

    except FileNotFoundError:
        print("File not found please check the path again")
    
    except Exception as e:
        print("Some Error occured at cleaning the text")
        print("Error - ", e)



def main():

    print("=============TEXT EXTRACTION PIPELINE STARTED=======================")
    extract_text_from_url()
    clean_text()
    print("=============TEXT EXTRACTION PIPELINE ENDED==========================")

if __name__ == "__main__":
    main()