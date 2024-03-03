import requests
from lxml import etree
import re
import os
import time
import random
from fake_useragent import UserAgent
import openpyxl
from concurrent.futures import ThreadPoolExecutor
import tqdm


def get_weibo(url):
    response = requests.get(url, headers=header, timeout=10)
    return response.text



def article_content(content, title, filtering_word):

    blogger_name = content.xpath(
        './div[@class="card"]/div[@class="card-feed"]/div[@class="content"]/div[@class="info"]/div[2]/a[1]/text()')[
        0]

    content_texts = content.xpath(
        './div[@class="card"]/div[@class="card-feed"]/div[@class="content"]/p[@class="txt"]')
    for txt in content_texts:
        content_texts = txt.xpath('./text()')
    content_text = ''.join(content_texts).strip().replace('\n', '').replace('【', '').replace('】', '')
    if filtering_word not in content_text:
        return blogger_name, None, content_text

    try:
        date = content.xpath(
            './div[@class="card"]/div[@class="card-feed"]/div[@class="content"]/p[@class="from"]/a[1]/text()')[
            0].strip()
    except IndexError:
        date = content.xpath(
            './div[@class="card"]/div[@class="card-feed"]/div[@class="content"]/div[@class="from"]/a[1]/text()')[
            0].strip()

    try:
        try:
            source = content.xpath(
                './div[@class="card"]/div[@class="card-feed"]/div[@class="content"]/p[@class="from"]/a[2]/text()')[
                0].strip()
        except IndexError:
            source = content.xpath(
                './div[@class="card"]/div[@class="card-feed"]/div[@class="content"]/div[@class="from"]/a[2]/text()')[
                0].strip()
    except IndexError:
        source = ""

    number_forwards = ""
    comment_number = ""
    number = content.xpath('./div[@class="card"]/div[@class="card-act"]/ul/li')
    if len(number) == 4:

        number_forwards = \
            content.xpath('./div[@class="card"]/div[@class="card-act"]/ul/li[2]/a/text()')[0].replace('转发', '').strip()

        comment_number = \
            content.xpath('./div[@class="card"]/div[@class="card-act"]/ul/li[3]/a/text()')[0].replace('评论', '').strip()

    if len(number) == 3:

        number_forwards = content.xpath('./div[@class="card"]/div[@class="card-act"]/ul/li[1]/a//text()')[1].strip()
        comment_number = content.xpath('./div[@class="card"]/div[@class="card-act"]/ul/li[2]/a//text()')[0].strip()

    try:
        number_forwards = int(number_forwards)
        number_forwards = str(number_forwards)
    except:
        number_forwards = 0

    try:
        comment_number = int(comment_number)
        comment_number = str(comment_number)
    except:
        comment_number = 0

    try:
        try:
            like_number = content.xpath('./div[@class="card"]/div[@class="card-act"]/ul/li[4]/a/em/text()')[0].replace(
                '赞', '0')
        except IndexError:
            like_number = content.xpath(
                './div[@class="card"]/div[@class="card-act"]/ul/li[3]/a/button[@class="woo-like-main toolbar_btn"]/span[@class="woo-like-count"]/text()')[
                0].replace('赞', '0')
    except IndexError:
        like_number = ""

    try:
        try:
            authentication = content.xpath(
                './div[@class="card"]/div[@class="card-feed"]/div[@class="content"]/div[@class="info"]/div[2]/a[2]/@title')[
                0]
        except IndexError:
            authentication = content.xpath(
                './div[@class="card"]/div[@class="card-feed"]/div[@class="avator"]/a/span/@title')[0]
    except IndexError:
        authentication = ""
    print(blogger_name, content_text, date, source, authentication, number_forwards, comment_number, like_number)

    if os.path.exists(f'Collected Data/{title}/博文信息/博文txt.txt'):
        with open(f'Collected Data/{title}/博文信息/博文txt.txt', "r", encoding="utf-8") as f:
            m = 1
            for line in f:
                if blogger_name == line.strip().split('$%')[0] and content_text == line.strip().split('$%')[
                    1] and date == line.strip().split('$%')[2]:

                    m = 2
                    break
            if m == 1:
                with open(f'Collected Data/{title}/博文信息/博文txt.txt', "a", encoding="utf-8") as b:
                    b.write(
                        f"{blogger_name}$%{content_text}$%{date}$%{source}$%{authentication}$%{number_forwards}$%{comment_number}$%{like_number}\n")

    else:
        with open(f'Collected Data/{title}/博文信息/博文txt.txt', "a", encoding="utf-8") as f:
            f.write(
                f"{blogger_name}$%{content_text}$%{date}$%{source}$%{authentication}$%{number_forwards}$%{comment_number}$%{like_number}\n")

    workbook = openpyxl.Workbook()
    wb = workbook.active
    wb.title = "博文"
    with open(f'Collected Data/{title}/博文信息/博文txt.txt', "r", encoding="utf-8") as w:
        i = 1
        for line in w:
            if line.startswith('\n'):
                continue

            try:
                blogger_name = line.strip().split('$%')[0]
                content_text = line.strip().split('$%')[1]
                date = line.strip().split('$%')[2]
                source = line.strip().split('$%')[3]
                authentication = line.strip().split('$%')[4]
                number_forwards = line.strip().split('$%')[5]
                comment_number = line.strip().split('$%')[6]
                like_number = line.strip().split('$%')[7]
            except:
                continue
            if i == 1:
                wb.append(['博主名称', '博文内容', '发表时间', '来源', '认证', '转发数量', '评论数量', '获赞数量']) #Header of the collected dataset
            wb.append([blogger_name, content_text, date, source, authentication, number_forwards, comment_number,
                       like_number])
            i += 1
            workbook.close()
    workbook.save(f"Collected Data/{title}/博文信息/博文.xlsx")
    return blogger_name, comment_number, content_text



