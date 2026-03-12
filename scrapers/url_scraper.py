import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.decathlon2000.com/meetings"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("Downloading the page and analyze the HTML...")
response = requests.get(URL, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    data_found = []

    subitem_spans = soup.find_all('span', class_='menubox-subitem')

    for span in subitem_spans:
        a_tag = span.find('a')

        if a_tag and 'href' in a_tag.attrs:
            odkaz = a_tag['href']
            nazev_zavodu = a_tag.text.strip()


            if "all-time" in odkaz.lower():
                continue

            if "fred-kudu-memorial" in odkaz.lower():
                continue

            data_found.append({
                'Nazev': nazev_zavodu,
                'URL': odkaz
            })

    df_urls = pd.DataFrame(data_found)
    csv = 'decathlon2000_urls.csv'
    df_urls.to_csv(csv, index=False)

    print(f"Number of data found: {len(data_found)}.")

else:
    print(f"Error: {response.status_code}")