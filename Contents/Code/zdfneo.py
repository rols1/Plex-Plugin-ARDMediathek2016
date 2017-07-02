# -*- coding: utf-8 -*-
# zdfneo.py	- Aufruf durch __init__.py/ZDF_get_content
#
# Die Funktionen dienen zur Auswertung der ZDF-Neo-Seiten
#

Neo_Base = 'https://www.neo-magazin-royale.de'

PREFIX 			= '/video/ardmediathek2016/zdfneo'			
####################################################################################################
@route(PREFIX + '/neo_content')
def neo_content(path, ID, offset=0):			
	Log('neo_content')
	# JUMPPATH = 'https://www.neo-magazin-royale.de/zdi/?start=%s&count=8' 	# auch redakt. Beiträge
	# JUMPPATH: start=0: Seite 1, 8=Seite 2
	JUMPPATH = 'https://www.neo-magazin-royale.de/zdi/themen/134270/thema-ganze-folge.html?start=%s&count=8' 	

	title_main = 'NEO MAGAZIN ROYALE'
	if offset == 0:					# 1. Pfad (aus ZDF_get_content) verwerfen, jumppath enthält ganze Folgen
		path = JUMPPATH % str(0)
	page = HTTP.Request(path).content

	pagination = blockextract('class="pagination', page)	# "pagination active" = akt. Seite
	page_cnt = len(pagination)
	last_page = stringextract('count=8">', '</a>', pagination[-1]) # letzte Seite
	act_page = stringextract('pagination active">', 'a>', page)
	act_page = stringextract('count=8">', '<', act_page)
	if offset == 0:
		act_page = '1'
	cnt_per_page = 8
		
	oc = ObjectContainer(title2='Seite ' + act_page, view_group="List")
	oc = home(cont=oc, ID='ZDF')								# Home-Button
	
	content = blockextract('class="modules', page)
	if len(oc) == 0:
		msg_notfound = title + ': Auswertung fehlgeschlagen'	
		title = msg_notfound.decode(encoding="utf-8", errors="ignore")
		name = "ZDF Mediathek"				
		summary = 'zurück zur ' + name.decode(encoding="utf-8", errors="ignore")		
		oc.add(DirectoryObject(key=Callback(Main_ZDF, name=name), title=title, 
			summary=summary, tagline='TV', thumb=R(ICON_MAIN_ZDF)))
		return oc
							
	for rec in content:
		url = Neo_Base + stringextract('href="', '"', rec)	
		img = stringextract('sophoraimage="', '"', rec)				# ZDF-Pfad 	
		if img == '':
			img = Neo_Base + stringextract('src="', '"', rec)		# NEO-Pfad ohne Base
		img = img.decode(encoding="utf-8", errors="ignore")			# Umlaute im Pfad (hurensöhne_mannheims)		
		img_alt = 'Bild: ' + stringextract('alt="', '"', rec)
		img_alt = unescape_neo(img_alt)	
		img_alt = img_alt.decode(encoding="utf-8", errors="ignore")
				
		title = stringextract('name">', '</h3', rec)
		if title == '':
			title = stringextract('content="', '"', rec)	
		dataplayer = stringextract('data-player="', '"', rec)	
		sid = stringextract('data-sophoraid="', '"', rec)
		datetime = ''	
		if 'datetime=""' in rec:
			datetime = stringextract('datetime="">', '</time>', rec)# datetime="">07.09.2016</time>
		else:
			datetime = stringextract('datetime="', '</time>', rec)		# ="2017-05-18 18:10">18.05.2017</time>
			datetime = datetime[18:]									# 1. Datum + (falsche) Uhrzeit abschneiden
		Log('neuer Satz:')
		Log(url);Log(img);Log(title);Log(dataplayer);Log(sid);Log(datetime);
		title = title.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(GetNeoVideoSources, url=url, sid=sid, title=title, summary=datetime, 
			tagline=img_alt, thumb=img), title=title, summary=datetime, tagline=img_alt, thumb=img))
		
	# Prüfung auf Mehr
	Log('offset: ' + str(offset));Log(act_page); Log(last_page)
	if int(act_page) < int(last_page):
		offset = int(offset) + 8
		JUMPPATH = JUMPPATH % offset
		Log(JUMPPATH);
		oc.add(DirectoryObject(key=Callback(neo_content, path=JUMPPATH, ID=ID, offset=offset),
		title=title_main, thumb=R(ICON_MEHR), summary=''))						
	
	return oc
	
