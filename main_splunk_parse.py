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


def execution():

    soup = fetch_page_data(url)
    if soup:
        data = parse_detections_page(soup)
    else:
        data = "N/A"

    return data


all_links = execution()

#print(all_links)

for link in all_links:
    print(link)
    #sdp.parse_detection_url(link)
