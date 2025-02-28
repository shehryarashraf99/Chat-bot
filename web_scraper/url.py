import os
from tavily import TavilyClient
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime
import requests


# Initialize the translator



scrape_date = datetime.today().strftime("%Y-%m-%d")

TAVILY_API_KEY = 'YOUR_TAVILY_KEY'

# Instantiate the Tavily client
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# Execute a simple search query
#response = tavily_client.search("MLX81113KDC-BBB-000-RE")
mpn='RC0603FR-0724KL'
response = tavily_client.search(mpn,max_results=20)

# Print the search results
# Extract URLs from the search results
urls = [result['url'] for result in response['results']]


# Print the extracted URLs


'''
digikey_urls=[]
mouser_urls=[]

# Categorize URLs based on the presence of 'digikey' or 'mouser'

for url in urls:
    if 'digikey' in url:
        digikey_urls.append(url)
    elif 'mouser' in url:
        mouser_urls.append(url)
'''

digikey_urls = [url for url in urls if urlparse(url).netloc.endswith('digikey.com')]
mouser_urls = [url for url in urls if urlparse(url).netloc.endswith('eu.mouser.com')]




# Check if digikey.com URLs are found
print(urls)
# if digikey_urls is not null
if len(digikey_urls) != 0:
    digikey_url = digikey_urls[0]
    parsed_url = urlparse(digikey_url)
    print(f"digikey_url={digikey_url}")
    domain = parsed_url.netloc
    path = parsed_url.path
    # Headers copied from your browser
    headers = {
        "authority": domain,
        "method": "GET",
        "path": path,
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie":"enter_your_cookies",
        "priority": "u=0, i",
        "referer": "https:www.google.com",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "enter_your_user-agent_here"
    }

    response = requests.get(digikey_url, headers=headers, timeout=10)
    output = response.text


    #  Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(output, "html.parser")
    # Get today's date


    # Extract product attributes
    product_attributes_table = soup.find('table', id='product-attributes')
    attributes_data = []
    if product_attributes_table:
        attributes_rows = product_attributes_table.find_all('tr')[1:]  # Skip the header row
        for row in attributes_rows:
            cells = row.find_all('td')
            if len(cells) >= 2:
                type_cell = cells[0].get_text(strip=True)
                description_cell = cells[1].get_text(strip=True)
                attributes_data.append((type_cell, description_cell))

    # Extract pricing details
    pricing_tables = soup.find_all('table', class_='MuiTable-root')
    pricing_data = []
    for table in pricing_tables:
        if 'pricing-table' in table.get('data-testid', ''):
            rows = table.find_all('tr')[1:]  # Skip the header row
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 3:
                    quantity = cells[0].get_text(strip=True)
                    unit_price = cells[1].get_text(strip=True)
                    ext_price = cells[2].get_text(strip=True)
                    pricing_data.append((quantity, unit_price, ext_price))

    # Convert product attributes to Markdown table
    attributes_markdown = "| Type | Description |\n|------|-------------|\n"
    for attr in attributes_data:
        attributes_markdown += f"| {attr[0]} | {attr[1]} |\n"

    # Convert pricing details to Markdown table
    pricing_markdown = "| Quantity | Unit Price | Extended Price |\n|---------|------------|---------------|\n"
    for price in pricing_data:
        pricing_markdown += f"| {price[0]} | {price[1]} | {price[2]} |\n"

    # Save the Markdown tables to a file
    output_file = "scraped_data.md"
    with open(output_file, "w") as file:
        file.write(f"MPN: {mpn}")
        file.write("\n\n")
        file.write(f"# Data Scraped from digikey on {scrape_date} from {digikey_url}\n\n")
        file.write(soup.select_one("div.tss-css-iue0qg-title div[data-testid='title-messages'] span").get_text())
        file.write("\n\n")
        file.write("## Product Attributes\n\n")
        file.write(attributes_markdown)
        file.write("\n\n")
        file.write("## Pricing Details\n\n")
        file.write(pricing_markdown)

    print(f"Data has been saved from  to {output_file}")

