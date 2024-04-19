import json
import re
import requests


def main(page):
    url_dangdang = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-' + str(page)
    html = request_dangdang(url_dangdang)
    items = parse_result(html)  # 解析过滤我们想要的信息

    for item in items:
        print(item)


def request_dangdang(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def parse_result(html):
    pattern = re.compile('<li>.*?list_num.*?(\d+).</div>'
                         '.*?<img src="(.*?)"'
                         '.*?class="name".*?title="(.*?)">'
                         '.*?class="star">.*?class="tuijian">(.*?)</span>'
                         '.*?class="publisher_info">.*?target="_blank">(.*?)</a>'
                         '.*?class="publisher_info">.*?target="_blank">(.*?)</a>'
                         '.*?class="biaosheng">.*?<span>(.*?)</span></div>'
                         '.*?class="price_n">&yen;(.*?)</span>.*?</li>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'range': item[0],
            'iamge_url': item[1],
            'title': item[2],
            'recommend': item[3],
            'author': item[4],
            'publisher': item[5],
            'star_times': item[6],
            'price': item[7]
        }


def write_item_to_file(item):
    with open('book.txt', 'a', encoding='UTF-8') as f:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')
        f.close()


if __name__ == "__main__":
    for i in range(1, 26):
        main(i)
