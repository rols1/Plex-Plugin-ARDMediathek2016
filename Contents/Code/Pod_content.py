# -*- coding: utf-8 -*-
# Pod_content.py	- Aufruf durch __init__.py/PodFavoritenListe 
#
# Die Funktionen dienen zur Auswertung von Podcasts außerhalb www.ardmediathek.de/radio
# Basis ist die Liste podcast-favorits.txt (Default/Muster im Ressourcenverzeichnis), die
# 	Liste enthält weitere  Infos zum Format und zu bereits unterstützten Podcast-Seiten
# 	- siehe nachfolgende Liste Podcast_Scheme_List


Podcast_Scheme_List = [		# Liste vorhandener Auswertungs-Schemata
	'http://www.br-online.de', 'https://www.swr3.de/mehr/podcasts',  
	'http://www.deutschlandfunk.de', 'http://mediathek.rbb-online.de',
	'http://www.ardmediathek.de', 'http://www1.wdr.de/mediathek/podcast',
	'www1.wdr.de/mediathek/audio', 'http://www.ndr.de']	

PREFIX 			= '/video/ardmediathek2016/Pod_content'			

####################################################################################################
@route(PREFIX + '/PodFavoriten')
def PodFavoriten(title, path, offset=1):
	Log('PodFavoriten'); Log(offset)
			
	rec_per_page = 20							# Anzahl pro Seite 
	title_org = title

	Scheme = ''
	for s in Podcast_Scheme_List:				# Prüfung: Schema für path vorhanden?
		# Log(s); Log(path[:80])
		if path.find(s) >= 0:
			Scheme = s
			Log(Scheme)
			break			
	if Scheme == '':			
		msg='Auswertungs-Schema fehlt für Url:\n' +  path
		msg = msg.decode(encoding="utf-8", errors="ignore")
		Log(msg)
		return ObjectContainer(header='Error', message=msg)
		
	# Indices: 	0. Gesamtzahl, 1. Url, 2. Originaltitel, 3. Summary, 4. Datum,
	#			5. Dauer, 6. Größe, 7. Titel (zusammengesetzt), 8. Bild	, 9. Tagline
	POD_rec = get_pod_content(url=path, rec_per_page=rec_per_page, baseurl=Scheme, offset=offset)
	
	rec_cnt = len(POD_rec)							# Anzahl gelesener Sätze
	start_cnt = int(offset) + 1						# Startzahl diese Seite
	end_cnt = int(start_cnt) + int(rec_per_page)-1	# Endzahl diese Seite
	
	try:
		title2 = 'Pocasts %s - %s (%s)' % (start_cnt,  min(end_cnt,POD_rec[0][0]), POD_rec[0][0])
	except:
		title2=''
		
	oc = ObjectContainer(view_group="InfoList", title1='Favoriten', title2=title2, art = ObjectContainer.art)
	oc = home(cont=oc, ID='PODCAST')					# Home-Button
	
	if rec_cnt == 0:			
		msg='Keine Podcast-Daten gefunden. Url:\n' +  path
		msg = msg.decode(encoding="utf-8", errors="ignore")
		return ObjectContainer(header='Error', message=msg)
			
	url_list = []									# url-Liste für Sammel-Downloads (Dict['url_list'])	
	DLMultiple = True
	for rec in POD_rec:
		max_len=rec[0]
		url=rec[1]; summ=rec[3]; tagline=rec[9]; title=rec[7];
		if url == '':								# skip Satz ohne url - kann vorkommen
			continue
		if  url.endswith('.mp3') == False:			# Sammel-Downloads abschalten, falls Mehrfachseiten folgen
			DLMultiple = False
		title = unescape(title)
		url_list.append(url)
		img = R(ICON_NOTE)	
		Log(title); Log(summ[:40]); Log(url); Log(DLMultiple)
		if rec[8]:
			img = rec[8]
		if rec[8] == 'PageControl':					# Schemata mit Seitenkontrolle, Bsp. RBB
			pagepos = url.find('page')				# Bsp.: ..page-1.html, ..page1.html, ..mcontent=page.1
			page = url[pagepos:]
			pagenr = (page.replace('-', '').replace('.', '').replace('html', '').replace('page', ''))
			Log(pagenr)
			oc.add(DirectoryObject(key=Callback(PodFavoriten, title=title, path=url, offset=pagenr), 
				title=title, tagline=path, summary=summ,  thumb=R(ICON_STAR)))
		else:
			# nicht direkt zum TrackObject, sondern zu SingleSendung, um Downloadfunktion zu nutzen
			# oc.add(CreateTrackObject(url=url, title=title, summary=summ, fmt='mp3', thumb=img))
			oc.add(DirectoryObject(key=Callback(SingleSendung, path=url, title=title, thumb=img, 
				duration='leer', tagline=tagline, ID='PODCAST', summary=summ), title=title, tagline=tagline, 
				summary=summ, thumb=img))
		
	# Mehr Seiten anzeigen:
	Log(rec_cnt);Log(offset);Log(max_len)
	if (rec_cnt + int(offset)) < int(max_len): 
		new_offset = rec_cnt + int(offset)
		Log(new_offset); Log(path)
		title=title_org.decode(encoding="utf-8", errors="ignore")
		summ = 'Mehr (insgesamt ' + str(max_len) + ' Podcasts)'
		summ = summ.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(PodFavoriten, title=title, path=path, offset=new_offset), 
			title=title, tagline='Favoriten', summary=summ,  thumb=R(ICON_MEHR)))
			
	if DLMultiple == True and len(oc) > 1:			# True z.B. bei "Weiter zu Seite 1"
		# Sammel-Downloads - alle angezeigten Favoriten-Podcasts downloaden?
		#	für "normale" Podcasts erfolgt die Abfrage in SinglePage
		title='Achtung! Alle angezeigten Podcasts ohne Rückfrage speichern?'
		title = title.decode(encoding="utf-8", errors="ignore")
		summ = 'Download von insgesamt %s Podcasts' % len(POD_rec)	
		Dict['url_list'] = url_list			# als Dict - kann zu umfangreich sein als url-Parameter
		Dict['POD_rec'] = POD_rec	
		Dict.Save()
		oc.add(DirectoryObject(key=Callback(DownloadMultiple, key_url_list='url_list', key_POD_rec='POD_rec'), 
			title=title, tagline='', summary=summ,  thumb=R(ICON_DOWNL)))
				 
	return oc

