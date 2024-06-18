#
"""
    列表
"""
list1 = [1,2,3,4,"ddd",[6,7,8]]

print(list1[5][0])
print(len(list1[5]))

list1[1] = list1[1] * 3
list1 = list1 * 3

print(list1)

print("aaa"* 4 == "aaaaaaaaaaaa")

print(list1[::-1][0][::-1])
print(list1)
del list1[0]
list1.append("ccccccccc")
list1.insert(1,["11","22"])
#list1.clear();
print(list1)
list1.remove(6)
list1.pop(1) #返回值 移除的数据
list1.reverse()
print(list1)
print(list1.index([6, 7, 8]))#下标
print(list1.index([6, 7, 8],2))
