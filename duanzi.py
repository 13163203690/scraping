import requests
from lxml import etree
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
    # 'referer': 'https://dytt8.net/html/gndy/dyzz/list_23_2.html'
}


def judgment_sex(class_name):
    if class_name == 'womenIcon':
        return '女'
    else:

        return '男'


def parse_page(url):
    response = requests.get(url, headers=headers)
    text = response.text
    users = re.findall('<h2.*?>(.*?)</h2>', text, flags=re.DOTALL)
    sexs = re.findall('<div class="articleGender(.*?)">', text, re.S)
    contents = re.findall('<div class="content">.*?<span>(.*?)</span>', text, re.S)
    laughs = re.findall('<i class="number.*?>(\d+)</i>', text, flags=re.DOTALL)
    info_lists = []
    for value in zip(users, sexs, contents, laughs):
        user, sex, content, laugh = value
        #user=re.sub("\n", "", user)
        content=re.sub("<.*?>", "", content)
        info = {
            'user': user.strip(),
            'sex': judgment_sex(sex),
            'content': content.strip(),
            'laugh': laugh
        }
        info_lists.append(info)
    print(info_lists)
    #保存到本地，可以不保存
    for info_list in info_lists:
        f = open('C:\\Users\\wei\\Desktop\\qiushi.txt', 'a+')
        try:
            f.write(info_list['user'] + '\n')
            f.write(info_list['sex'] + '\n')
            f.write(info_list['content'] + '\n')
            f.write(info_list['laugh'] + '\n')
            f.close()
        except UnicodeEncodeError:
            pass


def spider():
    url = 'https://www.qiushibaike.com/text/page/2/'
    parse_page(url)


if __name__ == '__main__':
    spider()
