import os

file_path = 'C:\\Users\\corbi\\PycharmProjects\\splunk_scraper\\splunk_research_output.csv'

if os.path.exists(file_path):
    # Delete the file
    os.remove(file_path)

