## 基于selenuim对6pm.com网站商品信息的抓取

### 项目简述

本项目用来抓取6pm.com网站商品信息，包括商品颜色，尺码，价格，图片及库存信息。抓取到到结果保存到csv中。  
由于6pm.com网站采用JavaScript渲染及动态数据，本项目采用Selenium＋PhantomJS来抓取相应内容，采用延时等待，模拟下拉选项卡的点击等方法驱动浏览器渲染页面。  
项目实现了如下功能：

* 模拟点击下拉选项卡，并提取选项中元素
* 选择下拉选项卡中元素，动态加载出不同颜色的商品所对应的价格及库存信息
* 实现了动态网页数据的抓取




### 项目说明

下拉选项卡的处理

```
sel_sizes = driver.find_elements_by_xpath("//form//select[@id='pdp-size-select']")
sel_size = next(element for element in sel_sizes if element.is_displayed())
sel_size = Select(sel_size)
```

提取option标签，得颜色、尺码、宽度的信息

```
element = driver.find_elements_by_tag_name('option')
for i in element:
    lst.append(i.text)
```

迭代依次选中每件商品的颜色、尺码、宽度下拉选项框，获取库存情况信息

```
for i in color_lst:
    sel_color.select_by_visible_text(i)
	 for j in size_lst:
		sel_size.select_by_visible_text(j)
		for k in width_lst:
		    sel_width.select_by_visible_text(k)
```

获取图片链接并保存图片

```
    src = driver.find_element_by_xpath("//img[@title='{}']".format(i))
    link = src.get_attribute('src')
    # print(link)
    filename = link.split('/')[-1]
    pic = requests.get(link, timeout=3)
    with open('pics/' + filename, 'wb') as f:
        f.write(pic.content)
    print('downloading', filename)
```

写入csv文件中

```
with open('6pm.csv','w') as csvfile:
    writer =csv.writer(csvfile)
    writer.writerow(['颜色', '尺码', '宽度','价格','库存'])
    for data in results:
        writer.writerow(data)
```