elif len(digikey_urls) ==0 and len(mouser_urls) != 0:
    mouser_url = mouser_urls[0]
    parsed_url = urlparse(mouser_url)
    print(f"mouser_url={mouser_url}")
    domain = parsed_url.netloc
    path = parsed_url.path
    headers = {
        'authority': domain,
        'method': 'GET',
        'path': path,
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'your_cookies',
        'priority': 'u=0, i',
        'referer': 'https://www.google.com/',
        'sec-ch-device-memory': '8',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-full-version-list': '"Not(A:Brand";v="99.0.0.0", "Google Chrome";v="133.0.6943.127", "Chromium";v="133.0.6943.127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'enter_your_custom_user-agent_here'
    }
    response = requests.get(mouser_url, headers=headers, timeout=10)
    html_content = response.text

    # Step 2: Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")
    ## product attributes

    print(soup)

    in_stock = soup.find('h2', class_='pdp-pricing-header')
    stocks = in_stock.get_text(strip=True)
    stocks = stocks.replace(".", "")

    # Find the specifications table
    specs_table = soup.find('table', class_='specs-table')

    # Extract the table headers
    headers = [th.get_text(strip=True) for th in specs_table.find_all('th')]

    # Extract the table rows
    product_info = []
    for row in specs_table.find_all('tr')[1:]:  # Skip the header row
        cells = [td.get_text(strip=True) for td in row.find_all('td')]
        product_info.append(cells)

    # Print the extracted data

    headers = ["type", "description"]
    ## print (markdown table)
    description_markdown_table = "| " + " | ".join(headers) + " |\n"
    description_markdown_table += "| " + " | ".join(["---"] * len(headers)) + " |\n"

    for row in product_info:
        type_value = row[0].strip(":")  # Remove colon from type
        description_value = row[1]
        description_markdown_table += f"| {type_value} | {description_value} |\n"

    # Extract pricing table data
    pricing_table = soup.find('table', class_='pricing-table')
    if pricing_table:
        headers = [th.get_text(strip=True) for th in pricing_table.find_all('th') if th.get_text(strip=True)]

        price_data = []
        for row in pricing_table.find_all('tr')[1:]:  # Skip the header row
            cells = [td.get_text(strip=True) for td in row.find_all('td')]
            if cells:
                price_data.append(cells)
        '''
        print("Headers:", headers)

        for row in rows:
            print(row)
    else:
        print("Pricing table not found.")
    '''


    ###################################
    # data cleaning
    def clean_string(value):
        # Remove all dots
        value_without_dots = value.replace('.', '')
        # Remove all spaces
        value_without_spaces = value_without_dots.replace(' ', '')
        return value_without_spaces


    cleaned_headers = [clean_string(value) for value in headers]


    def can_convert_to_int(value):
        try:
            int(value)
            return True
        except ValueError:
            return False


    qty = []
    for i in range(1, len(cleaned_headers)):
        if can_convert_to_int(cleaned_headers[i]):
            qty.append(int(cleaned_headers[i]))

    # Add cleaned values as the first element of each row
    for i, cleaned_value in enumerate(qty):
        if i < len(price_data):
            price_data[i].insert(0, cleaned_value)

    # Print the updated rows

    headers = headers[:3]
    # Create Markdown table
    pricing_markdown_table = "| " + " | ".join(headers) + " |\n"
    pricing_markdown_table += "| " + " | ".join(["---"] * len(headers)) + " |\n"

    for row in price_data:
        pricing_markdown_table += "| " + " | ".join(map(str, row)) + " |\n"

    print(pricing_markdown_table)

    output_file = "mouser_scraped_data.md"
    with open(output_file, "w") as file:
        file.write(f"# Data Scraped from mouser on {scrape_date} from {mouser_url}\n\n")
        file.write("\n\n")
        file.write(f"MPN: {mpn}")
        file.write("\n\n")
        file.write(f"{stocks}")
        file.write("\n\n")
        file.write("## Product Attributes \n\n")
        file.write(description_markdown_table)
        file.write("\n\n")
        file.write("## Pricing Details\n\n")
        file.write(pricing_markdown_table)

    print(f"Data has been saved from  to {output_file}")

else:
    print("No URLs found with the specified domains.")






#print(domain)
#print(path)