#-------------------------
@route(PREFIX + '/GetNeoVideoSources')
# 	Ladekette ähnlich ZDF (get_formitaeten), aber nur bei videodat_url identisch
def GetNeoVideoSources(url, sid, title, summary, tagline, thumb):				
	Log('GetNeoVideoSources url: ' + url)

	oc = ObjectContainer(title2='Videoformate', view_group="List")
	oc = home(cont=oc, ID='ZDF')							# Home-Button

	formitaeten, duration = get_formitaeten(sid=sid, ID='NEO')	# Video-URL's ermitteln
	if formitaeten == '':									# Nachprüfung auf Videos
		msg = 'Video nicht vorhanden / verfügbar'  + ' Seite:\r' + url
		msg = msg.decode(encoding="utf-8", errors="ignore")		
		return ObjectContainer(header='Error', message=msg)
			
	if tagline:
		if 'min' in tagline == False:	# schon enthalten?
			tagline = tagline + " | " + duration
	else:
		tagline = duration

	only_list = ["h264_aac_ts_http_m3u8_http"]
	oc, download_list = show_formitaeten(oc=oc, title_call=title, formitaeten=formitaeten, tagline=tagline,
		thumb=thumb, only_list=only_list)		  

	title_oc='weitere Video-Formate'
	if Prefs['pref_use_downloads']:	
		title=title + ' und Download'
	# oc = Parseplaylist(oc, videoURL, thumb)	# hier nicht benötigt - das ZDF bietet bereits 3 Auflösungsbereiche
	oc.add(DirectoryObject(key=Callback(NEOotherSources, title=title, tagline=tagline, thumb=thumb, sid=sid),
		title=title_oc, summary='', thumb=R(ICON_MEHR)))
	
	return oc

#-------------------------
@route(PREFIX + '/NEOotherSources')
def NEOotherSources(title, tagline, thumb, sid):	
				
	Log('NEOotherSources')
	title_org = title		# Backup für Textdatei zum Video
	summary_org = tagline	# Tausch summary mit tagline (summary erstrangig bei Wiedergabe)

	oc = ObjectContainer(title2='Videoformate', view_group="List")
	oc = home(cont=oc, ID='ZDF')							# Home-Button
	
	formitaeten, duration = get_formitaeten(sid=sid, ID='NEO')	# Video-URL's ermitteln
	if formitaeten == '':										# Nachprüfung auf Videos
		msg = 'Video nicht vorhanden / verfügbar'  + ' Seite:\r' + url
		msg = msg.decode(encoding="utf-8", errors="ignore")		
		return ObjectContainer(header='Error', message=msg)
	
	if tagline:
		if 'min' in tagline == False:	# schon enthalten?
			tagline = tagline + " | " + duration
	else:
		tagline = duration
	
	only_list = ["h264_aac_mp4_http_na_na", "vp8_vorbis_webm_http_na_na", "vp8_vorbis_webm_http_na_na"]
	oc, download_list = show_formitaeten(oc=oc, title_call=title, formitaeten=formitaeten, tagline=tagline,
		thumb=thumb, only_list=only_list)	
		
	# high=0: 	1. Video bisher höchste Qualität:  [progressive] veryhigh
	oc = test_downloads(oc,download_list,title_org,summary_org,tagline,thumb,high=0)  # Downloadbutton(s)
			  
	return oc
	
####################################################################################################
# htmlentities in neo, Zeichen s. http://aurelio.net/bin/python/fix-htmldoc-utf8.py
# HTMLParser() versagt hier
def unescape_neo(line):		
	line_ret = (line.replace("&Atilde;&para;", "ö").replace("&Atilde;&curren", "Ä").replace("&Atilde;&frac14", "ü")
		.replace("&Atilde;\x96", "Ö").replace("&Atilde;\x84", "Ä").replace("&Atilde;\x9c", "Ü")
		.replace("&Atilde;\x9f", "ß"))
	
	return	line_ret
