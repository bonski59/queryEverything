import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin, urlparse
import os
import re
from test_data import read_random_lines


# global variable used for later
detect_repo = "https://www.elastic.co/guide/en/security/7.16/prebuilt-rules.html"

base_url = "https://www.elastic.co/guide/en/security/7.16/"

# fetches url and makes it a readable variable or returns error
def fetch_page_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(response.status_code)
        print(f"Error fetching {url}")
        return None

# test
# print(fetch_page_data(detect_repo))


# parses page for specific information and makes a dictionary output.


# takes a dictionary and outputs a csv with headers respective to the order of the dictionary
def save_to_csv(data, filename="elastic_research_output.csv"):
    #print(data)
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

    # find the type of query

    def find_bullet(bullet_bold_title):
        # find the bold title of a section and use the return to parse what you need.
        return soup.find(lambda tag: tag.name == "p" and tag.find('strong', string=bullet_bold_title))

    def mitre_data(tac_or_tech, data_id):
        return [tactic.find_next_sibling('div').find('li', string=lambda text: data_id in text if text else False).text.strip().replace(data_id, "") for tactic in soup.find_all('p', string=tac_or_tech)]
    # parsed data dictionary
    data = {
        #    ## <-- this tag means they have been tested successfully among at least 10/608 urls (i know thats not a lot)
        
        "url": url if url else "N/A",
        "title": soup.find("h2", {"class": "title"}).text.strip() if soup.find("h2", {"class": "title"}) else "N/A",
        "mitre_tactic_name": mitre_data("Tactic:", "Name: "),
        "mitre_tactic": mitre_data("Tactic:", "ID: "),
        "mitre_technique_name": mitre_data("Technique:", "Name: "),
        "mitre_technique": mitre_data("Technique:", "ID: "),
        "description": soup.find("h2", {"class": "title"}).find_next("p").text.strip() if soup.find("h2", {"class": "title"}) else "N/A",
        "type": find_bullet("Rule type").text.strip().split(": ")[1:] if find_bullet("Rule type") else "N/A",
        "elastic_query": soup.find("div", {"class": "pre_wrapper lang-js"}).text.strip().replace("\n", "") if soup.find("div", {"class": "pre_wrapper lang-js"}) else "N/A",
        "rule_indices": [indi.text.strip() for indi in find_bullet("Rule indices").find_next("div", {"class": "ulist itemizedlist"}).find_all("li")] if find_bullet("Rule indices") else "N/A",
        "references": [href.get("href") for href in find_bullet("References").find_next("div", {"class": "ulist itemizedlist"}).find_all("a")] if find_bullet("References") else "N/A",
        "tags": [tag.text.strip() for tag in find_bullet("Tags").find_next("div", {"class": "ulist itemizedlist"}).find_all("li")] if find_bullet("Tags") else "N/A"

    }


    save_to_csv(data)

# testing
#[print(parse_endpoint_url(the_url).values()) for the_url in read_random_lines('detections_repo_links.txt')]


# reads the detection repo, finds all filtered links, and returns a list of links
def parse_detections_page():
    soup = fetch_page_data(detect_repo)
    data_list = [urljoin(base_url, link.get("href")) for link in soup.find_all("a", {"class": "xref"}, title=True)
                 if "#" not in link['href']]

    return data_list

# test
# print(parse_detections_page())


# print(parse_detections_page())


# takes the detections repo and makes a txt file listing each of them line by line, so we don't need to keep querying
def make_detections_repo_file(list_links):
    file = 'detections_repo_links.txt'
    with open(file, "w") as f:
        for link in list_links:
            f.write(f"{link}\n")
    return


# test or use to generate ./detections_repo_links.txt
# make_detections_repo_file(parse_detections_page())

def parse_all_repo_links():
    with open('detections_repo_links.txt', 'r') as file:
        for line in file:
            print(line)
            if fetch_page_data(line.strip('\n')) is None:
                pass
            parse_endpoint_url(line.strip('\n'))


if __name__ == "__main__":
    parse_all_repo_links()
    #parse_endpoint_url("https://research.splunk.com/endpoint/44fddcb2-8d3b-454c-874e-7c6de5a4f7ac/")




