import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import os

def fetch_page_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Error fetching {url}")
        return None


def parse_page(soup, link):
    # Assuming the structure based on common patterns; you may need to adjust these

    # macros parse
    my_macros = [macro.text.strip() for macro in soup.find_all('a', href=lambda href: href and href.endswith('.yml'))]

    # required fields parse
    h4_req_fields = soup.find('h4', id='required-fields')
    ul_or_ol = h4_req_fields.find_next_sibling('ul')
    if ul_or_ol:
        li_elements = ul_or_ol.find_all('li')
    else:
        li_elements = []

    data = {
        "url": link if link else "N/A",
        "title": soup.find("h1", id="page-title").text.strip() if soup.find("h1", id="page-title") else "N/A",
        "mitre_attack_codes": [tcode.text.strip() for tcode in soup.find('h4', id='attck').find_next_sibling('table').find_all('a')] if soup.find('h4', id='attck').find_next_sibling('table').find_all('a') else "N/A",
        "description": soup.find("h4", id="description").find_next_sibling("p").text.strip() if soup.find("h4", id="description").find_next_sibling("p").text.strip() else "N/A",
        "type": [link.text.strip() for link in soup.find_all("a", href=True) if "Types" in link['href']],
        "last_update": soup.find("time").text.strip() if soup.find("time") else "N/A",
        "splunk_query": soup.find("td", {"class": "rouge-code"}).text.strip() if soup.find("td", {"class": "rouge-code"}) else "N/A",
        "required_macros": [macros for macros in my_macros if "source" not in macros] if my_macros else "N/A",
        "required_fields": [element.text.strip() for element in li_elements],
        "false_positives": soup.find('h4', id='known-false-positives').find_next_sibling("p").text.strip() if soup.find('h4', id='known-false-positives').find_next_sibling("p").text.strip() else "N/A",
        "associated_analytics": [code.text.strip() for code in soup.findAll("a", href=True) if "stories" in code['href'] if
                       "Analytic Stories" not in code],
        "analytic_stories": [urljoin("https://research.splunk.com", code.get("href")) for code in
                        soup.findAll("a", href=True) if "stories" in code['href'] if "Analytic Stories" not in code],
        "references": [href.get("href") for href in soup.find('h4', id='reference').find_next_sibling('ul').findAll("a", href=True)],
        "tags": [tag.text.strip() for tag in soup.find("span", itemprop="keywords").find_all("a") if "tags" in tag["href"]],
        "category": [cat.text.strip() for cat in soup.find_all("a", href=True) if "categories" in cat["href"]]
    }
    return data


def save_to_csv(data, filename="splunk_research_output.csv"):
    keys = data[0].keys()
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)

        if not file_exists:  # Only write the header if the file doesn't exist
            dict_writer.writeheader()

        dict_writer.writerows(data)


def parse_detection_url(urls):
    all_data = []
    for url in urls:
        soup = fetch_page_data(url)
        if soup:
            data = parse_page(soup, url)
            all_data.append(data)

    save_to_csv(all_data)


"""urls = ["https://research.splunk.com/cloud/ccb3e4af-23d6-407f-9842-a26212816c9e/"]


if __name__ == "__main__":
    parse_detection_url(urls)
"""