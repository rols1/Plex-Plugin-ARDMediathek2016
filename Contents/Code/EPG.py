# -*- coding: utf-8 -*-
# EPG, Daten von tvtoday.de 
#	URL-Schema: http://www.tvtoday.de/programm/standard/sender/%s.html  %s=ID, z.B. ard oder ARD
#	Datumsbereich: 12 Tage, Bsp. MO - FR
#	Zeitbereich	5 Uhr - 5 Uhr Folgetag
#		Einteilung (tvtoday.de): 5-11, 11-14, 14-18, 18-20, 20-00, 00-05 Uhr  (hier nicht verwendet)
#	Struktur:
#		Container: tv-show-container js-tv-show-container
#		Blöcke: <a href=" .. </a>
#		Sendezeit: data-start-time="", data-end-time=""
#		
 
import time
import datetime
from datetime import date


EPG_BASE =  "http://www.tvtoday.de"

PREFIX = '/video/ardmediathek2016'			
@route(PREFIX + '/EPG')		# EPG-Daten holen
# 	mode: 		falls 'OnlyNow' dann JETZT-Sendungen
# 	day_offset:	1,2,3 ... Offset in Tagen (Verwendung zum Blättern in EPG_ShowSingle)
def EPG(ID, mode=None, day_offset=None):
	Log('EPG ID: ' + ID)
	Log(mode)
	url="http://www.tvtoday.de/programm/standard/sender/%s.html" % ID
	Log(url)

	page, err = get_page(path=url, cTimeout=1)				# Absicherung gegen Connect-Probleme
	# Log(page[:500])	# bei Bedarf
	if err:
		return ''	# Verarbeitung in SenderLiveListe (rec = EPG.EPG..)
	Log(len(page))

	pos = page.find('tv-show-container js-tv-show-container')	# ab hier relevanter Inhalt
	page = page[pos:]
	Log(len(page))

	liste = blockextract('href=\"', page)  
	Log(len(liste));	

	# today.de verwendet Unix-Format, Bsp. 1488830442
	now,today,today_5Uhr,nextday,nextday_5Uhr = get_unixtime(day_offset)# lokale Unix-Zeitstempel holen + Offsets
	now_human = datetime.datetime.fromtimestamp(int(now))				# Debug: Übereinstimmung mit UTC, Timezone?	
	now_human =  now_human.strftime("%d.%m.%Y, %H:%M:%S")				# deutsches Format
	today_human = datetime.datetime.fromtimestamp(int(today_5Uhr))
	today_human =  today_human.strftime("%d.%m.%Y, %H:%M Uhr")			# deutsches Format mit Offset (Datumanzeige ab ...)
	
	Log(now); Log(now_human); Log(today_human);
	# Log(today); Log(today_5Uhr); Log(nextday); Log(nextday_5Uhr)	# bei Bedarf

	# Ausgabe: akt. Tag ab 05 Uhr(Start) bis nächster Tag 05 Uhr (Ende)
	#	
	# Log("neuer Satz:")
	EPG_rec = []
	for i in range (len(liste)):		# ältere + jüngere Sendungen in Liste - daher Schleife + Zeitabgleich	
		# Log(liste[i])					# bei Bedarf
		rec = []
		starttime = stringextract('data-start-time=\"', '\"', liste[i]) # Sendezeit, Bsp. "1488827700" (UTC)
		if starttime == '':									# Ende (Impressum)
			break
		endtime = stringextract('data-end-time=\"', '\"', liste[i])	 	# Format wie starttime
		href = stringextract('href=\"', '\"', liste[i])					# wenig zusätzl. Infos
		img = stringextract('data-lazy-load-src=\"', '\"', liste[i])
		sname = stringextract('class=\"h7 name\">', '</p>', liste[i])
		stime = stringextract('class=\"h7 time\">', '</p>', liste[i])   # Format: 06:00
		stime = stime.strip()
		summ = get_summ(liste[i])								# Beschreibung holen
		
		sname = stime + ' | ' + sname							# Titel: Bsp. 06:40 | Nachrichten

		s_start = 	datetime.datetime.fromtimestamp(int(starttime))	# Zeit-Konvertierung UTC-Startzeit
		s_startday =  s_start.strftime("%A") 					# Locale’s abbreviated weekday name
		
		von = stime
		bis = datetime.datetime.fromtimestamp(int(endtime))
		bis = bis.strftime("%H:%M") 
		vonbis = von + '-' + bis
		
		# Auslese - nur akt. Tag 05 Uhr (einschl. Offset in Tagen ) + Folgetag 05 Uhr:
		if starttime < today_5Uhr:				# ältere verwerfen
			# Log(starttime); Log(nextday_5Uhr)
			continue
		if starttime > nextday_5Uhr:			# jüngere verwerfen
			# Log(starttime); Log(nextday_5Uhr)
			continue
						
		if now >= starttime and now < endtime:
			# Log(now); Log(starttime); Log(endtime)	# bei Bedarf
			sname = "JETZT: " + sname
			# Log(sname); Log(img)				# bei Bedarf
			if mode == 'OnlyNow':				# aus EPG_ShowAll - nur aktuelle Sendung
				rec = [starttime,href,img,sname,stime,summ,vonbis]  # Index wie EPG_rec
				# Log(rec)
				return rec						# Rest verwerfen - Ende		
		
		iWeekday = transl_wtag(s_startday)
		sname = iWeekday[0:2] + ' | ' + sname	# Wochentag voranstellen

		# Indices EPG_rec: 0=starttime, 1=href, 2=img, 3=sname, 4=stime, 5=summ, 6=vonbis, 7=today_human:  
		# Link href zum einzelnen Satz hier nicht verwendet - wenig zusätzl. Infos
		rec.append(starttime);rec.append(href); rec.append(img); rec.append(sname);	# Listen-Element
		rec.append(stime); rec.append(summ); rec.append(vonbis); rec.append(today_human);
		EPG_rec.append(rec)											# Liste Gesamt (2-Dim-Liste)
	
	EPG_rec.sort()						# Sortierung	
	Log(len(EPG_rec))
	return EPG_rec
