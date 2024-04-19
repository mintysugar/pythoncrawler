import requests
import xlwt
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/123.0.0.0 Safari/537.36'}


def save_to_excel(soup):
    list = soup.find(class_='grid_view').find_all('li')
    for item in list:
        item_index = item.find(class_='').string
        item_img = item.find('a').find('img').get('src')
        item_name = item.find(class_='title').string
        item_author = item.find('p').text
        item_score = item.find(class_='rating_num').string

        sheet.write(int(item_index), 0, item_index)
        sheet.write(int(item_index), 1, item_img)
        sheet.write(int(item_index), 2, item_name)
        sheet.write(int(item_index), 3, item_author)
        sheet.write(int(item_index), 4, item_score)


def main(page):
    url_douban = 'https://movie.douban.com/top250?start=' + str(page*25) + '&filter='
    html = request_douban(url_douban)
    soup = BeautifulSoup(html, 'lxml')
    save_to_excel(soup)


def request_douban(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


if __name__ == "__main__":
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)

    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
    sheet.write(0, 0, '排名')
    sheet.write(0, 1, '图片')
    sheet.write(0, 2, '电影名')
    sheet.write(0, 3, '导演&主演')
    sheet.write(0, 4, '评分')
    sheet.write(0, 5, '推荐语')

    for i in range(0, 10):
        main(i)
    book.save('豆瓣最受欢迎的250部电影.xls')