def comment_information(mid, uid, max_id, page):
    page_url = "https://weibo.com/ajax/statuses/buildComments?"
    if page == 1:
        param = {
            "is_reload": 1,
            "id": mid,
            "is_show_bulletin": 2,
            "is_mix": 0,
            "count": 20,
            "uid": uid
        }
        response = requests.get(page_url, headers=header, params=param, timeout=10)
        return response.json()
    else:
        param = {
            "flow": 0,
            "is_reload": 1,
            "id": mid,
            "is_show_bulletin": 2,
            "is_mix": 0,
            "max_id": max_id,
            "count": 20,
            "uid": uid
        }
        response = requests.get(page_url, headers=header, params=param, timeout=10)
        return response.json()


def download_comment(comment_json, wb, page, text_raw):
    comment_list = comment_json['data']
    n = 1
    for comment in comment_list:

        name = comment['user']['screen_name']

        content = comment['text_raw']

        date = comment['created_at']

        try:
            source = comment['source']
        except KeyError:
            source = ""

        like_counts = comment['like_counts']
        if page == 1 and n == 1:
            wb.append(["用户名称", "评论内容", "评论时间", "发布地域", "点赞数量", "博文内容"])
            wb.append([name, content, date, source, like_counts, text_raw])

        else:
            wb.append([name, content, date, source,  like_counts])
        print(name, content, date, source,  like_counts)
        n += 1