#------------------------	
@route(PREFIX + '/DownloadMultiple')
# Sammeldownload lädt alle angezeigten Podcasts herunter.
# Im Gegensatz zum Einzeldownload wird keine Textdatei zum Podcast angelegt.
# DownloadExtern kann nicht von hier aus verwendet werden, da der wiederholte Einzelaufruf 
# 	von Curl kurz hintereinander auf Linux Prozessleichen hinterlässt: curl (defunct)
# Zum Problem command-line splitting (curl-Aufruf) und shlex-Nutzung siehe:
# 	http://stackoverflow.com/questions/33560364/python-windows-parsing-command-lines-with-shlex
# Das Problem >curl "[Errno 36] File name too long"< betrifft die max. Pfadlänge auf verschiedenen
#	Plattformen (Posix-Standard 4096). Teilweise ist die Pfadlänge manuell konfigurierbar.
#	Die hier gewählte platform-abhängige Variante funktioniert unter Linux + Windows (Argumenten-Länge
#	bis ca. 4 KByte getestet) 
# Rücksprung-Problem: der Button DownloadsTools ruft zwar die Funktion DownloadsTools auf, führt aber vorher
#	noch einmal den Curl-Aufruf aus mit kompl. Download - keine Abhilfe mit no_cache=True im ObjectContainer
#	oder Parameter time=time.time() für dem Callback DownloadsTools.
#	

def DownloadMultiple(key_url_list, key_POD_rec):						# Sammeldownloads
	Log('DownloadMultiple'); 
	import shlex											# Parameter-Expansion
	
	url_list = Dict[key_url_list]
	POD_rec = Dict[key_POD_rec]
	
	oc = ObjectContainer(view_group="InfoList", title1='Favoriten', title2='Sammel-Downloads', 
		art = ObjectContainer.art, no_cache=True)
	oc = home(cont=oc, ID='PODCAST')						# Home-Button
	
	rec_len = len(POD_rec)
	AppPath = Prefs['pref_curl_path']
	AppPath = os.path.abspath(AppPath)
	dest_path = Prefs['pref_curl_download_path']
	curl_param_list = '-k '									# schaltet curl's certificate-verification ab

	if os.path.exists(AppPath)	== False:					# Existenz Curl prüfen
		msg='curl nicht gefunden'
		return ObjectContainer(header='Error', message=msg)		
	if os.path.isdir(dest_path)	== False:			
		msg='Downloadverzeichnis nicht gefunden: ' + path	# Downloadverzeichnis prüfen
		return ObjectContainer(header='Error', message=msg)	
	
	i = 0
	for rec in POD_rec:										# Parameter-Liste für Curl erzeugen
		i = i + 1
		#if  i > 2:											# reduz. Testlauf
		#	break
		url = rec[1]; title = rec[7]
		title = unescape(title)								# schon in PodFavoriten, hier erneut nötig 
		if 	Prefs['pref_generate_filenames']:				# Dateiname aus Titel generieren
			dfname = make_filenames(title) + '.mp3'
		else:												# Bsp.: Download_2016-12-18_09-15-00.mp4  oder ...mp3
			now = datetime.datetime.now()
			mydate = now.strftime("%Y-%m-%d_%H-%M-%S")	
			dfname = 'Download_' + mydate + '.mp3'

		# Parameter-Format: -o Zieldatei_kompletter_Pfad Podcast-Url -o Zieldatei_kompletter_Pfad Podcast-Url ..
		curl_fullpath = os.path.join(dest_path, dfname)		 
		curl_fullpath = os.path.abspath(curl_fullpath)		# os-spezischer Pfad
		curl_param_list = curl_param_list + ' -o '  + curl_fullpath + ' ' + url
		
	cmd = AppPath + ' ' + curl_param_list
	Log(len(cmd))
	
	Log(sys.platform)
	if sys.platform == 'win32':								# s. Funktionskopf
		args = cmd
	else:
		args = shlex.split(cmd)								# ValueError: No closing quotation (1 x, Ursache n.b.)
	Log(len(args))

	try:
		call = subprocess.Popen(args, shell=False)			# shell=True entf. hier nach shlex-Nutzung	
		output,error = call.communicate()					#  output,error = None falls Aufruf OK
		Log('call = ' + str(call))	
		if str(call).find('object at') > 0:  				# Bsp.: <subprocess.Popen object at 0x7fb78361a210>
			title = 'curl: Download erfolgreich gestartet'	# trotzdem Fehlschlag möglich, z.B. ohne Schreibrecht								
			summary = 'Anzahl der Podcast: %s' % rec_len
			tagline = 'zurück zu den Download-Tools'.decode(encoding="utf-8", errors="ignore")
			oc.add(DirectoryObject(key = Callback(DownloadsTools), title=title, summary=summary, 
				tagline=tagline, thumb=R(ICON_OK)))		
			return oc				
		else:
			raise Exception('Start von curl fehlgeschlagen')			
	except Exception as exception:
		msgH = 'Fehler'; 
		summary = str(exception)
		summary = summary.decode(encoding="utf-8", errors="ignore")
		Log(summary)		
		tagline='Exception: Download fehlgeschlagen | '.decode(encoding="utf-8", errors="ignore") 
		oc.add(DirectoryObject(key = Callback(DownloadsTools), title = 'Fehler', summary=summary, 
				tagline=tagline, thumb=R(ICON_CANCEL), tagline=tagline))		
		return oc
		
	return oc

