# TODO
# 1. Make a request to the ebay.com and a page
# 2. Collect data from each detail page
# 3. Collect all links to detail page
# 4. Write scraped data to a csv file

import requests
from bs4 import BeautifulSoup
import csv


def get_page(url):
    response = requests.get(url)

    if not response.ok:
        print('Server responded:', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_detail_data(soup):
    try:
        title = soup.find('h1', id='itemTitle').text.strip('Details about   ')
    except:
        title = ''
    # print(title)

    try:
        price = soup.find('span', id="prcIsum")
        currency = price.text.split(' ')[0]
        price = price.get('content')
    except:
        price = ''
    # print(price)
    # print(currency)

    try:
        sold = soup.find('a', class_='vi-txt-underline').text.split(' ')[0]
    except:
        sold = ''
    # print(sold)

    data = {
        'title': title,
        'price': price,
        'currency': currency,
        'total_sold': sold
    }

    return data


def get_index_data(soup):
    try:
        links = soup.find_all('a', class_='s-item__link')
    except:
        links = []

    urls = [item.get('href') for item in links]

    # print(urls)
    return urls


def write_csv(data, url):
    with open('output.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)

        row = [data['title'], data['price'], data['currency'], data['total_sold'], url]

        writer.writerow(row)


def main():
    """url = 'https://www.ebay.com/itm/233946842651?_trkparms=ispr%3D1&hash=item367851861b:g:KssAAOSwCChgYcVU&amdata=enc' \
          '%3AAQAGAAACkPYe5NmHp%252B2JMhMi7yxGiTJkPrKr5t53CooMSQt2orsSRAQR8FABHjfpFoyRlXhWmT2iBpHl3ge2CWMdbL5WaD' \
          '%252Ffw6H19aQ7V5PD6wt3PFs7W3U%252F1ywXmmdwmIr0W%252Bs%252B0qVqpS73t8pYSqpgEh2ciqfN' \
          '%252FOx9787i1zWmED6cnGeSEF24f7ttz2twb3sN6p6eBAl' \
          '%252FjDW2upFmkj9vybvCXWbVIZx1QTUDblHZtJp9LMg402SUZhymlNjC2iz' \
          'E03Ru7LCOt0aEkcW4kGWveeME2pPM9tOM4KyoJgSf11sw1qQBpLIlhZr79Pcz2UIhvc' \
          'GBSZTJaZl%252Ff4dCV4%252BMUvJBOsW5WH6XPvjXwctBptxPhi5z6k0jQYYJfo%25' \
          '2B2Rj89edh1TcMMP7GXiJz6zoBIdPVKDCAHpc5hU0L5td3VnjjNtFo2jNNod5seXOE' \
          'zWBbSouhKPqcW4jOsO4rkhuHQ%252B6fXfU0HcwtrUoxGd2Advsh6XUAzu0f4zVBhT' \
          '%252FXIjWlZs2QwKducX9qxtmc9AEN3VkWdReLiSWVZd8%252BWziEpSU3Lj8POR6' \
          'hXBjyBF6XGC4Rq2H26W1smJTNi1HpCVgDGdWbMSe%252BtF7WD9bAHS%252B4ynu' \
          'EEGH5HVx%252BSwrr9AJhfEE6gohudlEf0nSBfoZK8loQx0LrxfEbb8P9KPhf' \
          'WUMJ%252FNRPDl9AKbKE3OHjJtD2PEwXyvG2w%252BowhEfFvTZqHqg7pafHr' \
          'F6IaB%252FaqLi6rBhTUV0Z18iCqoHWdaXhJS5GUK1l42p3cl51inz%252FPlU' \
          '1agVJh7jpDHGQO49qQV99FSqXq3N4WWxVqYSXk%252FoxNxDElRygSczuy5hmOT' \
          'b2XfpwmSQaYv3Ks1ampfbaI2mP7MJ5X2O6YqIO6%7Campid%3APL_CLK%7Cclp%3A2334524 '"""

    url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=skmei+mens+waterproof&_sacat=0&LH_TitleDesc=0&_pgn=2'
    # get_detail_data(get_page(url))
    # get_index_data(get_page(url))
    products = get_index_data(get_page(url))

    for link in products:
        try:
            data = get_detail_data(get_page(link))
            write_csv(data, link)
        except:
            print('no data')


if __name__ == '__main__':
    main()
