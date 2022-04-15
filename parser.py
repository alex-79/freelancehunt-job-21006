#!/usr/bin/python3

import os
import requests
from bs4 import BeautifulSoup
import json

base_url = 'https://makeup.com.ua'
path = 'result'


def getPage(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def getNextPage(page):
    paginator = page.select('div.catalog-page-list-wrap > ul > li')
    check_flag = False
    for item in paginator:
        if check_flag:
            if item.a:
                return item.a.get('href')
            else:
                return False
        if item.input.has_attr('checked'):
            check_flag = True
    return False


def getReview(url):

    print(url)
    page = getPage(url)

    id = page.find('meta', attrs={"itemprop": "productID"}).get('content')

    reviews = page.find_all('li', attrs={"itemprop": "review"})
    list = []
    for review in reviews:
        data = {}
        data['author'] = review.find('span', attrs={"itemprop": "author"}).text
        data['date'] = review.find('meta', attrs={"itemprop": "datePublished"}).get('content')
        data['rating'] = review.find('meta', attrs={"itemprop": "ratingValue"}).get('content')
        data['review'] = review.find('p', attrs={"itemprop": "reviewBody"}).text

        list.append(data)

    if len(list):
        result = {}
        result[id] = list

        f = open(path + '/' + id + '.json', 'w', encoding='utf-8')
        f.write(json.dumps(result, ensure_ascii=False))
        f.close()


def parser(url):
    page = getPage(url)

    reviews = page.find_all('div', attrs={"class": "simple-slider-list__reviews"})
    for review in reviews:
        if review.a:
            review_url = base_url + review.a.get('href')
            getReview(review_url)

            # exit()

    url = getNextPage(page)
    if url:
        parser(base_url + '/ua' + url)


def main():

    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

    home_page = getPage(base_url + '/ua/')
    categories = home_page.find_all('li', attrs={"class": "menu-column-list__item"})

    for category in categories:
        category_url = base_url + category.a.get('href')
        parser(category_url)

        exit()


main()
