from dbcomm import DBComm

dbcomm = DBComm('Mitchell', 'Mitchellpass123', 'canvasDB')
print('connected')

dbcomm.insertUser('John', 'Doe', 3)

dbcomm.insertPixel(40, 5, 10, 4, 5, 6)
print('pixel inserted')

out = dbcomm.selectPixelsByUser(40)
for line in out:
    print(line)

dbcomm.close()
print('close')
