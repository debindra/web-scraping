from bs4 import BeautifulSoup
import requests
import csv


BASE_URL = "https://www.yellowpagesnepal.com"

def scrape_page(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    title =  soup.find('h1', class_='t600')
    last_update_date =  soup.find('div', class_='updated-date')
    visits =  soup.find('div', class_='visits').text
    category = soup.find('p').find('a').text
    
    data = {};
    data['title'] = title.text.strip();

    data['last_visited_date'] = last_update_date.text.strip()
    data['visits'] =   visits;
    data['category'] = category;
        
    return data

def get_scrape_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    h3_tags = soup.find_all('h3', class_="font-20");#h.find('a')
    links = [h3.find('a')['href'] for h3 in h3_tags if h3.find('a')]
    
    data = []

    for link in links:
        url = f"{BASE_URL}/{link}"

        result = scrape_page(url)
        data.append(result)
 
    return data


def scrape_muliple_pages(num_pages):
    all_data = []
    print (num_pages);

    for page_num in range(1, num_pages + 1):
        url = f"{BASE_URL}/airlines?page={page_num}"
        page_data = get_scrape_data(url)
        # print(page_data)
        if page_data:
            all_data.extend(page_data)
    
    return all_data

def save_to_csv(data, csv_file):
    if data:
        keys = data[0].keys()
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=keys)
            
            # Write header
            writer.writeheader()
            
            # Write data
            writer.writerows(data)
            
        print(f"Data saved to {csv_file}")
    else:
        print("No data to save.")
    
num_of_pages_to_scrape = 2;



# Specify the CSV file to save the data
csv_filename = 'airlines.csv'

data = scrape_muliple_pages(num_of_pages_to_scrape)
save_to_csv(data, csv_filename)