from os import read
import time
import json
import requests
import datetime
#{"name": "Mosquitto Server #2 (Public MQTT)", "url": "https://mq02.cy2.me/"},
while True:
	urlFile = open("urls.json", "r", encoding="utf8")
	urlStr = urlFile.read()
	urls = json.loads(urlStr)
	out = {'results':[]}
	for urlDict in urls:
		url = urlDict['url']
		start = time.time()
		result = ""
		code = 0
		try:
			code = requests.get(url).status_code
			if code == 200:
				result = "ONLINE"
			else:
				result = "ERROR"
		except:
			result = "FAIL: request failed"
		timeTaken = time.time()-start
		print(result+":		"+urlDict['name'])
		out['results'].append({'name': urlDict['name'], 'result': result, 'code': code, 'time': timeTaken})
	out['timeStr'] = datetime.datetime.now().strftime("%m/%d/%Y @ %H:%M:%S")
	# print(json.dumps(out))
	readableList = ""
	simpleStatus = ""
	for result in out['results']:
		readableList+="<tr>"
		readableList+="\n<td class='left'>"+result['name']+"</td>"
		if result['result'] == "ONLINE":
			color = 'style="color: green;"'
			simpleStatus+="P"
		else:
			color = 'style="color: red;"'
			simpleStatus+="F"
		readableList+="\n<td "+color+" class='center'>"+result['result']+"</td>"
		readableList+="\n<td class='right'>"+str(round(result['time'], 5))+"s"+"</td>"
		readableList+="</tr>"
	page = open("template.html", "r").read()
	page = page.replace("&pages", readableList)
	page = page.replace("&timeLastUpdated", out['timeStr'])
	open("index.html", "w").write(page)
	open("short.txt", "w").write(simpleStatus)
	print("COMPLETED	"+out['timeStr'])
	print("Running again in 60s")
	time.sleep(60)