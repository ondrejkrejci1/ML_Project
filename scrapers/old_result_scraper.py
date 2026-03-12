import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

DISCIPLINES = ['100m', 'Long_Jump', 'Shot_Put', 'High_Jump', '400m', '110m_Hurdles', 'Discus', 'Pole_Vault', 'Javelin', '1500m']

def clean_and_convert_performance(value):
    if pd.isna(value) or value in ['DNF', 'DNS', 'NM']: return None
    value = str(value).replace(',', '.')

    if value.count('.') == 2:
        try:
            parts = value.split('.')
            return round((float(parts[0]) * 60) + float(parts[1] + '.' + parts[2]), 2)
        except ValueError:
            return None

    elif ':' in value:
        try:
            parts = value.split(':')
            return round((float(parts[0]) * 60) + float(parts[1]), 2)
        except ValueError:
            return None

    try:
        return float(value)
    except ValueError:
        return None


def clean_points(text_body):
    try:
        clean_value = "".join(c for c in str(text_body) if c.isdigit())
        return int(clean_value) if clean_value else None
    except ValueError:
        return None


def extract_data_old(race_name, valid_cookies):
    path_to_urls = f'urls/{race_name}.csv'

    if not os.path.exists(path_to_urls):
        print(f"File not found - {path_to_urls}")
        return

    df_urls = pd.read_csv(path_to_urls, header=None)
    first_value = str(df_urls.iloc[0, 1])

    if not first_value.startswith('http'):
        df_urls = df_urls.iloc[1:]

    urls_to_scrape = df_urls.iloc[:, 1].tolist()

    years_of_old_scoring = [str(year) for year in range(1975, 1985)]
    urls_to_search = [url for url in urls_to_scrape if any(year in url for year in years_of_old_scoring)]

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    my_cookies = {"PHPSESSID": f"{valid_cookies}"}

    extracted_data = []

    for url in urls_to_search:
        print(f"Downloading: {url}")
        try:
            response = requests.get(url, headers=headers, cookies=my_cookies, timeout=10)
            if "VIP-member" in response.text:
                print("VIP-membership problem.")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            table_rows = soup.find_all('tr')

            for row in table_rows:
                cells = row.find_all(['td', 'th'])

                if len(cells) >= 6:
                    name = cells[1].get_text(strip=True)
                    if name.lower() in ['athlete', 'name', 'decathlete', '']:
                        continue

                    points = cells[-3].get_text(strip=True)
                    cleaned_points = clean_points(points)

                    clear_text = cells[-2].get_text(separator=" ").strip().replace('-', ' ')

                    decathlon_disciplines_results = clear_text.split()
                    results = [v for v in decathlon_disciplines_results if any(c.isdigit() for c in v) or v in ['DNF', 'DNS', 'NM']]

                    if len(results) >= 10 and cleaned_points is not None:
                        record = {'Name': name, 'Points': cleaned_points, 'Event_URL': url}

                        for idx, disc in enumerate(DISCIPLINES):
                            record[disc] = clean_and_convert_performance(results[idx])

                        extracted_data.append(record)

        except Exception as e:
            print(f"Error: {e}")

    if extracted_data:

        df_results = pd.DataFrame(extracted_data)
        df_results = df_results.dropna(subset=DISCIPLINES + ['Points'])

        column_alignment = ['Name', 'Points'] + DISCIPLINES + ['Event_URL']
        df_results = df_results[column_alignment]

        path_to_file = f'data/{race_name}_data_old.csv'
        df_results.to_csv(path_to_file, index=False)
        print(f"Number of results {len(df_results)} downloaded to {path_to_file}.")
    else:
        print("No data found")


extract_data_old("gotzis","1730b1455b0fb4ec8ff5ef060909fe0d")