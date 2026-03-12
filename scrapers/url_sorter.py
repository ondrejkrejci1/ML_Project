meetings = ["gotzis", "talence", "ratigen", "usa", "multistars", "kladno", "alhama", "fred", "estonian"]

sorted_urls = {meeting: [] for meeting in meetings}

with open('../urls/decathlon2000_urls.csv', 'r', encoding='utf-8') as file:
    lines = file.read().splitlines()

for line in lines:
    parts = line.split(',')

    url = parts[1].strip()
    last_part = url.strip('/').split('/')[-1].lower()

    for meeting in meetings:
        if meeting in last_part:
            sorted_urls[meeting].append(line)
            break

saved = 0

for meeting, list_of_lines in sorted_urls.items():

    if list_of_lines:

        with open(f"{meeting}.csv", 'w', encoding='utf-8') as f:

            for radek in list_of_lines:
                f.write(f"{radek}\n")
                saved += 1

print(saved)