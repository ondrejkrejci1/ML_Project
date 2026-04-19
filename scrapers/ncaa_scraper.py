import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def time_to_seconds(time_str):
    if pd.isna(time_str) or time_str == 0 or str(time_str).strip() == '':
        return 0.0

    time_str = str(time_str).strip()
    try:
        if ':' in time_str:
            parts = time_str.split(':')
            minutes = float(parts[0])
            seconds = float(parts[1])
            return round((minutes * 60) + seconds, 2)
        else:
            return float(time_str)
    except ValueError:
        return 0.0


def scrape_decathlon(url=None, raw_html=None):
    if url:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers)
        html_content = response.text
    else:
        html_content = raw_html

    soup = BeautifulSoup(html_content, 'html.parser')

    hidden_classes = set()
    for style in soup.find_all('style'):
        matches = re.findall(r'\.([a-zA-Z0-9_-]+)\s*\{\s*display:\s*none', style.text)
        hidden_classes.update(matches)

    def is_hidden(tag):
        classes = tag.get('class', [])
        return any(c in hidden_classes for c in classes)

    athletes_data = {}

    for title_div in soup.find_all('div', class_='custom-table-title'):
        h3 = title_div.find('h3')
        if not h3:
            continue

        raw_event_name = h3.text.strip()

        if "Decathlon" in raw_event_name and "Meters" not in raw_event_name:
            event_key = "Total_Points";
            target_col = "POINTS"
        elif "100 Meters" in raw_event_name:
            event_key = "100m"; target_col = "TIME"
        elif "Long Jump" in raw_event_name:
            event_key = "Long_Jump"; target_col = "MARK"
        elif "Shot Put" in raw_event_name:
            event_key = "Shot_Put"; target_col = "MARK"
        elif "High Jump" in raw_event_name:
            event_key = "High_Jump"; target_col = "MARK"
        elif "400 Meters" in raw_event_name:
            event_key = "400m"; target_col = "TIME"
        elif "110 Hurdles" in raw_event_name:
            event_key = "110m_Hurdles"; target_col = "TIME"
        elif "Discus" in raw_event_name:
            event_key = "Discus"; target_col = "MARK"
        elif "Pole Vault" in raw_event_name:
            event_key = "Pole_Vault"; target_col = "MARK"
        elif "Javelin" in raw_event_name:
            event_key = "Javelin"; target_col = "MARK"
        elif "1500 Meters" in raw_event_name:
            event_key = "1500m"; target_col = "TIME"
        else:
            continue

        table = title_div.find_next('table')
        if not table or not table.find('tbody'):
            continue

        headers = []
        for th in table.find('thead').find_all('th'):
            if not is_hidden(th):
                headers.append(th.text.strip().upper())

        for tr in table.find('tbody').find_all('tr', recursive=False):
            if tr.find('div', class_='div-subRow-table'):
                continue

            tds = tr.find_all('td', recursive=False)
            visible_tds = [td for td in tds if not is_hidden(td)]

            if len(headers) != len(visible_tds):
                continue

            row_dict = {headers[i]: visible_tds[i].text.strip() for i in range(len(headers))}

            name = row_dict.get('NAME')
            if not name:
                continue

            name = " ".join(name.split())

            if name not in athletes_data:
                athletes_data[name] = {'Athlete_Name': name}

            val = row_dict.get(target_col)
            if val:
                if val.endswith('m'):
                    val = val[:-1].strip()
                athletes_data[name][event_key] = val

    df = pd.DataFrame(list(athletes_data.values()))

    col_order = ['Athlete_Name', 'Total_Points', '100m', 'Long_Jump', 'Shot_Put', 'High_Jump', '400m', '110m_Hurdles', 'Discus', 'Pole_Vault', 'Javelin', '1500m']
    existing_cols = [c for c in col_order if c in df.columns]
    df = df[existing_cols]

    invalid_values = ['DNF', 'NH', 'DNS', 'NM', 'DQ', 'FOUL']
    df = df.replace(invalid_values, 0)
    df = df.fillna(0)

    time_disciplines = ['100m', '400m', '110m_Hurdles', '1500m']
    for col in time_disciplines:
        if col in df.columns:
            df[col] = df[col].apply(time_to_seconds)

    return df


def save_to_csv(df, filename="NCAA_data.csv"):
    file_exists = os.path.isfile(filename)

    df.to_csv(filename, mode='a', index=False, header=not file_exists, encoding='utf-8')

    if file_exists:
        print(f"Successfully saved")
    else:
        print(f"File was created and data was saved")


URL_ADDRESS = "https://tfrrs.org/results/93526/5832716/Harding_Invitational/Mens-Decathlon"
finale_dataframe = scrape_decathlon(url=URL_ADDRESS)

save_to_csv(finale_dataframe, "../data/NCAA_data.csv")