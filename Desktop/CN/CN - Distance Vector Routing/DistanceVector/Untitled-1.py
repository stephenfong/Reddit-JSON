#print("hi")

tup = (1, (2,3,4))
#print(tup[0])
#print(tup[1])

word = "word?"
word = word.replace("?", "")
#print(word)

dict1 = {"a" : 1}
#print(list(dict1.keys()))

list1 = [1,2,3,4,5]
ind_last_msg = list1.index(3)
print(ind_last_msg)
list1 = list1[ind_last_msg + 1::]
print(list1)