#------------------------	
def get_pod_content(url, rec_per_page, baseurl, offset):
	Log('get_pod_content'); Log(rec_per_page); Log(baseurl); Log(offset);

	url = unescape(url)							# einige url enthalten html-escapezeichen
	page, err = get_page(path=url)				# Absicherung gegen Connect-Probleme
	if page == '':
		return err
	Log(len(page))

	# baseurl aus Podcast_Scheme_List 
	if baseurl == 'http://www.br-online.de':
		return Scheme_br_online(page, rec_per_page, offset)
	if baseurl == 'https://www.swr3.de/mehr/podcasts':
		return Scheme_swr3(page, rec_per_page, offset)
	if baseurl == 'http://www.deutschlandfunk.de':
		return Scheme_deutschlandfunk(page, rec_per_page, offset)
	if baseurl == 'http://mediathek.rbb-online.de':
		sender = ''								# mp3-url mittels documentId zusammensetzen
		if url.find('documentId=24906530') > 0:
			sender = 'Fritz'					# mp3-url auf Ziel-url ermitteln
		return Scheme_rbb(page, rec_per_page, offset, sender, baseurl)
		
	if baseurl == 'http://www1.wdr.de/mediathek/podcast' or baseurl == 'www1.wdr.de/mediathek/audio':
		return Scheme_wdr(page, rec_per_page, offset)
	if baseurl == 'http://www.ndr.de':
		return Scheme_ndr(page, rec_per_page, offset)
		
	if baseurl == 'http://www.ardmediathek.de':
		return Scheme_ARD(page, rec_per_page, offset, baseurl)
		
#------------------------
def Scheme_br_online(page, rec_per_page, offset):		# Schema www.br-online.de
	Log('Scheme_br_online')
	sendungen = blockextract('class="episode-teaser"', page)
	max_len = len(sendungen)					# Gesamtzahl gefundener Sätze
	Log(max_len)
	tagline = ''
	
	POD_rec = []			# Datensaetze gesamt (1. Dim.)
	for i in range(len(sendungen)):
		cnt = int(i) + int(offset)
		# Log(cnt); Log(i)
		if int(cnt) >= max_len:			# Gesamtzahl überschritten?
			break
		if i >= rec_per_page:			# Anzahl pro Seite überschritten?
			break
		s = sendungen[cnt]
		
		single_rec = []		# Datensatz einzeln (2. Dim.)
		title_org = stringextract('"podcast-title">', '</span>', s) 
		title = title_org.strip(); title=cleanhtml(title)
		summ = stringextract('"episode-title">', '</h3>', s) 
		summ = summ.strip(); summ=cleanhtml(summ); summ=unescape(summ)
		playlist = stringextract('class="playlist"', 'Herunterladen', s)
		url = stringextract('href="', '"', playlist) 
		img =  ''						# Bild nicht vorhanden
		
		datum = stringextract('publish-date">', '</span>', s) 				# im Titel bereits vorhanden
		dauer = stringextract('duration">', '</span>', s) 
		groesse = stringextract('Gr&ouml;&szlig;e:</strong>', '</span>', s)
		
		title = '%s | %s' % (datum, title)
		if groesse:
			title = '%s | %s' % (title, groesse)	
		title = mystrip(title)
		
		Log(title); Log(summ); Log(url); 
		title=title.decode(encoding="utf-8", errors="ignore")
		summ=summ.decode(encoding="utf-8", errors="ignore")
		
		# Indices: 	0. Gesamtzahl, 1. Url, 2. Originaltitel, 3. Summary, 4. Datum,
		#			5. Dauer, 6. Größe, 7. Titel (zusammengesetzt), 8. Bild, 9. Tagline
		single_rec.append(max_len); single_rec.append(url); single_rec.append(title_org); 
		single_rec.append(summ); single_rec.append(datum); single_rec.append(dauer); 
		single_rec.append(groesse); single_rec.append(title); single_rec.append(img);
		single_rec.append(tagline);
		POD_rec.append(single_rec)
		
	Log(len(POD_rec))	
	return POD_rec
	
# ------------------------
def Scheme_swr3(page, rec_per_page, offset):	# Schema www.br-online.de
	Log('Scheme_swr3')
	sendungen = blockextract('<li id=\"audio-', page)
	max_len = len(sendungen)					# Gesamtzahl gefundener Sätze
	Log(max_len)
	tagline = ''
	
	POD_rec = []			# Datensaetze gesamt (1. Dim.)
	for i in range(len(sendungen)):
		cnt = int(i) + int(offset)
		# Log(cnt); Log(i)
		if int(cnt) >= max_len:			# Gesamtzahl überschritten?
			break
		if i >= rec_per_page:			# Anzahl pro Seite überschritten?
			break
		s = sendungen[cnt]
		
		single_rec = []		# Datensatz einzeln (2. Dim.)
		title_org = stringextract('data-title="', '\"', s) 
		title = title_org.strip()
		summ = stringextract('"duration" content="T', '\"', s) 			# Dauer statt Beschreibung (fehlt)
		summ = summ.strip()
		url = stringextract('data-mp3="', '\"', s) 
		img =  stringextract('<img src="', '\"', s) 
		img_alt =  stringextract('alt="', '\"', s) 						# Bildbeschr. - nicht verwendet
		
		datum = stringextract('datePublished">', '</time>', s) 			# im Titel ev. bereits vorhanden
		dauer = stringextract('content="T', '">', s) 
		groesse = stringextract('data-ati-size="', '"', s)
		groesse = float(int(groesse)) / 1000000						# Konvert. nach MB, auf 2 Stellen gerundet
		groesse = '%.2f MB' % groesse
		
		title = ' %s | %s' % (title, datum)
		summ = ' Dauer %s | Größe %s' % (dauer, groesse)
		
		Log(title); Log(summ); Log(url); 
		title=title.decode(encoding="utf-8", errors="ignore")
		summ=summ.decode(encoding="utf-8", errors="ignore")
		
		# Indices: 	0. Gesamtzahl, 1. Url, 2. Originaltitel, 3. Summary, 4. Datum,
		#			5. Dauer, 6. Größe, 7. Titel (zusammengesetzt), 8. Bild, 9. Tagline
		single_rec.append(max_len); single_rec.append(url); single_rec.append(title_org); 
		single_rec.append(summ); single_rec.append(datum); single_rec.append(dauer); 
		single_rec.append(groesse); single_rec.append(title); single_rec.append(img);
		single_rec.append(tagline);
		POD_rec.append(single_rec)
		
	Log(len(POD_rec))	
	return POD_rec
		
