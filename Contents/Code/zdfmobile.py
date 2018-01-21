################################################################################
#				zdfmobile.py - Part of Plex-Plugin-ARDMediathek2016
#							mobile Version der ZDF Mediathek
################################################################################
# 	dieses Modul nutzt nicht die Webseiten der Mediathek ab https://www.zdf.de/,
#	sondern die Seiten ab https://zdf-cdn.live.cellular.de/mediathekV2 - diese
#	Seiten werden im json-Format ausgeliefert

#import  json		# bereits geladen

PREFIX		 	= "/video/ardmediathek2016/zdfmobile.py"
imgWidth		= 840			# max. Breite Teaserbild
imgWidthLive	= 1280			# breiter für Videoobjekt

@route(PREFIX + '/Main_ZDF')
def Main_ZDFmobile(name):
	Log('zdfmobile.Main_ZDF')
	oc = ObjectContainer(title2='ZDFmobile', view_group="InfoList")
	oc = home(cont=oc, ID=NAME)	 		# Home-Button -> 'ARD Mediathek 2016'
	
	# Suche bleibt abgeschaltet - bisher keine Suchfunktion bei zdf-cdn.live.cellular.de gefunden.
	# Web-Player: folgendes DirectoryObject ist Deko für das nicht sichtbare InputDirectoryObject dahinter:
#	name = 'ZDFmobile'
#	oc.add(DirectoryObject(key=Callback(Main_ZDFmobile, name=name),title='Suche: im Suchfeld eingeben', 
#		summary='', tagline='TV', thumb=R(ICON_SEARCH)))
#	oc.add(InputDirectoryObject(key=Callback(ZDFmSearch, s_type='video', title=u'%s' % L('Search Video')),
#		title=u'%s' % L('Search'), prompt=u'%s' % L('Search Video'), thumb=R(ICON_SEARCH)))
		
	title = 'Startseite'
	oc.add(DirectoryObject(key=Callback(Hub, ID=title), title=title, 
		thumb=R(ICON_DIR_FOLDER)))	
	oc.add(DirectoryObject(key=Callback(Hub, ID="Kategorien"), title="Kategorien", 
		thumb=R(ICON_DIR_FOLDER)))	 
	oc.add(DirectoryObject(key=Callback(Hub, ID="Sendungen A-Z"), title="Sendungen A-Z",
		thumb=R(ICON_DIR_FOLDER)))	
	oc.add(DirectoryObject(key=Callback(Hub, ID='Sendung verpasst'), title="Sendung verpasst", 
		thumb=R(ICON_DIR_FOLDER)))	
	oc.add(DirectoryObject(key=Callback(Hub, ID='Live TV'), title='Live TV',
		thumb=R(ICON_DIR_FOLDER)))
		
	return oc
	
@route(PREFIX + '/Hub')
# ID = Dict-Parameter und title2 für ObjectContainer 
def Hub(ID):
	Log('Hub, ID: %s' % ID)
	
	if ID=='Startseite':
		# lokale Testdatei:
		# path = '/daten/entwicklung/Plex/Codestuecke/ZDF_JSON/ZDF_start-page.json'
		# page = Resource.Load(path)
		path = 'https://zdf-cdn.live.cellular.de/mediathekV2/start-page'
	
	if ID=='Kategorien':
		path = 'https://zdf-cdn.live.cellular.de/mediathekV2/categories'
		
	if ID=='Sendungen A-Z':
		path = 'https://zdf-cdn.live.cellular.de/mediathekV2/brands-alphabetical'
		
	if ID=='Sendung verpasst':
		oc = Verpasst(DictID='Verpasst')	
		return oc		# raus - jsonObject wird in Verpasst_load geladen	

	if ID=='Live TV':
		now 	= datetime.datetime.now()
		datum 	= now.strftime("%Y-%m-%d")	
		path = 'https://zdf-cdn.live.cellular.de/mediathekV2/live-tv/%s' % datum
		
	oc = ObjectContainer(title2=ID, view_group="InfoList")		
	page = loadPage(path)		
	Log(len(page))
	if page.startswith('Fehler'):
		return ObjectContainer(header='Error', message=page)
	jsonObject = json.loads(page)
				
	if ID=='Startseite':
		Dict['Startpage'] = jsonObject		# speichern
		oc = videoObjects=PageMenu(oc,jsonObject,DictID='Startpage')		
	if ID=='Kategorien':
		Dict['Kategorien'] = jsonObject		
		oc = videoObjects=PageMenu(oc,jsonObject,DictID='Kategorien')		
	if ID=='Sendungen A-Z':
		Dict['A_Z'] = jsonObject		
		oc = videoObjects=PageMenu(oc,jsonObject,DictID='A_Z')		
	if ID=='Live TV':
		Dict['Live'] = jsonObject		
		oc = videoObjects=PageMenu(oc,jsonObject,DictID='Live')		
	
	return oc

