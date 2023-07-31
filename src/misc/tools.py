import pandas as pd
import bs4 as bs
import urllib.request
import sqlite3
import json

def get_links(url):
    #scrape all urls from specific webpage and returns as list
    source = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(source,features="xml")
    
    return [url.text.strip() for url in soup.find_all('loc')]

def get_product_info_json(url):
    #scrape product detail page for product information. Return json containing information.
    source = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(source,'lxml')
    
    product_description = soup.find('script', id='thd-helmet__script--productStructureData')
    description_json = json.loads(product_description.contents[0])
    
    reorganized_data = {
        'name': description_json['name'],
        'description': description_json['description'],
        'color': description_json['color'],
        'brandName': description_json['brand']['name'],
        'url': description_json['offers']['url'],
        'price': description_json['offers']['price']
    }
    
    return reorganized_data

def create_table(conn):
    # Create the table if it doesn't exist
    query = '''
    CREATE TABLE IF NOT EXISTS my_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        color TEXT,
        brandName TEXT,
        url TEXT,
        price REAL
    );
    '''
    conn.execute(query)

def insert_row(conn, data):
    # Insert a row into sql table
    insert_query = '''
    INSERT INTO my_table (
        name, description, color, brandName, url, price
    ) VALUES (?, ?, ?, ?, ?, ?);
    '''
    conn.execute(insert_query, data)
    conn.commit()
    
def read_db_to_dataframe(db_path):
    # Returns table in pd.DataFrame
    conn = sqlite3.connect(db_path)

    query = "SELECT * FROM my_table;"
    df = pd.read_sql_query(query, conn)

    # Close the connection
    conn.close()

    return df
