# from xml.dom.minidom import parse
# import xml.dom.minidom
 
# # 使用minidom解析器打开 XML 文档
# DOMTree = xml.dom.minidom.parse("NR_MRO_HUAWEI_132097040007_8553507_20240409220000.xml")
# collection = DOMTree.documentElement
# if collection.hasAttribute("id"):
#    print ("Root element : %s" % collection.getAttribute("id"))
 
# # 在集合中获取所有电影
# smr = collection.getElementsByTagName("smr")# 打印每部电影的详细信息
# # data = smr.getElementsByTagName("object")# 打印每部电影的详细信息
# for s in smr:
#     print(s.childNodes[0].data)
#     data = s.getElementsByTagName('object')[0]
#     print(data)
#     type = s.getElementsByTagName('type')[0]
#     # print("Type: %s" % data.childNodes[0].data)
# #    print ("*****Movie*****")
# #    if smr.hasAttribute("title"):
#     #   print "Title: %s" % movie.getAttribute("title")

import xml.etree.ElementTree as ET

# 解析XML文件
tree = ET.parse('NR_MRO_HUAWEI_132097040007_8553507_20240409220000.xml')
root = tree.getroot()

# 遍历所有子元素
# for child in root:
#     print(child.tag, child.attrib)  # 打印标签名和属性

#     # 遍历子元素的子元素
#     for subchild in child:
#         print(subchild.tag, subchild.attrib, subchild.text)  # 打印子标签名、属性和文本内容

# 查找具有特定标签的元素
for element in root.iter('smr'):
    print(element.text)  # 打印subelement1的文本内容

# 查找具有特定属性的元素
for element in root.iter('object'):
    print(element.attrib)  # 打印subelement2的属性
    for subchild in element:
        print(subchild.text)  # 打印子标签名、属性和文本内容