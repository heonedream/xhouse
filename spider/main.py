# - * - encoding:utf-8 - * -

import urllib2
from bs4 import BeautifulSoup
import csv
import re
import datetime
import os
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def crawl(cities, lianjia_types, lianjia_regions, pages_num, path, save_file):

    #get url lists
    url_lists = []
    for i in cities:
        for k in lianjia_types:
            for l in lianjia_regions:
                for n in range(1, pages_num+1):
                    url_lists.append("https://" + str(i) + ".lianjia.com/" + str(k) + "/" + str(l) + "/pg" + str(n))

    # write the colnames firstly
    path_file = os.path.join(path, save_file)
    with open(path_file, "a+") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["city", "zone", "data_el", "house_name", "house_code", "data_link", "room_num", "built_year", "direction",
             "total_price",
             "mean_price", "area", "house_style", "floor", "building_type", "crawl_time", "persons_in_attention",
             "published_date", "subway", "vr", "taxfree", "haskey", "community", "region"])

    for link in url_lists:
        req = urllib2.Request(link)
        #读取网页
        response = urllib2.urlopen(req)
        the_page = response.read()
        #解析网页
        soup = BeautifulSoup(the_page, 'html.parser')

        # list containers to contain pages content
        city = []
        zone = []
        data_el = []
        house_name = []
        house_code = []
        data_link = []
        room_num = []
        built_year = []
        direction = []
        total_price = []
        mean_price = []
        # **平米
        area = []

        # 精装or简装
        house_style = []

        # 高低楼层
        floor = []

        # 板楼等类型
        building_type = []

        # followed_info
        crawl_time = []
        persons_in_attention = []
        published_date = []

        # tag_info
        subway = []
        vr = []
        taxfree = []
        haskey = []

        # position
        community = []
        region = []

        # whole dataset
        data_list = []

        #get titile
        for tag1 in soup.find_all(name="div", attrs={"class": re.compile("title")}):
            ta1 = tag1.find(name="a", attrs={"target": re.compile("_blank"), "data-el": re.compile("ershoufang")})
            if ta1 != None:
                city.append(link.split('/')[2].split('.')[0])
                zone.append(link.split('/')[4])
                data_el.append(ta1.attrs["data-el"])
                house_name.append(ta1.string)
                house_code.append(ta1.attrs["data-housecode"])
                data_link.append(ta1.attrs["href"])

        #get area and room number etc.
        for tag2 in soup.find_all(name="div", attrs={"class": re.compile("houseInfo")}):
            house_info = tag2.text.split("|")

            #add to list
            if len(house_info) == 7: #make user the list len is 7
                room_num.append(house_info[0].strip())
                area.append(house_info[1].strip())
                direction.append(house_info[2].strip())
                house_style.append(house_info[3].strip())
                floor.append(house_info[4].strip())
                built_year.append(house_info[5].strip())
                building_type.append(house_info[6].strip())
            else:
                room_num.append("None")
                area.append("None")
                direction.append("None")
                house_style.append("None")
                floor.append("None")
                built_year.append("None")
                building_type.append("None")

        #get price info
        for tag3 in soup.find_all(name="div", attrs={"class": re.compile("priceInfo")}):
            price_info = tag3.text.split("单价")
            total_price.append(price_info[0])
            mean_price.append(price_info[1])

        #get follow_info
        for tag4 in soup.find_all(name="div", attrs={"class": re.compile("followInfo")}):
            #persons_in_attentions
            follow_text = tag4.text.split("/")
            persons_in_attention.append(follow_text[0].strip())

            #crawl_time
            now = datetime.date.today()
            crawl_time.append(str(now))

            #published_time
            if ("月" in follow_text[1].strip()):
                num_month = int(follow_text[1].strip().split("个")[0])
                published_day = datetime.date.today() + datetime.timedelta(days=-30 * num_month)
                published_date.append(str(published_day))
            elif ("年" in follow_text[1].strip()):
                num_year = follow_text[1].strip().split("年")[0]

                def chinese2num(chinese_num):
                    numbers = {
                        u'一':1,
                        u'二':2,
                        u'三':3,
                        u'四':4,
                        u'五':5,
                        u'六':6,
                        u'七':7,
                        u'八':8,
                        u'九':9,
                        u'十':10}
                    return numbers.get(chinese_num, None)
                a = chinese2num(num_year)
                num_day = chinese2num(num_year) * 365
                published_day = datetime.date.today() + datetime.timedelta(days=-1 * num_day)
                published_date.append(str(published_day))

            elif ("刚刚" in follow_text[1].strip()):
                published_day = datetime.date.today()
                published_date.append(str(published_day))

            else:
                num_day = int(follow_text[1].strip().split("天")[0])
                published_day = datetime.date.today() + datetime.timedelta(days=-1 * num_day)
                published_date.append(str(published_day))

        #get tag info
        for tag5 in soup.find_all(name="div", attrs={"class": re.compile("info clear")}):
            subway_info = tag5.find(name="span", attrs={"class": re.compile("subway")})
            vr_info = tag5.find(name="span", attrs={"class": re.compile("vr")})
            taxfree_info = tag5.find(name="span", attrs={"class": re.compile("taxfree")})
            haskey_info = tag5.find(name="span", attrs={"class": re.compile("haskey")})

            if subway_info != None:
                subway.append(subway_info.text)
            else:
                subway.append("None")

            if vr_info != None:
                vr.append(vr_info.text)
            else:
                vr.append("None")

            if taxfree_info != None:
                taxfree.append(taxfree_info.text)
            else:
                taxfree.append("None")

            if haskey_info != None:
                haskey.append(haskey_info.text)
            else:
                haskey.append("None")

        #position info
        for tag5 in soup.find_all(name="div", attrs={"class": re.compile("info clear")}):

            position_info = tag5.find(name="div", attrs={"class": re.compile("positionInfo")})
            position_info = position_info.find_all(name="a", attrs={"target": re.compile("_blank")})
            community_info = position_info[0].text
            region_info = position_info[1].text

            community.append(community_info)
            region.append(region_info)

        #check all list are the save lenth
        assert len(city)==len(data_el)==len(zone)==len(house_code)==len(house_name)==len(data_link)==len(room_num)==len(built_year)==\
               len(direction)==len(total_price)==len(mean_price)==len(area)==len(house_style)==len(floor)==\
               len(building_type)==len(crawl_time)==len(persons_in_attention)==len(published_date)==\
               len(subway)==len(vr)==len(taxfree)==len(haskey)==len(community)==len(region)

        print(link.split('/')[-2]+ " " + "第" + link.split('/')[-1] + "页完成")
        #sleep 10s
        time.sleep(2)

        for i in range(0, len(city)):
            data_list.append((city[i], zone[i], data_el[i], house_name[i], house_code[i], data_link[i], room_num[i], built_year[i], direction[i],
                             total_price[i], mean_price[i], area[i], house_style[i], floor[i], building_type[i],
                             crawl_time[i], persons_in_attention[i], published_date[i], subway[i], vr[i], taxfree[i], haskey[i],
                              community[i], region[i]))

        with open(path_file, "a+") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data_list)

if __name__ =="__main__":
    # set space to crawl
    cities = ["gz"]
    lianjia_types = ["ershoufang"]
    lianjia_regions_shenzhen = ["luohuqu", "futianqu", "nanshanqu",  "yantianqu", "baoanqu", "longgangqu", "longhuaqu", "guangmingqu", "pingshanqu", "dapengxinqu"]
    # lianjia_regions_guagnzhou = ["tianhe", "yuexiu", "liwan", "haizhu", "panyu", "baiyun", "huangpu", "conghua", "zengcheng", "huadu"]
    lianjia_regions_guagnzhou = ["huangpu", "conghua", "zengcheng", "huadu"]
    pages_num = 100
    path = "/Users/hewenjun/Documents/project/xhouse"
    save_file = "ershoufang_guangzhou.csv"

    crawl(cities, lianjia_types, lianjia_regions_guagnzhou, pages_num, path, save_file)
