from datetime import *
import time
import json
import requests #requires pip install
import threading
import codecs
import os

class Pinnacle:
	matchupResponses=[]
	straightResponses=[]
	
	headers = {
		'User-Agent': 'Mozilla/5.0',
		'content-type': 'application/json',
		'X-API-Key': "CmX2KcMrXuFmNg6YFbmTxE0y9CIrOi0R"
	}

	def __init__(self, lowCapacityCPU=True):
		self.lowCapacityCPU = lowCapacityCPU

	def getLeaguesIDs():
		url='https://guest.api.arcadia.pinnacle.com/0.1/sports/29/leagues?all=false'
		response=json.loads(requests.get(url,headers=Pinnacle.headers).text)
		leagueIDs=[]
		for league in response: leagueIDs.append(league['id'])
		return leagueIDs
	def generateLinks():
		leagueIDs=Pinnacle.getLeaguesIDs()
		links=[]
		for league in leagueIDs:
			link='https://guest.api.arcadia.pinnacle.com/0.1/leagues/{}/matchups'.format(league)
			links.append(link)
			link='https://guest.api.arcadia.pinnacle.com/0.1/leagues/{}/markets/straight'.format(league)
			links.append(link)
		return links
	def ExecuteRequest(link):
		response = requests.get(link,headers=Pinnacle.headers).text
		# _json = json.loads(response)
		try: _json = json.loads(response)
		except:
			print(response)
			print('milaneee')
			return
		if 'matchups' in link: Pinnacle.matchupResponses.append(_json)
		elif 'straight' in link: Pinnacle.straightResponses.append(_json)
	def GenerateThreads():
		links = Pinnacle.generateLinks()
		threads = []
		threadNumber = len(links)

		if True: # Change for stronger CPUs 
			threadNumber = min(2,threadNumber)

		for i in range(threadNumber):
			t = threading.Thread(target=Pinnacle.ExecuteRequest, args=[links[i]])
			t.daemon = True
			threads.append(t)
		for i in range(threadNumber):
			threads[i].start()
		for i in range(threadNumber):
			threads[i].join()
	def ProcessResponses():

		betDict = {
			's;0;m': ["ki1", "ki2", "kix"],
			's;1;m': ["Iki1", "Iki2", "Ikix"],
			's;0;ou;1.5': ["ug2+","ug0-1"],
			's;0;ou;2.5': ["ug3+", "ug0-2"],
			's;0;ou;3.5': ["ug4+", "ug0-3"],
			's;1;ou;1.5': ["Iug2+", "Iug0-1"],
		}

		mapaID_Podaci={}
		mapaID_Kvote={}

		for matchup in Pinnacle.matchupResponses:
			for match in matchup:

				id=match['id']
				if match['parentId'] != None:
					continue
				if match['type'] == 'special':
					continue
				mapaID_Kvote[id]=[]
				startTime = match['startTime']
				dt = datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=2)
				date, time = dt.strftime('%m.%d.'), dt.strftime('%H:%M')
				home=away=''
				league = match['league']['name'].strip()
				home = match['participants'][0]['name'].strip()
				away = match['participants'][1]['name'].strip()

				mapaID_Podaci[id]={
					'home':home,
					'away':away,
					'date':date,
					'time':time,
					'league':league
				}
		for straight in Pinnacle.straightResponses:
			for match in straight:
				matchupId = match['matchupId']
				key=match['key']
				if (matchupId not in mapaID_Podaci) or (key not in betDict): continue
				i=0
				try:
					for o in match['prices']:
						value=o['price']
						if value>=0:
							value=1+value/100
						else:
							value=1-100/value
						game=betDict[key][i]
						mapaID_Kvote[matchupId].append([game,round(value,2)])
						i+=1
				except:
					print(matchupId)
					print(mapaID_Podaci[matchupId])
					print(key)
					print('*****************')

		Pinnacle.WriteToScraped(mapaID_Podaci,mapaID_Kvote)
		return
	def WriteToScraped(data,odds):
		folderpath = os.getcwd() + os.sep + 'Scraped'

		if not os.path.exists(os.path.join(folderpath, 'Pinnacle Scraped.txt')):
			os.makedirs(folderpath)
			with open(os.path.join(folderpath, 'Pinnacle Scraped.txt'), "w"):
				pass
		

		scrapedFile = codecs.open('./Scraped/Pinnacle Scraped.txt', 'r+', 'utf-8')
		for ID in data:
			Data=data[ID]
			M_data=[Data['date'],Data['time'],Data['home'],Data['away'],Data['league']]
			M_odds=[]
			for o in odds[ID]:
				game,value=o[0],o[1]
				M_odds.append('%s-[%s]'%(game,value))
			scrapedFile.write("; ".join(M_data) + "; \n")
			scrapedFile.write("; ".join([str(x) for x in M_odds]) + "; \n")
			scrapedFile.write('\n')
		scrapedFile.close()
	def Scrape():
		s_time=time.time()

		Pinnacle.GenerateThreads()
		Pinnacle.ProcessResponses()

		e_time = time.time()
		print("Pinnacle: ", round(e_time - s_time, 2))


Pinnacle.Scrape()