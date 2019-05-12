
def test2(html):
    list = ['Occupation', 'University', 'Party', 'City', 'Nationality', 'BD', 'height', 'parents',
            'brothersister', 'othername', 'Child', 'Region']  # 使用mdr来提取的属性
    # 下列为每个属性的别名，即别名中包含属性信息
    list_attr_BD = ['Birth', 'Birth Date', 'Born', 'dbo:birthDate']
    list_attr_Occupation = ['Famous As', 'Occupation', 'Profession', 'dbo:office']
    list_attr_Nationality = ['Nationality', 'dbo:country']
    list_attr_City = ['Birth Place', 'Place of Birth', 'Residence']  # Birth Place为出生地
    list_attr_height = ['Height']
    list_attr_University = ['Education', 'Alma mater']  # Education是教育，与大学不同,可能要做处理
    list_attr_brothersister = ['Brother', 'Sister']
    list_attr_othername = ['Birth Name', 'Full Name', 'Nickname(s)']
    list_attr_parents = ['Father', 'Mother', 'Parents']
    list_attr_Party = ['political affiliation', 'Political party', 'dbo:party']
    list_attr_Child = ['Children', 'dbo:child']
    list_attr_Region = ['dbo:region']
    dict = {}  # 存储网页结构化直接提取出的属性
    mdr = MDR()
    r = html.encode('utf8')
    x = replace(r)
    # print x
    candidates, doc = mdr.list_candidates(x)
    # 候选子节点
    bbb = [doc.getpath(c) for c in candidates[:10]]
    # 保存所有叶节点内容
    list_tag = []
    # 保存tale表单里的内容
    list_table = {}
    list_attr_key = []
    for attr in list:
        list_attr_key.extend(eval("list_attr_"+attr))
    # for bb in bbb:
    #     # 处理为table的表单,
    #     # 将所有包含table路径的节点都进行截断处理，得到路径上到table的最长路径
    #     # 源路径：/html/body/div[3]/div[3]/div[4]/div/div[8]/table/tbody/tr/td/div/ul
    #     # 提取table：/body/div[3]/div[3]/div[4]/div/table
    #     # 然后对其提取包含下列格式的内容信息
    #     # 格式为 <tr> <th>onlyOne</th> <td>more</td> <td>more</td>... </tr>
    #     if 'table' in bb:
    #         node = bb.split('html')[1].split('/table')[:-1]
    #         node = '/table'.join(node) + '/table'
    #         node_html = etree.tostring(doc.find(node))
    #         node_soup = BeautifulSoup(node_html, 'lxml')
    #         stype_node_list = []  # 存放找到属性名的样式标签
    #         # print node_soup.table
    #         for child in node_soup.descendants:
    #             if child.string and child.string in list_attr_key:
    #                 if isinstance(child, NavigableString):  # 不是字符串即叶节点
    #                     # print child
    #                     continue
    #                 else:
    #                     stype_node = {'name':child.name, "attrs":child.attrs}
    #                     if stype_node not in stype_node_list:
    #                         stype_node_list.append(stype_node)
    #                         print "标签内容为：", child
    #                         print "tag:", child.name
    #                         print child.attrs
    #                         list_attr_name = []
    #                         list_attr_value = []
    #                         temp_list = []
    #                         node_list = node_soup.find_all(name=child.name, attrs=child.attrs)
    #                         for i,childNode in enumerate(node_list):
    #                             list_attr_name.append(childNode.string)
    #                             if i < len(node_list)-1:
    #                                 pattern = re.compile(unicode(childNode)+r"(.*?)"+unicode(node_list[i+1]),re.S)
    #                                 attr_value_m = re.search(pattern, node_html)
    #                                 if attr_value_m:
    #                                     soup_value = BeautifulSoup(attr_value_m.group(1))
    #                                     attr_value_list = [string for string in soup_value.stripped_strings]
    #                                     attr_value_string = ' '.join(attr_value_list)
    #                                     print "属性名:", childNode.string
    #                                     print "属性值：",attr_value_string
    feature_dict = {}
    for c in candidates[:10]:
        node_html = etree.tostring(c)
        node_soup = BeautifulSoup(node_html, 'lxml')
        stype_node_list = []  # 存放找到属性名的样式标签
        # print node_soup.table
        for child in node_soup.descendants:
            if child.string and child.string.strip() in list_attr_key:
                if isinstance(child, NavigableString):  # 是字符串即叶节点
                    # print child
                    continue
                else:
                    stype_node = {'name': child.name, "attrs": child.attrs}
                    if stype_node not in stype_node_list:
                        stype_node_list.append(stype_node)
                        print "标签内容为：", child
                        print "tag:", child.name
                        print child.attrs
                        list_attr_name = []
                        list_attr_value = []
                        temp_list = []
                        node_list = node_soup.find_all(name=child.name, attrs=child.attrs)
                        for i, childNode in enumerate(node_list):
                            list_attr_name.append(childNode.string)
                            if i < len(node_list) - 1:
                                # 因为BeatifulSoup自动对标签去掉空格，导致<br />会变成<br>，导致无法匹配到，需要提前处理，保证统一
                                # 将字符串中的特殊字符转义，防止出现无法匹配的问题
                                pattern = re.compile(re.escape(unicode(childNode)) + r"(.*?)" + re.escape(unicode(node_list[i + 1])),
                                                     re.S)
                                print unicode(childNode) + r"(.*?)" + unicode(node_list[i + 1])
                                attr_value_m = re.search(pattern, node_html)
                                if attr_value_m:
                                    soup_value = BeautifulSoup(attr_value_m.group(1))
                                    attr_value_list = [string for string in soup_value.stripped_strings]
                                    attr_value_string = ' '.join(attr_value_list)
                                    attr_key_string = childNode.string
                                    print i
                                    print "属性名:", childNode.string
                                    print "属性值：", attr_value_string
                                    if attr_key_string and len(attr_value_string) > 0:
                                        for attr in list:
                                            # 因为先找可能性高的，所有不能覆盖掉先找到的属性
                                            if attr_key_string in eval('list_attr_'+attr) and attr not in feature_dict:
                                                feature_dict[attr] = attr_value_string
                                                break
                        # 最后一个标签
                        last_node = node_list[-1]
                        print last_node
                        for node_i in last_node.next_element.next_elements:
                            if isinstance(node_i, NavigableString):
                                attr_value_string = unicode(node_i.string).strip()
                                if attr_value_string is not u"":
                                    attr_key_string = last_node.string.replace()
                                    if attr_key_string and len(attr_value_string) > 0:
                                        for attr in list:
                                            # 因为先找可能性高的，所有不能覆盖掉先找到的属性
                                            if attr_key_string in eval('list_attr_'+attr) and attr not in feature_dict:
                                                feature_dict[attr] = attr_value_string
                                    print "属性名:", last_node.string
                                    print "属性值：", attr_value_string
                                    break
                        # print last_node
                        # print last_node.next_sibling

    return feature_dict
