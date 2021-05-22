import requests
import re
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
def parse_page(results,text):
    titles_ret = re.findall(r'<div class="p-name.*?>.*?<em>(.*?)</em>.*?</div>', text, flags=re.DOTALL)
    titles=[]
    for title in titles_ret:
        temp = re.sub("<.*?>", "",title)
        titles.append(temp.strip())
    print('title', titles)
    prices = re.findall(r'<div class="p-price">.*?<i>(.*?)</i>.*?</div>', text,flags=re.DOTALL)
    hrefs=re.findall(r'<div class="p-name.*?>.*?<a.*?href="(.*?)".*?>.*?</div>', text, flags=re.DOTALL)
    for value in zip(titles, prices, hrefs):
        title, price,href = value
        results.append([title, price,href])
    return results


def getHTMLText(url):
    '''从网络上获取网页内容'''
    try:
        r = requests.get(url, headers=headers,timeout=40)
        # #如果状态不是200，就会引发HTTPError异常
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def printGoodsList(ilt):
    tplt = "{:4}\t{:8}\t{:40}\t{:60}"
    print(tplt.format("序号", "价格", "链接","商品名称"))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g[1], g[2],g[0]))

def main():
    keyword ='女装套装'
    base_url='https://search.jd.com/Search?keyword='+keyword
    num=5
    list=[]
    for x in range(1,num+ 1):
        url=base_url+'&page=%d'% x
        print(url)
        text = getHTMLText(url)
        list = parse_page(list,text)
    printGoodsList(list)
if __name__ == '__main__':
    main()