# ------------------------
def Scheme_deutschlandfunk(page, rec_per_page, offset):		# Schema www.deutschlandfunk.de, XML-Format
	Log('Scheme_deutschlandfunk')
	sendungen = blockextract('<item>', page)
	max_len = len(sendungen)								# Gesamtzahl gefundener Sätze
	Log(max_len)
	tagline = ''
	
	POD_rec = []			# Datensaetze gesamt (1. Dim.)
	for i in range(len(sendungen)):
		cnt = int(i) + int(offset)
		# Log(cnt); Log(i)
		if int(cnt) >= max_len:			# Gesamtzahl überschritten?
			break
		if i >= rec_per_page:			# Anzahl pro Seite überschritten?
			break
		s = sendungen[cnt]
		
		single_rec = []		# Datensatz einzeln (2. Dim.)
		title_org = stringextract('<title>', '</title>', s) 
		title = title_org.strip()
		summ = stringextract('vspace="4"/>', '<br', s) 			# direkt nach Bildbeschreibung
		summ = summ.strip()
		url = stringextract('<enclosure url="', '"', s) 
		img =  stringextract('<img src="', '\"', s) 
		img_alt =  stringextract('alt="', '\"', s) 						# 
		
		author = stringextract('itunes:author>', '</itunes:author>', s) 
		datum = stringextract('<pubDate>', '</pubDate>', s)
		datum = datum.replace('+0200', '')	
		dauer = stringextract('duration>', '</itunes', s) 
		groesse = stringextract('length="', '"', s) 
		groesse = float(int(groesse)) / 1000000						# Konvert. nach MB, auf 2 Stellen gerundet
		groesse = '%.2f MB' % groesse
		
		title = ' %s | %s' % (title, datum)
		summ = ' Autor %s | Datum %s | Größe %s' % (author, datum, groesse)
		
		Log(title); Log(summ); Log(url); 
		title=title.decode(encoding="utf-8", errors="ignore")
		summ=summ.decode(encoding="utf-8", errors="ignore")
		
		# Indices: 	0. Gesamtzahl, 1. Url, 2. Originaltitel, 3. Summary, 4. Datum,
		#			5. Dauer, 6. Größe, 7. Titel (zusammengesetzt), 8. Bild, 9. Tagline
		single_rec.append(max_len); single_rec.append(url); single_rec.append(title_org); 
		single_rec.append(summ); single_rec.append(datum); single_rec.append(dauer); 
		single_rec.append(groesse); single_rec.append(title); single_rec.append(img);
		single_rec.append(tagline);
		POD_rec.append(single_rec)
		
	Log(len(POD_rec))	
	return POD_rec
		
