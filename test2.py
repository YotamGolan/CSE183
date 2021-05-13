from dbcomm import DBComm

dbcomm = DBComm('Mitchell', 'Mitchellpass123', 'canvasDB')
print('connected')
dbcomm.close()
print('close')
