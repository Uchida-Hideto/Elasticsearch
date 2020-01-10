import json
string =[{'_index': '192.168.15.168', '_type': '_doc', '_id': 'D:\\new\\测试1.doc', '_score': 7.3987164, '_source': {'filepath': 'D:\\new\\测试1.doc', 'title': '测试1'}},{'_index': '192.168.15.168', '_type': '_doc', '_id': 'D:\\文档\\测试文档.doc', '_score': 6.5267797, '_source': {'filepath': 'D:\\文档\\测试文档.doc', 'title': '测试文档'}}]
string2 = []

ret = []
for i in string:
    if i.get('_id', '') != 'D:\\new\\测试1.doc':
        ret.append(i)

print(ret)