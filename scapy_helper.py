import requests
from bs4 import BeautifulSoup
import json

def read_file(file_path):
    with open(file_path, 'r') as f:
        sections = f.readlines()
        lowercase_sections = [i.lower().strip() for i in sections]
        return lowercase_sections

def scrap_bl_doc_and_obtain_arguments(sections, url="https://scapy.readthedocs.io/en/stable/api/scapy.layers.bluetooth.html#"):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    dl_tags = soup.find_all('dl', class_='py class')

    results = {}
    for dl in dl_tags:
        dt = dl.find('dt')
        if dt:
            span = dt.find("span", class_="sig-name")
            if span:
                text = span.text
                text_lower = text.lower()
                if text_lower in sections:
                    all_dls = dl.find_all("dl", class_="attribute")
                    last_dl = all_dls[len(all_dls)-1]
                    table = last_dl.find("table")
                    if table:
                        rows = table.find("tbody").find_all("tr")
                        # text_row = rows[0].find("p")
                        results[text] = {
                            "fields": []
                        }
                        for i in rows:
                            results[text]["fields"].append(i.find('p').text)
                        # results.append(text_row.text)

    return results

def write_to_json(data, output_file="results/llm_helper.json"):
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    sections = read_file("results/output.txt")
    results = scrap_bl_doc_and_obtain_arguments(sections)
    write_to_json(results)