# ------------------------
def Scheme_rbb(page, rec_per_page, offset,sender, baseurl):		# Schema mediathek.rbb-online.de
# 	Besonderheit: offset = Seitennummer
# 	1. Aufruf kommt mit ..&mcontent=page.1
	Log('Scheme_rbb'); Log(offset); Log(sender)

	POD_rec = []			# Datensaetze gesamt (1. Dim.)
	pages = blockextract('entry" data-ctrl-contentLoader-source', page)		# Seiten-Urls
	max_len = len(pages)
	Log(max_len)
	page_href = baseurl + stringextract('href="', '">', pages[0])
	page_href = page_href.split('mcontent=')[0]		# Basis-url ohne Seitennummer
	tagline = ''
	
	if offset == '0':								# 1. Durchlauf - Seitenkontrolle 
		pagenr = 1
		for p in pages:
			single_rec = []							# Datensatz einzeln (2. Dim.)
			url = page_href + 'mcontent=page.' + str(pagenr)	 # url mit Seitennr, ergänzen
			title = 'Weiter zu Seite %s' % pagenr
			img = 'PageControl';					# 'PageControl' steuert 
			summ = ''; title_org = ''; datum = ''; dauer = ''; groesse = ''; 
			pagenr = pagenr + 1
			
			Log(title); Log(url); 
			title=title.decode(encoding="utf-8", errors="ignore")
			summ=summ.decode(encoding="utf-8", errors="ignore")
			
			# Indices: 	0. Gesamtzahl, 1. Url, 2. Originaltitel, 3. Summary, 4. Datum,
			#			5. Dauer, 6. Größe, 7. Titel (zusammengesetzt), 8. Bild, 9. Tagline
			single_rec.append(max_len); single_rec.append(url); single_rec.append(title_org); 
			single_rec.append(summ); single_rec.append(datum); single_rec.append(dauer); 
			single_rec.append(groesse); single_rec.append(title); single_rec.append(img);
			single_rec.append(tagline);
			POD_rec.append(single_rec)
		return POD_rec
	
	sendungen = blockextract('class="teaser"', page)  # Struktur wie ARD-Mediathek
	del sendungen[0]; del sendungen[1]			# Sätze 1 + 2 keine Podcasts
	max_len = len(sendungen)					# Gesamtzahl gefundener Sätze dieser Seite
	Log(max_len)
	
	for i in range(len(sendungen)):
		cnt = int(i) 		# + int(offset) Offset entfällt (pro Seite Ausgabe aller Sätze)
		# Log(cnt); Log(i)
		#if int(cnt) >= max_len:		# Gesamtzahl überschritten? - entf. hier
		s = sendungen[cnt]
		
		single_rec = []		# Datensatz einzeln (2. Dim.)
		title_org = stringextract('dachzeile">', '</p>', s) 
		summ = stringextract('subtitle">', '<', s) 		# Bsp.: Do 13.04.17 00:00 | 03:28 min	
		headline = stringextract('headline">', '</h4>', s)  # häufig mehr Beschreibung als Headline
		
		url_local = stringextract('<a href="', '"', s) 		# Homepage der Sendung
		url_local = baseurl + url_local
		url_local = decode_url(url_local)					# f%C3%BCr -> für, 	&amp; -> &
		Log(url_local)
		try:												# mp3-url auf Ziel-url ermitteln
			url_local = unescape(url_local)
			page, err = get_page(path=url_local)			# Absicherung gegen Connect-Probleme
			url = stringextract('<div data-ctrl-ta-source', 'target="_blank"', page)
			url = stringextract('a href="', '"', url)
			Log(url)		
		except:	
			url=''											

		if url.endswith('.mp3') == False:					# mp3-url mittels documentId zusammensetzen
			documentId =  re.findall("documentId=(\d+)", url_local)[0]
			url = baseurl + '/play/media/%s?devicetype=pc&features=hls' % documentId
			Log('hlsurl: ' + url)
			try:
				url_content, err = get_page(path=url)				# Textdatei, Format ähnlich parseLinks_Mp4_Rtmp
				url = stringextract('stream":"', '"}', url_content) # geändert 24.01-2018	
			except:
				url=''
		Log(url)
			
		text = stringextract('urlScheme', '/noscript', s)
		img, img_alt = img_urlScheme(text, 320, ID='PODCAST') # img_alt nicht verwendet
		
		author = ''	  										# fehlt
		groesse = ''	  										# fehlt
		datum = summ.split('|')[0]
		dauer = summ.split('|')[1]
				
		title = ' %s | %s  | %s' % (title_org, datum, dauer)
		summ = headline
		summ = unescape(summ)
		
		Log(title); Log(summ); Log(url); 
		title=title.decode(encoding="utf-8", errors="ignore")
		summ=summ.decode(encoding="utf-8", errors="ignore")
		
		# Indices: 	0. Gesamtzahl, 1. Url, 2. Originaltitel, 3. Summary, 4. Datum,
		#			5. Dauer, 6. Größe, 7. Titel (zusammengesetzt), 8. Bild, 9. Tagline
		single_rec.append(max_len); single_rec.append(url); single_rec.append(title_org); 
		single_rec.append(summ); single_rec.append(datum); single_rec.append(dauer); 
		single_rec.append(groesse); single_rec.append(title); single_rec.append(img);
		single_rec.append(tagline);
		POD_rec.append(single_rec)
		
	Log(len(POD_rec))	
	return POD_rec
		
# ------------------------
def Scheme_wdr(page, rec_per_page, offset):		# Schema WDR, XML-Format
	Log('Scheme_wdr')
	sendungen = blockextract('<item>', page)
	max_len = len(sendungen)									# Gesamtzahl gefundener Sätze
	Log(max_len)
	title_channel = stringextract('<title>', '</title>', page)	# Channel-Titel
	tagline = ''
	
	POD_rec = []			# Datensaetze gesamt (1. Dim.)
	for i in range(len(sendungen)):
		cnt = int(i) + int(offset)
		# Log(cnt); Log(i)
		if int(cnt) >= max_len:			# Gesamtzahl überschritten?
			break
		if i >= rec_per_page:			# Anzahl pro Seite überschritten?
			break
		s = sendungen[cnt]
		
		single_rec = []		# Datensatz einzeln (2. Dim.)
		title_org = stringextract('<title>', '</title>', s) 
		title = title_org.strip()
		summ = stringextract('<description>', '</description>', s) 			
		summ = summ.strip()
		summ = unescape(summ)
		url = stringextract('<enclosure url="', '"', s) 
		img =  stringextract('<img src="', '\"', s) 
		img_alt =  stringextract('alt="', '\"', s) 						# 
		
		author = stringextract('itunes:author>', '</itunes:author>', s) 
		datum = stringextract('<pubDate>', '</pubDate>', s)
		datum = datum.replace('GMT', '')	
		dauer = stringextract('duration>', '</itunes', s) 
		groesse = stringextract('length="', '"', s) 					# fehlt
		#groesse = float(int(groesse)) / 1000000						# Konvert. nach MB, auf 2 Stellen gerundet
		#groesse = '%.2f MB' % groesse
		
		title = ' %s | %s'			% (title, datum)
		summ = ' Autor %s | %s' 	% (author, summ)
		
		Log(title); Log(summ); Log(url); 
		title=title.decode(encoding="utf-8", errors="ignore")
		summ=summ.decode(encoding="utf-8", errors="ignore")
		
		# Indices: 	0. Gesamtzahl, 1. Url, 2. Originaltitel, 3. Summary, 4. Datum,
		#			5. Dauer, 6. Größe, 7. Titel (zusammengesetzt), 8. Bild, 9. Tagline
		single_rec.append(max_len); single_rec.append(url); single_rec.append(title_org); 
		single_rec.append(summ); single_rec.append(datum); single_rec.append(dauer); 
		single_rec.append(groesse); single_rec.append(title); single_rec.append(img);
		single_rec.append(tagline);
		POD_rec.append(single_rec)
		
	Log(len(POD_rec))	
	return POD_rec
		
