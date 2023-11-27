from bs4 import BeautifulSoup
import requests
import csv

BASE_URL = "https://www.yellowpagesnepal.com" # base url 
TOTAL_PAGES = 1 # Chnages this value based on # of pages
CATEGORY = 'airlines'

# Function to scrape the page contents
def scrape_page(url):

    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        title =  soup.find('h1', class_='t600')
        address = soup.select_one('div span:nth-of-type(2)').get_text()
        last_update_date =  soup.find('div', class_='updated-date')
        visits =  soup.find('div', class_='visits').text
        category = soup.find('p').find('a').text
        
        data = {}

        data['title'] = title.text.strip()
        data['address'] = address
        data['last_visited_date'] = last_update_date.text.strip()
        # data['last_visited_date'] = last_update_date.tex÷t.strip().split(':')[1]
        data['visits'] =   visits
        # data['visits'] =   visits.split(' ')[0]
        data['category'] = category
        return data    
    except Exception as e:
        # Handle other exceptions
        print(f"An unexpected error occurred: {e}")
    
    finally:
        # Code to be executed no matter what (e.g., cleanup operations)
        print(f"Current URL is : {url}")       


# Function to list the links from individual pages 
def get_scrape_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    h3_tags = soup.find_all('h3', class_="font-20")
    links = [h3.find('a')['href'] for h3 in h3_tags if h3.find('a')]
    
    data = []

    for link in links:
        url = f"{BASE_URL}/{link}"
        result = scrape_page(url)

        data.append(result)
 
    return data

# Function to generate page with page number
def scrape_muliple_pages(num_pages):
    all_data = []

    for page_num in range(1, num_pages + 1):
        url = f"{BASE_URL}/{CATEGORY}?page={page_num}"
        page_data = get_scrape_data(url)
        # print(page_data)
        if page_data:
            all_data.extend(page_data)
    
    return all_data

# Function to save generate data to CSV
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

# Specify the CSV file to save the data
csv_filename = f"{CATEGORY}.csv"

#Function call to generate data
data = scrape_muliple_pages(TOTAL_PAGES)

#Function call to generate data to CSV file
save_to_csv(data, csv_filename) 