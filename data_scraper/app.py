## scrapanje, obrada i punjenje u bazu
import pandas as pd
from requests import request
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# class real_estate(Base):
#     __tablename__ = "realestates"
#     broj_soba = Column(Integer),
#     broj_spavacih_soba = Column(Integer),
#     broj_toaleta = Column(Integer),
#     cijena_km = Column(Integer),
#     kvadratura_m2 = Column(Integer)
#     lokacija_grad = Column(Integer)
    # opis
    # kvadratura
    # cjena
    # eur_cjena
    # mjesto
    # poslovnica


def get_main_page(url_link, real_agency):
    if real_agency == 'remax':
        driver = webdriver.Chrome()
        driver.get(url_link)
        # page_content = request('GET', url = url_link)
        soup = bs(driver.page_source)
        all_links = soup.find_all('a', {'class': 'LinkImage'})
        return ['http://www.remax-bh.ba' + link.attrs['href'] for link in all_links]


def get_real_data(url_link, real_agency):
    if real_agency == 'remax':
        driver = webdriver.Chrome()
        driver.get(url_link)
        # page_content = request('GET', url = url_link)
        soup = bs(driver.page_source)
        re = real_estate()
        re.title = soup.find_all('h2', {'itemprop': 'name'})[0].text or ""
        re.price = soup.find_all('a', {'itemprop': 'price'})[0].text or ""
        re.place = soup.find_all('div', {'class': 'col-xs-12 key-address'})[0].text or ""
        if len(soup.find_all('div', {'class': 'data-item-value'})) > 1:
            re.lot_size = soup.find_all('div', {'class': 'data-item-value'})[0].text or ""
            re.object_size = soup.find_all('div', {'class': 'data-item-value'})[1].text or ""
        else:
            re.object_size = soup.find_all('div', {'class': 'data-item-value'})[0].text or ""
        built_tag = False
        lot_tag = False
        # for i in soup.find_all('div', {'class': 'data-item-row'})[0].children:
        #     if isinstance(i, NavigableString):
        #         continue
        #     for j in i.children:
        #         if isinstance(j, NavigableString):
        #             continue
        #         if j.attrs['title'] == 'Built Area (m²)':
        #             built_tag = True
        #         elif j.attrs['title'] == 'Lot Size (m2)':
        #             lot_tag = True
        #         if built_tag and j.attrs['class'] == 'data-item-value':
        #             re.object_size = j.text
        #         if lot_tag and j.attrs['class'] == 'data-item-value':
        #             re.lot_size = j.text

        re.description = soup.find_all('div', {'itemprop': 'description'})[0].text or ""
        return re


def transform_scraped_data_list():
    pass


def write_into_database(data_to_write):
    data_to_write.to_sql('realestates', engine, if_exists='append')


def transform_csv_data(data):
    data['kvadratura_new'] = data.apply(lambda row: row['kvadratura'].replace("m 2", "").split(" - ")[0].replace(".", ""), axis=1)
    data['cjena_new'] = data.apply(lambda row: row['cjena'].replace(" KM", "").replace("Na upit","0").split(" - ")[0].replace(".", ""), axis=1)
    data_to_write = data[['kvadratura_new', 'cjena_new', 'mjesto']]
    #rename columns
    data_to_write.columns = ['kvadratura_m2', 'cijena_km', 'lokacija_grad']
    return data_to_write


def main(url):
    if scrape:
        counter = 0 # just for the testing phase
        #  get main page of url
        main_page_links = get_main_page(url, 'remax');
        # get data from each individual page
        real_data = []
        for link in main_page_links:
            if counter > 1:
                break
            else:
                counter += 1
            time.sleep(2)
            real_data.append(get_real_data(link, 'remax'))
        # transform the data
        data_to_write = transform_scraped_data_list(real_data)

    if load_from_excel:
        data = pd.read_csv('./data/prostor_cijene.csv')
        data_to_write = transform_csv_data(data)
    write_into_database(data_to_write)

if __name__ == '__main__':
    url = 'http://www.remax-bh.ba/PublicListingList.aspx#mode=gallery&tt=261&cr=2&cur=BAM&la=All&sb=PriceIncreasing&page=1&sc=82&sid=0452cd51-ff11-42b1-88fc-7960a847970e'
    scrape = False
    engine = create_engine('postgresql://postgres:thinkcentre@localhost/realestate_proj')
    load_from_excel  = True
    main(url)
