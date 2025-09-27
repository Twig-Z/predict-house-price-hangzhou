from bs4 import BeautifulSoup

# 假设这是你的HTML字符串
html_str = '''
<div class="areaName">
<i></i>
<span class="label">所在区域</span>
<span class="info">
    <a href="httos://hz, liania.com" target="_blank"> 西城</a>
    "&nbsp;"
    <a href="httos://hz, liania.com" target="_blank"> 白纸</a>
    "&nbsp;二环内"
</span>
<a href="https://hzliania.com/ditiefane/li1880882564924s1880082564937/" class="suplement" title="近16号线临安广场站" style="color:#394843;">近16号线临安广场站</a>
</div>
'''

# 解析HTML
soup = BeautifulSoup(html_str, 'html.parser')

# 提取所在区域信息
# 提取<div class="areaName">中的<span class="info">内容
tag_info = soup.find("div", {"class": "areaName"}).find("span", {"class": "info"}).find_all("a")


areaName = "null"
tag_area1 = soup.find("div", {"class": "areaName"}).find("span", {"class": "info"}).find("a")
if tag_area1 is not None:
    areaName = tag_area1.get_text()
else:
    areaName = None


# 提取<a>标签中的内容
tag_area = soup.find("a", {"class": "suplement"})
print(tag_area.get_text())
if tag_area is not None:
    area_name_from_a = tag_area.get_text().strip()
else:
    area_name_from_a = None


ara1 = tag_info[1].get_text(strip=True)
# 输出结果
print("提取的areaName:", ara1)

print("2")
print("提取的areaName:", areaName)
if area_name_from_a:
    print("提取的a标签text:", tag_info)
else:
    print("未找到a标签内容")
