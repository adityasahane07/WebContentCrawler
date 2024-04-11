import os
import re
import requests
from bs4 import BeautifulSoup
from sys import argv
from datetime import datetime

def extract_titles_from_wikipedia(URL):
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'lxml')
    title = soup.select('title')
    print("Title is ")
    print(title[0].getText())
    arr = soup.select(".mw-headline")
    print("Topics:")
    for element in arr:
        print(element.text)

def fetch_links_from_wikipedia(URL):
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'lxml')
    links = soup.find_all('a', href=True)
    return [element['href'] for element in links if "#" not in element['href']]

def download_images_from_website(URL, download_folder):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_tags = soup.find_all('img')
    urls = [img['src'] for img in image_tags]
    folder_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Generate folder name based on current timestamp
    download_folder = os.path.join(download_folder, folder_name)
    os.makedirs(download_folder, exist_ok=True)  # Create download folder if it doesn't exist
    for url in urls:
        filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
        if not filename:
             print("Regular expression didn't match with the url: {}".format(url))
             continue
        with open(os.path.join(download_folder, filename.group(1)), 'wb') as f:
            if 'http' not in url:
                url = '{}{}'.format(URL, url)
            response = requests.get(url)
            f.write(response.content)
    print("Download complete, downloaded images can be found in the folder:", download_folder)

def main():
    print("-- Aditya Sahane --")
    print("Application name : " + argv[0])

    if len(argv) == 2:
        if argv[1] == "-h" or argv[1] == "-H":
            print("This script is used to perform various operations on Wikipedia.")
            exit()
        if argv[1] == "-u" or argv[1] == "-U":
            print("Usage : ApplicationName")
            exit()

    # URL = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    URL = "https://en.wikipedia.org/wiki/Cristiano_Ronaldo"

    download_folder = "downloaded_images"  # Specify the parent folder for downloaded images

    extract_titles_from_wikipedia(URL)

    links = fetch_links_from_wikipedia(URL)
    print("Links are:")
    for link in links:
        print(link)

    download_images_from_website(URL, download_folder)

if __name__ == "__main__":
    main()