#-----------------------
def get_summ(block):		# Beschreibung holen
	summ = ''
	descr_list = blockextract('small-meta description', block)	# 1-2 mal vorhanden
	i = 0
	for item in descr_list:
		descr = stringextract('small-meta description\">', '</p>', item)
		if descr:
			if summ:
				summ = summ  + ' | ' + descr
			else:
				summ = descr
		i = i + 1
			
	childinfo = stringextract('children-info\">', '</p>', block)
	if childinfo:
		summ = summ + ' | ' + childinfo	
	return summ

####################################################################################################
#									Hilfsfunktionen
####################################################################################################
# get_unixtime() ermittelt 'jetzt', 'nächster Tag' und 'nächster Tag, 5 Uhr 'im Unix-Format
#	tvtoday.de verwendet Unix-Format: data-start-time, data-end-time (beide ohne Sekunden)
# 	day_offset:	1,2,3 ... Offset in Tagen
#	Rückgabe today: today + Offset
def get_unixtime(day_offset=None):		
	dt = datetime.datetime.now()								# Format 2017-03-09 22:04:19.044463
	now = time.mktime(dt.timetuple())							# Unix-Format 1489094334.0
	dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)  # auf 0 Uhr setzen: 2017-03-09 00:00:00
	today = time.mktime(dt.timetuple())							# Unix-Format 1489014000.0
	# today = time.mktime(d.timetuple()) 						# Ergebnis wie oben
		
	if day_offset:
		today = today + (int(day_offset) * 86400)				# Zuschlag in ganzen Tagen (1 Tag = 86400 sec)
	nextday = today + 86400										# nächster Tag 			(+ 86400 sec = 24 x 3600)
	today_5Uhr = today + 18000									# today+Offset, 05 Uhr  (+ 18000 sec = 5 x 3600)
	nextday_5Uhr = nextday + 18000								# nächster Tag, 05 Uhr 
	
	now = str(now).split('.')[0]								# .0 kappen (tvtoday.de ohne .0)
	today = str(today).split('.')[0]
	nextday = str(nextday).split('.')[0]
	nextday_5Uhr = str(nextday_5Uhr).split('.')[0]
	today_5Uhr = str(today_5Uhr).split('.')[0]
	
	# Bei Bedarf Konvertierung 'Human-like':
	# nextday_str = datetime.datetime.fromtimestamp(int(nextday))
	# nextday_str = nextday.strftime("%Y%m%d")	# nächster Tag, Format 20170331
		
	return now,today,today_5Uhr,nextday,nextday_5Uhr
#----------------------------------------------------------------  
def transl_wtag(tag):	# Wochentage engl./deutsch wg. Problemen mit locale-Setting 
	wt_engl = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	wt_deutsch = ["MONTAG", "DIENSTAG", "MITTWOCH", "DONNERSTAG", "FREITAG", "SAMSTAG", "SONNTAG"]
	
	wt_ret = tag
	for i in range (len(wt_engl)):
		el = wt_engl[i]
		if el == tag:
			wt_ret = wt_deutsch[i]
			break
	return wt_ret
#----------------------------------------------------------------  
def get_page(path, cTimeout=None):		# holt kontrolliert raw-Content - s. Erweiterung in init.py
	Log('get_page');
	msg = ''; page = ''				
	try:
		if cTimeout:					# mit Cachevorgabe
			page = HTTP.Request(path, cacheTime=int(cTimeout) ).content
		else:
			page = HTTP.Request(path).content
	except Exception as exception:
		summary = str(exception)
		summary = summary.decode(encoding="utf-8", errors="ignore")
		Log(summary)		
		
	if page == '':	
		error_txt = 'Seite nicht erreichbar'			 			 	 
		msgH = 'Fehler'; msg = error_txt + ' | Seite: ' + path
		Log(msg)
		msg =  msg.decode(encoding="utf-8", errors="ignore")
		# err = ObjectContainer(header=msgH, message=msg)

	return page, msg	
#----------------------------------------------------------------  
def stringextract(mFirstChar, mSecondChar, mString):  	# extrahiert Zeichenkette zwischen 1. + 2. Zeichenkette
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
def blockextract(blockmark, mString):  	# extrahiert Blöcke aus mString, begrenzt durch blockmark 
	#	blockmark bleibt Bestandteil der Rückgabe
	#	Rückgabe in Liste. Letzter Block reicht bis Ende mString (undefinierte Länge)
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

		