def dispatch(urls, c_num, filtering_word, KEYWORD):

    source_code = get_weibo(urls)
    etree_html = etree.HTML(source_code)
    title = KEYWORD

    if not os.path.exists('Collected Data'):
        os.mkdir('Collected Data')
    if not os.path.exists(f"Collected Data/{title}"):
        os.mkdir(f"Collected Data/{title}")
    if not os.path.exists(f"Collected Data/{title}/博文信息"):
        os.mkdir(f"Collected Data/{title}/博文信息")
    if not os.path.exists(f"Collected Data/{title}/评论信息"):
        os.mkdir(f"Collected Data/{title}/评论信息")

    content_list = etree_html.xpath('//div[@id="pl_feedlist_index"]/div/div[@class="card-wrap"]')

    for content in content_list:
        try:
            mid = content.xpath('./@mid')[0]
            uids = content.xpath('./div[@class="card"]/div[@class="card-act"]/ul/li[1]/a/@action-data')[0]
            uid = re.findall('&uid=(.*?)&', uids)[0]
        except IndexError:
            continue
        blogger_name, comment_number, content_text = article_content(content, title, filtering_word)
        if comment_number == None:
            print(f"The text does not contain the word 'filtering_word'; skipped!")
            continue

        if int(comment_number) < c_num:

            time.sleep(random.uniform(2.5, 4.5))
            continue

        if os.path.exists(f"Collected Data/{title}/评论信息/{blogger_name}.xlsx"):
            blogger_name = f"{blogger_name} {int(time.time() * 1000)}"
        workbook = openpyxl.Workbook()
        wb = workbook.active
        wb.title = blogger_name
        page = 1
        max_id = ""
        while True:
            comment_json = comment_information(mid, uid, max_id, page)
            if len(comment_json['data']) == 0:
                tq_list = [x for x in range(100)]
                for _ in zip(tqdm.tqdm(range(len(tq_list)))): #Server detected no response; program paused for 5 seconds before automatic retry.
                    time.sleep(0.05)
                comment_json = comment_information(mid, uid, max_id, page)
                if len(comment_json['data']) == 0:
                    print(f"{blogger_name} 仍无评论信息返回,程序执行跳过措施!") #No comments returned; program execution skipped as a precautionary measure.
                    break
            download_comment(comment_json, wb, page, content_text)
            if comment_json['max_id'] == 0:
                workbook.save(f'Collected Data/{title}/评论信息/{blogger_name}.xlsx')
                break
            else:
                max_id = comment_json['max_id']
            page += 1
            workbook.save(f'Collected Data/{title}/评论信息/{blogger_name}.xlsx')
            time.sleep(random.uniform(3.5, 5.5))


def main(main_url, t_num, c_num, filtering_word, KEYWORD, date_start, date_termination):

    n = 0
    urls_list = []
    try:
        source_code_url = get_weibo(main_url)
        source_code_url_list = etree.HTML(source_code_url)
        url_list = source_code_url_list.xpath(
            '//div[@id="pl_feedlist_index"]/div[@class="m-page"]/div/span/ul[@class="s-scroll"]/li')
        if len(url_list) == 0:
            n = 1
            url_list = [main_url]
    except:
        n = 1
        url_list = [main_url]
    if n == 0:
        for urls in url_list:
            url = urls.xpath('./a/@href')[0]
            url = "https://s.weibo.com/" + url
            urls_list.append(url)
    else:
        urls_list = url_list
    print(f"{date_start} ~ {date_termination}共有{len(urls_list)}页")
    with ThreadPoolExecutor(t_num) as t:
        for urls in urls_list:
            t.submit(dispatch, urls, c_num, filtering_word, KEYWORD)


if __name__ == '__main__':
    cookies = []
    day_list = []
    month = ""
    with open("Weibo_cookie.txt", "r", encoding="utf-8") as fw:
        for i in fw:
            if i.startswith('\n'):
                continue
            cookies.append(i.strip())
    header = {
        "user-agent": UserAgent().chrome,
        "cookie": random.choice(cookies)
    }
    filtering_word = "方舱"


    KEYWORD = "方舱医院"

    t_num = 2

    c_num = 2


    year_list = [2022]

    month_list = [11]
    for year in year_list:
        for months in month_list:

            if months in [1, 3, 5, 7, 8, 10, 12]:
                day_list = [i for i in range(1, 32)]
            if months in [2, 4, 6, 9, 11]:
                day_list = [i for i in range(1, 31)]
            if months == 2:
                day_list = [i for i in range(1, 29)]
            for day in day_list:
                if int(months) < 10:
                    month = f"0{months}"
                if int(months) >= 10:
                    month = int(months)
                if int(day) < 10:
                    day = f"0{int(day)}"

                date_start = f"{year}-{month}-{day}"

                date_termination = f"{year}-{month}-{day}"
                main_url = f"https://s.weibo.com/weibo?q={KEYWORD}&typeall=1&suball=1&timescope=custom%3A{date_start}%3A{date_termination}&Refer=g"
                main(main_url, t_num, c_num, filtering_word, KEYWORD, date_start, date_termination)
