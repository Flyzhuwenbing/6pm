# coding: utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests
import csv

url = 'https://www.6pm.com/p/lifestride-spark-red/product/8872328/color/585'
driver = webdriver.PhantomJS('/usr/local/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
driver.get(url)
driver.implicitly_wait(10) #隐式延时

#h获取颜色下拉框
sel_colors = driver.find_elements_by_xpath("//form//select[@id='pdp-color-select']")
sel_color = next(element for element in sel_colors if element.is_displayed())
sel_color= Select(sel_color)

#获取尺码下拉框
sel_sizes = driver.find_elements_by_xpath("//form//select[@id='pdp-size-select']")
sel_size = next(element for element in sel_sizes if element.is_displayed())
sel_size = Select(sel_size)

# 获取widths下拉框
sel_widths = driver.find_elements_by_xpath("//form//select[@id='pdp-width-select']")
sel_width = next(element for element in sel_widths if element.is_displayed())
sel_width = Select(sel_width)

lst = []
results = []
# 获取option标签，得颜色、尺码、宽度的信息
element = driver.find_elements_by_tag_name('option')
for i in element:
    lst.append(i.text)
# print(lst)
color_lst = lst[0:6]
size_lst = lst[7:19]
width_lst = lst[20:22]

for i in color_lst:
    sel_color.select_by_visible_text(i) # 通过文本选中下拉框中颜色元素
    price = driver.find_elements_by_class_name("_3r_Ou")# 通过切换不同颜色的下拉框，依次得到不同颜色的价格信息
    price = next(element for element in price if element.is_displayed()) # 当元素显示时逐个获取
    # print(price.text)

    # 获取图片链接并保存图片
    src = driver.find_element_by_xpath("//img[@title='{}']".format(i))
    link = src.get_attribute('src')
    # print(link)
    filename = link.split('/')[-1]
    pic = requests.get(link, timeout=3)
    with open('pics/' + filename, 'wb') as f:
        f.write(pic.content)
    print('downloading', filename)
    for j in size_lst:
        sel_size.select_by_visible_text(j)
        for k in width_lst:
            sel_width.select_by_visible_text(k)
            # 选中颜色、尺码、宽度之后显示库存信息
            stock = driver.find_elements_by_xpath("//div[contains(text(), ' in stock')]")
            if stock:
                stock = next(element for element in stock if element.is_displayed())
                print(stock.text)
                results.append([i, price.text,j, k,stock.text])
            else:
                print('out of stock')
                results.append([i,price.text, j, k, 'out of stock'])
# print(results)

#写入csv文件中
with open('6pm.csv','w') as csvfile:
    writer =csv.writer(csvfile)
    writer.writerow(['颜色', '价格', '尺码', '宽度', '库存'])
    for data in results:
        writer.writerow(data)











