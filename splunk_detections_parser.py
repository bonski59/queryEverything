import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import os
import re

# global variable used for later
detect_repo = "https://research.splunk.com/detections/"

# fetches url and makes it a readable variable or returns error
def fetch_page_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(response.status_code)
        print(f"Error fetching {url}")
        return None

# parses page for specific information and makes a dictionary output.


# takes a dictionary and outputs a csv with headers respective to the order of the dictionary
def save_to_csv(data, filename="splunk_research_output.csv"):
    print(data)
    keys = data.keys()
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)

        if not file_exists:  # Only write the header if the file doesn't exist
            dict_writer.writeheader()

        dict_writer.writerow(data)
    print(f"{data.get('title')} retrieved and written")

# reads the specified url, parses, and then sends it to a csv
def parse_endpoint_url(url):
    soup = fetch_page_data(url)

    # Assuming the structure based on common patterns; you may need to adjust these

    # macros parse
    my_macros = [req.text.strip() for req in soup.find('h4', id='macros').find_next_sibling('ul')]

    # required fields parse
    h4_req_fields = [req.text.strip() for req in soup.find('h4', id='required-fields').find_next_sibling('ul')] \
        if soup.find('h4', id='required-fields') else "N/A"

    # parsed data dictionary
    data = {
        "url": url if url else "N/A",
        "title": soup.find("h1", id="page-title").text.strip() if soup.find("h1", id="page-title") else "N/A",
        "mitre_attack_codes": [tcode.text.strip() for tcode in soup.find('h4', id='attck').find_next_sibling('table').find_all('a')] if soup.find('h4', id='attck').find_next_sibling('table').find_all('a') else "N/A",
        "description": soup.find("h4", id="description").find_next_sibling("p").text.strip() if soup.find("h4", id="description").find_next_sibling("p").text.strip() else "N/A",
        "type": [link.text.strip() for link in soup.find_all("a", href=True) if "Types" in link['href']],
        "last_update": soup.find("time").text.strip() if soup.find("time") else "N/A",
        "splunk_query": soup.find("td", {"class": "rouge-code"}).text.strip() if soup.find("td", {"class": "rouge-code"}) else "N/A",
        "required_macros": list(filter(lambda item: item != '', my_macros)),
        "required_fields": list(filter(lambda item: item != '', h4_req_fields)),
        "false_positives": soup.find('h4', id='known-false-positives').find_next_sibling("p").text.strip() if soup.find('h4', id='known-false-positives').find_next_sibling("p").text.strip() else "N/A",
        "associated_analytics": [code.text.strip() for code in soup.findAll("a", href=True) if "stories" in code['href'] if "Analytic Stories" not in code],
        "analytic_stories": [urljoin("https://research.splunk.com", code.get("href")) for code in soup.findAll("a", href=True) if "stories" in code['href'] if "Analytic Stories" not in code],
        "references": [href.get("href") for href in soup.find('h4', id='reference').find_next_sibling('ul').findAll("a", href=True)] if soup.find('h4', id='reference').find_next_sibling('ul') else "N/A",
        "tags": [tag.text.strip() for tag in soup.find("span", itemprop="keywords").find_all("a") if "tags" in tag["href"]],
        "category": [cat.text.strip() for cat in soup.find_all("a", href=True) if "categories" in cat["href"]]
    }

    save_to_csv(data)


# reads the detection repo, finds all filtered links, and returns a list of links
def parse_detections_page():
    soup = fetch_page_data(detect_repo)
    data_list = [urljoin("https://research.splunk.com/", link.get("href"))
                 for link in soup.find_all("a", href=True) if "endpoint" in link['href']]

    return data_list

# takes the detections repo and makes a txt file listing each of them line by line, so we don't need to keep querying
def make_detections_repo_file(list_links):
    file = './detections_repo_links.txt'
    with open(file, "w") as f:
        for link in list_links:
            if verify_detections_repo(link):
                f.write(f"{link}\n")
            else:
                pass
                print("link did not match regex pattern - ", link)

    return

# verify links found in detect repo are the correct links we want to follow
def verify_detections_repo(url):

    pattern = r"https://research\.splunk\.com/endpoint*-*-*-*"

    if re.match(pattern, url):
        return True
    else:
        return False


def parse_all_repo_links():
    with open('./detections_repo_links.txt', 'r') as file:
        for line in file:
            print(line)
            if fetch_page_data(line.strip('\n')) is None:
                pass
            parse_endpoint_url(line.strip('\n'))


if __name__ == "__main__":
    parse_all_repo_links()




