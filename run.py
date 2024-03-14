import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import html
from urllib.parse import urljoin, urlparse
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


if __name__ == '__main__':

    def get_links(url, session):
        response = session.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = {link.get('href') for link in soup.find_all('a') if link.get('href')}
            return links
        else:
            print(f"Failed to fetch the page. Status Code: {response.status_code}")
            return set()

    def get_watch_links(initial_url, session):
        all_links_set = set()
        links = get_links(initial_url, session)

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_link = {executor.submit(get_links, urljoin(initial_url, link), session): link for link in links}
            for future in as_completed(future_to_link):
                link = future_to_link[future]
                try:
                    page_links = future.result()
                    all_links_set.update(page_links)
                except Exception as exc:
                    print(f"Link {link} generated an exception: {exc}")

        watch_links = {link for link in all_links_set if link.startswith('https://www.fpjourne.com/en/collection/')}
        return watch_links

    def extract_watch_info(link, session):
        try:
            response = session.get(link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                watch_title = soup.find('a', class_='mc-elem-url 99')
                return {link}
            else:
                print(f"Failed to fetch the page {link}. Status Code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error processing the page {link}: {e}")
            return None
        
        


    initial_url = 'https://www.fpjourne.com/en/collections'
    with requests.Session() as session:
            watch_links = get_watch_links(initial_url, session)
            with ThreadPoolExecutor(max_workers=10) as executor:
                watch_info_list = [result for result in executor.map(lambda link: extract_watch_info(link, session), watch_links) if result]

    collections_links = [list(watch_info)[0] for watch_info in watch_info_list]
    def extract_watch_info(link):
        try:
            
            response = requests.get(link)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                watch_title = soup.find_all('a', class_='mc-elem-url 99')
                
    

                return {
                    'link': link,
                    'title': watch_title,
                    
                    
                }

            else:
                print(f"Failed to fetch the page {link}. Status Code: {response.status_code}")
                return None

        except Exception as e:
            print(f"Error processing the page {link}: {e}")
            return None

    # My list of links
    collections_links

    # Create a list to store 
    watch_info_list = []

    # Iterate 
    for link in collections_links:
        watch_info = extract_watch_info(link)
        if watch_info:
            watch_info_list.append(watch_info)


    html_content = '<ul>\n'
    for watch in watch_info_list:
        html_content += f'  <li><a href="{watch["link"]}">{watch["title"]}</a></li>\n'
    html_content += '</ul>'

    # # Write HTML content to a file
    # with open('watches.html', 'w', encoding='utf-8') as file:
    #     file.write(html_content)
        
    soup = BeautifulSoup(html_content, 'html.parser')

    watch_links = [a['href'] for a in soup.find_all('a', {'class': 'mc-elem-url 99'})]


    prefix = 'https://www.fpjourne.com/'

    # Add the prefix 
    full_watch_links = [f"{prefix}{link}" for link in watch_links]



    def scrape_images_from_url(url, prefix, session):
        try:
            response = session.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.select('div._slides img[itemprop="image"]')
            image_urls = [f"{prefix}{img['data-src']}" for img in img_tags]

            return image_urls
        except requests.exceptions.RequestException as e:
            print(f"Error while scraping {url}: {e}")
            return []

    def filter_first_urls_by_prefix(image_urls, prefix_length=5):
        first_urls_per_prefix = {}

        for url in image_urls:
            model_prefix = extract_model_prefix(url, prefix_length)
            if model_prefix is not None and model_prefix not in first_urls_per_prefix:
                first_urls_per_prefix[model_prefix] = url

        return list(first_urls_per_prefix.values())

    def extract_model_prefix(url, prefix_length):
        parts = url.split('/')
        declination_index = parts.index('declination')
        if declination_index + 1 < len(parts):
            return parts[declination_index + 1][:prefix_length]
        return None

    # Assuming full_watch_links is a list of URLs
    prefix = 'https://www.fpjourne.com/'

    with requests.Session() as session:
        image_urls_dict = {watch_url: filter_first_urls_by_prefix(scrape_images_from_url(watch_url, prefix, session)) for watch_url in full_watch_links}

    watch_url_list = [{"watch_URL": watch_url, "image_URL": filtered_url} for watch_url, filtered_urls in image_urls_dict.items() for filtered_url in filtered_urls]
    # Extract information from watch_url_list
    parent_models = []
    specific_models = []
    brand_name = []

    for link in watch_url_list:
        match = re.search(r'/collection/([^/]+)/([^/]+)$', link["watch_URL"])
        if match:
            parent_model = match.group(1)
            specific_model = match.group(2)
            parent_models.append(parent_model)
            specific_models.append(specific_model)
            brand_name.append('F.P. Journe')
        else:
            parent_models.append(None)
            specific_models.append(None)

    # Extract image URLs from watch_url_list
    image_urls = [row["image_URL"] for row in watch_url_list]


    watches_dict = ({
        'reference_number':'',
        'watch_URL': [row["watch_URL"] for row in watch_url_list],
        'type':'',
        'brand': brand_name,
        'year_introduced':'',
        'parent_model': parent_models,
        'specific_model': specific_models,
        'nickname':'',
        'marketing_name':'',
        'style':'',
        'currency':'',
        'price':'',
        'image_URL': image_urls,
        'made_in':'',
        'case_shape':''

    })

    links_df = pd.DataFrame(watches_dict)



    ###############################################




    import requests
    from bs4 import BeautifulSoup
    import pandas as pd



    def scrape_info_from_link(link, session):
        try:
            response = session.get(link)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            div = soup.find('div', class_="product-summary")
            if div:
                desc_div = div.find('div', class_="_desc")
                description = desc_div.get_text(separator="\n", strip=True) if desc_div else None
                return {'Description': description}
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching content from {link}: {e}")
            return None

    def scrape_info_from_links(df):
        scraped_data = []
        with requests.Session() as session:
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_link = {executor.submit(scrape_info_from_link, row["watch_URL"], session): row["watch_URL"] for index, row in df.iterrows()}
                for future in as_completed(future_to_link):
                    result = future.result()
                    if result:
                        scraped_data.append(result)
        return scraped_data

    def get_html_content_from_link(link):
        try:
            response = requests.get(link)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching content from {link}: {e}")
            return None

    def extract_product_info(scraped_data):
        product_list = []
        for product in scraped_data:
            description = product.get('Description', '')
            description_list = description.split('\n')
            product_info = {line.split(':', 1)[0].strip().replace(' ', '_'): line.split(':', 1)[1].strip() for line in description_list if ':' in line}
            product_info['case_material'] = description_list[0].strip() if description_list else 'None'
            product_info.setdefault('Description', None)
            product_list.append(product_info)
        return product_list

    def map_product_info(product_list, key_mapping):
        mapped_info_list = [{new_key: product_info.get(old_key, 'None') for old_key, new_key in key_mapping.items()} for product_info in product_list]
        return mapped_info_list

    # Assuming links_df is a DataFrame with a column 'watch_URL'
    scraped_data = scrape_info_from_links(links_df)
    product_list = extract_product_info(scraped_data)

    key_mapping = {
        'case_material': 'Case Material',
        'case_finish': 'case_finish',
        'caseback': 'caseback',
        'Diameter': 'diameter',
        'between_lugs': 'between_lugs',
        'lug_to_lug': 'lug_to_lug',
        'Overall_height': 'case_thickness',
        'bezel_material': 'bezel_material',
        'bezel_color':'bezel_color',
        'crystal': 'crystal',
        # 'water_resistance': 'water_resistance',
        'weight': 'weight',
        'Dial': 'dial_color',
        'numerals': 'numerals',
        'Hands': 'bracelet_material',
        'bracelet_color': 'bracelet_color',
        'clasp_type':'clasp_type'
    }

    mapped_info_list = map_product_info(product_list, key_mapping)
    product_df = pd.DataFrame(mapped_info_list)



    ########################################


    def get_html_content_from_link(link, session):
        try:
            response = session.get(link)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching content from {link}: {e}")
            return None

    def extract_info_from_link(link, session):
        result = {}
        caliber_info = {}

        html_content = get_html_content_from_link(link, session)

        if html_content:
            tree = html.fromstring(html_content)
            div_elements = tree.xpath("//div[@class='product-list-specs']")
            seen_titles = set()
            link_data = []

            for div_element in div_elements:
                title_text = div_element.xpath(".//div[@class='_title']/text()")[0].strip()

                if title_text in seen_titles:
                    break

                seen_titles.add(title_text)
                title_texts = {title_text.lower(): []}
                p_texts = div_element.xpath(".//ul[@class='_list']//p/text()")
                title_texts[title_text.lower()] = [text.strip() for text in p_texts]
                link_data.append(title_texts)

            result = link_data
            caliber_texts = tree.xpath("/html/body/div[2]/div/div[1]/main/div/div[2]/div[2]/div[1]/div[1]/h1/span[2]/span/span")
            caliber_info = {'caliber': caliber_texts[0].text_content().strip()} if caliber_texts else {'caliber': None}

        return result, caliber_info

    def extract_info_from_links(df):
        result_dict = {}
        caliber_data = {}

        with requests.Session() as session:
            with ThreadPoolExecutor(max_workers=10) as executor:
                # Create a dictionary of futures with their corresponding index
                futures = {executor.submit(extract_info_from_link, row['watch_URL'], session): index for index, row in df.iterrows()}

                for future in as_completed(futures):
                    result, caliber = future.result()
                    index = futures[future]  # Get the index corresponding to this future
                    result_dict[index] = result
                    caliber_data[index] = caliber

        return result_dict, caliber_data

    # Assuming links_df is a DataFrame with a column 'watch_URL'
    result_dict, caliber_data = extract_info_from_links(links_df)



    # Specify the keys you want to keep in the merged data
    keys_to_keep = ['movement', 'caliber',
                    'power_reserve','frequency',
                    'number of jewels','nbre de jewels',
                    'features','description','short_description','case']


    merged_data = []

    # Iterate over result_dict and caliber_data to merge the data
    for link_index, title_texts in result_dict.items():
        entry_data = {key: None for key in keys_to_keep}  # Initialize a new dictionary for each link
        
        # Update entry_data with data from title_texts
        for title_text_dict in title_texts:
            title_key = list(title_text_dict.keys())[0]
            title = title_key.split(':')[0].strip()
            if title in keys_to_keep:
                texts = title_text_dict[title_key]
                entry_data[title] = ', '.join(texts) if texts else None

        # Update entry_data with data from caliber_data
        entry_data['caliber'] = caliber_data[link_index]['caliber']

        # Get the values for 'number of jewels' and 'nbre de jewels', handling None values
        jewels1 = entry_data.get('number of jewels', '')
        jewels2 = entry_data.get('nbre de jewels', '')

        # Merge either 'number of jewels' or 'nbre de jewels' key into a new key 'jewels'
        entry_data['jewels'] = jewels1 if jewels1 else jewels2

        # Remove both 'number of jewels' and 'nbre de jewels' keys
        entry_data.pop('number of jewels', None)
        entry_data.pop('nbre de jewels', None)

        # Append the entry_data to the merged_data list
        merged_data.append(entry_data)
        


    # Create DataFrame using pd.DataFrame.from_dict
    technicalSpec_df = pd.DataFrame.from_dict(merged_data)


    technicalSpec_df['water_resistance'] = technicalSpec_df['case'].str.extract(r'Water resistant to (\d+) meters') + 'm'
    technicalSpec_df = technicalSpec_df.drop('case', axis=1)


    ##########################################


    links_df = links_df.fillna('')
    product_df = product_df.replace({None: '', 'None': '', 'nan': ''})
    technicalSpec_df = technicalSpec_df.fillna('')  
    scrapes_df = pd.concat([links_df, product_df, technicalSpec_df] , axis=1)

    column_order = ['reference_number',
        'watch_URL',
        'type',
        'brand',
        'year_introduced',
        'parent_model',
        'specific_model',
        'nickname',
        'marketing_name',
        'style',
        'currency',
        'price',
        'image_URL',
        'made_in',
        'case_shape',
        'Case Material',
        'case_finish',
        'caseback',
        'diameter',
        'between_lugs',
        'lug_to_lug',
        'case_thickness',
        'bezel_material',
        'bezel_color',
        'crystal',
        'water_resistance',
        'weight',
        'dial_color',
        'numerals',
        'bracelet_material',
        'bracelet_color',
        'clasp_type',
        'movement',
        'caliber',
        'power_reserve',
        'frequency',
        'jewels',
        'features',
        'description',
        'short_description',

        ] 
    scrapes_df = scrapes_df[column_order]
    # scrapes_df.to_csv('F.P.Journe-Scrapes.csv',)


    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')



    # Save the DataFrame to a CSV file with the timestamp in the filename
    # file_path = f"data/F.P.Journe-Scrapes_{timestamp}.csv"
    # file_path = f"/home/ubuntu/rcp/data/F.P.Journe-Scrapes_{timestamp}.csv"
    file_path = f"/app/data/F.P.Journe-Scrapes_{timestamp}.csv"

    scrapes_df.to_csv(file_path, index=False)

    print(f"Data saved to {file_path}")
    

 