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

def getPageAjax(url):
    response = requests.get(url).json()
    return BeautifulSoup(response['html'], 'html.parser')


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

    print('  > ' + url)
    page = getPage(url)

    id = page.find('meta', attrs={"itemprop": "productID"}).get('content')

    review_base_url = 'https://makeup.com.ua/ua/ajax/comments/{id}/{offset}/0/'

    list = []
    offset = 0
    flag = True
    while flag:
        review_url = review_base_url.format(id = id, offset = offset)
        print('    ~ ' + review_url)
        page = getPageAjax(review_url)

        reviews = page.find_all('li', attrs={"class": "comments-list__item"})

        if len(reviews):
            for review in reviews:
                data = {}
                data['url'] = url
                data['author'] = review.find('span', attrs={"class": "review-author-name"}).text
                data['date'] = review.find('time', attrs={"class": "comment__time"}).text
                if review.find('meta', attrs={"itemprop": "ratingValue"}):
                    data['stars'] = review.find('meta', attrs={"itemprop": "ratingValue"}).get('content')
                else:
                    data['stars'] = ''
                data['title'] = ''
                data['content'] = review.find('div', attrs={"class": "comment-user-data"}).p.text
                if review.find('img', attrs={"class": "disscuss-img"}):
                    data['image'] = review.find('img', attrs={"class": "disscuss-img"}).get('src')
                else:
                    data['image'] = ''

                list.append(data)
            offset += 10        
        else:
            flag = False

    if len(list):
        f = open(path + '/' + id + '.json', 'w', encoding='utf-8')
        f.write(json.dumps(list, ensure_ascii=False))
        f.close()


def parser(url):

    print('* ' + url)
    page = getPage(url)

    catalog = page.find('div', attrs={"class": "catalog-products"})
    reviews = catalog.findAll('div', attrs={"class": "simple-slider-list__reviews"})
    
    i = 0
    for review in reviews:
        if review.a:
            review_url = base_url + review.a.get('href')
            getReview(review_url)
            
            i += 1
            if i == 3:
                return

    url = getNextPage(page)
    if url:
        parser(base_url + '/ua' + url)


def main():

    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

    home_page = getPage(base_url)
    categories = home_page.find_all('li', attrs={"class": "menu-column-list__item"})

    i = 0

    for category in categories:
        category_url = base_url + category.a.get('href')
        parser(category_url)

        i += 1
        if i == 3:
            exit()


main()
