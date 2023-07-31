import sqlite3
import tqdm

from tools import *

def main():
    db_path = "../product_database.db"

    conn = sqlite3.connect(db_path)
    create_table(conn)
    
    #homedepot sitemap
    detail_list = get_links('https://www.homedepot.com/sitemap/d/pip_sitemap.xml')

    #Attempts to access product page and fetch product details saved in SQL table. 
    for page in tqdm.tqdm(detail_list):
        try:
            temp_links = get_links(page)
            for product_link in temp_links:
                try:
                    product_info = get_product_info_json(product_link)
                    insert_row(conn, tuple(product_info.values()))
                    
                except Exception:
                    pass
        except Exception:
            pass

    conn.close()

if __name__ == "__main__":
    main()