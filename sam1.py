import requests
import time
import json
import sqlite3
import threading
import datetime


def get_database(Time):
	con=sqlite3.connect('train.db')
	all=con.execute('SELECT * FROM train WHERE checkPoint=?',(Time,))
	arr=[]
	for i in all:
		for j in i:
			arr.append(j)
			
	return arr
	
def get_status(trainNo,src,dst,time=time.strftime('%Y%m%d')):
	try:
		res=requests.get('https://travel.paytm.com/api/trains/v1/detail?class=SL&departureDate='+time+'&destination='+dst+'&quota=GN&requestid=81635f2a-1e74-4c88-976f-f2e469d513d8&source='+src+'&trainNumber='+str(trainNo)+'&train_type=O&client=%27mweb%27').json()	
		#print(res)
		return res['body']['availability'][0]['status']
	except Exception as e:
		return 'someThingFishy as '+str(e)

def set_firebase(path,data):
	url1='https://guvi-41d93.firebaseio.com/'+path+'/.json'
	if path=='':
		url1='https://guvi-41d93.firebaseio.com/'
	r = json.dumps(data)
	to_database = json.loads(r)
	requests.patch(url = url1 , json = to_database)

def doAll(arr):
	tommorow=datetime.date.today()+datetime.timedelta(1)
	tommorow=str(tommorow).replace('-','')
	print(time.strftime('%T'),': Uploading status of ',arr[1],'from '+arr[2]+' to '+arr[3])
	if (arr[-1]==1):
		status=get_status(arr[1],arr[2],arr[3],tommorow)
	else:
		status=get_status(arr[1],arr[2],arr[3])
	set_firebase(arr[2]+'-'+arr[3]+'/'+arr[1]+'/'+time.strftime('%d-%m-%Y'),{time.strftime('%T'):status})
	print(time.strftime('%T'),': Uploaded status as',status)


while True:
	print('Processing',time.strftime('%H:%M'))
	arr=get_database(time.strftime('%H:%M'))
	if (arr!=[]):
		threading.Thread(target=doAll,args=(arr,)).start()
	time.sleep(60)
