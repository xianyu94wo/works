file1 = open("E:\\work\\DATA\\A\\A52963-201406.txt","r",encoding="gb18030")
b = []
count = 0
for i in file1.readlines():
	count += 1
	if i.strip("\n") == "W0":
		a = count
		b.append(count)
	if i.strip("\n")[-1:] == "=":
		b.append(count)
for i in range(len(b)):
	if b[i] == a:
		c = b[i+1]
print(a)
print(b)
print(c)
file1.close()
file1 = open("I:\\data\\A\\A52963-201406.txt","r",encoding="gb18030")
r = file1.readlines()
for i in range(a,c):
	print(r[i].strip("\n").strip("="))




'''
print(len(file1.readlines()))

'''