# ------------------------
def Scheme_ndr(page, rec_per_page, offset):		# Schema NDR
	Log('Scheme_ndr'); Log(offset);Log(len(page))

	baseurl = 'http://www.ndr.de'
	POD_rec = []			# Datensaetze gesamt (1. Dim.)	

	pages = stringextract('<div class="pagination">', '<a title=', page)	# Seiten-Urls für Seitenkontrolle
	page_href = baseurl + stringextract('href="', '-', pages)				# zum Ergänzen mit 1.html, 2.html usw.
	# Log(page_href)
	entry_type = '_page-'
	pages = pages.split(entry_type)				# .. href="/ndr2/programm/podcast2958_page-6.html" title="Zeige Seite 6">		
	# Log(pages)
	last_page = pages[-1]						# Bsp. 6.html
	last_page = re.search('(\d+)', last_page).group(1)	
	Log(last_page)
	tagline = ''
	
	if offset == '0':									# 1. Durchlauf - Seitenkontrolle:
		pagenr = 0
		# Log(last_page)
		for i in range(int(last_page)):
			title_org=''; 
			max_len = last_page
			single_rec = []								# Datensatz einzeln (2. Dim.)
			pagenr = i + 1
			if pagenr >= last_page:
				break
			url = page_href + '-' + str(pagenr) + '.html' # url mit Seitennr. ergänzen
			title = 'Weiter zu Seite %s' % pagenr
			img = 'PageControl';						# 'PageControl' steuert in PodFavoriten
			summ = ''; title_org = ''; datum = ''; dauer = ''; groesse = ''; 
			
			Log(title); Log(url); Log(pagenr); Log(last_page)
			title=title.decode(encoding="utf-8", errors="ignore")
			summ=summ.decode(encoding="utf-8", errors="ignore")
			
			# Indices: 	0. Gesamtzahl, 1. Url, 2. Originaltitel, 3. Summary, 4. Datum,
			#			5. Dauer, 6. Größe, 7. Titel (zusammengesetzt), 8. Bild, 9. Tagline
			single_rec.append(max_len); single_rec.append(url); single_rec.append(title_org); 
			single_rec.append(summ); single_rec.append(datum); single_rec.append(dauer); 
			single_rec.append(groesse); single_rec.append(title); single_rec.append(img);
			single_rec.append(tagline);
			POD_rec.append(single_rec)
		return POD_rec							# Rückkehr aus Seitenkontrolle
		
												# 2. Durchlauf - Inhalte der einzelnen Seiten:
	sendungen = blockextract('class="module list w100">', page) 
	if sendungen[2].find('urlScheme') >= 0:								# 2 = Episodendach
		text = stringextract('urlScheme', '/noscript', sendungen[2])
		img_src_header, img_alt_header = img_urlScheme(text, 320, ID='PODCAST') 
		teasertext = stringextract('class="teasertext">', '</p>', sendungen[2])
		Log(img_src_header);Log(img_alt_header);Log(teasertext);
	
	
	max_len = len(sendungen)					# Gesamtzahl gefundener Sätze dieser Seite
	Log(max_len)
	
	for i in range(len(sendungen)):
		# cnt = int(i) 		# + int(offset) Offset entfällt (pro Seite Ausgabe aller Sätze)
		# Log(cnt); Log(i)
		# if int(cnt) >= max_len:		# Gesamtzahl überschritten? - entf. hier
		# s = sendungen[cnt]
		s = sendungen[i]
		# Log(s)
		
		single_rec = []		# Datensatz einzeln (2. Dim.)
		title_org = stringextract('title="Zum Audiobeitrag: ', '"', s) 
		subtitle =  stringextract('subline">', '<', s)			# Bsp.: 06.04.2017 06:50 Uhr
		if subtitle == '':
			subtitle =  stringextract('subline date">', '<', s)	# Bsp.: date">18.05.2017 06:50 Uhr
		summ = stringextract('<p>', '<a title', s) 			
		dachzeile = ''										# fehlt		
		headline = ''										# fehlt	
		
		pod = stringextract('podcastbuttons">', 'class="button"', s)
		pod = pod.strip()
		Log(pod[40:])
		url = stringextract('href=\"', '\"', pod)		# kompl. Pfad
		if url == '':									# kein verwertbarer Satz 
			continue			
			
		img = ''											# fehlt	
		author = ''	  										# fehlt
		groesse = ''	  									# fehlt
		datum = subtitle
		dauer = stringextract('class="cta " >', '</a>', s) 
		
		title = '%s | %s' % (subtitle, title_org)
		tagline = '%s | %s' % (subtitle, dauer)
						
		Log(title); Log(summ); Log(url); 
		title=title.decode(encoding="utf-8", errors="ignore")
		summ=summ.decode(encoding="utf-8", errors="ignore")
		tagline=tagline.decode(encoding="utf-8", errors="ignore")
		
		# Indices: 	0. Gesamtzahl, 1. Url, 2. Originaltitel, 3. Summary, 4. Datum,
		#			5. Dauer, 6. Größe, 7. Titel (zusammengesetzt), 8. Bild, 9. Tagline
		single_rec.append(max_len); single_rec.append(url); single_rec.append(title_org); 
		single_rec.append(summ); single_rec.append(datum); single_rec.append(dauer); 
		single_rec.append(groesse); single_rec.append(title); single_rec.append(img);
		single_rec.append(tagline);
		POD_rec.append(single_rec)
		
	Log(len(POD_rec))	
	return POD_rec	
		
