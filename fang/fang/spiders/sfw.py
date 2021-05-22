import scrapy
import re
from fang.items import NewHouseItem,ESFHouseItem

class SfwSpider(scrapy.Spider):
    name = 'sfw'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        trs=response.xpath('.//div[@class="outCont"]//tr')
        provice = None
        for tr in trs:
            # 排除掉第一个td，两个第二个和第三个td标签
            tds = tr.xpath(".//td[not(@class)]")
            provice_td = tds[0]
            provice_text = provice_td.xpath(".//text()").get()
            # 如果第二个td里面是空值，则使用上个td的省份的值
            provice_text = re.sub(r"\s", "", provice_text)
            if provice_text:
                provice = provice_text
            # 排除海外城市
            if provice == '其它':
                continue
            city_td=tds[1]
            city_links = city_td.xpath(".//a")
            for city_link in city_links:
                city = city_link.xpath(".//text()").get()
                city_url = city_link.xpath(".//@href").get()
                # print("省份：",provice)
                # print("城市：",city)
                # print("城市链接：",city_url)
                # 下面通过获取的city_url拼接出新房和二手房的url链接
                # 城市url：https://sz.fang.com/
                # 新房url:https://sz.newhouse.fang.com/house/s/
                # 二手房：https://sz.esf.fang.com/
                url_module = re.split('[.//]',city_url)
                scheme = 'https://'#url_module[0] =http: 使用这个会重定向到https:
                domain = url_module[2]  # cq.fang.com/
                if 'bj' in domain:
                    newhouse_url = 'https://newhouse.fang.com/house/s/'
                    esf_url = 'https://esf.fang.com/'
                else:
                    # 新房url
                    newhouse_url = scheme + domain + ".newhouse." + "fang.com/house/s/"
                    # 二手房url
                    esf_url = scheme + domain + ".esf.fang.com"
                #print("新房链接：",newhouse_url)
                #print("二手房链接：",esf_url)
                yield scrapy.Request(url=newhouse_url,callback=self.parse_newhouse,
                                     meta={'info': (provice, city)}
                                     )
                yield scrapy.Request(url=esf_url,callback=self.parse_esf,meta={'info': (provice, city)})

            break#只获取了表格中一行城市的数据



    def parse_newhouse(self,response):
        #新房
        provice,city = response.meta.get('info')
        lis=response.xpath("//div[contains(@class,'nl_con')]/ul/li")
        for li in lis:
            name=li.xpath('.//div[@class="nlcd_name"]/a/text()').get()
            #print(name)

            if name:
                name = re.sub(r"\s", "", name)
                house_type_list = li.xpath(".//div[contains(@class,'house_type')]/a/text()").getall()
                house_type_list = list(map(lambda x: re.sub(r"\s", "", x), house_type_list))
                rooms = list(filter(lambda x: x.endswith("居"), house_type_list))
                # 面积
                area = "".join(li.xpath(".//div[contains(@class,'house_type')]/text()").getall())
                area = re.sub(r"\s|－|/", "", area)
                # 地址
                address = li.xpath(".//div[@class='address']/a/@title").get()
                address = re.sub(r"[请选择]", "", address)
                sale = li.xpath(".//div[contains(@class,'fangyuan')]/span/text()").get()
                price = "".join(li.xpath(".//div[@class='nhouse_price']//text()").getall())
                price = re.sub(r"\s|广告|\t|\n", "", price)
                # 详情页url
                origin_url = li.xpath(".//div[@class='nlcd_name']/a/@href").get()

                item = NewHouseItem(
                    name=name,
                    rooms=rooms,
                    area=area,
                    address=address,
                    sale=sale,
                    price=price,
                    origin_url=origin_url,
                    provice=provice,
                    city=city
                )
                yield item
        #next_url = response.xpath("//div[@class='page']//a[@class='next']/@href").get()
        next_url = response.xpath("//div[@class='page']//a[@class='active']/following-sibling::a[1]/@href").get()
        #next_url = response.urljoin(next_url)
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),
                                 callback=self.parse_newhouse,
                                 meta={'info': (provice, city)}
                                 )

    def parse_esf(self,response):
        #二手房
        provice, city = response.meta.get('info')
        dls = response.xpath("//div[@class='shop_list shop_list_4']/dl")
        for dl in dls:
            item = ESFHouseItem(provice=provice, city=city)
            name=dl.xpath(".//span[@class='tit_shop']/text()").get()
            if name:
                name = re.sub(r"\s", "", name)
                print(name)
                infos = dl.xpath(".//p[@class='tel_shop']/text()").getall()
                infos = list(map(lambda x: re.sub(r"\s", "", x), infos))

                for info in infos:
                    if "厅" in info:
                        item["rooms"] = info
                    elif '层' in info:
                        item["floor"] = info
                    elif '向' in info:
                        item['toward'] = info
                    elif '㎡' in info:
                        item['area'] = info
                    elif '年建' in info:
                        item['year'] = re.sub("年建", "", info)
                item['address'] = dl.xpath(".//p[@class='add_shop']/span/text()").get()
                # 总价
                price= "".join(dl.xpath(".//span[@class='red']//text()").getall())
                price = re.sub(r"\s|广告|\t|\n", "", price)
                item['price'] =price
                # 单价
                item['unit'] = dl.xpath(".//dd[@class='price_right']/span[2]/text()").get()
                item['name'] = name
                detail = dl.xpath(".//h4[@class='clearfix']/a/@href").get()
                item['origin_url'] = response.urljoin(detail)
                print(item)
                yield  item
            #下一页
            #next_url = response.xpath("//div[@class='page_al']//span[@class='on']/following-sibling::span[1]/a/@href").get()
            #上面依旧不能爬取5到6页之后的数据
            #next_url = response.xpath("//div[@class='page_al']/p/a/@href").get()
            next_url = response.xpath("//div[@class='page_al']//p[1]/a/@href").get()
            if next_url:
                yield scrapy.Request(url=response.urljoin(next_url),
                                     callback=self.parse_esf,
                                     meta={'info': (provice, city)}
                                     )