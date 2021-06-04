from dbcomm import DBComm

dbcomm = DBComm('Yotam', '', 'canvasDB')
print('connected')

#dbcomm.insertUser(40, 'John', 'Doe', 3)

for i in range (100):
    dbcomm.insertPixel(40, i+100, i+100, i+100, i+100, i+100)

>>>>>>> main
print('pixel inserted')

out = dbcomm.selectPixelsByUser(40)
for line in out:
    print(line)

dbcomm.close()
print('close')