# ------------------------
def Scheme_ARD(page, rec_per_page, offset,baseurl):		# Schema ARD = www.ardmediathek.de
# 	Schema für die Podcastangebote der ARD-Mediathek
# 	1. Aufruf kommt mit ..&mcontents=page.1 (nicht ..content=..)
	Log('Scheme_ARD'); Log(offset);

	POD_rec = []			# Datensaetze gesamt (1. Dim.)
	page = stringextract('class="section onlyWithJs sectionA">', '<!--googleoff: snippet-->', page)
	
	pages = blockextract('class="entry"', page)			# Seiten-Urls für Seitenkontrolle
	max_len = len(pages)
	Log(max_len)
	if pages:											# Seiten ohne Seitenkontrolle möglich
		page_href = baseurl + stringextract('href="', '">', pages[0])
		if page_href.find('mcontents=page.') > 0:			# ..mcontents=page.1
			entry_type = 'mcontents=page.'
		if page_href.find('mcontent=page.') > 0:			# ..mcontent=page.1
			entry_type = 'mcontent=page.'
		page_href = page_href.split(entry_type)[0]			# Basis-url ohne Seitennummer
		Log(entry_type)
	tagline = ''

	# für Seiten mit offset=0 aber ohne Seitenkontrolle direkt weiter bei sendungen
	if offset == '0' and pages:							# 1. Durchlauf - Seitenkontrolle
		pagenr = 1
		for p in pages:
			single_rec = []								# Datensatz einzeln (2. Dim.)
			url = page_href + entry_type + str(pagenr)	 # url mit Seitennr. ergänzen
			url = unescape(url)
			title = 'Weiter zu Seite %s' % pagenr
			img = 'PageControl';						# 'PageControl' steuert 
			summ = ''; title_org = ''; datum = ''; dauer = ''; groesse = ''; 
			pagenr = pagenr + 1
			
			Log(title); Log(url); 
			title=title.decode(encoding="utf-8", errors="ignore")
			summ=summ.decode(encoding="utf-8", errors="ignore")
			
			# Indices: 	0. Gesamtzahl, 1. Url, 2. Originaltitel, 3. Summary, 4. Datum,
			#			5. Dauer, 6. Größe, 7. Titel (zusammengesetzt), 8. Bild, 9. Tagline
			single_rec.append(max_len); single_rec.append(url); single_rec.append(title_org); 
			single_rec.append(summ); single_rec.append(datum); single_rec.append(dauer); 
			single_rec.append(groesse); single_rec.append(title); single_rec.append(img);
			single_rec.append(tagline);
			POD_rec.append(single_rec)
		return POD_rec							# Rückkehr aus Seitenkontrolle
		
												# 2. Durchlauf - bzw. ohne Seitenkontrolle direkt -
												# Inhalte der einzelnen Seiten:	
	sendungen = blockextract('class="teaser"', page)  # Struktur für Podcasts + Videos ähnlich
	img_src_header=''; img_alt_header=''; teasertext=''
	max_len = len(sendungen)					# Gesamtzahl gefundener Sätze dieser Seite
	# Log('sendungen[0]; ' + sendungen[0])		# bei Bedarf
	if sendungen[0].find('urlScheme') >= 0:								# [0] = Episodendach
		text = stringextract('urlScheme', '/noscript', sendungen[0])
		img_src_header, img_alt_header = img_urlScheme(text, 320, ID='PODCAST') 
		teasertext = stringextract('class="teasertext">', '</p>', sendungen[0])
		max_len = str(max_len - 1)				# sonst klappt's nicht mit 'Mehr'-Anzeige
		Log(img_src_header);Log(img_alt_header);Log(teasertext);
	
	Log('max_len: ' + max_len)
	
	for i in range(len(sendungen)):
		# cnt = int(i) 		# + int(offset) Offset entfällt (pro Seite Ausgabe aller Sätze)
		# Log(cnt); Log(i)
		# if int(cnt) >= max_len:		# Gesamtzahl überschritten? - entf. hier
		# s = sendungen[cnt]
		s = sendungen[i]
		Log(len(s));    # Log(s)
		
		single_rec = []		# Datensatz einzeln (2. Dim.)
		title_org = stringextract('dachzeile">', '</p>', s) 
		subtitle =  stringextract('subtitle">', '<', s)		# Bsp.: 06.02.2017 | 1 Min.
		summ = stringextract('teasertext">', '<', s) 			
		dachzeile = stringextract('dachzeile">', '</p>', s)  # Sendereihe		
		headline = stringextract('headline">', '</h4>', s)  # Titel der einzelnen Sendung
		
		url_local = stringextract('<a href="', '"', s) 		# Homepage der Sendung
		if url_local == '' or url_local.find('documentId=') == -1:	# kein verwertbarer Satz 
			continue
		url_local = baseurl + url_local
		Log('url_local: ' + url_local)
		documentId =  re.findall("documentId=(\d+)", url_local)[0]
		url = baseurl + '/play/media/%s?devicetype=pc&features=hls' % documentId 	# Quelldatei Podcast
		url_content, err = get_page(path=url)			# Textdatei, Format ähnlich parseLinks_Mp4_Rtmp
		Log('url_content: ' + url_content[:60])
		if url_content == '':
			Log('url_content leer')
			return err
		url = stringextract('stream":"', '"', url_content) # manchmal 2 identische url
		Log('mp3-url: ' + url)	
			
		text = stringextract('urlScheme', '/noscript', s)
		img, img_alt = img_urlScheme(text, 320, ID='PODCAST') # img_alt nicht verwendet
		if img == '':										# Episodenbild 
			img =img_src_header 
		
		author = '';  groesse = ''  						# fehlen hier
		datum = '';  dauer = '';			
		if subtitle.find('|') > 0:
			datum = subtitle.split('|')[0]
			dauer = subtitle.split('|')[1]
		
		if dachzeile:
			title = ' %s | %s ' % (dachzeile, headline)
			summ =  ' %s | %s' % (datum, dauer)
		else:
			title = ' %s | %s | %s' % (headline, datum, dauer)
			if teasertext:
				summ = teasertext
		title = title.replace('|  |', '')						# Datum + Dauer können fehlen
				
		tagline = teasertext									# aus Episodendach, falls vorh.
		tagline = unescape(tagline)
		summ = unescape(summ)
		
		Log(title); Log(summ); Log(url); 
		title=title.decode(encoding="utf-8", errors="ignore")
		summ=summ.decode(encoding="utf-8", errors="ignore")
		tagline=tagline.decode(encoding="utf-8", errors="ignore")
		
		# Indices: 	0. Gesamtzahl, 1. Url, 2. Originaltitel, 3. Summary, 4. Datum,
		#			5. Dauer, 6. Größe, 7. Titel (zusammengesetzt), 8. Bild, 9. Tagline
		single_rec.append(max_len); single_rec.append(url); single_rec.append(title_org); 
		single_rec.append(summ); single_rec.append(datum); single_rec.append(dauer); 
		single_rec.append(groesse); single_rec.append(title); single_rec.append(img);
		single_rec.append(tagline);
		POD_rec.append(single_rec)
		
	Log(len(POD_rec))	
	return POD_rec	
		
