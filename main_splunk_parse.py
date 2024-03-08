import requests
from bs4 import BeautifulSoup
import splunk_detections_parser as sdp
import csv
from urllib.parse import urljoin

url = "https://research.splunk.com/detections/"

def fetch_page_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Error fetching {url}")
        return None


def parse_detections_page(soup):

    data_list = [urljoin("https://research.splunk.com/detections/", link.get("href")) for link in soup.find_all("a", href=True) if "endpoint" in link['href']]

    return data_list


# this is a test  jklkljkl njknjk
def execution():

    soup = fetch_page_data(url)
    if soup.find("td", {"class": "rouge-code"}):
        data = parse_detections_page(soup)
    else:
        return 0

    return data


all_links = execution()

print(all_links)

sdp.parse_detection_url(all_links)