# ----------------------------------------------------------------------
def Verpasst(DictID):					# Wochenliste
	Log('Verpasst')
	
	oc = ObjectContainer(view_group="InfoList", title2='Sendungen verpasst')
	oc = home(cont=oc, ID='ZDFmobile')		# Home-Button	
		
	wlist = range(0,7)
	now = datetime.datetime.now()

	for nr in wlist:
		rdate = now - datetime.timedelta(days = nr)
		iDate = rdate.strftime("%Y-%m-%d")		# ZDF-Format 	
		display_date = rdate.strftime("%d-%m-%Y") 	# Formate s. man strftime(3)
		iWeekday =  rdate.strftime("%A")
		if nr == 0:
			iWeekday = 'Heute'	
		if nr == 1:
			iWeekday = 'Gestern'	
		iWeekday = transl_wtag(iWeekday)		# -> ARD Mediathek
		path = 'https://zdf-cdn.live.cellular.de/mediathekV2/broadcast-missed/%s' % iDate
		title =	"%s | %s" % (display_date, iWeekday)
		Log(title)
		oc.add(DirectoryObject(key=Callback(Verpasst_load,path=path,datum=display_date),
			title=title,thumb=R(ICON_DIR_FOLDER)))	
	return oc
# ----------------------------------------------------------------------
@route(PREFIX + '/Verpasst_load')	# lädt json-Datei für gewählten Wochtentag:
def Verpasst_load(path, datum):		# 5 Tages-Abschnitte in 1 Datei, path -> DictID 
	Log('Verpasst_load')
	oc = ObjectContainer(title2=datum, view_group="InfoList")
	
	page = loadPage(path)		
	Log(len(page))
	if page.startswith('Fehler'):
		return ObjectContainer(header='Error', message=page)
	jsonObject = json.loads(page)
	Dict[path] = jsonObject		
	oc =PageMenu(oc,jsonObject,DictID=path)
	return oc
				
# ----------------------------------------------------------------------
# Bisher nicht genutzt
@route(PREFIX + '/ZDFmSearch')	
def ZDFmSearch(query=None, title=L('Search'), s_type='video', offset=0, **kwargs):
	Log('ZDFmSearch')
	Log('query: %s' % query)
	oc = ObjectContainer(title2='Suche', view_group="InfoList")
	
	return oc		
# ----------------------------------------------------------------------			
def PageMenu(oc,jsonObject,DictID):										# Start- + Folgeseiten
	Log('PageMenu, DictID: ' + DictID)
	oc = home(cont=oc, ID='ZDFmobile')					# Home-Button	

	if("stage" in jsonObject):
		i=0
		for stageObject in jsonObject["stage"]:
			if(stageObject["type"]=="video"):							# Videos am Seitenkopf
				title,subTitle,descr,img,date,dauer = Get_content(stageObject,imgWidth) 
				if subTitle:
					title = '%s | %s' % (title,subTitle)
				if date:
					title = '%s | %s' % (title,date)
				if dauer:
					title = '%s |  %s' % (title, dauer)
				date = '%s |  Länge: %s' % (date, dauer)
				date = date.decode(encoding="utf-8")
				path = 'stage|%d' % i
				Log(path)
				oc.add(DirectoryObject(key=Callback(ShowVideo,path=path,DictID=DictID),
					title=title, tagline=date, summary=descr, thumb=img))	
			i=i+1							
	
	if("cluster" in jsonObject):
		for counter, clusterObject in enumerate(jsonObject["cluster"]):	# Bsp. "name":"Neu in der Mediathek"
			if "teaser" in clusterObject and "name" in clusterObject:
				path = "cluster|%d|teaser" % counter
				title = clusterObject["name"]
				if title == '':
					title = 'ohne Titel'
				oc.add(DirectoryObject(key=Callback(SingleRubrik,path=path,
					title=title,DictID=DictID), title=title, thumb=R(ICON_DIR_FOLDER)))
								
	if("broadcastCluster" in jsonObject):
		for counter, clusterObject in enumerate(jsonObject["broadcastCluster"]):
			if clusterObject["type"].startswith("teaser") and "name" in clusterObject:
				path = "broadcastCluster|%d|teaser" % counter
				title = clusterObject["name"]
				oc.add(DirectoryObject(key=Callback(SingleRubrik,path=path,
					title=title,DictID=DictID), title=title, thumb=R(ICON_DIR_FOLDER)))
								
	if("epgCluster" in jsonObject):
		for counter, epgObject in enumerate(jsonObject["epgCluster"]):
			if("liveStream" in epgObject and len(epgObject["liveStream"]) >= 0):
				path = "epgCluster|%d|liveStream" % counter
				title = epgObject["name"] + ' Live'
				oc.add(DirectoryObject(key=Callback(ShowVideo,path=path,DictID=DictID),
					title=title, thumb=R(ICON_DIR_FOLDER)))	
	return oc				
				
