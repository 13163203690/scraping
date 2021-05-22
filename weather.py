# 爬取全国所有城市名称和最低气温

# http://www.weather.com.cn/textFC/hb.shtml
import requests
from bs4 import BeautifulSoup
from pyecharts.charts import Bar

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    # 'referer': 'https://dytt8.net/html/gndy/dyzz/list_23_2.html'
}
ALL_DATA = []
def parse_page(url):
    response = requests.get(url,headers)
    text = response.content.decode('utf-8') # 解决乱码
    soup = BeautifulSoup(text,'html5lib')#增强容错性，使用lxml港澳台的时候会出错
    # 网页解析
    conMidtab = soup.find('div',class_= 'conMidtab')
    # table
    tables = conMidtab.find_all('table')
    # tr
    for table in tables:
        #print(table)
        trs = table.find_all("tr")[2:]
        for index, tr in enumerate(trs):
            tds = tr.find_all('td')
            city_td=tds[0]
            if index==0:
                city_td = tds[1]
            city = list(city_td.stripped_strings)[0] # 打印子孙节点的文本
            temp_td = tr.find_all('td')[-2]
            temp = list(temp_td.stripped_strings)[0]
            ALL_DATA.append({"城市": city, "最低气温": int(temp)})
            print(city,temp)


def main():

    #parse_page('http://www.weather.com.cn/textFC/gat.shtml')
    areas = ['hb','hd','gat','xn','xb','gat']
    for area in areas:
        url = 'http://www.weather.com.cn/textFC/{}.shtml'.format(area)
        parse_page(url)
    ALL_DATA.sort(key=lambda data:data["最低气温"])
    min_data = ALL_DATA[:20]
    cities_min = list(map(lambda x:x["城市"], min_data))
    min_temp = list(map(lambda x:x["最低气温"], min_data))


    bar1 = Bar()
    bar1.add_xaxis(cities_min)
    bar1.add_yaxis("气温/℃", min_temp)
    bar1.set_global_opts(title_opts={"text": "中国城市气温排行榜", "subtext": "最低气温"})
    bar1.render("最低气温.html")


if __name__ == '__main__':
    main()