#----------------------------------------------------------------  

####################################################################################################
#									Hilfsfunktionen
####################################################################################################
#def stringextract(mFirstChar, mSecondChar, mString):  	# extrahiert Zeichenkette zwischen 1. + 2. Zeichenkette
	pos1 = mString.find(mFirstChar)						# return '' bei Fehlschlag
	ind = len(mFirstChar)
	#pos2 = mString.find(mSecondChar, pos1 + ind+1)		
	pos2 = mString.find(mSecondChar, pos1 + ind)		# ind+1 beginnt bei Leerstring um 1 Pos. zu weit
	rString = ''

	if pos1 >= 0 and pos2 >= 0:
		rString = mString[pos1+ind:pos2]	# extrahieren 
		
	#Log(mString); Log(mFirstChar); Log(mSecondChar); 	# bei Bedarf
	#Log(pos1); Log(ind); Log(pos2);  Log(rString); 
	return rString
#----------------------------------------------------------------  
def teilstring(zeile, startmarker, endmarker):  		# rfind: endmarker=letzte Fundstelle, return '' bei Fehlschlag
  # die übergebenen Marker bleiben Bestandteile der Rückgabe (werden nicht abgeschnitten)
  pos2 = zeile.find(endmarker, 0)
  pos1 = zeile.rfind(startmarker, 0, pos2)
  if pos1 & pos2:
    teils = zeile[pos1:pos2+len(endmarker)]	# 
  else:
    teils = ''
  #Log(pos1) Log(pos2) 
  return teils 
#----------------------------------------------------------------  
def blockextract(blockmark, mString):  	# extrahiert Blöcke begrenzt durch blockmark aus mString
	#	blockmark bleibt Bestandteil der Rückgabe
	#	Rückgabe in Liste. Letzter Block reicht bis Ende mString (undefinierte Länge),
	#		Variante mit definierter Länge siehe Plex-Plugin-TagesschauXL (extra Parameter blockendmark)
	#	Verwendung, wenn xpath nicht funktioniert (Bsp. Tabelle EPG-Daten www.dw.com/de/media-center/live-tv/s-100817)
	rlist = []				
	if 	blockmark == '' or 	mString == '':
		Log('blockextract: blockmark or mString leer')
		return rlist
	
	pos = mString.find(blockmark)
	if 	mString.find(blockmark) == -1:
		Log('blockextract: blockmark nicht in mString enthalten')
		# Log(pos); Log(blockmark);Log(len(mString));Log(len(blockmark));
		return rlist
	pos2 = 1
	while pos2 > 0:
		pos1 = mString.find(blockmark)						
		ind = len(blockmark)
		pos2 = mString.find(blockmark, pos1 + ind)		
	
		block = mString[pos1:pos2]	# extrahieren einschl.  1. blockmark
		rlist.append(block)
		# reststring bilden:
		mString = mString[pos2:]	# Rest von mString, Block entfernt	
	return rlist  
#----------------------------------------------------------------  
def unescape(line):	# HTML-Escapezeichen in Text entfernen, bei Bedarf erweitern. ARD auch &#039; statt richtig &#39;
#					# s.a.  ../Framework/api/utilkit.py
	line_ret = (line.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
		.replace("&#39;", "'").replace("&#039;", "'").replace("&quot;", '"').replace("&#x27;", "'")
		.replace("&ouml;", "ö").replace("&auml;", "ä").replace("&uuml;", "ü").replace("&szlig;", "ß")
		.replace("&Ouml;", "Ö").replace("&Auml;", "Ä").replace("&Uuml;", "Ü").replace("&apos;", "'")
		.replace("&#xD;", " "))
		
	# Log(line_ret)		# bei Bedarf
	return line_ret	
#----------------------------------------------------------------  	
def decode_url(line):	# in URL kodierte Umlaute und & wandeln, Bsp. f%C3%BCr -> für, 	&amp; -> &
	urllib.unquote(line)
	line = line.replace('&amp;', '&')
	return line
#----------------------------------------------------------------  	
def mystrip(line):	# eigene strip-Funktion, die auch Zeilenumbrüche innerhalb des Strings entfernt
	line_ret = line	
	line_ret = line.replace('\t', '').replace('\n', '').replace('\r', '')
	line_ret = line_ret.strip()	
	# Log(line_ret)		# bei Bedarf
	return line_ret
#----------------------------------------------------------------  	