# ----------------------------------------------------------------------	
def Get_content(stageObject, maxWidth):
	Log('Get_content')
	title=stageObject["headline"]
	subTitle=stageObject["titel"]

	if(len(title)==0):
		title = subTitle
		subTitle = ""
	descr=''	
	if("beschreibung" in stageObject):
		descr = stageObject["beschreibung"]
	dauer=''
	if("length" in stageObject):
		sec = stageObject["length"]
		if sec:
			dauer = time.strftime('%H:%M:%S', time.gmtime(sec))	
		
	img="";
	if("teaserBild" in stageObject):
		for width,imageObject in stageObject["teaserBild"].iteritems():
			if int(width) <= maxWidth:
				img=imageObject["url"];
	if("visibleFrom" in stageObject):
		# date = time.strptime(stageObject["visibleFrom"],"%d.%m.%Y %H:%M")
		date = stageObject["visibleFrom"]
	else:
		now = datetime.datetime.now()
		date = now.strftime("%d.%m.%Y %H:%M")	
	# Log('Get_content: %s |%s | %s | %s | %s | %s' % (title,subTitle,descr,img,date,dauer) )		
	return title,subTitle,descr,img,date,dauer
# ----------------------------------------------------------------------			
@route(PREFIX + '/SingleRubrik')
# einzelne Rubrik mit Videobeiträgen, alles andere wird ausgefiltert	
def SingleRubrik(path, title, DictID):		
	Log('SingleRubrik: %s' % path)
	
	path_org = path
	
	jsonObject = Dict[DictID]
	jsonObject = GetJsonByPath(path, jsonObject)
	Log('jsonObjects: ' + str(len(jsonObject)))	
	oc = ObjectContainer(title2=title, view_group="InfoList")
	oc = home(cont=oc, ID='ZDFmobile')					# Home-Button	

	i=0
	for entry in jsonObject:
		path = path_org + '|%d' % i
		date=''; title=''; descr=''; img=''
		Log('entry-type: %s' % entry["type"])
		# Log(entry)
		
		# alle anderen entry-types werden übersprungen, da sie keine 
		# verwendbaren Videos enthalten - Bsp.:
		#	category, brandsAlphabetical, externalUrl, broadcastMissed
		# Bei "brand" nehmen wir in Kauf, dass Infoseiten leere Videos
		#	zurückliefern - Bsp. Heute-Journal
					
		if entry["type"] == "video" or entry["type"] == "brand":
			title,subTitle,descr,img,date,dauer = Get_content(entry,imgWidth)
			if subTitle: 
				title = '%s | %s' % (title,subTitle)
			if date:
				title = '%s | %s' % (title,date)
			if dauer:
				title = '%s |  %s' % (title, dauer)
				date = '%s |  Länge: %s' % (date, dauer)
				date = date.decode(encoding="utf-8")
			# Log('video-content: %s |  %s |  %s |  %s | ' % (title,subTitle,descr,img))	
			oc.add(DirectoryObject(key=Callback(ShowVideo,path=path,DictID=DictID),
				title=title, tagline=date, summary=descr, thumb=img))			
		i=i+1
		# break		# Test Einzelsatz
	return oc

# ----------------------------------------------------------------------
# iteriert durch das Objekt	und liefert Restobjekt ab path
def GetJsonByPath(path, jsonObject):		
	Log('GetJsonByPath: '+ path)
	path = path.split('|')
	i = 0
	while(i < len(path)):
		if(isinstance(jsonObject,list)):
			index = int(path.pop(0))
		else:
			index = path.pop(0)
		Log('i=%s, index=%s' % (i,index))
		jsonObject = jsonObject[index]	
	# Log(jsonObject)
	return jsonObject	
