import requests
from lxml import etree
#from openpyxl  import Workbook
# URL = 'https://dytt8.net/html/gndy/dyzz/list_23_1.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    # 'referer': 'https://dytt8.net/html/gndy/dyzz/list_23_2.html'
}
BASE_DOMIN = 'https://dytt8.net/'


# 进入详情页获取详细信息
def parse_detail_page(url):
    response = requests.get(url, headers=headers)
    text = response.content.decode('gbk')
    html = etree.HTML(text)
    title = html.xpath("//h1/font[@color='#07519a']/text()")[0]
    ZoomE = html.xpath("//div[@id='Zoom']")[0]
    cover = ZoomE.xpath('.//img/@src')
    infos = ZoomE.xpath(".//text()")
    for index, info in enumerate(infos):
        if info.startswith("◎年　　代"):
            year = info.replace("◎年　　代", "").strip()
        if info.startswith("◎豆瓣评分"):
            douban_rating = info.replace("◎豆瓣评分", '').strip()
        if info.startswith("◎片　　长"):
            duration=info.replace("◎片　　长", '').strip()
            # 获取影片导演
        if info.startswith('◎导　　演'):
            director = info.replace('◎导　　演', '').strip()
        # 获取影片编剧
        if info.startswith('◎编　　剧'):
            scenarists = [info]
            for x in range(index + 1, len(infos)):
                scenarist = infos[x]
                if scenarist.startswith("◎"):
                    break
                scenarists.append(scenarist.strip())
        if info.startswith("◎主　　演"):
            # 从当前位置，一直往下面遍历
            actors = [info]
            for x in range(index + 1, len(infos)):
                actor = infos[x]
                if actor.startswith("◎"):
                    break
                actors.append(actor.strip())
            #print(",".join(actors))

    try:
        info = {
            'title': title,
            'cover': cover,
            'year': year,
            'duration': duration,  # 部分页面没有
            'douban_rating': douban_rating,
            'director': director,
            'scenarist': scenarist,
            'actor': actor,
        }
    except:
        pass
    return info



# 获取影片的详情页url
def get_detail_urls(url):
    response = requests.get(url, headers=headers)
    text = response.text
    # print(text)
    html = etree.HTML(text)
    detail_urls = html.xpath('//a[@class="ulink"]/@href')
    detail_urls = map(lambda url: BASE_DOMIN + url, detail_urls)
    # for detail_url in detail_urls:
    #     print('get_detail_urls detail_urls ',detail_url)
    return detail_urls

#将信息写入excel中
# def save_excel(infos):
#     wb = Workbook()
#     dest_filename = '电影天堂最新电影.xlsx'
#     ws1 = wb.active
#     ws1.title = "电影"
#
#     #打印表头
#     _ = ws1.cell(column=1, row=1, value="{0}".format('标题'))
#     _ = ws1.cell(column=2, row=1, value="{0}".format('封面URL'))
#     _ = ws1.cell(column=3, row=1, value="{0}".format('年份'))
#     _ = ws1.cell(column=4, row=1, value="{0}".format('时长'))
#     _ = ws1.cell(column=5, row=1, value="{0}".format('导演'))
#     _ = ws1.cell(column=6, row=1, value="{0}".format('编剧'))
#     _ = ws1.cell(column=7, row=1, value="{0}".format('主演'))
#
#     row = 2
#     for info in infos:
#         clo=1
#         for key,value in info.items():
#             _ = ws1.cell(column=clo, row=row, value="{0}".format(value))
#             clo += 1
#         row += 1
#
#     wb.save(filename=dest_filename)
def spider():
    base_url = 'https://dytt8.net/html/gndy/dyzz/list_23_{}.html'
    movies = []
    for x in range(1, 4):
        print('正在爬取第{}页：'.format(x))
        url = base_url.format(x)
        detail_urls = get_detail_urls(url)
        for detail_url in detail_urls:
            #print('spider', detail_url)
            movie = parse_detail_page(detail_url)
            movies.append(movie )
            print(movie)
    #save_excel(movies)
if __name__ == '__main__':
    spider()
