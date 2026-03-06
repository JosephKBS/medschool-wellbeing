import os

import pandas as pd

from .config import DATA_DIR, DELAY_BETWEEN_SCHOOLS_LOW, DELAY_BETWEEN_SCHOOLS_HIGH
from .url_utils import extract_url_from_text
from .scraper import extract_sub_websites, extract_page_text, smart_delay
from .text_cleaning import clean_text


def load_university_list(csv_path=None):
    """Load and normalize the university list CSV.

    Handles both column naming conventions:
    - 'Medical School Name' / 'Website Address' (semicolon-separated)
    - 'Medical_School' / 'Website' (comma-separated)
    """
    if csv_path is None:
        csv_path = os.path.join(DATA_DIR, "med_list.csv")

    # Try semicolon-separated first (original format)
    df = pd.read_csv(csv_path, sep=";")
    if "Medical School Name" in df.columns:
        df = df.rename(columns={
            "Medical School Name": "Medical_School",
            "Website Address": "Website",
        })
    df = df[["Medical_School", "Website"]].dropna().reset_index(drop=True)
    # Clean URLs
    df["Website"] = df["Website"].apply(extract_url_from_text)
    return df


def collect_all_subpages(df, num=None):
    """Step 1: Discover subpages for all universities.

    Parameters
    ----------
    df : DataFrame
        Input DataFrame with Medical_School and Website columns.
    num : int or None
        If specified, randomly sample *num* universities from df.
        If None (default), process all universities.

    Returns a DataFrame with columns: Medical_School, Website, Subpage_URL
    """
    if num is not None:
        df = df.sample(n=min(num, len(df)), random_state=None).reset_index(drop=True)

    rows = []
    total = len(df)
    for idx, row in df.iterrows():
        school = row["Medical_School"]
        url = row["Website"]
        print(f"[{idx + 1}/{total}] {school}: discovering subpages...")
        try:
            subpages = extract_sub_websites(url)
            for sub_url in subpages:
                rows.append({
                    "Medical_School": school,
                    "Website": url,
                    "Subpage_URL": sub_url,
                })
            print(f"  Found {len(subpages)} subpages")
        except Exception as e:
            print(f"  Error: {e}")
        smart_delay(DELAY_BETWEEN_SCHOOLS_LOW, DELAY_BETWEEN_SCHOOLS_HIGH)

    return pd.DataFrame(rows, columns=["Medical_School", "Website", "Subpage_URL"])


def scrape_all_pages(subpages_df):
    """Step 2: Scrape text from all subpages.

    Returns a DataFrame with columns: Medical_School, Website, Subpage_URL, Text
    """
    results = subpages_df.copy()
    results["Text"] = ""
    total = len(results)

    for idx in results.index:
        sub_url = results.at[idx, "Subpage_URL"]
        school = results.at[idx, "Medical_School"]
        if idx % 50 == 0 or idx == total - 1:
            print(f"[{idx + 1}/{total}] Scraping {school}: {sub_url[:80]}...")
        try:
            text = extract_page_text(sub_url)
            results.at[idx, "Text"] = text if text else ""
        except Exception as e:
            print(f"  Error scraping {sub_url}: {e}")
            results.at[idx, "Text"] = ""
        smart_delay()

    scraped = results[results["Text"].str.len() > 0].reset_index(drop=True)
    print(f"Scraped {len(scraped)}/{total} pages with content")
    return results


def clean_all_texts(df):
    """Step 3: Clean scraped text — remove stopwords and punctuation.

    Adds columns: Cleaned_Text, Word_Count_Raw, Word_Count_Clean
    """
    result = df.copy()
    result["Text"] = result["Text"].fillna("").astype(str)
    result["Text"] = result["Text"].str.replace("Main content not found", "", regex=False)

    result["Word_Count_Raw"] = result["Text"].apply(lambda x: len(x.split()))
    result["Cleaned_Text"] = result["Text"].apply(clean_text)
    result["Word_Count_Clean"] = result["Cleaned_Text"].apply(lambda x: len(x.split()))

    print(f"Cleaned {len(result)} rows")
    print(f"Avg raw words: {result['Word_Count_Raw'].mean():.0f}, "
          f"Avg clean words: {result['Word_Count_Clean'].mean():.0f}")
    return result