# ----------------------------------------------------------------------			
@route(PREFIX + '/ShowVideo')
def ShowVideo(path, DictID):
	Log('ShowVideo')
	
	jsonObject = Dict[DictID]
	videoObject = GetJsonByPath(path,jsonObject)
	title,subTitle,descr,img,date,dauer = Get_content(videoObject,imgWidthLive)
	if subTitle:
		title = '%s | %s' % (title,subTitle)
	if date:
		if DictID <> 'Live':				# kein Datum bei Livestreams 
			title = '%s | %s' % (title,date)
	if dauer:
		title = '%s |  %s' % (title, dauer)
		
	oc = ObjectContainer(no_cache=True, title2=title, view_group="InfoList")
		
	if("formitaeten" in videoObject):
		formitaeten = get_formitaeten(videoObject)			
	else:
		Log('formitaeten fehlen, lade videoObject-url')
		formitaeten=[]; detail=[]
		url = videoObject["url"]
		# url=url.replace('https', 'http')
		page = loadPage(url)		
		jsonObject = json.loads(page)

		Log("formitaeten" in jsonObject["document"])	# OK - hat Videoquellen
		if "formitaeten" in jsonObject["document"]:
			# Log(jsonObject["document"]["formitaeten"])
			formitaeten = get_formitaeten(jsonObject["document"])
		else:
			DictID=url
			Dict[DictID] = jsonObject					# speichern
			Log('DictID: ' + DictID)
			oc = videoObjects=PageMenu(oc,jsonObject,DictID=DictID)	# Rubrik o.ä.	
			return oc

	# CreateVideoStreamObject + CreateVideoClipObject -> ARD Mediathek
	title_org=title
	i=0
	for detail in formitaeten:	
		i = i + 1
		quality = detail[0]
		# hd = 'HD: ' + str(detail[1])	# falsch bei mp4-Dateien (False trotz high)
		url = detail[2]
		url = url.replace('https', 'http')
		typ = detail[3]
		if url.find('master.m3u8') > 0:		# 
			title=str(i) + '. ' + title_org + ' | ' + quality + ' [m3u8]'
			tagline = 'Qualität: ' + quality + ' | Typ: ' + typ + ' [m3u8-Streaming]'
			tagline = tagline.decode(encoding="utf-8")
			oc.add(CreateVideoStreamObject(url=url, title=title, rtmp_live='nein', summary=descr, 
				tagline=tagline, meta=Plugin.Identifier + str(i), thumb=img, resolution='unbekannt'))	
		else:
			title=str(i) + '. ' + title_org + ' | ' + quality	
			tagline = 'Qualität: ' + quality + ' | Typ: ' + typ
			tagline = tagline.decode(encoding="utf-8")
			oc.add(CreateVideoClipObject(url=url, title=title, summary=descr,
				meta= Plugin.Identifier + str(i), tagline=tagline, thumb=img, 
				duration='duration', resolution='unbekannt'))		
		
	return oc
# ----------------------------------------------------------------------
def get_formitaeten(jsonObject):
	Log('get_formitaeten')
	forms=[]
	for formitaet in jsonObject["formitaeten"]:
		detail=[]
		url = formitaet["url"];
		quality = formitaet["quality"]
		hd = formitaet["hd"]
		typ = formitaet["type"]
		Log("quality:%s hd:%s url:%s" % (quality,hd,url))
		detail.append(quality); detail.append(hd); 
		detail.append(url); detail.append(typ)
		forms.append(detail)
	# Log('forms: ' + str(forms))
	return forms		
# ----------------------------------------------------------------------			
def loadPage(url, maxTimeout = None):
	try:
		safe_url = url.replace( " ", "%20" ).replace("&amp;","&")
		Log(safe_url)

		req = urllib2.Request(safe_url)
		gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11')
		req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
		req.add_header('Accept-Language', 'de-de,de;q=0.8,en-us;q=0.5,en;q=0.3')
		req.add_header('Accept-Charset', 'utf-8')

		if maxTimeout == None:
			maxTimeout = 60;
		r = urllib2.urlopen(req, timeout=maxTimeout, context=gcontext)
		doc = r.read()	
		doc = doc.encode('utf-8')
		return doc
		
	except Exception as exception:
		msg = 'Fehler: ' + str(exception)
		msg = msg + '\r\n' + safe_url			 			 	 
		msg =  msg.decode(encoding="utf-8", errors="ignore")
		Log(msg)
		return msg