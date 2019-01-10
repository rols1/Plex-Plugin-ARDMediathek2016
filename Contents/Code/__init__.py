# -*- coding: utf-8 -*-
import string
import random			# Zufallswerte für rating_key
import urllib			# urllib.quote(), 
import urllib2			# urllib2.Request
import ssl				# HTTPS-Handshake
import os, subprocess 	# u.a. Behandlung von Pfadnamen
import shlex			# Parameter-Expansion für subprocess.Popen (os != windows)
import sys				# Plattformerkennung
import shutil			# Dateioperationen
import re				# u.a. Reguläre Ausdrücke, z.B. in CalculateDuration
import time
import datetime
import json				# json -> Textstrings
import locale

import updater
import EPG
import update_single


# +++++ ARD Mediathek 2016 Plugin for Plex +++++

VERSION =  '3.6.7'		# Wechsel: update_single_files löschen/leeren
VDATE = '10.01.2019'

# 
#	

# (c) 2016 by Roland Scholz, rols1@gmx.de
#	GUI by Arauco (Plex-Forum) from V1.5.1
# 
#     Functions -> README.md
# 
# 	Licensed under MIT License (MIT)
# 	(previously licensed under GPL 3.0)
# 	A copy of the License you find here:
#		https://github.com/rols1/Plex-Plugin-ARDMediathek2016/blob/master/LICENSE.md

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.

####################################################################################################

NAME			= 'ARD Mediathek 2016'
PREFIX 			= '/video/ardmediathek2016'			
												
PLAYLIST 		= 'livesenderTV.xml'		# TV-Sender-Logos erstellt von: Arauco (Plex-Forum). 											
PLAYLIST_Radio  = 'livesenderRadio.xml'		# Liste der RadioAnstalten. Einzelne Sender und Links werden 
											# 	vom Plugin ermittelt
											# Radio-Sender-Logos erstellt von: Arauco (Plex-Forum). 
FAVORITS_Pod 	= 'podcast-favorits.txt' 	# Lesezeichen für Podcast-Erweiterung 

ART 					= 'art.png'			# ARD 
ICON 					= 'icon.png'		# ARD
ICON_SEARCH 			= 'ard-suche.png'						
ICON_ZDF_SEARCH 		= 'zdf-suche.png'						

ICON_MAIN_ARD 			= 'ard-mediathek.png'			
ICON_MAIN_ZDF 			= 'zdf-mediathek.png'
ICON_MAIN_ZDFMOBILE		= 'zdf-mobile.png'			
ICON_MAIN_TVLIVE 		= 'tv-livestreams.png'		
ICON_MAIN_RADIOLIVE 	= 'radio-livestreams.png' 	
ICON_MAIN_UPDATER 		= 'plugin-update.png'		
ICON_UPDATER_NEW 		= 'plugin-update-new.png'

ICON_ARD_AZ 			= 'ard-sendungen-az.png'
ICON_ARD_VERP 			= 'ard-sendung-verpasst.png'			
ICON_ARD_RUBRIKEN 		= 'ard-rubriken.png' 			
ICON_ARD_Themen 		= 'ard-themen.png'	 			
ICON_ARD_Filme 			= 'ard-ausgewaehlte-filme.png' 	
ICON_ARD_FilmeAll 		= 'ard-alle-filme.png' 		
ICON_ARD_Dokus 			= 'ard-ausgewaehlte-dokus.png'			
ICON_ARD_DokusAll 		= 'ard-alle-dokus.png'		
ICON_ARD_Serien 		= 'ard-serien.png'				
ICON_ARD_MEIST 			= 'ard-meist-gesehen.png' 	
ICON_ARD_BARRIEREARM 	= 'ard-barrierearm.png' 
ICON_ARD_HOERFASSUNGEN	= 'ard-hoerfassungen.png' 
ICON_ARD_NEUESTE 		= 'ard-neueste-videos.png' 	
ICON_ARD_BEST 			= 'ard-am-besten-bewertet.png' 	
ICON_ARD_BILDERSERIEN 	= 'ard-bilderserien.png'

ICON_ZDF_AZ 			= 'zdf-sendungen-az.png' 		
ICON_ZDF_VERP 			= 'zdf-sendung-verpasst.png'	
ICON_ZDF_RUBRIKEN 		= 'zdf-rubriken.png' 		
ICON_ZDF_Themen 		= 'zdf-themen.png'			
ICON_ZDF_MEIST 			= 'zdf-meist-gesehen.png' 	
ICON_ZDF_BARRIEREARM 	= 'zdf-barrierearm.png' 
ICON_ZDF_HOERFASSUNGEN	= 'zdf-hoerfassungen.png' 
ICON_ZDF_UNTERTITEL 	= 'zdf-untertitel.png'
ICON_ZDF_INFOS 			= 'zdf-infos.png'
ICON_ZDF_BILDERSERIEN 	= 'zdf-bilderserien.png'
ICON_ZDF_NEWCONTENT 	= 'zdf-newcontent.png'

ICON_MAIN_POD			= 'radio-podcasts.png'
ICON_POD_AZ				= 'pod-az.png'
ICON_POD_FEATURE 		= 'pod-feature.png'
ICON_POD_TATORT 		= 'pod-tatort.png'
ICON_POD_RUBRIK	 		= 'pod-rubriken.png'
ICON_POD_NEU			= 'pod-neu.png'
ICON_POD_MEIST			= 'pod-meist.png'
ICON_POD_REFUGEE 		= 'pod-refugee.png'
ICON_POD_FAVORITEN		= 'pod-favoriten.png'


ICON_OK 				= "icon-ok.png"
ICON_INFO 				= "icon-info.png"
ICON_WARNING 			= "icon-warning.png"
ICON_NEXT 				= "icon-next.png"
ICON_CANCEL 			= "icon-error.png"
ICON_MEHR 				= "icon-mehr.png"
ICON_DOWNL 				= "icon-downl.png"
ICON_DOWNL_DIR			= "icon-downl-dir.png"
ICON_DELETE 			= "icon-delete.png"
ICON_STAR 				= "icon-star.png"
ICON_NOTE 				= "icon-note.png"
ICON_SPEAKER 			= "icon-speaker.png"								# Breit-Format

ICON_DIR_CURLWGET 		= "Dir-curl-wget.png"
ICON_DIR_FOLDER			= "Dir-folder.png"
ICON_DIR_PRG 			= "Dir-prg.png"
ICON_DIR_IMG 			= "Dir-img.png"
ICON_DIR_TXT 			= "Dir-text.png"
ICON_DIR_MOVE 			= "Dir-move.png"
ICON_DIR_MOVE_SINGLE	= "Dir-move-single.png"
ICON_DIR_MOVE_ALL 		= "Dir-move-all.png"
ICON_DIR_BACK	 		= "Dir-back.png"
ICON_DIR_SAVE 			= "Dir-save.png"
ICON_DIR_VIDEO 			= "Dir-video.png"
ICON_DIR_WORK 			= "Dir-work.png"
ICON_MOVEDIR_DIR 		= "Dir-moveDir.png"
ICON_DIR_FAVORITS		= "Dir-favorits.png"



# 01.12.2018 	Änderung der BASE_URL von www.ardmediathek.de zu classic.ardmediathek.de
#				Änderung der Sparten-Url's auch hinter der BASE_URL
#				ARD-Podcasts bisher ohne Änderung
BASE_URL 		= 'https://classic.ardmediathek.de'
ARD_VERPASST 	= '/tv/sendungVerpasst?tag='								# ergänzt mit 0, 1, 2 usw.
ARD_AZ 			= '/tv/sendungen-a-z?buchstabe='							# ergänzt mit 0-9, A, B, usw.
ARD_Suche 		= '/tv/suche?searchText=%s&words=and&source=tv&sort=date'	# Vorgabe UND-Verknüpfung
ARD_Live 		= '/tv/live'

# Aktualisierung der ARD-ID's in Update_ARD_Path (entfällt ab 01.12.2018)
ARD_Rubriken 	= 'https://classic.ardmediathek.de/tv/Rubriken/mehr?documentId=21282550'
ARD_Serien 		= 'https://classic.ardmediathek.de/tv/Komplette-Staffeln/mehr?documentId=56477862'
ARD_Dokus 		= 'https://classic.ardmediathek.de/tv/Doku-Tipps-der-Redaktion/mehr?documentId=33649086'
ARD_DokusAll	= 'https://classic.ardmediathek.de/tv/dokus'
ARD_Filme 		= 'https://classic.ardmediathek.de/tv/Film-Tipps-der-Redaktion/mehr?documentId=33649088'
ARD_FilmeAll 	= 'https://classic.ardmediathek.de/tv/filme'
ARD_Neu 		= 'https://classic.ardmediathek.de/tv/Neueste-Videos/mehr?documentId=21282466'
ARD_Best 		= 'https://classic.ardmediathek.de/tv/Am-besten-bewertet/mehr?documentId=21282468'
ARD_RadioAll 	= 'http://www.ardmediathek.de/radio/live?genre=Alle+Genres&kanal=Alle'

# ARD-Podcasts
POD_SEARCH  = '/suche?source=radio&sort=date&searchText=%s&pod=on&playtime=all&words=and&to=all='
POD_AZ 		= 'http://www.ardmediathek.de/radio/sendungen-a-z?sendungsTyp=podcast&buchstabe=' 
POD_RUBRIK 	= 'http://www.ardmediathek.de/radio/Rubriken/mehr?documentId=37981136'
POD_FEATURE = 'http://www.ardmediathek.de/radio/das-ARD-radiofeature/Sendung?documentId=3743362&bcastId=3743362'
POD_TATORT 	= 'http://www.ardmediathek.de/radio/ARD-Radio-Tatort/Sendung?documentId=1998988&bcastId=1998988'
POD_NEU 	= 'http://www.ardmediathek.de/radio/Neueste-Audios/mehr?documentId=23644358'
POD_MEIST 	= 'http://www.ardmediathek.de/radio/Meistabgerufene-Audios/mehr?documentId=23644364'
POD_REFUGEE = 'https://www1.wdr.de/radio/cosmo/programm/refugee-radio/refugee-radio-112.html'	# z.Z. Refugee Radio via Suche

# Relaunch der Mediathek beim ZDF ab 28.10.2016: xml-Service abgeschaltet
ZDF_BASE				= 'https://www.zdf.de'
# ZDF_Search_PATH: siehe ZDF_Search, ganze Sendungen, sortiert nach Datum, bei Bilderserien ohne ganze Sendungen
ZDF_SENDUNG_VERPASST 	= 'https://www.zdf.de/sendung-verpasst?airtimeDate=%s'  # Datumformat 2016-10-31
ZDF_SENDUNGEN_AZ		= 'https://www.zdf.de/sendungen-a-z?group=%s'			# group-Format: a,b, ... 0-9: group=0+-+9
ZDF_WISSEN				= 'https://www.zdf.de/doku-wissen'						# Basis für Ermittlung der Rubriken
ZDF_SENDUNGEN_MEIST		= 'https://www.zdf.de/meist-gesehen'
ZDF_BARRIEREARM			= 'https://www.zdf.de/barrierefreiheit-im-zdf'


REPO_NAME		 	= 'Plex-Plugin-ARDMediathek2016'
GITHUB_REPOSITORY 	= 'rols1/' + REPO_NAME
myhost			 	= 'http://127.0.0.1:32400'

''' 
####################################################################################################
TV-Live-Sender: Liste siehe Resources/livesenderTV.xml, ca. 35 Sender
	Aufteilung: Überregional (öffentlich-rechtliche TV-Sender bundesweit)
				Regional (öffentlich-rechtliche TV-Sender der Bundesländer)
				Privat (weitere ausgewählte TV-Sender, z.B. n-tv, N24)

Radio-Live-Streams der ARD: alle Radiosender von Bayern, HR, mdr, NDR, Radio Bremen, RBB, SR, SWR, WDR, 
	Deutschlandfunk. Insgesamt 10 Stationen, 63 Sender

Versions-Historie: siehe Datei HISTORY
####################################################################################################
'''

def Start():
	#Log.Debug()  	# definiert in Info.plist
	# Problem Voreinstellung Plakate/Details/Liste:
	#	https://forums.plex.tv/discussion/211755/how-do-i-make-my-objectcontainer-display-as-a-gallery-of-thumbnails
	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
	Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
	
	#ObjectContainer.art        = R(ART)
	ObjectContainer.art        = R(ICON)  # gefällt mir als Hintergrund besser
	ObjectContainer.title1     = NAME

	HTTP.CacheTime = CACHE_1HOUR # Debugging: falls Logdaten ausbleiben, Browsercache löschen

#----------------------------------------------------------------
# handler bindet an das bundle
@route(PREFIX)
@handler(PREFIX, NAME, art = ART, thumb = ICON)
def Main():
	Log('Funktion Main'); Log(PREFIX); 
	Log('Plugin-Version: ' + VERSION); Log('Plugin-Datum: ' + VDATE)
	client_platform = str(Client.Platform)								# Client.Platform: None möglich
	client_product = str(Client.Product)								# Client.Product: None möglich
	Log('Client-Platform: ' + client_platform)							
	Log('Client-Product: ' + client_product)							
    
	Log('Plattform: ' + sys.platform)									# Server-Infos
	Log('Platform.OSVersion: ' + Platform.OSVersion)					# dto.
	Log('Platform.CPU: '+ Platform.CPU)									# dto.
	Log('Platform.ServerVersion: ' + Platform.ServerVersion)			# dto.
	
	Dict.Reset()							# Speicherobjekte des Plugins löschen
	Dict['R'] = Core.storage.join_path(Core.bundle_path, 'Contents', 'Resources')
	# Log(Dict['R'])	
			
	oc = ObjectContainer(view_group="InfoList", art=ObjectContainer.art)	# Plex akzeptiert nur InfoList + List, keine
																			# Auswirkung auf Wiedergabe im Webplayer																																						
	oc.add(DirectoryObject(key=Callback(Main_ARD, name="ARD Mediathek"), title="ARD Mediathek",
		summary='', tagline='TV', thumb=R(ICON_MAIN_ARD)))
		
	if Prefs['pref_use_zdfmobile']:
		import zdfmobile
		oc.add(DirectoryObject(key=Callback(zdfmobile.Main_ZDFmobile, name="ZDFmobile"), title="ZDFmobile", 
			summary='', tagline='TV', thumb=R(ICON_MAIN_ZDFMOBILE)))
	else:
		oc.add(DirectoryObject(key=Callback(Main_ZDF, name="ZDF Mediathek"), title="ZDF Mediathek", 
			summary='', tagline='TV', thumb=R(ICON_MAIN_ZDF)))
		
	oc.add(DirectoryObject(key=Callback(SenderLiveListePre, title='TV-Livestreams'), title='TV-Livestreams',
		summary='', tagline='TV', thumb=R(ICON_MAIN_TVLIVE)))
	oc.add(DirectoryObject(key=Callback(RadioLiveListe, path=ARD_RadioAll, title='Radio-Livestreams'), 
		title='Radio-Livestreams', summary='', tagline='Radio', thumb=R(ICON_MAIN_RADIOLIVE)))
		
	if Prefs['pref_use_podcast'] == True:	# ARD-Radio-Podcasts
		summary = 'ARD-Radio-Podcasts suchen, hören und herunterladen'
		summary = summary.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key = Callback(Main_POD, name="PODCAST"), title = 'Radio-Podcasts', 
			summary=summary, thumb = R(ICON_MAIN_POD)))
								
	if Prefs['pref_use_downloads'] == True:	# Download-Tools. zeigen, falls Downloads eingeschaltet
		summary = 'Download-Tools: Verschieben, Löschen, Ansehen, Verzeichnisse bearbeiten'
		summary = summary.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key = Callback(DownloadsTools), title = 'Download-Tools', 
			summary=summary, thumb = R(ICON_DOWNL_DIR)))
								
	repo_url = 'https://github.com/{0}/releases/'.format(GITHUB_REPOSITORY)
	call_update = False
	if Prefs['pref_info_update'] == True:				# Hinweis auf neues Update beim Start des Plugins 
		ret = updater.update_available(VERSION)
		int_lv = ret[0]			# Version Github
		int_lc = ret[1]			# Version aktuell
		latest_version = ret[2]	# Version Github, Format 1.4.1
		if ret[0] == False:
			msgH = 'Error'; msg = 'Github ist nicht errreichbar. Bitte in den Einstellungen die Update-Anzeige abschalten.'		
			return ObjectContainer(header=msgH, message=msg)		
		
		if int_lv > int_lc:								# Update-Button "installieren" zeigen
			call_update = True
			title = 'neues Update vorhanden - jetzt installieren'
			summary = 'Plugin aktuell: ' + VERSION + ', neu auf Github: ' + latest_version
			url = 'https://github.com/{0}/releases/download/{1}/{2}.bundle.zip'.format(GITHUB_REPOSITORY, latest_version, REPO_NAME)
			oc.add(DirectoryObject(key=Callback(updater.update, url=url , ver=latest_version), 
				title=title, summary=summary, tagline=cleanhtml(summary), thumb=R(ICON_UPDATER_NEW)))
		else:	
			# Update von Einzeldateien, wenn kein aktuelles Plugin-Update vorliegt: 
			ret, info = update_single.check_repo(mode='check')		# ret=1: Einzeldateien aktualisieren
			Log('update_single: ' + str(ret)); 
			if ret:
				call_update = True
				oc.add(DirectoryObject(
					key = Callback(update_single.check_repo, mode='replace'), 
					title = 'neue Einzeldateien vorhanden - jetzt installieren',
					summary = info,
					tagline = 'Version bleibt %s' % VERSION,
				thumb = R(ICON_UPDATER_NEW)))			
				
	if call_update == False:							# Update-Button "Suche" zeigen	
		title = 'Plugin-Update | akt. Version: ' + VERSION + ' vom ' + VDATE	
		summary='Suche starten nach Updates für Plugin und Einzeldateien'.decode(encoding="utf-8")
		tagline='Bezugsquelle: ' + repo_url			
		oc.add(DirectoryObject(key=Callback(SearchUpdate, title='Plugin-Update'), 
			title=title, summary=summary, tagline=tagline, thumb=R(ICON_MAIN_UPDATER)))

	# Menü Einstellungen (obsolet) ersetzt durch Info-Button
	title 	= 'Nachfolgeplugin ARDundZDF verfügbar!'.decode(encoding="utf-8")
	summary = 'Forum: https://forums.plex.tv/t/rel-ardundzdf/309751'
	tagline = 'Download: https://github.com/rols1/ARDundZDF/releases/latest'
	oc.add(DirectoryObject(key = Callback(Main), title = title, summary = summary, 
		tagline=tagline, thumb = R(ICON_INFO)))
						
	return oc
	
#----------------------------------------------------------------
@route(PREFIX + '/Main_ARD')
def Main_ARD(name):
	Log('Funktion Main_ARD'); Log(PREFIX); Log(VERSION); Log(VDATE)	
	oc = ObjectContainer(view_group="InfoList", art=ObjectContainer.art)	
	oc = home(cont=oc, ID=NAME)							# Home-Button
		
	
	if 'Web' in str(Client.Product):
		# Web-Player: folgendes DirectoryObject ist Deko für das nicht sichtbare InputDirectoryObject dahinter:
		oc.add(DirectoryObject(key=Callback(Main_ARD, name=name),title='Suche: im Suchfeld eingeben', 
			tagline='TV', thumb=R(ICON_SEARCH)))
			
	oc.add(InputDirectoryObject(key=Callback(Search,  channel='ARD', s_type='video', title=u'%s' % L('Search Video')),
		title=u'%s' % L('Search'), prompt=u'%s' % L('Search Video'), thumb=R(ICON_SEARCH)))
		
	title = 'Sendung verpasst (1 Woche)'
	oc.add(DirectoryObject(key=Callback(VerpasstWoche, name='ARD', title='Sendung verpasst', sender='DAS ERSTE', 
		kanal='208'), title=title, summary=title, tagline='TV', thumb=R(ICON_ARD_VERP)))
	title = 'Sendungen A-Z'
	oc.add(DirectoryObject(key=Callback(SendungenAZ, name='Sendungen 0-9 | A-Z', ID='ARD'), 
		title='Sendungen A-Z', summary=title, tagline='TV', thumb=R(ICON_ARD_AZ)))
						
		
	title = 'Ausgewählte Filme'.decode(encoding="utf-8", errors="ignore")
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Filme, next_cbKey='SingleSendung', 
		ID='ARD', mode = 'Sendereihen'), title=title,summary=title, tagline='TV', thumb=R(ICON_ARD_Filme)))
	title = 'Alle Filme'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_FilmeAll, next_cbKey='SingleSendung', 
		ID='ARD', mode = 'Sendereihen'), title=title,summary=title, tagline='TV', thumb=R(ICON_ARD_FilmeAll)))
	title = 'Ausgewählte Dokus'.decode(encoding="utf-8", errors="ignore")
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Dokus, next_cbKey='SingleSendung', ID='ARD', 
		mode='Sendereihen'), title=title,summary=title, tagline='TV', thumb=R(ICON_ARD_Dokus)))
	title = 'Alle Dokus'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_DokusAll, next_cbKey='SingleSendung', ID='ARD', 
		mode='Sendereihen'), title=title,summary=title, tagline='TV', thumb=R(ICON_ARD_DokusAll)))
	title = 'Serien'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Serien, next_cbKey='SinglePage', ID='ARD', 
		mode = 'Sendereihen'), title=title, summary=title, tagline='TV', thumb=R(ICON_ARD_Serien)))
	title = 'Rubriken'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Rubriken, next_cbKey='SinglePage', ID='ARD', 
		mode = 'Sendereihen'), title=title, summary=title, tagline='TV', thumb=R(ICON_ARD_RUBRIKEN)))
	title = 'neueste Videos'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Neu, next_cbKey='SingleSendung', ID='ARD', 
		mode = 'Sendereihen'), title=title, summary=title, tagline='TV', thumb=R(ICON_ARD_NEUESTE)))
	title = 'am besten bewertet'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Best, next_cbKey='SingleSendung', ID='ARD', 
		mode='Sendereihen'), title=title, summary=title, tagline='TV', thumb=R(ICON_ARD_BEST)))
		 	
	oc.add(DirectoryObject(key=Callback(BarriereArmARD, name="Barrierearm"), title="Barrierearm", 
		thumb=R(ICON_ARD_BARRIEREARM))) 			
	title = 'Bilderserien'
	oc.add(DirectoryObject(key=Callback(Search,  query=title, channel='ARD', s_type=title, title=title), title=title, 
		thumb=R('ard-bilderserien.png'))) 	

	return oc	
	
#---------------------------------------------------------------- 
@route(PREFIX + '/Main_ZDF')
def Main_ZDF(name):
	Log('Funktion Main_ZDF'); Log(PREFIX); Log(VERSION); Log(VDATE)
	oc = ObjectContainer(view_group="InfoList", art=ObjectContainer.art, title1=name)	
	oc = home(cont=oc, ID=NAME)								# Home-Button	
	
	if 'Web' in str(Client.Product):
		# folgendes DirectoryObject ist Deko für das nicht sichtbare InputDirectoryObject dahinter:
		oc.add(DirectoryObject(key=Callback(Main_ZDF, name=name),title='Suche: im Suchfeld eingeben', 
			summary='', tagline='TV', thumb=R(ICON_ZDF_SEARCH)))
	oc.add(InputDirectoryObject(key=Callback(ZDF_Search, s_type='video', title=u'%s' % L('Search Video')),
		title=u'%s' % L('Search'), prompt=u'%s' % L('Search Video'), thumb=R(ICON_ZDF_SEARCH)))
		
	oc.add(DirectoryObject(key=Callback(VerpasstWoche, name=name, title='Sendung verpasst', sender='ZDF', 
		kanal='leer'), title="Sendung verpasst (1 Woche)", thumb=R(ICON_ZDF_VERP)))
	oc.add(DirectoryObject(key=Callback(ZDFSendungenAZ, name="Sendungen A-Z"), title="Sendungen A-Z",
		thumb=R(ICON_ZDF_AZ)))
	oc.add(DirectoryObject(key=Callback(Rubriken, name="Rubriken"), title="Rubriken", 
		thumb=R(ICON_ZDF_RUBRIKEN))) 
	oc.add(DirectoryObject(key=Callback(MeistGesehen, name="Meist gesehen"), title="Meist gesehen (1 Woche)", 
		thumb=R(ICON_ZDF_MEIST))) 
	oc.add(DirectoryObject(key=Callback(NeuInMediathek, name="Neu in der Mediathek"), title="Neu in der Mediathek)", 
		thumb=R(ICON_ZDF_NEWCONTENT))) 
	oc.add(DirectoryObject(key=Callback(BarriereArm, name="Barrierearm"), title="Barrierearm", 
		thumb=R(ICON_ZDF_BARRIEREARM))) 
	oc.add(DirectoryObject(key=Callback(International, name="ZDFenglish"), title="ZDFenglish", 
		thumb=R('ZDFenglish.png'))) 
	oc.add(DirectoryObject(key=Callback(International, name="ZDFarabic"), title="ZDFarabic", 
		thumb=R('ZDFarabic.png'))) 
		
	oc.add(DirectoryObject(key=Callback(ZDF_Search, s_type='Bilderserien', title="Bilderserien", query="Bilderserien"), 
		title="Bilderserien", thumb=R(ICON_ZDF_BILDERSERIEN))) 
	return oc	

#----------------------------------------------------------------
@route(PREFIX + '/Main_POD')
def Main_POD(name):
	oc = ObjectContainer(view_group="InfoList", art=ObjectContainer.art, title1=name)	
	oc = home(cont=oc, ID=NAME)								# Home-Button	
	
	# folgendes DirectoryObject ist Deko für das nicht sichtbare InputDirectoryObject dahinter:
	oc.add(DirectoryObject(key=Callback(Main_POD, name=name),title='Suche: im Suchfeld eingeben', 
		summary='', tagline='TV', thumb=R(ICON_SEARCH)))
	# die Suchfunktion nutzt die ARD-Mediathek-Suche
	oc.add(InputDirectoryObject(key=Callback(Search,  channel='PODCAST', s_type='video', title=u'%s' % L('Search Video')),
		title=u'%s' % L('Search'), prompt=u'%s' % L('Search Audio'), thumb=R(ICON_SEARCH)))
		
	title = 'Sendungen A-Z'
	oc.add(DirectoryObject(key=Callback(SendungenAZ, name=title, ID='PODCAST'), title=title, thumb=R(ICON_ARD_AZ)))			
	title = 'Rubriken'	
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=POD_RUBRIK, next_cbKey='SinglePage', ID='PODCAST',
		mode='Sendereihen'), title=title, summary=title, thumb=R(ICON_POD_RUBRIK)))
	title="Radio-Feature"	 
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=POD_FEATURE, next_cbKey='SingleSendung', ID='PODCAST',
		mode='Sendereihen'), title=title, summary=title, thumb=R(ICON_POD_FEATURE)))
	title="Radio-Tatort"	 
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=POD_TATORT, next_cbKey='SingleSendung', ID='PODCAST',
		mode='Sendereihen'), title=title, summary=title, thumb=R(ICON_POD_TATORT)))
	title="Neueste Audios"	 
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=POD_NEU, next_cbKey='SingleSendung', ID='PODCAST',
		mode='Sendereihen'), title=title, summary=title, thumb=R(ICON_POD_NEU)))
	title="Meist abgerufen"	 
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=POD_MEIST, next_cbKey='SingleSendung', ID='PODCAST',
		mode='Sendereihen'), title=title, summary=title, thumb=R(ICON_POD_MEIST)))
	
	title="Refugee-Radio"; query='Refugee Radio'	# z.Z. Refugee Radio via Suche
	oc.add(DirectoryObject(key=Callback(Search, query=query, channel='PODCAST'), title=title, 
		summary=title, thumb=R(ICON_POD_REFUGEE)))
	
	title="Podcast-Favoriten"; ICON_POD_FAVORITEN
	oc.add(DirectoryObject(key=Callback(PodFavoritenListe, title=title),title=title, summary=title, thumb=R(ICON_POD_FAVORITEN)))
	
	return oc

################################################################
################################################################	
	
#----------------------------------------------------------------
def home(cont, ID):												# Home-Button, Aufruf: oc = home(cont=oc, ID=NAME)
	Log('home')	
	title = 'Zurück zum Hauptmenü ' + str(ID)
	title = title.decode(encoding="utf-8", errors="ignore")
	summary = title
	
	if ID == NAME:		# 'ARD Mediathek 2016'
		cont.add(DirectoryObject(key=Callback(Main),title=title, summary=summary, tagline=NAME, thumb=R('home.png')))
	if ID == 'ARD':
		name = "ARD Mediathek"
		cont.add(DirectoryObject(key=Callback(Main_ARD, name=name),title=title, summary=summary, tagline=name, 
			thumb=R('home-ard.png')))
	if ID == 'ZDF':
		name = "ZDF Mediathek"
		cont.add(DirectoryObject(key=Callback(Main_ZDF,name=name),title=title, summary=summary, tagline=name, 
			thumb=R('home-zdf.png')))
	if ID == 'ZDFmobile':
		import zdfmobile		# ohne wird Callback nicht akzeptiert
		name = "ZDFmobile"
		cont.add(DirectoryObject(key=Callback(zdfmobile.Main_ZDFmobile,name=name),title=title, summary=summary, tagline=name, 
			thumb=R(ICON_MAIN_ZDFMOBILE)))
	if ID == 'PODCAST':
		name = "Radio-Podcasts"
		cont.add(DirectoryObject(key=Callback(Main_POD,name=name),title=title, summary=summary, tagline=name, 
			thumb=R(ICON_MAIN_POD)))

	return cont
	
####################################################################################################

def ValidatePrefs():
	Log('ValidatePrefs')
	# Dict.Save()	# n.b. - Plex speichert in Funktion Set, benötigt trotzdem Funktion ValidatePrefs im Plugin
	return
	
####################################################################################################
@route(PREFIX + '/SearchUpdate')
def SearchUpdate(title):		#
	oc = ObjectContainer(no_cache=True, view_group="InfoList", art=ObjectContainer.art)	

	ret = updater.update_available(VERSION)
	int_lv = ret[0]			# Version Github
	int_lc = ret[1]			# Version aktuell
	latest_version = ret[2]	# Version Github, Format 1.4.1
	summ = ret[3]			# Plugin-Name
	tag = ret[4]			# History (last change)

	url = 'https://github.com/{0}/releases/download/{1}/{2}.bundle.zip'.format(GITHUB_REPOSITORY, latest_version, REPO_NAME)
	Log(latest_version); Log(int_lv); Log(int_lc); Log(url); 
	
	if int_lv > int_lc:		# zum Testen drehen (akt. Plugin vorher sichern!)
		oc.add(DirectoryObject(
			key = Callback(updater.update, url=url , ver=latest_version), 
			title = 'neues Update vorhanden - jetzt installieren',
			summary = 'Plugin aktuell: ' + VERSION + ', neu auf Github: ' + latest_version,
			tagline = cleanhtml(summ),
			thumb = R(ICON_UPDATER_NEW)))
			
		oc.add(DirectoryObject(
			key = Callback(Main), 
			title = 'Update abbrechen',
			summary = 'weiter im aktuellen Plugin',
			thumb = R(ICON_UPDATER_NEW)))
	else:	
		# Update von Einzeldateien, wenn kein aktuelles Plugin-Update vorliegt: 
		ret, info = update_single.check_repo(mode='check')		# ret=1: Einzeldateien aktualisieren
		Log('update_single: ' + str(ret)); 
		if ret:
			oc.add(DirectoryObject(
				key = Callback(update_single.check_repo, mode='replace'), 
				title = 'neue Einzeldateien vorhanden - jetzt installieren',
				tagline = 'Version bleibt %s' % VERSION,
				summary = info,
				thumb = R(ICON_UPDATER_NEW)))

			oc.add(DirectoryObject(
				key = Callback(Main), 
				title = 'Update abbrechen',
				summary = 'weiter im aktuellen Plugin',
				thumb = R(ICON_UPDATER_NEW)))
		else:
			summary = 'keine neue Version / keine neuen Einzeldateien gefunden'
			oc.add(DirectoryObject(
				#key = Callback(updater.menu, title='Update Plugin'), 
				key = Callback(Main), 
				title = 'Plugin Version %s ist aktuell | weiter zum aktuellen Plugin' % VERSION,
				summary = summary,
				tagline = cleanhtml(summ),
				thumb = R(ICON_OK)))
			
	return oc
	
####################################################################################################
@route(PREFIX + '/SendungenAZ')
# 	Auflistung 0-9 (1 Eintrag), A-Z (einzeln) 
#	ID = PODCAST, ARD
def SendungenAZ(name, ID):		
	Log('SendungenAZ: ' + name)
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=name, art = ObjectContainer.art)
	oc = home(cont=oc, ID=ID)							# Home-Button
	
	azlist = list(string.ascii_uppercase)					# A - Z, 0-9
	azlist.append('0-9')
	
	next_cbKey = 'PageControl'	# SinglePage zeigt die Sendereihen, PageControl dann die weiteren Seiten
	
	path = azPath = BASE_URL + ARD_AZ + 'A'		# A-Seite laden für Prüfung auf inaktive Buchstaben
	Log(path)
	page = HTTP.Request(path).content
	Log(len(page))
	
	inactive_list = ""							# inaktive Buchstaben?
	inactive_range = stringextract('Aktuelle TV Auswahl:', 'subressort collapsed', page)
	inactive_list = blockextract('class=\"inactive\"', inactive_range)
	Log('Inaktive: ' + str(len(inactive_list)))		

	inactive_char = ""
	if inactive_list:							# inaktive Buchstaben -> 1 String
		for element in inactive_list:
			char = stringextract('<a>', '</a>', element)
			char = char.strip()
			inactive_char =  inactive_char + char
	Log(inactive_char)							# z.B. XY
	
	for element in azlist:	
		# Log(element)
		if ID == 'ARD':
			azPath = BASE_URL + ARD_AZ + element
		if ID == 'PODCAST':
			azPath = POD_AZ + element
		button = element
		title = "Sendungen mit " + button
		if inactive_char.find(button) >= 0:		# inaktiver Buchstabe?
			title = "Sendungen mit " + button + ': keine gefunden'
			oc.add(DirectoryObject(key=Callback(SendungenAZ, name = 'Sendungen 0-9 | A-Z', ID=ID), 
					title=title, thumb=R(ICON_WARNING)))
		else:
			oc.add(DirectoryObject(key=Callback(SinglePage, title=title, path=azPath, next_cbKey=next_cbKey, 
				mode='Sendereihen', ID=ID), title=title,  thumb=R(ICON_ARD_AZ)))
	Log(len(oc))
	return oc
   
####################################################################################################
@route(PREFIX + '/Search')	# Suche - Verarbeitung der Eingabe
	# Vorgabe UND-Verknüpfung (auch Podcast)
	# offset: verwendet nur bei Bilderserien (Funktionen s. ARD_Bildgalerie.py)
def Search(query=None, title=L('Search'), channel='ARD', s_type=None, offset=0, path=None, **kwargs):
	Log('Search:'); Log(query); Log(channel); Log(str(offset))
	query = query.replace(' ', '+')			# Leer-Trennung = UND-Verknüpfung bei Podcast-Suche 
	query = urllib2.quote(query, "utf-8")
	Log(query)

	name = 'Suchergebnis zu: ' + urllib2.unquote(query)
	name = name.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=name, art = ObjectContainer.art)
	next_cbKey = 'SinglePage'	# cbKey = Callback für Container in PageControl
			
	if channel == 'ARD':
		if s_type == 'Bilderserien':
			if path == None:			# path belegt bei offset > 0
				path = 'http://www.ard.de/home/ard/23116/index.html?q=Bildergalerie'
		else:
			path =  BASE_URL +  ARD_Suche 
			path = path % query
		ID='ARD'
	if channel == 'PODCAST':	
		path =  BASE_URL  + POD_SEARCH
		path = path % query
		ID=channel
	Log(path) 
	headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36", \
		'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}
	page = HTTP.Request(path, headers=headers).content
	Log(len(page))
	
	if page.find('<strong>keine Treffer</strong') >= 0:
		msg_notfound = 'Leider kein Treffer.'
		title = msg_notfound.decode(encoding="utf-8", errors="ignore")
		if channel == 'ARD':		
			summary = 'zurück zu ' + NAME
			summary = summary.decode(encoding="utf-8", errors="ignore")
			oc.add(DirectoryObject(key=Callback(Main_ARD, name=NAME), title=msg_notfound, 
				summary=summary, tagline='TV', thumb=R(ICON_MAIN_ARD)))
		if channel == 'PODCAST':		
			summary = 'zurück zu ' + "Radio-Podcasts"
			summary = summary.decode(encoding="utf-8", errors="ignore")
			oc.add(DirectoryObject(key=Callback(Main_POD, name="Radio-Podcasts"), title=msg_notfound, 
				summary=summary, tagline='Radio', thumb=R(ICON_MAIN_POD)))
	else:
		if s_type == 'Bilderserien':
			oc = home(cont=oc, ID='ARD')
			entries = blockextract('class="entry">',  page)
			if offset:		# 5 Seiten aus vorheriger Liste abziehen
				entries = entries[4:]
			Log(len(entries))
			if len(entries) == 0:
				err = 'keine weitere Bilderserie gefunden'
				return ObjectContainer(header='Fehler', message=err)	
			
			
			page_high = re.findall('ctype="nav.page">(\d+)', page)[-1]	# letzte NR der nächsten Seiten
			Log(page_high)
			href_high = blockextract('class="entry">',  page)[-1]		# letzter Pfad der nächsten Seiten
			href_high = 'http://www.ard.de' + stringextract('href="', '"', href_high)
			Log(href_high)
			
			import ARD_Bildgalerie
			if offset == 0:
				title = "Weiter zu Seite 1"						# 1. Link fehlt in entries
				oc.add(DirectoryObject(key=Callback(ARD_Bildgalerie.page,name=s_type + ': 1', path=path, offset=0), 
					title=title, thumb=R(ICON_NEXT)))
			for rec in entries:
				href =  'http://www.ard.de' + stringextract('href="', '"', rec)
				Log(href[:44])
				pagenr = re.search('ctype="nav.page">(\d+)', rec).group(1)
				title = "Weiter zu Seite %s" % pagenr
				title2 = name="%s: %s " %(s_type, pagenr)
				oc.add(DirectoryObject(key=Callback(ARD_Bildgalerie.page,name=title2, path=href, offset=0), 
					title=title, thumb=R(ICON_NEXT)))
					
			# Mehr Seiten Bilderserien anzeigen:
			#	Ablauf im Web (Klick auf die höchste Seite): Paging zeigt 4 vorige und 5 nächste Seiten, 
			#	Bsp. Seite 10: 6 -9, 11 - 15
			#	Hier zeigen wir nur die nächsten 5, um Wiederholungen zu vermeiden
			Log('page_high: ' + page_high)
			title = 'Mehr %s'	% s_type					
			oc.add(DirectoryObject(key=Callback(Search, query=query, channel='ARD', s_type=s_type, 
				offset=page_high, path=href_high), title=title, thumb=R(ICON_MEHR)))	
		else:	
			oc = PageControl(title=name, path=path, cbKey=next_cbKey, mode='Suche', ID=ID) 	# wir springen direkt
	 
	return oc
 		
#-----------------------
# 02.09.2018	erweitert um 2. Alternative mit urllib2.Request +  ssl.SSLContext
#	Bei Bedarf get_page in EPG-Modul nachrüsten.
#	S.a. loadPage in Modul zdfmobile.
#
def get_page(path, cTimeout=None):		# holt kontrolliert raw-Content, cTimeout für cacheTime
	Log('get_page')
	msg = ''; page = ''				
	try:
		if cTimeout:					# mit Cachevorgabe
			page = HTTP.Request(path, cacheTime=int(cTimeout) ).content	# 1. Versuch HTTP.Request 
		else:
			page = HTTP.Request(path).content
	except Exception as exception:
		summary = str(exception)
		summary = summary.decode(encoding="utf-8", errors="ignore")
		Log(summary)		
		
	if page == '':
		try:
			req = urllib2.Request(path)									# 2. Versuch urllib2.Request 
			gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
			gcontext.check_hostname = False
			r = urllib2.urlopen(req, context=gcontext)
			page = r.read()			
		except Exception as exception:
			summary = str(exception)
			summary = summary.decode(encoding="utf-8", errors="ignore")
			Log(summary)		
			
	if page == '':
		error_txt = 'Seite nicht erreichbar oder nicht mehr vorhanden'			 			 	 
		msgH = 'Fehler'; msg = error_txt + ' | Seite: ' + path
		Log(msg)
		msg =  msg.decode(encoding="utf-8", errors="ignore")

	return page, msg	

####################################################################################################
@route(PREFIX + '/VerpasstWoche')	# Liste der Wochentage
	# Ablauf (ARD): 	
	#		2. PageControl: Liste der Rubriken des gewählten Tages
	#		3. SinglePage: Sendungen der ausgewählten Rubrik mit Bildern (mehrere Sendungen pro Rubrik möglich)
	#		4. Parseplaylist: Auswertung m3u8-Datei (verschiedene Auflösungen)
	#		5. CreateVideoClipObject: einzelnes Video-Objekt erzeugen mit Bild + Laufzeit + Beschreibung
def VerpasstWoche(name, title, sender, kanal):	# Wochenliste zeigen, name: ARD, ZDF Mediathek
	Log('VerpasstWoche: ' + sender)
	title_org = '%s | aktuell: %s'	% (title, sender)
	title_org=title_org.decode(encoding="utf-8", errors="ignore")
	
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=title_org, art = ObjectContainer.art)
	if name == 'ZDF Mediathek':
		oc = home(cont=oc, ID='ZDF')						# Home-Button
	else:	
		oc = home(cont=oc, ID='ARD')						# Home-Button	
		
	wlist = range(0,7)
	now = datetime.datetime.now()

	for nr in wlist:
		iPath = BASE_URL + ARD_VERPASST + '%s&kanal=%s' 	% (str(nr), kanal)
		rdate = now - datetime.timedelta(days = nr)
		iDate = rdate.strftime("%d.%m.%Y")		# Formate s. man strftime (3)
		zdfDate = rdate.strftime("%Y-%m-%d")		
		iWeekday =  rdate.strftime("%A")
		punkte = '.'
		if nr == 0:
			iWeekday = 'Heute'	
		if nr == 1:
			iWeekday = 'Gestern'	
		iWeekday = transl_wtag(iWeekday)
		Log(iPath); Log(iDate); Log(iWeekday);
		#title = ("%10s ..... %10s"% (iWeekday, iDate))	 # Formatierung in Plex ohne Wirkung
		title =	"%s | %s" % (iDate, iWeekday)
		cbKey = 'SinglePage'	# cbKey = Callback für Container in PageControl
		if name.find('ARD') == 0 :
			oc.add(DirectoryObject(key=Callback(PageControl, title=title, path=iPath, cbKey='SinglePage', 
				mode='Verpasst', ID='ARD'), title=title, thumb=R(ICON_ARD_VERP)))				
		else:
			oc.add(DirectoryObject(key=Callback(ZDF_Verpasst, title=title, zdfDate=zdfDate),	  
				title=title, thumb=R(ICON_ZDF_VERP)))
				
	if name.find('ARD') == 0 :
		title = 'Wählen Sie Ihren Sender | aktuell: %s'	% sender
		title=title.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(KanalWahl, title=title, sender=sender), title=title,
			summary=title, thumb=R(ICON_ARD_VERP)))
		
	return oc
#------------
def transl_wtag(tag):	# Wochentage engl./deutsch wg. Problemen mit locale-Setting 
	wt_engl = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	wt_deutsch = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
	
	wt_ret = tag
	for i in range (len(wt_engl)):
		el = wt_engl[i]
		if el == tag:
			wt_ret = wt_deutsch[i]
			break
	return wt_ret
#------------
@route(PREFIX + '/KanalWahl')	
# 	Kanal-Wahl für Verpasst (nur ARD) - falls die Kanäle sich ändern, von
#	Verpasst-Seite (BASE_URL + ARD_VERPASST) neu holen (1. Block class="entryGroup")
def KanalWahl(title, sender):	
	Log('KanalWahl'); 	
	title=title.decode(encoding="utf-8", errors="ignore")
	entries = ['Das Erste:208', 'BR:2224', 'HR:5884', 'KiKA:5886', 'MDR Fernsehen:5882', 
				'MDR THÜRINGEN:1386988', 'MDR SACHSEN-ANHALT:1386898', 'MDR SACHSEN:1386804', 
				'rbb Fernsehen:5874', 'rbb Fernsehen Brandenburg:21518356', 'rbb Fernsehen Berlin:21518358', 
				'SR:5870', 'SWR Fernsehen:5310', 'SWR Rheinland-Pfalz:5872', 'SWR Baden-Württemberg:5904', 
				'WDR:5902', 'tagesschau24:5878', 'ARD-alpha:5868', 'ONE:673348']
			
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=title, art = ObjectContainer.art)
	oc = home(cont=oc, ID='ARD')						# Home-Button	
	
	for entry in entries:
		Log(entry)
		sender, kanal = entry.split(':')
		Log(sender); Log(kanal)
		url = BASE_URL + ARD_VERPASST + 'kanal=' + kanal
		title = 'Verpasst-Sender: %s' % sender
		title=title.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(VerpasstWoche, name='ARD', title='Sendung Verpasst', sender=sender, 
			kanal=kanal), title=title, summary=title, tagline='TV', thumb=R(ICON_ARD_VERP)))		 
	
	return oc
		
####################################################################################################
@route(PREFIX + '/PodFavoritenListe')		
def PodFavoritenListe(title, offset=0):
	import Pod_content
	
	Log('PodFavoritenListe'); 
	title_org = title
	
	fname =  Prefs['pref_podcast_favorits']		# Default: podcast-favorits.txt im Ressourcenverz.
	Log(fname)
	if os.path.isfile(fname) == False:
		Log(fname + ' nicht gefunden')					
		Inhalt = Resource.Load(FAVORITS_Pod)	
	else:										
		try:
			Inhalt = Core.storage.load(fname)	# pers. Datei verwenden (Name ebenfalls podcast-favorits.txt)	
		except:
			Inhalt = ''

	if  Inhalt is None or Inhalt == '':	
		msg='Datei podcast-favorits.txt nicht gefunden oder nicht lesbar.\nBitte Einstellungen prüfen.'
		return NotFound(msg)
							
	# Log(Inhalt) 
	bookmarks = []
	lines = Inhalt.splitlines()
	for line in lines:						# Kommentarzeilen + Leerzeilen löschen
		if line.startswith('#'):			
			continue
		if line.strip() == '':		
			continue
		bookmarks.append(line)
		
	rec_per_page = 20								# Anzahl pro Seite
	max_len = len(bookmarks)						# Anzahl Sätze gesamt
	start_cnt = int(offset) 						# Startzahl diese Seite
	end_cnt = int(start_cnt) + int(rec_per_page)	# Endzahl diese Seite
				
	title2 = 'Favoriten %s - %s (%s)' % (start_cnt+1, min(end_cnt,max_len) , max_len)
	oc = ObjectContainer(view_group="InfoList", title1='Favoriten', title2=title2, art = ObjectContainer.art)
	oc = home(cont=oc, ID='PODCAST')							# Home-Button

	for i in range(len(bookmarks)):
		cnt = int(i) + int(offset)
		# Log(cnt); Log(i)
		if int(cnt) >= max_len:				# Gesamtzahl überschritten?
			break
		if i >= rec_per_page:				# Anzahl pro Seite überschritten?
			break
		line = bookmarks[cnt]
		try:		
			title = line.split('|')[0]	
			path = line.split('|')[1]
			title = title.strip(); 
			path = path.strip() 
		except:
			title=''; path=''
		Log(title); Log(path)
		if path == '':						# ohne Link kein verwertbarer Favorit
			continue
		
		Log(title); Log(path)
		title=title.decode(encoding="utf-8", errors="ignore")
		summary='Favoriten: ' + title
		summary=summary.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(Pod_content.PodFavoriten, title=title, path=path, offset=0), 
			title=title, tagline=path, summary=summary,  thumb=R(ICON_STAR)))
				
	
	# Mehr Seiten anzeigen:
	Log(offset); Log(cnt); Log(max_len);
	if (int(cnt) +1) < int(max_len): 						# Gesamtzahl noch nicht ereicht?
		new_offset = cnt + int(offset)
		Log(new_offset)
		summ = 'Mehr (insgesamt ' + str(max_len) + ' Favoriten)'
		summ = summ.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(PodFavoritenListe, title=title_org, offset=new_offset), 
			title=title_org, tagline='Favoriten', summary=summ,  thumb=R(ICON_MEHR)))	
	
	return oc

####################################################################################################
@route(PREFIX + '/ARDMore')	# Dachfunktion für 'Ausgewählte Filme' .. 'am besten bewertet' bis einschl. 'Rubriken'
							# ab 06.04.2017 auch Podcasts: 'Rubriken' .. 'Meist abgerufen'
# next_cbKey: Vorgabe für nächsten Callback in SinglePage
# mode: 'Sendereihen', 'Suche' 	- steuert Ausschnitt in SinglePage + bei Podcast Kopfauswertung 1.Satz
#									
def ARDMore(title, morepath, next_cbKey, ID, mode):
	Log('ARDMore'); Log(morepath); Log(ID)
	title2=title.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=title2, art = ObjectContainer.art)
	oc = home(cont=oc, ID=ID)							# Home-Button
					 
	path = morepath
	# Update_ARD_Path entfällt ab 01.12.0218 (Webseiten geändert)
	# path = Update_ARD_Path(morepath)		# Pfad aktualisieren - bei Podcast i.d.R. unverändert
	page = HTTP.Request(path).content
							
	pagenr_path =  re.findall("=page.(\d+)", page) # Mehrfachseiten?
	Log(pagenr_path)
	if pagenr_path:
		del pagenr_path[-1]						# letzten Eintrag entfernen (Doppel) - OK
	Log(pagenr_path)
	Log(path)	
	
	if page.find('mcontents=page.') >= 0: 		# Podcast
		prefix = 'mcontents=page.'
	if page.find('mcontent=page') >= 0: 		# Default
		prefix = 'mcontent=page.'
	if page.find('mresults=page') >= 0: 		# Suche (hier i.d.R. nicht relevant, Direktsprung zu PageControl)
		prefix = 'mresults=page.'

	if pagenr_path:	 							# bei Mehrfachseiten Liste Weiter bauen, beginnend mit 1. Seite
		title = 'Weiter zu Seite 1'
		path = morepath + '&' + prefix + '1' # 1. Seite, morepath würde auch reichen
		Log(path)
		oc.add(DirectoryObject(key=Callback(SinglePage, path=path, title=title, next_cbKey=next_cbKey, mode=mode, ID=ID), 
			title=title, tagline='', summary='',  thumb=R(ICON_NEXT)))			
		
		for page_nr in pagenr_path:
			path = morepath + '&' + prefix + page_nr
			title = 'Weiter zu Seite ' + page_nr
			Log(path)
			oc.add(DirectoryObject(key=Callback(SinglePage, path=path, title=title, next_cbKey=next_cbKey, 
				mode=mode, ID=ID), title=title, tagline='', summary='', thumb=R(ICON_NEXT)))			
	else:										# bei nur 1 Seite springen wir direkt, z.Z. bei Rubriken
		oc = SinglePage(path=path, title=title, next_cbKey=next_cbKey, mode='Sendereihen', ID=ID)
		
	return oc

#------------------------	
# 01.12.2018 entfällt 
def Update_ARD_Path(path):		# aktualisiert den Zugriffspfad fallls mötig, z.B. für "Alle Filme"
	Log('Update_ARD_Path old: ' + path)	
	
	try:
		search_path = stringextract(BASE_URL, '?', path) 	# Base + documentId abschneiden
		search_path = 'href="' + search_path				# Bsp.: href="/tv/Neueste-Videos/mehr
		Log(search_path)
		page, msg = get_page(BASE_URL)						# BASE_URL enthält alle weiter führenden Pfade
		if page == '':	
			return 	ObjectContainer(header='Error', message=msg)						
		
		pos = page.find(search_path)
		if pos >= 0:	# search_path  + Länge documentId (20) + 10 Reserve:
			temp_path = page[pos:pos + len(search_path) + 30]
			temp_path = stringextract('href="', '"', temp_path) # Pfadanteil einschl. documentId	
			Log(temp_path)	
			new_path = BASE_URL + temp_path
			Log(new_path)	
			if new_path == path:
				Log('Update_ARD_Path new=old: ' + path)	
				return path
			else:
				Log('Update_ARD_Path new: ' + path)	
				return new_path
		else:
			Log('Update_ARD_Path: Basispfad nicht gefunden - kein Update')
			return path			# weiter mit altem Pfad - bei Podcast üblich
			
	except:						# bei Zugriffsproblemen mit altem Pfad arbeiten
		Log('Update_ARD_Path: Zugriffsproblem')	
		return path
	
####################################################################################################
@route(PREFIX + '/BarriereArmARD')	# z.Z. nur Hörfassungen - siehe ZDF (BarriereArm)
# ausbauen, falls PMS mehr erlaubt (Untertitle)
# ohne offset - ARD-Ergebnisse werden vom Sender seitenweise ausgegeben 
def BarriereArmARD(name):		# 
	Log('BarriereArmARD')
	
	title = name.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(title2='ARD: ' + title, view_group="List")
	oc = home(cont=oc, ID='ARD')								# Home-Button

	query = urllib2.quote('Hörfassung', "utf-8")
	path = BASE_URL + ARD_Suche	%  query	
	
	title = 'Hörfassungen'.decode(encoding="utf-8")		
	next_cbKey = 'SinglePage'	# cbKey = Callback für Container in PageControl
	oc.add(DirectoryObject(key=Callback(PageControl,title=title, path=path, cbKey=next_cbKey, mode='Suche', 
		ID='ARD'), title=title, summary=title, tagline='TV', thumb=R(ICON_ARD_HOERFASSUNGEN)))			

	return oc
	
####################################################################################################
@route(PREFIX + '/PageControl')	# kontrolliert auf Folgeseiten. Mehrfache Verwendung.
	# Wir laden beim 1. Zugriff alle Seitenverweise in eine Liste. Bei den Folgezugriffen können die Seiten-
	# verweise entfallen - der Rückschritt zur Liste ist dem Anwender nach jedem Listenelement  möglich.
	# Dagegen wird in der Mediathek geblättert.
	# ARDMore stellt die Seitenverweise selbst zusammen.	
	# 
def PageControl(cbKey, title, path, mode, ID, offset=0):  # ID='ARD', 'POD', mode='Suche', 'VERPASST', 'Sendereihen'
	Log('PageControl'); Log('cbKey: ' + cbKey); Log(path)
	Log('mode: ' + mode); Log('ID: ' + str(ID))
	title1='Folgeseiten: ' + title.decode(encoding="utf-8", errors="ignore")
	
	oc = ObjectContainer(view_group="InfoList", title1=title1, title2=title1, art = ObjectContainer.art)
	oc = home(cont=oc, ID=ID)							# Home-Button
	
	page = HTTP.Request(path).content
	Log(len(page))
	path_page1 = path							# Pfad der ersten Seite sichern, sonst gehts mit Seite 2 weiter	

	pagenr_suche = re.findall("mresults=page", page)   
	pagenr_andere = re.findall("mcontents=page", page)  
	pagenr_einslike = re.findall("mcontent=page", page)  	# auch in ARDThemen
	Log(pagenr_suche); Log(pagenr_andere); Log(pagenr_einslike)
	if (pagenr_suche) or (pagenr_andere) or (pagenr_einslike):
		Log('PageControl: Mehrfach-Seite mit Folgeseiten')
	else:												# keine Folgeseiten -> SinglePage
		Log('PageControl: Einzelseite, keine Folgeseiten'); Log(cbKey); Log(path); Log(title)
		oc = SinglePage(title=title, path=path, next_cbKey='SingleSendung', mode=mode, ID=ID) # wir springen direkt 
		if len(oc) == 1:								# 1 = Home
			msgH = 'Error'; msg = 'Keine Inhalte gefunden.'		
			return ObjectContainer(header=msgH, message=msg)		
		return oc																				

	# pagenr_path =  re.findall("&mresults{0,1}=page.(\d+)", page) # lange Form funktioniert nicht
	pagenr_path =  re.findall("=page.(\d+)", page) # 
	Log(pagenr_path)
	if pagenr_path:
		# pagenr_path = repl_dop(pagenr_path) 	# Doppel entfernen (z.B. Zif. 2) - Plex verweigert, warum?
		del pagenr_path[-1]						# letzten Eintrag entfernen - OK
	Log(pagenr_path)
	pagenr_path = pagenr_path[0]	# 1. Seitennummer in der Seite - brauchen wir nicht , wir beginnen bei 1 s.u.
	Log(pagenr_path)		
	
	# ab hier Liste der Folgeseiten. Letzten Eintrag entfernen (Mediathek: Rückverweis auf vorige Seite)
	# Hinw.: die Endmontage muss mit dem Pfad der 1. Seite erfolgen, da ev. Umlaute in den Page-Links 
	#	nicht erfolgreich gequotet werden können (Bsp. Suche nach 'Hörfassung) - das ZDF gibt die
	#	Page-Links unqoted aus, die beim HTTP.Request zum error führen.
	list = blockextract('class=\"entry\"', page)  # sowohl in A-Z, als auch in Verpasst, 1. Element
	del list[-1]				# letzten Eintrag entfernen - wie in pagenr_path
	Log(len(list))

	first_site = True								# falls 1. Aufruf ohne Seitennr.: im Pfad ergänzen für Liste		
	if (pagenr_suche) or (pagenr_andere) or (pagenr_einslike) :		# re.findall s.o.  
		if 	'=page'	not in path:
			if pagenr_andere: 
				path_page1 = path_page1 + 'mcontents=page.1'
				path_end =  '&mcontents=page.'				# path_end für die Endmontage
			if pagenr_suche:
				path_page1 = path_page1 + '&mresults=page.1'# Suche
				path_end = '&mresults=page.' 
			if pagenr_einslike:								#  einslike oder Themen
				path_page1 = path_page1 + 'mcontent=page.1'
				path_end = '&mcontent=page.'
		Log('path_end: ' + path_end)
	else:
		first_site = False
		
	Log(first_site)
	if  first_site == True:										
		path_page1 = path
		title = 'Weiter zu Seite 1'
		next_cbKey = 'SingleSendung'
			
		Log(first_site); Log(path_page1); Log(next_cbKey)
		oc.add(DirectoryObject(key=Callback(SinglePage, title=title, path=path_page1, next_cbKey=next_cbKey, mode=mode, 
				ID=ID), title=title, thumb=ICON))
	else:	# Folgeseite einer Mehrfachseite - keine Liste mehr notwendig
		Log(first_site)													# wir springen wieder direkt:
		oc = SinglePage(title=title, path=path, next_cbKey='SingleSendung', mode=mode, ID=ID) 
	for element in list:	# [@class='entry'] 
		pagenr_suche = ''; pagenr_andere = ''; title = ''; href = ''
		href = stringextract(' href=\"', '\"', element)
		href = unescape(href)
		if href == '': 
			continue							# Satz verwerfen
			
		# Log(element); 	# Log(s)  # class="entry" - nur bei Bedarf
		pagenr =  re.findall("=page.(\d+)", element) 	# einzelne Nummer aus dem Pfad s ziehen	
		Log(pagenr); 
					
		if (pagenr):							# fehlt manchmal, z.B. bei Suche
			if href.find('=page.') >=0:			# Endmontage
				title = 'Weiter zu Seite ' + pagenr[0]
				href =  path_page1 + path_end + pagenr[0]
			else:				
				continue						# Satz verwerfen
		else:
			continue							# Satz verwerfen
			
		Log('href: ' + href); Log('title: ' + title)
		next_cbKey = 'SingleSendung'
		oc.add(DirectoryObject(key=Callback(SinglePage, title=title, path=href, next_cbKey=next_cbKey, mode=mode, ID=ID), 
				title=title, thumb=R(ICON_NEXT)))
	    
	Log(len(oc))
	return oc
  
####################################################################################################
@route(PREFIX + '/SinglePage')	# Liste der Sendungen eines Tages / einer Suche 
								# durchgehend angezeigt (im Original collapsed)
def SinglePage(title, path, next_cbKey, mode, ID, offset=0):	# path komplett
	Log('Funktion SinglePage: ' + path)
	Log('mode: ' + mode); Log('next_cbKey: ' + next_cbKey); Log('ID: ' + str(ID))
	title = title.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(view_group="InfoList", title1=title, art=ICON)
	oc = home(cont=oc, ID=ID)					# Home-Button
	
	func_path = path								# für Vergleich sichern					
	page = HTTP.Request(path).content
	sendungen = ''
	
	if mode == 'Suche':									# relevanten Inhalt ausschneiden, Blöcke bilden
		page = stringextract('data-ctrl-scorefilterloadableLoader-source', '<!-- **** END **** -->', page)	
	if mode == 'Verpasst':								
		page = stringextract('"boxCon isCollapsible', '<!-- **** END **** -->', page)	
	if mode == 'Sendereihen':	
		if ID == 'PODCAST':						       # auch A-Z 
			# Filter nach next_cbKey (PageControl, 	SinglePage, SingleSendung) hier nicht erforderlich	
			page = stringextract('class=\"section onlyWithJs sectionA\">', '<!-- content -->', page)
		else:
			page = stringextract('data-ctrl-layoutable', '<!-- **** END **** -->', page)	
	sendungen = blockextract('class="teaser"', page)	# Sendungsblöcke in PODCAST: 1. teaser=Sendungskopf, 
	Log('sendungen: ' + str(len(sendungen)))			#   Rest Beiträge - Auswertung in get_sendungen	
	Log(len(page));													
	if len(sendungen) == 0:								# Fallback 	
		sendungen = blockextract('class="entry"', page) 				
		Log('sendungen, Fallback: ' + str(len(sendungen)))
	
	send_arr = get_sendungen(oc, sendungen, ID, mode)	# send_arr enthält pro Satz 9 Listen 
	# Rückgabe send_arr = (send_path, send_headline, send_img_src, send_millsec_duration)
	#Log(send_arr); Log('Länge send_arr: ' + str(len(send_arr)))
	send_path = send_arr[0]; send_headline = send_arr[1]; send_subtitel = send_arr[2];
	send_img_src = send_arr[3]; send_img_alt = send_arr[4]; send_millsec_duration = send_arr[5]
	send_dachzeile = send_arr[6]; send_sid = send_arr[7]; send_teasertext = send_arr[8]

	#Log(send_path); Log(send_arr)
	Log(len(send_path));
	for i in range(len(send_path)):					# Anzahl in allen send_... gleich
		path = send_path[i]
		headline = send_headline[i]
		headline = unescape(headline)				# HTML-Escapezeichen  im Titel	
		subtitel = send_subtitel[i]
		img_src = send_img_src[i]
		img_alt = send_img_alt[i]
		img_alt = unescape(img_alt)
		millsec_duration = send_millsec_duration[i]
		if not millsec_duration:
			millsec_duration = "leer"
		dachzeile = send_dachzeile[i]
		Log(dachzeile)
		sid = send_sid[i]
		summary = ''
		if send_teasertext[i] != "":				# teasertext z.B. bei Podcast
			summary = send_teasertext[i]
		else:  
			if dachzeile != "":
				summary = dachzeile 
			if  subtitel != "":
				summary = subtitel
				if  dachzeile != "":
					summary = dachzeile + ' | ' + subtitel
		summary = unescape(summary)
		summary = summary.decode(encoding="utf-8", errors="ignore")
		summary = cleanhtml(summary)
		subtitel = subtitel.decode(encoding="utf-8", errors="ignore")
		subtitel = cleanhtml(subtitel)
		Log(subtitel); Log(dachzeile)
		
		Log('neuer Satz'); Log('path: ' + path); Log(title); Log(headline); Log(img_src); Log(millsec_duration);
		Log('next_cbKey: ' + next_cbKey); Log('summary: ' + summary);
		if next_cbKey == 'SingleSendung':		# Callback verweigert den Funktionsnamen als Variable
			Log('path: ' + path); Log('func_path: ' + func_path); Log('subtitel: ' + subtitel); Log(sid)
			Log(ID)				
			if ID == 'PODCAST':					# Icon für Podcast
				img_src = R(ICON_NOTE)					     
			if func_path == BASE_URL + path: 	# überspringen - in ThemenARD erscheint der Dachdatensatz nochmal
				Log('BASE_URL + path == func_path | Satz überspringen');
				continue
			if sid == '':
				continue
			#if subtitel == '':	# ohne subtitel verm. keine EinzelSendung, sondern Verweis auf Serie o.ä.
			#	continue		#   11.10.2017: Rubrik "must see" ohne subtitel
			if subtitel == summary or subtitel == '':
				subtitel = img_alt.decode(encoding="utf-8", errors="ignore")
			# 27.12.2017 Sendungslisten (mode: Sendereihen) können (angehängte) Verweise auf Sendereihen enthalten,
			#	Bsp. http://www.ardmediathek.de/tv/filme. Erkennung: die sid enthält die bcastId, Bsp. 1933898&bcastId=1933898
			if '&bcastId=' in path:				#  keine EinzelSendung -> Sendereihe
				Log('&bcastId= in path: ' + path)
				if path.startswith('http') == False:	# Bsp. /tv/Film-im-rbb/Sendung?documentId=10009780&bcastId=10009780
					path = BASE_URL + path
				oc.add(DirectoryObject(key=Callback(PageControl, path=path, title=headline, cbKey='SinglePage', 
					mode='Sendereihen', ID=ID), title=headline, tagline=subtitel, summary='Folgeseiten', thumb=img_src))
			else:								# normale Einzelsendung, Bsp. für sid: 48545158
				path = BASE_URL + '/play/media/' + sid			# -> *.mp4 (Quali.-Stufen) + master.m3u8-Datei (Textform)
				Log('Medien-Url: ' + path)
				oc.add(DirectoryObject(key=Callback(SingleSendung, path=path, title=headline, thumb=img_src, 
					duration=millsec_duration, tagline=subtitel, ID=ID, summary=summary), title=headline, tagline=subtitel, 
					summary=summary, thumb=img_src))
		if next_cbKey == 'SinglePage':						# mit neuem path nochmal durchlaufen
			Log('next_cbKey: SinglePage in SinglePage')
			path = BASE_URL + path
			Log('path: ' + path);
			if mode == 'Sendereihen':			# Seitenkontrolle erforderlich, dto. Rubriken in Podcasts
				oc.add(DirectoryObject(key=Callback(PageControl, path=path, title=headline, cbKey='SinglePage', 
					mode='Sendereihen', ID=ID), title=headline, tagline=subtitel, summary=summary, thumb=img_src))
			else:
				oc.add(DirectoryObject(key=Callback(SinglePage, path=path, title=headline, next_cbKey='SingleSendung', 
					mode=mode, ID=ID), title=headline, tagline=subtitel, summary=summary, thumb=img_src))
		if next_cbKey == 'PageControl':		
			path = BASE_URL + path
			Log('path: ' + path);
			Log('next_cbKey: PageControl in SinglePage')
			oc.add(DirectoryObject(key=Callback(PageControl, path=path, title=headline, cbKey='SingleSendung', 
				mode='Sendereihen', ID=ID), title=headline, tagline=subtitel, summary=summary, thumb=img_src))

	Log(len(oc))	# Anzahl Einträge
						
	return oc
####################################################################################################
@route(PREFIX + '/SingleSendung')	# einzelne Sendung, path in neuer Mediathekführt zur 
# Quellenseite (verschiedene Formate -> 
#	1. Text-Seite mit Verweis auf .m3u8-Datei und / oder href_quality_ Angaben zu mp4-videos -
#		im Listenformat, nicht m3u8-Format, die verlinkte master.m3u8 ist aber im 3u8-Format
#	2. Text-Seite mit rtmp-Streams (Listenformat ähnlich Zif. 1, rtmp-Pfade müssen zusammengesetzt
#		werden
#   ab 01.04.2017 mit Podcast-Erweiterung auch Verabeitung von Audio-Dateien
#	18.04.2017 die Podcasts von PodFavoriten enthalten in path bereits mp3-Links, parseLinks_Mp4_Rtmp entfällt

def SingleSendung(path, title, thumb, duration, summary, tagline, ID, offset=0):	# -> CreateVideoClipObject
	title = title.decode(encoding="utf-8", errors="ignore")	# ohne: Exception All strings must be XML compatible
	title_org=title; summary_org=summary; tagline_org=tagline	# Backup 

	Log('SingleSendung path: ' + path)					# z.B. http://www.ardmediathek.de/play/media/11177770
	Log('ID: ' + str(ID))
	
	oc = ObjectContainer(view_group="InfoList", title1=title, art=ICON)
	
	client = Client.Platform
	if client == None:
		client = ''
	if client.find ('Plex Home Theater'): 
		oc = home(cont=oc, ID=ID)						# Home-Button macht bei PHT die Trackliste unbrauchbar 
	# Log(path)
	
	if ID == 'PODCAST':
		Format = 'Podcast-Format: MP3'					# Verwendung in summmary
	else:
		Format = 'Video-Format: MP4'

	# Bei Podcasts enthält path i.d.R. 1 Link zur Seite mit einer mp3-Datei, bei Podcasts von PodFavoriten 
	# wird der mp3-Link	direkt in path übergeben.
	if path.endswith('.mp3') == False:
		Log('vor parseLinks_Mp4_Rtmp')
		page, msg = get_page(path=path)				# Absicherung gegen Connect-Probleme. Page=Textformat
		if page == '':
			return ObjectContainer(header='Error', message=msg)
		link_path,link_img, m3u8_master, geoblock = parseLinks_Mp4_Rtmp(page) # link_img kommt bereits mit thumb, außer Podcasts						
		Log('m3u8_master: ' + m3u8_master); Log(link_img); Log(link_path); 
		if thumb == None or thumb == '': 
			thumb = link_img

		if link_path == []:	      		# keine Videos gefunden		
			Log('link_path == []') 		 
			msgH = 'keine Videoquelle gefunden - Abbruch'; msg = 'keine Videoquelle gefunden - Abbruch. Seite: ' + path;
			return ObjectContainer(header=msgH, message=msg)
		Log('geoblock: ' + geoblock)
		if geoblock == 'true':			# Info-Anhang für summary 
			geoblock = ' | Geoblock!'
		else:
			geoblock = ''
	else:
		m3u8_master = False
		# Nachbildung link_path, falls path == mp3-Link:
		link_path = []; link_path.append('1|'  + path)	# Bsp.: ['1|http://mp3-download.ard.de/...mp3]
  
	# *.m3u8-Datei vorhanden -> auswerten, falls ladefähig. die Alternative 'Client wählt selbst' (master.m3u8)
	# stellen wir voran (WDTV-Live OK, VLC-Player auf Nexus7 'schwerwiegenden Fehler'), MXPlayer läuft dagegen
	if m3u8_master:	  		  								# nicht bei rtmp-Links (ohne master wie m3u8)
		title = 'Bandbreite und Auflösung automatisch'			# master.m3u8
		Codecs = ''
		m3u8_master = m3u8_master.replace('https', 'http')	# 26.06.2017: nun auch ARD mit https
		oc.add(CreateVideoStreamObject(url=m3u8_master, title=title, rtmp_live='nein',
			summary='automatische Auflösung | Auswahl durch den Player' + geoblock, tagline=title, meta=Codecs, 
			thumb=thumb, resolution=''))			
		cont = Parseplaylist(oc, m3u8_master, thumb, geoblock)	# Liste der zusätzlichen einzelnen Auflösungen 
		#del link_path[0]								# master.m3u8 entfernen, Rest bei m3u8_master: mp4-Links
		Log(cont)  										
	 
	# ab hier Auswertung der restlichen mp4-Links bzw. rtmp-Links (aus parseLinks_Mp4_Rtmp)
	# Format: 0|http://mvideos.daserste.de/videoportal/Film/c_610000/611560/format706220.mp4
	# 	oder: rtmp://vod.daserste.de/ardfs/mp4:videoportal/mediathek/...
	#	
	href_quality_S 	= ''; href_quality_M 	= ''; href_quality_L 	= ''; href_quality_XL 	= ''
	download_list = []		# 2-teilige Liste für Download: 'title # url'
	for i in range(len(link_path)):
		s = link_path[i]
		href = s.split('|')[1].strip() # Bsp.: auto|http://www.hr.. / 0|http://pd-videos.daserste.de/..
		Log('s: ' + s)
		if s[0:4] == "auto":	# m3u8_master bereits entfernt. Bsp. hier: 	
			# http://tagesschau-lh.akamaihd.net/z/tagesschau_1@119231/manifest.f4m?b=608,1152,1992,3776 
			#	Platzhalter für künftige Sendungen, z.B. Tagesschau (Meldung in Original-Mediathek:
			# 	'dieser Livestream ist noch nicht verfügbar!'
			#	auto aber auch bei .mp4-Dateien beobachtet, Bsp.: http://www.ardmediathek.de/play/media/40043626
			# href_quality_Auto = s[2:]	
			href_quality_Auto = href	# auto auch bei .mp4-Dateien möglich (s.o.)
			title = 'Qualität AUTO'
			url = href_quality_Auto
			resolution = ''
		if s[0:1] == "0":			
			href_quality_S = href
			title = 'Qualität SMALL'
			url = href_quality_S
			resolution = 240
			download_list.append(title + '#' + url)
		if s[0:1] == "1":			
			href_quality_M = href
			title = 'Qualität MEDIUM'
			url = href_quality_M
			resolution = 480
			download_list.append(title + '#' + url)
		if s[0:1] == "2":			
			href_quality_L = href
			title = 'Qualität LARGE'
			url = href_quality_L
			resolution = 540
			download_list.append(title + '#' + url)
		if s[0:1] == "3":			
			href_quality_XL = href
			title = 'Qualität EXTRALARGE'
			url = href_quality_XL
			resolution = 720
			download_list.append(title + '#' + url)
			

		Log('title: ' + title); Log('url: ' + url); 
		if url:
			if '.m3u8' in url:				# master.m3u8 überspringen, oben bereits abgehandelt
				continue
			if 'manifest.f4m' in url:		# manifest.f4m überspringen
				continue
						
			if url.find('rtmp://') >= 0:	# 2. rtmp-Links:	
				summary = Format + 'RTMP-Stream'	
				oc.add(CreateVideoStreamObject(url=url, title=title, 
					summary=summary+geoblock, tagline=title, meta=path, thumb=thumb, duration=duration, 
					rtmp_live='nein', resolution=''))					
			else:
				summary = Format			# 3. Podcasts mp3-Links, mp4-Links
				if ID == 'PODCAST':
					oc.add(CreateTrackObject(url=url, title=title, summary=summary, fmt='mp3', thumb=thumb))	
				else:
					# 26.06.2017: nun auch ARD mit https - aber: bei den mp4-Videos liefern die Server auch
					#	mit http, während bei m3u8-Url https durch http ersetzt werden MUSS. 
					url = url.replace('https', 'http')	
					oc.add(CreateVideoClipObject(url=url, title=title, 
						summary=summary+geoblock, meta=path, thumb=thumb, tagline='leer', duration='leer', resolution='leer'))
	Log(download_list)
	if 	download_list:			
		# high=-1: letztes Video bisher höchste Qualität
		if summary_org == None:		# Absicherungen für MakeDetailText
			summary_org=''
		if tagline_org == None:
			tagline_org=''
		if thumb == None:
			thumb=''		
		Log(title);Log(summary_org);Log(tagline_org);Log(thumb);
		oc = test_downloads(oc,download_list,title_org,summary_org,tagline_org,thumb,high=-1)  # Downloadbutton(s)
	return oc

#-----------------------
# test_downloads: prüft ob curl/wget-Downloads freigeschaltet sind + erstellt den Downloadbutton
# high (int): Index für einzelne + höchste Video-Qualität in download_list
def test_downloads(oc,download_list,title_org,summary_org,tagline_org,thumb,high):  # Downloadbuttons (ARD + ZDF)
	Log('test_downloads')
	Log(Prefs['pref_use_downloads']) 							# Voreinstellung: False 
	if Prefs['pref_use_downloads'] == True and Prefs['pref_curl_download_path']:
		# Log(Prefs['pref_show_qualities'])
		if Prefs['pref_show_qualities'] == False:				# nur 1 (höchste) Qualität verwenden
			download_items = []
			download_items.append(download_list.pop(high))									 
		else:	
			download_items = download_list						# ganze Liste verwenden
		# Log(download_items)
		
		i=0
		for item in download_items:
			quality,url = item.split('#')
			Log(url); Log(quality); Log(title_org)
			if url.find('.m3u8') == -1 and url.find('rtmp://') == -1:
				# detailtxt =  Begleitdatei mit Textinfos zum Video / Podcast:
				detailtxt = MakeDetailText(title=title_org,thumb=thumb,quality=quality,
					summary=summary_org,tagline=tagline_org,url=url)
				Dict['detailtxt'+str(i)] = detailtxt
				if url.endswith('.mp3'):
					Format = 'Podcast ' 			
				else:	
					Format = 'Video '			# .mp4 oder .webm  (ARD nur .mp4)
				title = Format + 'Download: ' + title_org
				dest_path = Prefs['pref_curl_download_path'] 
				summary = Format + 'wird in ' + dest_path + ' gespeichert' 									
				tagline = 'Der Download erfolgt im Hintergrund | ' + quality
				summary=summary.decode(encoding="utf-8", errors="ignore")
				tagline=tagline.decode(encoding="utf-8", errors="ignore")
				title=title.decode(encoding="utf-8", errors="ignore")
				oc.add(DirectoryObject(key=Callback(DownloadExtern, url=url, title=title_org, dest_path=dest_path,
					key_detailtxt='detailtxt'+str(i)), title=title, summary=summary, thumb=R(ICON_DOWNL), 
					tagline=tagline))
				i=i+1					# Dict-key-Zähler
		Dict.Save()
	return oc
	
#-----------------------
def MakeDetailText(title, summary,tagline,quality,thumb,url):	# Textdatei für Download-Video / -Podcast
	Log('MakeDetailText')
		
	detailtxt = ''
	detailtxt = detailtxt + "%15s" % 'Titel: ' + "'"  + title + "'"  + '\r\n' 
	detailtxt = detailtxt + "%15s" % 'Beschreibung1: ' + "'" + tagline + "'" + '\r\n' 
	detailtxt = detailtxt + "%15s" % 'Beschreibung2: ' + "'" + summary + "'"  + '\r\n' 
	detailtxt = detailtxt + "%15s" % 'Qualitaet: ' + "'" + quality + "'"  + '\r\n' 
	detailtxt = detailtxt + "%15s" % 'Bildquelle: ' + "'" + thumb + "'"  + '\r\n' 
	detailtxt = detailtxt + "%15s" % 'Adresse: ' + "'" + url + "'"  + '\r\n' 
	
	return detailtxt
	
####################################################################################################
@route(PREFIX + '/DownloadExtern')	#  Verwendung von curl/wget mittels Phytons subprocess-Funktionen
# Wegen des Timeout-Problems (ca. 15 sec) macht es keinen Sinn, auf die Beendigung von curl/wget
#	mittels Pipes + communicate zu warten. Daher erfolgt der Start von curl/wget unter Verzicht auf dessen Output.
# Die experimentelle interne Download-Variante mit Bordmitteln wurde wieder entfernt, da nach ca. 15 
#	sec der Server die Verbindung zum Client mit timeout abbricht (unter Linux wurde der Download 
#	trotzdem weiter fortgesetzt).
# url=Video-/Podcast-Quelle, dest_path=Downloadverz.
# Bei Verwendung weiterer Videoformate (neben mp4, webm, mp3) Extensionsbehandlung anpassen: hier sowie
#	DownloadsTools, DownloadsList

# 30.08.2018:
# Zum Problemen "autom. Wiedereintritt" - auch bei PHT siehe Doku in LiveRecord.
#	Die Lösungen / Anpassungen für PHT  wurden hier analog umgesetzt. 
#

def DownloadExtern(url, title, dest_path, key_detailtxt):  # Download mittels curl/wget
	Log('DownloadExtern: ' + title)
	Log(url); Log(dest_path); Log(key_detailtxt)
	title=title.decode(encoding="utf-8", errors="ignore")	
	
	if Dict['PIDcurl']:								# ungewollten Wiedereintritt abweisen 
		Log('PIDcurl: %s' % Dict['PIDcurl'])
		Log('PIDcurl = %s | Blocking DownloadExtern' % Dict['PIDcurl'])
		Dict['PIDcurl'] = ''						# löschen für manuellen Aufruf 
		# Für PHT Info erst hier nach autom. Wiedereintritt nach Popen möglich:
		title1 = 'curl/wget: Download erfolgreich gestartet'
		if 'Home Theater' in str(Client.Platform):	# GetDirectory failed nach Info
			return ObjectContainer(header='Info', message=title1)
		#oc.add(DirectoryObject(key = Callback(DownloadsTools), title = 'Download-Tools', summary=summary, 
		#	thumb=R(ICON_OK), tagline=tagline))						
		return DownloadsTools()

	oc = ObjectContainer(view_group="InfoList", title1='curl/wget-Download', art=ICON)
	oc = home(cont=oc, ID=NAME)					# Home-Button	

	summary = 'Download-Tools: Verschieben, Löschen, Ansehen, Verzeichnisse bearbeiten'	# wie in Main()
	summary = summary.decode(encoding="utf-8", errors="ignore")
	oc.add(DirectoryObject(key = Callback(DownloadsTools), title = 'Download-Tools', 
		summary = summary, thumb = R(ICON_DOWNL_DIR)))		
	
	if 	Prefs['pref_generate_filenames']:				# Dateiname aus Titel generieren
		dfname = make_filenames(title) 
	else:												# Bsp.: Download_2016-12-18_09-15-00.mp4  oder ...mp3
		now = datetime.datetime.now()
		mydate = now.strftime("%Y-%m-%d_%H-%M-%S")	
		dfname = 'Download_' + mydate 
	
	if url.endswith('.mp3'):
		suffix = '.mp3'		
		dtyp = 'Podcast '
	else:												# .mp4 oder .webm	
		dtyp = 'Video '
		if url.endswith('.mp4'):				
			suffix = '.mp4'		
		if url.endswith('.webm'):				
			suffix = '.webm'		
		
	title = dtyp + 'curl/wget-Download: ' + title
	textfile = dfname + '.txt'
	dfname = dfname + suffix							# suffix: '.mp4', '.webm', oder '.mp3'
	
	pathtextfile = os.path.join(dest_path, textfile)	# kompl. Speicherpfad für Textfile
	Log(pathtextfile)
	detailtxt = Dict[key_detailtxt]					
	storetxt = 'Details zum ' + dtyp +  dfname + ':\r\n\r\n' + detailtxt	
			
	Log('Client-Platform: ' + str(Client.Platform))
	Log(sys.platform)
	try:
		Dict['PIDcurl'] = ''
		Core.storage.save(pathtextfile, storetxt)			# Text speichern
		
		AppPath = Prefs['pref_curl_path']
		i = os.path.exists(AppPath)					# Existenz curl/wget prüfen
		Log(AppPath); Log(i)
		if AppPath == '' or i == False:
			msg='Pfad zu curl/wget fehlt oder curl/wget nicht gefunden'
			Log(msg)
			return ObjectContainer(header='Error', message=msg)
			
		# i = os.access(curl_dest_path, os.W_OK)		# Zielverz. prüfen - nicht relevant für curl/wget
														# 	Anwender muss Schreibrecht sicherstellen
		curl_fullpath = os.path.join(dest_path, dfname)	# kompl. Speicherpfad für Video/Podcast
		Log(curl_fullpath)

		# 08.06.2017 wget-Alternative wg. curl-Problem auf Debian-System (Forum: 
		#	https://forums.plex.tv/discussion/comment/1454827/#Comment_1454827
		# 25.06.2018 Parameter -k (keine Zertifikateprüfung) erforderlich wg. curl-Problem
		#	mit dem Systemzertifikat auf manchen Systemen.
		# Debug curl: --trace file anhängen. 
		#
		# http://stackoverflow.com/questions/3516007/run-process-and-dont-wait
		#	creationflags=DETACHED_PROCESS nur unter Windows
		if AppPath.find('curl') > 0:									# curl-Call
			Log('%s %s %s %s %s' % (AppPath, url, "-o", curl_fullpath, "-k"))	
			sp = subprocess.Popen([AppPath, url, "-o", curl_fullpath, "-k"])	# OK, wartet nicht (ohne p.communicate())
			# sp = subprocess.Popen([AppPath, url, "-N", "-o", curl_fullpath])	# Buffering für curl abgeschaltet
		else:															# wget-Call
			Log('%s %s %s %s %s %s' % (AppPath, "--no-use-server-timestamps", "-q", "-O", curl_fullpath, url))	
			sp = subprocess.Popen([AppPath, "--no-check-certificate", "--no-use-server-timestamps", "-q", "-O", curl_fullpath, url])
			
		msgH = 'curl/wget: Download erfolgreich gestartet'
		Log('sp = ' + str(sp))
	
		if str(sp).find('object at') > 0:  				# subprocess.Popen object OK
			Dict['PIDcurl'] = sp.pid					# PID zum Abgleich gegen Wiederholung sichern
			Log('PIDcurl neu: %s' % Dict['PIDcurl'])
			Log(msgH)			
			tagline = 'Zusatz-Infos in Textdatei gespeichert:' + textfile
			summary = 'Ablage: ' + curl_fullpath
			summary = summary.decode(encoding="utf-8", errors="ignore")	
			# PHT springt hier zurück an den Funktionskopf - Info dort
			#if 'Home Theater' in str(Client.Platform):	# GetDirectory failed nach Info
			#return ObjectContainer(header='Info', message=msgH)
			# für andere Player: DirectoryObject wird nicht immer ausgeführt
			oc.add(DirectoryObject(key = Callback(DownloadsTools), title = 'Download-Tools', summary=summary, 
				thumb=R(ICON_OK), tagline=tagline))						
			return oc				
		else:
			raise Exception('Start von curl/wget fehlgeschlagen')
			
	except Exception as exception:
		summary = str(exception)
		summary = summary.decode(encoding="utf-8", errors="ignore")
		Log(summary)		
		tagline='Download fehlgeschlagen'
		# bei Fehlschlag gibt PHT die message aus (im Gegensatz zu oben):
		if 'Home Theater' in str(Client.Platform):	# GetDirectory failed nach Info
			return ObjectContainer(header='Fehler', message=tagline)
		oc.add(DirectoryObject(key = Callback(DownloadsTools), title = 'Fehler', summary=summary, 
				thumb=R(ICON_CANCEL), tagline=tagline))		
		return oc
	
#---------------------------
@route(PREFIX + '/DownloadsTools')		# Tools: Einstellungen,  Bearbeiten, Verschieben, Löschen
def DownloadsTools():
	Log('DownloadsTools');

	path = Prefs['pref_curl_download_path']
	Log(path)
	dirlist = []
	if path == None or path == '':									# Existenz Verz. prüfen, falls vorbelegt
		title1 = 'Downloadverzeichnis noch nicht festgelegt'
	else:
		if os.path.isdir(path)	== False:			
			msg='Downloadverzeichnis nicht gefunden: ' + path
			return ObjectContainer(header='Error', message=msg)
		else:
			dirlist = os.listdir(path)						# Größe Inhalt? 		
			
	Log(len(dirlist))
	mpcnt=0; vidsize=0
	for entry in dirlist:
		if entry.find('.mp4') > 0 or entry.find('.webm') > 0 or entry.find('.mp3') > 0:
			mpcnt = mpcnt + 1	
			fname = os.path.join(path, entry)					
			vidsize = vidsize + os.path.getsize(fname) 
	vidsize	= vidsize / 1000000
	title1 = 'Downloadverzeichnis: %s Download(s), %s MBytes' % (mpcnt, str(vidsize))
		
	oc = ObjectContainer(view_group="InfoList", title1=title1, art=ICON)
	oc = home(cont=oc, ID=NAME)								# Home-Button	
	
	s = Prefs['pref_curl_path']											# Einstellungen: Pfad curl/wget
	title = 'Einstellungen: Pfad zum Downloadprogramm curl/wget festlegen/ändern (%s)' %s	
	title=title.decode(encoding="utf-8", errors="ignore")
	tagline = 'Hier wird der Pfad zum Downloadprogramm curl/wget eingestellt.'
	summary = 'Dies kann auch manuell im Webplayer erfolgen (Zahnradsymbol) '
	oc.add(DirectoryObject(key=Callback(DirectoryNavigator,settingKey = 'pref_curl_path', fileFilter='curl|wget',
		newDirectory=s),title = title, tagline=tagline, summary=summary, thumb = R(ICON_DIR_CURLWGET)))

	s =  Prefs['pref_curl_download_path']								# Einstellungen: Pfad Downloaderz.
	title = 'Einstellungen: Downloadverzeichnisses festlegen/ändern (%s)' %s			
	title=title.decode(encoding="utf-8", errors="ignore")
	tagline = 'Das Downloadverzeichnis muss für Plex beschreibbar sein.'
	tagline=tagline.decode(encoding="utf-8", errors="ignore")
	# summary =    # s.o.
	oc.add(DirectoryObject(key=Callback(DirectoryNavigator,settingKey = 'pref_curl_download_path', fileFilter='DIR',
		newDirectory=s), title = title, tagline=tagline, summary=summary, thumb = R(ICON_DOWNL_DIR)))

	Log(Prefs['pref_VideoDest_path'])
	if Prefs['pref_VideoDest_path'] == None:			# Vorgabe Medienverzeichnis (Movieverz), falls leer
		data = HTTP.Request("%s/library/sections" % (myhost), immediate=True).content # . ermitteln 
		data = data.strip() 							# ohne strip fehlt unter Windows alles nach erstem /r/n
		s = stringextract('resources/movie.png', '/Directory>', data)					 
		movie_path = stringextract('path=\"', '\"', s)
	else:
		movie_path = Prefs['pref_VideoDest_path']
				
	if os.path.isdir(movie_path)	== False:			# Sicherung gegen Fehleinträge
		movie_path = None								# wird ROOT_DIRECTORY in DirectoryNavigator
	else:
		movie_path = True
	Log(movie_path)	
	videst = Prefs['pref_VideoDest_path']				# Einstellungen: Pfad Verschiebe-Verz.
	title = 'Einstellungen: Zielverzeichnis zum Verschieben festlegen/ändern (%s)' % (videst)	
	title=title.decode(encoding="utf-8", errors="ignore")
	tagline = 'Zum Beispiel das Medienverzeichnis. Das Zielverzeichnis muss außerhalb des Plugins liegen.' 
	tagline=tagline.decode(encoding="utf-8", errors="ignore")
	# summary =    # s.o.
	oc.add(DirectoryObject(key=Callback(DirectoryNavigator,settingKey = 'pref_VideoDest_path', fileFilter='DIR',
		newDirectory=videst), title = title, tagline=tagline, summary=summary, thumb = R(ICON_MOVEDIR_DIR)))
		
	Log(Prefs['pref_podcast_favorits'])					# Pfad zur persoenlichen Podcast-Favoritenliste
	s =  Prefs['pref_podcast_favorits']								
	title = 'Einstellungen: persönliche Podcast-Favoritenliste festlegen/ändern (%s)' %s			
	title=title.decode(encoding="utf-8", errors="ignore")
	tagline = 'Die Liste muss für Plex lesbar sein. Format siehe podcast-favorits.txt (Ressourcenverzeichnis)'
	tagline=tagline.decode(encoding="utf-8", errors="ignore")
	# summary =    # s.o.
	oc.add(DirectoryObject(key=Callback(DirectoryNavigator,settingKey = 'pref_podcast_favorits', fileFilter='podcast-favorits.txt',
		newDirectory=s), title = title, tagline=tagline, summary=summary, thumb = R(ICON_DIR_FAVORITS)))
			
	title = 'Downloads bearbeiten: %s Download(s)' % (mpcnt)				# Button Bearbeiten
	summary = 'Downloads im Downloadverzeichnis ansehen, löschen, verschieben'
	summary=summary.decode(encoding="utf-8", errors="ignore")
	oc.add(DirectoryObject(key=Callback(DownloadsList),title = title, summary=summary, thumb = R(ICON_DIR_WORK)))

	if dirlist:
		dlpath = Prefs['pref_curl_download_path'] 
		if videst and movie_path:
			title = 'alle Downloads verschieben: %s Download(s)' % (mpcnt)	# Button Verschieben (alle)
			tagline = 'Verschieben erfolgt ohne Rückfrage!' 
			tagline=tagline.decode(encoding="utf-8", errors="ignore")			
			summary = 'alle Downloads verschieben nach: %s'  % (videst)
			summary=summary.decode(encoding="utf-8", errors="ignore")
			oc.add(DirectoryObject(key=Callback(DownloadsMove, dfname='', textname='', dlpath=dlpath, 
				destpath=videst, single=False), title=title, tagline=tagline, summary=summary, 
				thumb=R(ICON_DIR_MOVE_ALL)))		
		
		title = 'alle Downloads löschen: %s Download(s)' % (mpcnt)			# Button Leeren (alle)
		title=title.decode(encoding="utf-8", errors="ignore")			
		tagline = 'Leeren erfolgt ohne Rückfrage!'						
		tagline=tagline.decode(encoding="utf-8", errors="ignore")
		summary = 'alle Dateien aus dem Downloadverzeichnis entfernen'
		oc.add(DirectoryObject(key=Callback(DownloadsDelete, dlpath=dlpath, single='False'),
			title=title, summary=summary, thumb=R(ICON_DELETE), tagline=tagline))
			
	return oc
	
#---------------------------
@route(PREFIX + '/DownloadsList')	 	# Downloads im Downloadverzeichnis zur Bearbeitung listen
def DownloadsList():
	Log('DownloadsList')	
	path = Prefs['pref_curl_download_path']
	
	dirlist = []
	if path == None or path == '':									# Existenz Verz. prüfen, falls vorbelegt
		title1 = 'Downloadverzeichnis noch nicht festgelegt'
	else:
		if os.path.isdir(path)	== False:			
			msg='Downloadverzeichnis nicht gefunden: ' + path
			return ObjectContainer(header='Error', message=msg)
		else:
			dirlist = os.listdir(path)						# Größe Inhalt? 		
	dlpath = path

	Log(len(dirlist))
	mpcnt=0; vidsize=0
	for entry in dirlist:
		if entry.find('.mp4') > 0 or entry.find('.webm') > 0 or entry.find('.mp3') > 0:
			mpcnt = mpcnt + 1	
			fname = os.path.join(path, entry)					
			vidsize = vidsize + os.path.getsize(fname) 
	vidsize	= vidsize / 1000000
	title1 = 'Downloadverzeichnis: %s Download(s), %s MBytes' % (mpcnt, str(vidsize))
	
	if mpcnt == 0:
		msg='Kein Download vorhanden | Pfad: %s' % (dlpath)
		return ObjectContainer(header='Error', message=msg)
		
		
	oc = ObjectContainer(view_group="InfoList", title1=title1, art=ICON)
	oc = home(cont=oc, ID='ARD')								# Home-Button	
	# Downloads listen:
	for entry in dirlist:							# Download + Beschreibung -> DirectoryObject
		if entry.find('.mp4') > 0 or entry.find('.webm') > 0 or entry.find('.mp3') > 0:
			localpath = entry
			title=''; tagline=''; summary=''; quality=''; thumb=''; httpurl=''
			fname =  entry							# Dateiname 
			basename = os.path.splitext(fname)[0]	# ohne Extension
			ext =     os.path.splitext(fname)[1]	# Extension
			Log(fname); Log(basename); Log(ext)
			txtfile = basename + '.txt'
			txtpath = os.path.join(path, txtfile)   # kompl. Pfad
			Log('entry: ' + entry)
			Log('txtpath: ' + txtpath)
			if os.path.exists(txtpath):
				txt = Core.storage.load(txtpath)		# Beschreibung laden - fehlt bei Sammeldownload
			else:
				txt = None
			if txt != None:			
				title = stringextract("Titel: '", "'", txt)
				tagline = stringextract("ung1: '", "'", txt)
				summary = stringextract("ung2: '", "'", txt)
				quality = stringextract("tät: '", "'", txt)
				thumb = stringextract("Bildquelle: '", "'", txt)
				httpurl = stringextract("Adresse: '", "'", txt)
				
				if tagline == '':
					tagline = quality
				else:
					if len(quality.strip()) > 0:
						tagline = quality + ' | ' + tagline
			else:										# ohne Beschreibung
				title = fname
				httpurl = fname							# Berücksichtigung in VideoTools - nicht abspielbar
				summary = 'Beschreibung fehlt - Abspielen nicht möglich'
				tagline = 'Beschreibung fehlt - Beschreibung gelöscht, Sammeldownload oder TVLive-Video'
				
			Log(httpurl); Log(tagline); Log(quality); # Log(txt); 			
			if httpurl.endswith('mp3'):
				oc_title = 'Bearbeiten: Podcast | ' + title
				thumb = R(ICON_NOTE)
			else:
				oc_title='Bearbeiten: ' + title
				if thumb == '':							# nicht in Beschreibung
					thumb = R(ICON_DIR_VIDEO)
			summary=summary.decode(encoding="utf-8", errors="ignore")
			tagline=tagline.decode(encoding="utf-8", errors="ignore")
			title=title.decode(encoding="utf-8", errors="ignore")
			oc_title=oc_title.decode(encoding="utf-8", errors="ignore")

			oc.add(DirectoryObject(key=Callback(VideoTools, httpurl=httpurl, path=localpath, dlpath=dlpath, 
				txtpath=txtpath, title=title,summary=summary, thumb=thumb, tagline=tagline), 
				title=oc_title, summary=summary, thumb=thumb, tagline=tagline))	
	return oc				

#---------------------------
@route(PREFIX + '/VideoTools')	# 			# Downloads im Downloadverzeichnis ansehen, löschen, verschieben
#	zum  Ansehen muss das Video  erneut angefordert werden - CreateVideoClipObject verweigert die Wiedergabe
#		lokaler Videos: networking.py line 224, in load ... 'file' object has no attribute '_sock'
#	httpurl=HTTP-Videoquelle, path=Videodatei (Name), dlpath=Downloadverz., txtpath=Textfile (kompl. Pfad)
#	
def VideoTools(httpurl,path,dlpath,txtpath,title,summary,thumb,tagline):
	Log('VideoTools: ' + path)
	
	title=title.decode(encoding="utf-8", errors="ignore") 
	title_org = title
	title1 = 'Bearbeiten: ' + title[:33] + '..'	# Begrenzung nötig für "Dateinamen aus dem Titel"
	title1=title1.decode(encoding="utf-8", errors="ignore")
	summary=summary.decode(encoding="utf-8", errors="ignore")

	oc = ObjectContainer(view_group="InfoList", title1=title1, art=ICON)
	oc = home(cont=oc, ID=NAME)					# Home-Button	
	
	if httpurl.endswith('mp4') or httpurl.endswith('webm'):
		title = title_org + ' | Ansehen' 											# 1. Ansehen
		title=title.decode(encoding="utf-8", errors="ignore")
		summary=summary.decode(encoding="utf-8", errors="ignore")
		oc.add(CreateVideoClipObject(url=httpurl, title=title , summary=summary, 
			meta=httpurl, thumb=thumb, tagline='leer', duration='leer', resolution='leer'))
	else:										# 'mp3' = Podcast
		if httpurl.startswith('http'):			# Dateiname bei fehl. Beschreibung, z.B. Sammeldownloads
			title = title_org + ' | Anhören' 										# 1. Anhören
			title=title.decode(encoding="utf-8", errors="ignore")
			oc.add(CreateTrackObject(url=httpurl, title=title, summary=summary,
				 thumb=thumb, fmt='mp3'))				# funktioniert hier auch mit aac
		
	title = title_org + ' | löschen ohne Rückfrage' 								# 2. Löschen
	title=title.decode(encoding="utf-8", errors="ignore")
	tagline = 'Datei: ' + path 
	tagline=tagline.decode(encoding="utf-8", errors="ignore")
	dest_path = Prefs['pref_curl_download_path']	
	fullpath = os.path.join(dest_path, path)
	oc.add(DirectoryObject(key=Callback(DownloadsDelete, dlpath=fullpath, single='True'),
		title=title, tagline=tagline, summary=summary, thumb=R(ICON_DELETE)))
		
	if Prefs['pref_VideoDest_path']:							# 3. Verschieben nur mit Zielpfad, einzeln
		textname = os.path.basename(txtpath)
		title = title_org + ' | verschieben nach: '	+ Prefs['pref_VideoDest_path']									
		title=title.decode(encoding="utf-8", errors="ignore")
		summary = title
		tagline = 'Das Zielverzeichnis kann im Menü Download-Tools geändert werden'
		tagline=tagline.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(DownloadsMove, dfname=path, textname=textname, dlpath=dlpath, 
			destpath=Prefs['pref_VideoDest_path'], single=True), title=title, tagline=tagline, summary=summary, 
			thumb=R(ICON_DIR_MOVE_SINGLE)))
			
	return oc
	
#---------------------------
@route(PREFIX + '/DownloadsDelete')	# 			# Downloadverzeichnis leeren (einzeln/komplett)
def DownloadsDelete(dlpath, single):
	Log('DownloadsDelete: ' + dlpath)
	Log('single=' + single)
	oc = ObjectContainer(view_group="InfoList", title1='Download-Tools', art=ICON)
	oc = home(cont=oc, ID=NAME)					# Home-Button	

	try:
		if single == 'False':
			for i in os.listdir(dlpath):		# Verz. leeren
				fullpath = os.path.join(dlpath, i)
				os.remove(fullpath)
			error_txt = 'Downloadverzeichnis geleert'
		else:
			txturl = os.path.splitext(dlpath)[0]  + '.txt' 
			if os.path.isfile(dlpath) == True:							
				os.remove(dlpath)				# Video löschen
			if os.path.isfile(txturl) == True:							
				os.remove(txturl)				# Textdatei löschen
			error_txt = 'Datei gelöscht: ' + dlpath
		Log(error_txt)			 			 	 
		title = 'Löschen erfolgreich | zurück zu den Download-Tools'
		title =  title.decode(encoding="utf-8", errors="ignore")
		tagline = error_txt
		tagline =  tagline.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(DownloadsTools), title=title, summary=title, thumb=R(ICON_OK), 
			tagline=tagline))
		return oc
	except Exception as exception:
		Log(str(exception))
		title = 'Fehler | zurück zu den Download-Tools'
		title =  title.decode(encoding="utf-8", errors="ignore")
		tagline='Löschen fehlgeschlagen | ' + str(exception)
		tagline =  tagline.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(DownloadsTools), title=title, summary=title, thumb=R(ICON_CANCEL), 
			tagline=tagline))
		return oc

#---------------------------
@route(PREFIX + '/DownloadsMove')	# 			# # Video + Textdatei verschieben
# dfname=Videodatei, textname=Textfile,  dlpath=Downloadverz., destpath=Zielverz.
#
def DownloadsMove(dfname, textname, dlpath, destpath, single):
	Log('DownloadsMove: ');Log(dfname);Log(textname);Log(dlpath);Log(destpath);
	Log('single=' + single)

	oc = ObjectContainer(view_group="InfoList", title1='Download-Tools', art=ICON)
	oc = home(cont=oc, ID=NAME)					# Home-Button	

	if  os.access(destpath, os.W_OK) == False:
		title = 'Fehler | zurück zu den Download-Tools'
		title =  title.decode(encoding="utf-8", errors="ignore")
		tagline='Download fehlgeschlagen | Kein Schreibrecht im Zielverzeichnis'
		oc.add(DirectoryObject(key=Callback(DownloadsTools), title=title, summary=title, thumb=R(ICON_CANCEL), 
			tagline=tagline))
		return oc
	
	try:
		cnt = 0
		if single == 'False':				# kompl. Verzeichmis
			for i in os.listdir(dlpath):
				src = os.path.join(dlpath, i)
				dest = os.path.join(destpath, i)							
				Log(src); Log(dest); 
				
				if os.path.isfile(src) == True:							
					shutil.copy(src, destpath)	# Datei kopieren	
					os.remove(src)				# Datei löschen
					cnt = cnt + 1
			error_txt = '%s Dateien verschoben nach: %s' % (cnt, destpath)		 			 	 
		else:
			textsrc = os.path.join(dlpath, textname)
			textdest = os.path.join(destpath, textname)	
			videosrc = os.path.join(dlpath, dfname)
			videodest = os.path.join(destpath, dfname)		
			Log(videosrc); Log(videodest);
								
			if os.path.isfile(textsrc) == True:	# Quelldatei testen						
				shutil.copy(textsrc, textdest)		
				os.remove(textsrc)				# Textdatei löschen
			if os.path.isfile(videosrc) == True:							
				shutil.copy(videosrc, videodest)				
				os.remove(videosrc)				# Videodatei dto.
			error_txt = 'Video + Textdatei verschoben: ' + 	dfname				 			 	 
		Log(error_txt)			 			 	 		
		title = 'Verschieben erfolgreich | zurück zu den Download-Tools'
		title =  title.decode(encoding="utf-8", errors="ignore")
		title =  title.decode(encoding="utf-8", errors="ignore")
		tagline = error_txt
		tagline =  tagline.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(DownloadsTools), title=title, summary=title, thumb=R(ICON_OK), 
			tagline=tagline))
		return oc

	except Exception as exception:
		Log(str(exception))
		title = 'Fehler | zurück zu den Download-Tools'
		title =  title.decode(encoding="utf-8", errors="ignore")
		tagline='Verschieben fehlgeschlagen | ' + str(exception)
		oc.add(DirectoryObject(key=Callback(DownloadsTools), title=title, summary=title, thumb=R(ICON_CANCEL), 
			tagline=tagline))
		return oc
		
####################################################################################################
def parseLinks_Mp4_Rtmp(page):		# extrahiert aus Mediendatei (Text) .mp4- und rtmp-Links (Aufrufer 
									# SingleSendung). Bsp.: http://www.ardmediathek.de/play/media/35771780
	Log('parseLinks_Mp4_Rtmp')		
	#Log('parseLinks_Mp4_Rtmp: ' + page)	# bei Bedarf
	
	if page.find('_previewImage') >= 0:
		#link_img = teilstring(page, 'http://www.ardmediathek.de/image', '\",\"_subtitleUrl')
		#link_img = stringextract('_previewImage\":\"', '\",\"_subtitle', page)
		link_img = stringextract('_previewImage\":\"', '\",', page) # ev. nur Mediatheksymbol
	else:
		link_img = ""

	link_path = []							# Liste nimmt Pfade und Quali.-Markierung auf
	m3u8_master = ''						# nimmt master.m3u8 zusätzlich auf	
	geoblock =  stringextract('_geoblocked":', '}', page)	# Geoblock-Markierung ARD
	
	if page.find('\"_quality\":') >= 0:
		s = page.split('\"_quality\":')	
		# Log(s)							# nur bei Bedarf
		del s[0]							# 1. Teil entfernen - enthält img-Quelle (s.o.)
		
		for i in range(len(s)):
			s1 =  s[i]
			s2 = ''
			Log(s1)						# Bsp.: 1,"_server":"","_cdn":"akamai","_stream":"http://avdlswr-..
				
			if s1.find('rtmp://') >= 0: # rtmp-Stream 
				Log('s1: ' + s1)
				t1 = stringextract('server\":\"', '\",\"_cdn\"', s1) 
				t2 = stringextract( '\"_stream\":\"', '\"}', s1) 
				s2 = t1 + t2	# beide rtmp-Teile verbinden
				#Log(s2)				# nur bei Bedarf
			else:						# http-Links, auch Links, die mit // beginnen
				s2 = stringextract('stream\":\"','\"', s1)
				if s2.startswith('//'):				# 12.09.2017: WDR-Links ohne http:
					s2 = 'http:' + s2
				if 'master.m3u8' in s1:
					m3u8_master = s2
			Log(s2); Log(len(s2))				# nur bei Bedarf
				
							
			if len(s2) > 9:						# schon url gefunden? Dann Markierung ermitteln
				if s1.find('auto') >= 0:
					mark = 'auto' + '|'					
				else:
					m = s1[0:1] 				# entweder Ziffern 0,1,2,3 
					mark = m + '|' 	
								
				link = mark + s2				# Qualität voranstellen			
				link_path.append(link)
				Log(mark); Log(s2); Log(link); # Log(link_path)
			
	#Log(link_path)				
	link_path = list(set(link_path))			# Doppel entfernen (gesehen: 0, 1, 2 doppelt)
	link_path.sort()							# Sortierung - Original Bsp.: 0,1,2,0,1,2,3
	Log(link_path); Log(len(link_path))					
		
	return link_path, link_img, m3u8_master, geoblock				 		
		
####################################################################################################
def get_sendungen(container, sendungen, ID, mode): # Sendungen ausgeschnitten mit class='teaser', aus Verpasst + A-Z,
	# 										Suche, Einslike
	# Headline + Subtitel sind nicht via xpath erreichbar, daher Stringsuche:
	# ohne linklist + Subtitel weiter (teaser Seitenfang od. Verweis auf Serie, bei A-Z teaser-Satz fast identisch,
	#	nur linklist fehlt )
	# Die Rückgabe-Liste send_arr nimmt die Datensätze auf (path, headline usw.)
	# ab 02.04.2017: ID=PODCAST	- bei Sendereihen enthält der 1. Satz Bild + Teasertext
	Log('get_sendungen'); Log(ID); Log(mode); 

	img_src_header=''; img_alt_header=''; teasertext_header=''; teasertext=''
	if ID == 'PODCAST' and mode == 'Sendereihen':							# PODCAST: Bild + teasertext nur im Kopf vorhanden
		# Log(sendungen[0])		# bei Bedarf
		if sendungen[0].find('urlScheme') >= 0:	# Bild ermitteln, versteckt im img-Knoten
			text = stringextract('urlScheme', '/noscript', sendungen[0])
			img_src_header, img_alt_header = img_urlScheme(text, 320, ID) # Format quadratisch bei Podcast
			teasertext_header = stringextract('<h4 class=\"teasertext\">', '</p>', sendungen[0])
		del sendungen[0]						# nicht mehr benötigt, Beiträge folgen dahinter
			
	# send_arr nimmt die folgenden Listen auf (je 1 Datensatz pro Sendung)
	send_path = []; send_headline = []; send_subtitel = []; send_img_src = [];
	send_img_alt = []; send_millsec_duration = []; send_dachzeile = []; send_sid = []; 
	send_teasertext = []; 
	arr_ind = 0
	for s in sendungen:	
		found_sendung = False
		if s.find('<div class="linklist">') == -1 or ID == 'PODCAST':  # PODCAST-Inhalte ohne linklistG::;
			if  s.find('subtitle') >= 0: 
				found_sendung = True
			if  s.find('dachzeile') >= 0: # subtitle in ARDThemen nicht vorhanden
				found_sendung = True
			if  s.find('<h4 class=\"headline\">') >= 0:  # in Rubriken weder subtitle noch dachzeile vorhanden
				found_sendung = True
				
		Log(found_sendung)
		# Log(s)				# bei Bedarf
		if found_sendung:				
			dachzeile = re.search("<p class=\"dachzeile\">(.*?)</p>\s+?", s)  # Bsp. <p class="dachzeile">Weltspiegel</p>
			if dachzeile:									# fehlt komplett bei ARD_SENDUNG_VERPASST
				dachzeile = dachzeile.group(1)
			else:
				dachzeile = ''
			headline = stringextract('<h4 class=\"headline\">', '</h4>', s)
			if headline == '':
				continue
		
			#if headline.find('- Hörfassung') >= 0:			# nicht unterdrücken - keine reine Hörfassung gesehen 
			#	continue
			if headline.find('Diese Seite benötigt') >= 0:	# Vorspann - irrelevant
				continue
			headline = headline .decode('utf-8')			# tagline-Attribute verlangt Unicode
			hupper = headline.upper()
			if hupper.find(str.upper('Livestream')) >= 0:			# Livestream hier unterdrücken (mehrfach in Rubriken)
				continue
			if s.find('subtitle') >= 0:	# nicht in ARDThemen
				subtitel = re.search("<p class=\"subtitle\">(.*?)</p>\s+?", s)	# Bsp. <p class="subtitle">25 Min.</p>
				subtitel = subtitel.group(1)
				subtitel = subtitel.replace('<br>', ' | ')				
			else:
				subtitel =""
								
			Log(headline)
			send_duration = subtitel						
			send_date = stringextract('class=\"date\">', '</span>', s) # auch Uhrzeit möglich
			Log(subtitel)
			Log(send_date)
			if send_date and subtitel:
				subtitel = send_date + ' Uhr | ' + subtitel				
				
			if send_duration.find('Min.') >= 0:			# Bsp. 20 Min. | UT
				send_duration = send_duration.split('Min.')[0]
				duration = send_duration.split('Min.')[0]
				#Log(duration)
				if duration.find('|') >= 0:			# Bsp. 17.03.2016 | 29 Min. | UT 
						duration = duration.split('|')[1]
				#Log(duration)
				millsec_duration = CalculateDuration(duration)
			else:
				millsec_duration = ''
			
			sid = ''
			if ID == 'PODCAST' and s.find('class=\"textWrapper\"') >= 0:	# PODCAST: textWrapper erst im 2. Durchlauf (Einzelseite)
				extr_path = stringextract('class=\"textWrapper\"', '</div>', s)
				id_path = stringextract('href=\"', '\"', extr_path)
			else:
				extr_path = stringextract('class=\"media mediaA\"', '/noscript', s)
				# Log(extr_path)
				id_path = stringextract('href=\"', '\"', extr_path)
			id_path = unescape(id_path)
			if id_path.find('documentId=') >= 0:		# documentId am Pfadende
				sid = id_path.split('documentId=')[1]	# ../Video-Podcast?bcastId=7262908&documentId=24666340
				
			Log('sid: ' + sid)
			path = id_path	# korrigiert in SinglePage für Einzelsendungen in  '/play/media/' + sid
			Log(path)
							
			if s.find('urlScheme') >= 0:			# Bild ermitteln, versteckt im img-Knoten
				text = stringextract('urlScheme', '/noscript', s)
				img_src, img_alt = img_urlScheme(text, 320, ID)
			else:
				img_src=''; img_alt=''	
			if ID == 'PODCAST' and img_src == '':		# PODCAST: Inhalte aus Episodenkopf verwenden
				if img_src_header and img_alt_header:
					img_src=img_src_header; img_alt=img_alt_header
				if teasertext_header:
					teasertext = teasertext_header
							
			if path == '':								# Satz nicht verwendbar
					continue							
						
			Log('neuer Satz')
			Log(sid); Log(id_path); Log(path); Log(img_src); Log(img_alt); Log(headline);  
			Log(subtitel); Log(send_duration); Log(millsec_duration); 
			Log(dachzeile); Log(teasertext); 

			send_path.append(path)			# erst die Listen füllen
			send_headline.append(headline)
			send_subtitel.append(subtitel)
			send_img_src.append(img_src)
			send_img_alt.append(img_alt)
			send_millsec_duration.append(millsec_duration)
			send_dachzeile.append(dachzeile)		
			send_sid.append(sid)	
			send_teasertext.append(teasertext)	
			
											# dann der komplette Listen-Satz ins Array		
	send_arr = [send_path, send_headline, send_subtitel, send_img_src, send_img_alt, send_millsec_duration, 
		send_dachzeile, send_sid, send_teasertext]
	Log(len(send_path))	 # Anzahl send_path = Anzahl Sätze		
	return send_arr
#-------------------
# def img_urlScheme: img-Url ermitteln für get_sendungen, ARDRubriken. text = string, dim = Dimension
def img_urlScheme(text, dim, ID):
	Log('img_urlScheme: ' + text[0:60])
	Log(dim)
	
	pos = 	text.find('class=\"mediaCon\">')			# img erst danach
	if pos >= 0:
		text = text[pos:]
		img_src = stringextract("urlScheme':'", '##width', text)
	else:
		img_src = stringextract(':&#039;', '##width', text)
		
	img_alt = stringextract('title=\"', '\"', text)
	if img_alt == '':
		img_alt = stringextract('alt=\"', '\"', text)
	img_alt = img_alt.replace('- Standbild', '')
	img_alt = 'Bild: ' + img_alt
	
		
	if img_src and img_alt:
		if img_src.startswith('http') == False:			# Base ergänzen, auch https möglich
			img_src = BASE_URL + img_src 
		img_src = img_src + str(dim)					# dim getestet: 160,265,320,640
		if ID == 'PODCAST':								# Format Quadrat klappt nur bei PODCAST,
			img_src = img_src.replace('16x9', '16x16')	# Sender liefert Ersatz, falls n.v.
		if '?mandant=ard' in text:						# Anhang bei manchen Bildern
			img_src =img_src + '?mandant=ard' 
		Log('img_urlScheme: ' + img_src)
		img_alt = img_alt.decode(encoding="utf-8", errors="ignore")	 # kommt vor:  utf8-decode-error bate 0xc3
		Log('img_urlScheme: ' + img_alt[0:40])
		return img_src, img_alt
	else:
		Log('img_urlScheme: leer')
		return '', ''		
	
####################################################################################################
@route(PREFIX + '/SenderLiveListePre')	# LiveListe Vorauswahl - verwendet lokale Playlist
def SenderLiveListePre(title, offset=0):	# Vorauswahl: Überregional, Regional, Privat
	Log.Debug('SenderLiveListePre')
	playlist = Resource.Load(PLAYLIST)	# lokale XML-Datei (Pluginverz./Resources)
	#Log(playlist)		# nur bei Bedarf

	oc = ObjectContainer(view_group="InfoList", title1='TV-Livestreams', title2=title, art = ICON)	
	oc = home(cont=oc, ID=NAME)				# Home-Button	
		
	doc = HTML.ElementFromString(playlist)		# unterschlägt </link>	
	liste = doc.xpath('//channels/channel')
	Log(len(liste))
	
	for element in liste:
		element_str = HTML.StringFromElement(element)
		name = stringextract('<name>', '</name>', element_str)
		name = name.decode(encoding="utf-8", errors="ignore")	
		img = stringextract('<thumbnail>', '</thumbnail>', element_str) # channel-thumbnail in playlist
		if img.find('://') == -1:	# Logo lokal? -> wird aus Resources geladen, Unterverz. leider n.m.
			img = R(img)
		else:
			img = img
		Log(name); Log(img); # Log(element_str);  # nur bei Bedarf	
		oc.add(DirectoryObject(key=Callback(SenderLiveListe, title=name, listname=name),
			title='Live-Sender: ' + name, thumb=img, tagline=''))

	title = 'EPG Alle JETZT'; summary='elektronischer Programmführer'.decode(encoding="utf-8", errors="ignore")
	oc.add(DirectoryObject(key=Callback(EPG_ShowAll, title=title),  				# EPG-Button All anhängen
			title=title, thumb=R('tv-EPG-all.png'), summary=summary, tagline='aktuelle Sendungen aller Sender'))
							
	title = 'EPG Sender einzeln'; summary='elektronischer Programmführer'.decode(encoding="utf-8", errors="ignore")
	tagline = 'Sendungen für ausgewählten Sender'.decode(encoding="utf-8", errors="ignore")
	oc.add(DirectoryObject(key=Callback(EPG_Sender, title=title),  					# EPG-Button Einzeln anhängen
			title=title, thumb=R('tv-EPG-single.png'), summary=summary, tagline=tagline))
	
	if Prefs['pref_LiveRecord']:		
		title = 'Recording TV-Live'													# TVLiveRecord-Button anhängen
		duration = Prefs['pref_LiveRecord_duration']
		duration, laenge = duration.split('/')
		tagline = Prefs['pref_curl_download_path'] 				
		oc.add(DirectoryObject(key=Callback(TVLiveRecordSender, title=title),  		
				title=title, thumb=R('icon-record.png'), summary=laenge, tagline=tagline))
	return oc
	
#-----------------------------------------------------------------------------------------------------
@route(PREFIX + '/EPG_Sender')		# EPG SenderListe , EPG-Daten holen in Modul EPG.py, Anzeige in EPG_Show
def EPG_Sender(title):
	Log('EPG_Sender')
	
	oc = ObjectContainer(view_group="InfoList", title1='EPG', title2='EPG Auswahl', art = ICON)	
	oc = home(cont=oc, ID=NAME)				# Home-Button	
	
	sort_playlist = get_sort_playlist()	
	# Log(sort_playlist)
	
	for rec in sort_playlist:
		title = rec[0].decode(encoding="utf-8", errors="ignore")
		link = rec[3]
		ID = rec[1]
		if ID == '':				# ohne EPG_ID
			title = title + ': ohne EPG' 
			summ = 'weiter zum Livestream'
			oc.add(DirectoryObject(key=Callback(SenderLiveResolution, path=link, title=title, thumb=R(rec[2])),
				title=title, summary='',  tagline='', thumb=R(rec[2])))
		else:
			summ = 'EPG verfügbar'.decode(encoding="utf-8", errors="ignore")
			oc.add(DirectoryObject(key=Callback(EPG_ShowSingle, ID=ID, name=title, stream_url=link, pagenr=0),
				title=title, thumb=R(rec[2]), summary=summ, tagline=''))		

	return oc
#-----------------------------
@route(PREFIX + '/TVLiveRecordSender')	
#	Liste aller TV-Sender wie EPG_Sender, hier mit Aufnahme-Button
def TVLiveRecordSender(title):
	Log('TVLiveRecordSender')
	Log(Prefs['pref_LiveRecord_ffmpegCall'])
	# Log('PID-Liste: %s' % Dict['PID'])		# PID-Liste, Initialisierung in Main
			
	oc = ObjectContainer(view_group="InfoList", title1='Recording TV-Live', title2='Sender Auswahl', art = ICON)	
	oc = home(cont=oc, ID=NAME)				# Home-Button	
	
	duration = Prefs['pref_LiveRecord_duration']
	duration, laenge = duration.split('/')
	duration = duration.strip()

	sort_playlist = get_sort_playlist()		# Senderliste
	Log('Sender: ' + str(len(sort_playlist)))
	for rec in sort_playlist:
		title 	= rec[0].decode(encoding="utf-8", errors="ignore")
		link 	= rec[3]
		title1 	= title + ': Aufnahme starten' 
		summ 	= 'Aufnahmedauer: %s' 	% laenge
		tag		= 'Zielverzeichnis: %s' % Prefs['pref_curl_download_path']
		oc.add(DirectoryObject(key=Callback(LiveRecord, url=link, title=title, duration=duration,
			laenge=laenge), title=title1, summary=summ,  tagline=tag, thumb=R(rec[2])))
	
	return oc

#-----------------------------
@route(PREFIX + '/LiveRecord')	
# 30.08.2018 Start Recording TV-Live
#	Problem: autom. Wiedereintritt hier + erneuter Popen-call nach Rückkehr zu TVLiveRecordSender 
#		(Ergebnis-Button nach subprocess.Popen, bei PHT vor Ausführung des Buttons)
#		OS-übergreifender Abgleich der pid problematisch - siehe
#		https://stackoverflow.com/questions/4084322/killing-a-process-created-with-pythons-subprocess-popen
#		Der Wiedereintritt tritt sowohl unter Linux als auch Windows auf.
#		Ursach n.b. - tritt in DownloadExtern mit curl/wget nicht auf.
#	1. Lösung: Verwendung des psutil-Moduls (../Contents/Libraries/Shared/psutil ca. 400 KB)
#		und pid-Abgleich Dict['PID'] gegen psutil.pid_exists(pid) - s.u.
#		verworfen - Modul lässt sich unter Windows nicht laden. Linux OK
#	2. Lösung: Dict['PIDffmpeg'] wird nach subprocess.Popen belegt. Beim ungewollten Wiedereintritt
#		wird nach TVLiveRecordSender (Senderliste) zurück gesprungen und Dict['PIDffmpeg'] geleert.
#		Beim nächsten manuellen Aufruf wird LiveRecord wieder frei gegeben ("Türsteherfunktion").
#
#	PHT-Problem: wie in TuneIn2017 (streamripper-Aufruf) sprint PHT bereits vor dem Ergebnis-Buttons (DirectoryObject)
#		in LiveRecord zurück.
#		Lösung: Ersatz des Ergebnis-Buttons durch return ObjectContainer. PHT steigt allerdings danach mit 
#			"GetDirectory failed" aus (keine Abhilfe bisher). Der ungewollte Wiedereintritt findet trotzdem
#			statt.
#
#	Siehe auch verwandtes Problem in TuneIn2017 mit https://forums.plex.tv/t/calling-an-external-program/126055/2?u=rols1 für streamripper:
#		https://forums.plex.tv/t/pht-problem-wrong-jump-after-after-os-functions-in-combination-with-writing-to-dict/212656
#		Nach den Tests in diesem Plugin scheint die Ursache aber nicht im Dict-Gebrauch zu liegen. Vermutung: Framework-
#			Problem im Umgang mit subprocess.Popen (Thread-Konflikt?).
#
def LiveRecord(url, title, duration, laenge):
	Log('LiveRecord')
	Log(url); Log(title); 
	Log('duration: %s, laenge: %s' % (duration, laenge))
		
	if Dict['PIDffmpeg']:								# ungewollten Wiedereintritt abweisen 
		Log('PIDffmpeg: %s' % Dict['PIDffmpeg'])
		Log('PIDffmpeg = %s | Blocking LiveRecord' % Dict['PIDffmpeg'])
		Dict['PIDffmpeg'] = ''							# löschen für manuellen Aufruf 
		# Für PHT Info erst hier nach autom. Wiedereintritt nach Popen möglich:
		title1 = 'Aufnahme gestartet: %s' % title
		title1 	= title1.decode(encoding="utf-8")		
		if 'Home Theater' in str(Client.Platform):	# GetDirectory failed nach Info
			return ObjectContainer(header='Info', message=title1)
		return TVLiveRecordSender(title)

	title2 = 'Recording TV-Live: ' + title
	oc = ObjectContainer(view_group="InfoList", title1='Sender Auswahl', title2=title2, art = ICON)
	oc = home(cont=oc, ID=NAME)				# Home-Button
	
	if Prefs['pref_curl_download_path'] == None or Prefs['pref_curl_download_path'].strip() == '':
		title1 	= 'Downloadverzeichnis fehlt in Einstellungen'
		summ	= 'zur Sender Auswahl'
		oc.add(DirectoryObject(key=Callback(TVLiveRecordSender, title=title),  		
				title=title1, thumb=R('icon-error.png'), summary=summ))
		return oc
		
	dest_path = Prefs['pref_curl_download_path']  	# Downloadverzeichnis fuer curl/wget verwenden
	now = datetime.datetime.now()
	mydate = now.strftime("%Y-%m-%d_%H-%M-%S")		# Zeitstempel
	dfname = make_filenames(title)					# Dateiname aus Sendername generieren
	dfname = "%s_%s.mp4" % (dfname, mydate) 	
	dest_file = os.path.join(dest_path, dfname)
	if url.startswith('http') == False:				# Pfad bilden für lokale m3u8-Datei
		if url.startswith('rtmp') == False:
			url 	= os.path.join(Dict['R'], url)	# rtmp-Url's nicht lokal
			url 	= '"%s"' % url						# Pfad enthält Leerz. - für ffmpeg in "" kleiden						
	
	cmd = Prefs['pref_LiveRecord_ffmpegCall']	% (url, duration, dest_file)
	Log(cmd); 
	
	Log('Client-Platform: ' + str(Client.Platform))
	Log(sys.platform)
	if sys.platform == 'win32':							
		args = cmd
	else:
		args = shlex.split(cmd)							

	try:
		Dict['PIDffmpeg'] = ''
		sp = subprocess.Popen(args, shell=False)
		Log('sp: ' + str(sp))

		if str(sp).find('object at') > 0:  			# subprocess.Popen object OK
			Dict['PIDffmpeg'] = sp.pid				# PID zum Abgleich gegen Wiederholung sichern
			Log('PIDffmpeg neu: %s' % Dict['PIDffmpeg'])
			title1 = 'Aufnahme gestartet: %s' % dfname
			summ	= 'zur Sender Auswahl'
			Log(title1)
			# PHT springt hier zurück an den Funktionskopf - Info dort
			#if 'Home Theater' in str(Client.Platform):	# GetDirectory failed nach Info
			#	return ObjectContainer(header='Info', message=title1)
			oc.add(DirectoryObject(key=Callback(TVLiveRecordSender, title=title),  		
					title=title1, thumb=R('icon-ok.png'), summary=summ))				
			return oc
	
	except Exception as exception:
		msg = str(exception)
		Log(msg)		
		title1 = "Fehler: %s" % msg
		title1 = title1.decode(encoding="utf-8")
		summ	= 'zur Sender Auswahl'
		tagline='Aufnahme fehlgeschlagen'
		# bei Fehlschlag gibt PHT die message aus (im Gegensatz zu oben):
		if 'Home Theater' in str(Client.Platform):	# GetDirectory failed nach Info
			return ObjectContainer(header='Fehler', message=title1)
		oc.add(DirectoryObject(key=Callback(TVLiveRecordSender, title=title),  		
				title=title1, thumb=R('icon-error.png'), summary=summ, tagline=tagline))
		
	
	return oc
#-----------------------------
def get_sort_playlist():								# sortierte Playliste der TV-Livesender
	Log('get_sort_playlist')
	playlist = Resource.Load(PLAYLIST)					# lokale XML-Datei (Pluginverz./Resources)
	stringextract('<channel>', '</channel>', playlist)	# ohne Header
	playlist = blockextract('<item>', playlist)
	sort_playlist =  []
	for item in playlist:   
		rec = []
		title = stringextract('<title>', '</title>', item)
		title = title.upper()										# lower-/upper-case für sort() relevant
		EPG_ID = stringextract('<EPG_ID>', '</EPG_ID>', item)
		img = 	stringextract('<thumbnail>', '</thumbnail>', item)
		link =  stringextract('<link>', '</link>', item)			# url für Livestreaming
		rec.append(title); rec.append(EPG_ID);						# Listen-Element
		rec.append(img); rec.append(link);
		sort_playlist.append(rec)									# Liste Gesamt
	
	# Zeilen-Index: title=rec[0]; EPG_ID=rec[1]; img=rec[2]; link=rec[3];	
	sort_playlist.sort()	
	return sort_playlist
	
#-----------------------------------------------------------------------------------------------------
@route(PREFIX + '/EPG_ShowSingle')		# EPG: Daten holen in Modul EPG.py, Anzeige hier, Klick zum Livestream
def EPG_ShowSingle(ID, name, stream_url, pagenr=0):
	Log('EPG_ShowSingle'); Log(name)
	
	# Indices EPG_rec: 0=starttime, 1=href, 2=img, 3=sname, 4=stime, 5=summ, 6=vonbis, 7=today_human: 
	# Link zur Einzelanzeige href=rec[1] hier nicht verwendet - wenig zusätzl. Infos
	EPG_rec = EPG.EPG(ID=ID, day_offset=pagenr)		# Daten holen
	
	if len(EPG_rec) == 0:			# kann vorkommen, Bsp. SR
		msg='Sender ' + name + ': keine EPG-Daten gefunden'
		msg = msg.decode(encoding="utf-8", errors="ignore")
		return ObjectContainer(header='Error', message=msg)
		
	today_human = 'ab ' + EPG_rec[0][7]
			
	# Log(EPG_rec[0]) # bei Bedarf
	name = name.decode(encoding="utf-8", errors="ignore") 
	oc = ObjectContainer(view_group="InfoList", title1=name, title2=today_human, art = ICON)	
	oc = home(cont=oc, ID=NAME)				# Home-Button	
	
	for rec in EPG_rec:
		href=rec[1]; img=rec[2]; sname=rec[3]; stime=rec[4]; summ=rec[5]; vonbis=rec[6];
		# Log(img)
		if img.find('http') == -1:	# Werbebilder today.de hier ohne http://, Ersatzbild einfügen
			img = R('icon-bild-fehlt.png')
		sname = unescape(sname)
		title=sname.decode(encoding="utf-8", errors="ignore")
		summ = unescape(summ)
		summ = summ.decode(encoding="utf-8", errors="ignore")
		tagline = 'Zeit: ' + vonbis
		tagline = tagline.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(SenderLiveResolution, path=stream_url, title=title, thumb=img),
			title=title, summary=summ,  tagline=tagline, thumb=img))
			
	# Mehr Seiten anzeigen:
	max = 12
	pagenr = int(pagenr) + 1
	if pagenr < max: 
		summ = 'nächster Tag'.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(EPG_ShowSingle, ID=ID, name=name, stream_url=stream_url, pagenr=pagenr),
			title=summ, thumb=R(ICON_MEHR), summary=summ, tagline=''))		
		
	return oc
#-----------------------------------------------------------------------------------------------------
# EPG: aktuelle Sendungen aller Sender mode='allnow'
# Todo: Sammelabruf in EPG-Modul integrieren - der ständige Wechsel in der Schleife hier ist 
#		sehr zeitaufwendig

@route(PREFIX + '/EPG_ShowAll')		
def EPG_ShowAll(title, offset=0):
	Log('EPG_ShowAll')
	title_org = title
	title2='Aktuelle Sendungen'
		
	oc = ObjectContainer(view_group="InfoList", title1='EPG', title2=title2, art = ICON)	
	oc = home(cont=oc, ID=NAME)				# Home-Button	

	# Zeilen-Index: title=rec[0]; EPG_ID=rec[1]; img=rec[2]; link=rec[3];	
	sort_playlist = get_sort_playlist()	
	Log(len(sort_playlist))
	
	rec_per_page = 10								# Anzahl pro Seite (Timeout ab 15 beobachtet)
	max_len = len(sort_playlist)					# Anzahl Sätze gesamt
	start_cnt = int(offset) 						# Startzahl diese Seite
	end_cnt = int(start_cnt) + int(rec_per_page)	# Endzahl diese Seite
	
	for i in range(len(sort_playlist)):
		cnt = int(i) + int(offset)
		# Log(cnt); Log(i)
		if int(cnt) >= max_len:				# Gesamtzahl überschritten?
			break
		if i >= rec_per_page:				# Anzahl pro Seite überschritten?
			break
		rec = sort_playlist[cnt]

		title_playlist = rec[0].decode(encoding="utf-8", errors="ignore")
		m3u8link = rec[3]
		img_playlist = R(rec[2])
		ID = rec[1]
		if ID == '':									# ohne EPG_ID
			title = title_playlist + ': ohne EPG'
			summ = 'weiter zum Livestream'
			tagline = ''
			img = img_playlist
		else:
			# Indices EPG_rec: 0=starttime, 1=href, 2=img, 3=sname, 4=stime, 5=summ, 6=vonbis: 
			rec = EPG.EPG(ID=ID, mode='OnlyNow')		# Daten holen - nur aktuelle Sendung
			# Log(rec)	# bei Bedarf
			if len(rec) == 0:							# Satz leer?
				title = title_playlist + ': ohne EPG'
				summ = 'weiter zum Livestream'
				tagline = ''
				img = img_playlist			
			else:	
				href=rec[1]; img=rec[2]; sname=rec[3]; stime=rec[4]; summ=rec[5]; vonbis=rec[6]
				if img.find('http') == -1:	# Werbebilder today.de hier ohne http://, Ersatzbild einfügen
					img = R('icon-bild-fehlt.png')
				sname = sname.replace('JETZT', title_playlist)			# JETZT durch Sender ersetzen
				Log(sname)
				title=sname.decode(encoding="utf-8", errors="ignore")
				summ = summ.decode(encoding="utf-8", errors="ignore")
				tagline = 'Zeit: ' + vonbis
				
		title = unescape(title)				
		tagline = tagline.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(SenderLiveResolution, path=m3u8link, title=title, thumb=img),
			title=title, summary=summ,  tagline=tagline, thumb=img))	

	# Mehr Seiten anzeigen:
	# Log(offset); Log(cnt); Log(max_len);
	if (int(cnt) +1) < int(max_len): 						# Gesamtzahl noch nicht ereicht?
		new_offset = cnt 
		Log(new_offset)
		summ = 'Mehr (insgesamt ' + str(max_len) + ') ' + title2
		summ = summ.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(EPG_ShowAll, title=title_org, offset=new_offset), 
			title=title_org, tagline=title2, summary=summ,  thumb=R(ICON_MEHR)))	
		
	return oc
#-----------------------------------------------------------------------------------------------------
@route(PREFIX + '/SenderLiveListe')	# LiveListe - verwendet lokale Playlist
def SenderLiveListe(title, listname, offset=0):	# 

	# SenderLiveListe -> SenderLiveResolution (reicht nur durch) -> Parseplaylist (Ausw. m3u8)
	#	-> CreateVideoStreamObject 
	Log.Debug('SenderLiveListe')
			
	title2 = 'Live-Sender ' + title
	title2 = title2.decode(encoding="utf-8", errors="ignore")	
	oc = ObjectContainer(view_group="InfoList", title1='Live-Sender', title2=title2, art = ICON)
	oc = home(cont=oc, ID=NAME)				# Home-Button
			
	
	# Besonderheit: die Senderliste wird lokal geladen (s.o.). Über den link wird die URL zur  
	#	*.m3u8 geholt. Nach Anwahl eines Live-Senders erfolgt in SenderLiveResolution die Listung
	#	der Auflösungsstufen.
	#
	playlist = Resource.Load(PLAYLIST)					# lokale XML-Datei (Pluginverz./Resources)
	playlist = blockextract('<channel>', playlist)
	Log(len(playlist)); Log(listname)
	for i in range(len(playlist)):						# gewählte Channel extrahieren
		item = playlist[i] 
		name =  stringextract('<name>', '</name>', item)
		Log(name)
		if name == listname:							# Bsp. Überregional, Regional, Privat
			mylist =  playlist[i] 
			break
	
	liste = blockextract('<item>', mylist)
	Log(len(liste));
	EPG_ID_old = ''											# Doppler-Erkennung
	sname_old=''; stime_old=''; summ_old=''; vonbis_old=''	# dto.
	summary_old=''; tagline_old=''
	for element in liste:							# EPG-Daten für einzelnen Sender holen 	
		link = stringextract('<link>', '</link>', element) 	# HTML.StringFromElement unterschlägt </link>
		link = unescape(link)						# amp; entfernen! Herkunft: HTML.ElementFromString bei &-Zeichen
		Log(link);
		
		# Bei link zu lokaler m3u8-Datei (Resources) reagieren SenderLiveResolution und ParsePlayList entsprechend:
		#	der erste Eintrag (automatisch) entfällt, da für die lokale Ressource kein HTTP-Request durchge-
		#	führt werden kann. In ParsePlayList werden die enthaltenen Einträge wie üblich aufbereitet
		#	
		# Spezialbehandlung für N24 in SenderLiveResolution - Test auf Verfügbarkeit der Lastserver (1-4)
		# EPG: ab 10.03.2017 einheitlich über Modul EPG.py (vorher direkt bei den Sendern, mehrere Schemata)
									
		title = stringextract('<title>', '</title>', element)
		epg_schema=''; epg_url=''
		epg_date=''; epg_title=''; epg_text=''; summary=''; tagline='' 
		# Log(Prefs['pref_use_epg']) 					# Voreinstellung: EPG nutzen? - nur mit Schema nutzbar 
		if Prefs['pref_use_epg'] == True:
			# Indices EPG_rec: 0=starttime, 1=href, 2=img, 3=sname, 4=stime, 5=summ, 6=vonbis:
			EPG_ID = stringextract('<EPG_ID>', '</EPG_ID>', element)
			Log(EPG_ID); Log(EPG_ID_old);
			if  EPG_ID == EPG_ID_old:					# Doppler: EPG vom Vorgänger verwenden
				sname=sname_old; stime=stime_old; summ=summ_old; vonbis=vonbis_old
				summary=summary_old; tagline=tagline_old
				Log('EPG_ID=EPG_ID_old')
			else:
				EPG_ID_old = EPG_ID
				try:
					rec = EPG.EPG(ID=EPG_ID, mode='OnlyNow')	# Daten holen - nur aktuelle Sendung
					if rec == '':								# Fehler, ev. Sender EPG_ID nicht bekannt
						sname=''; stime=''; summ=''; vonbis=''
					else:
						sname=rec[3]; stime=rec[4]; summ=rec[5]; vonbis=rec[6]	
				except:
					sname=''; stime=''; summ=''; vonbis=''						
				if sname:
					title = title + ': ' + sname
				if summ:
					summary = summ
				else:
					summary = ''
				if vonbis:
					tagline = 'Sendung: %s Uhr' % vonbis
				else:
					tagline = ''
				# Doppler-Erkennung:	
				sname_old=sname; stime_old=stime; summ_old=summ; vonbis_old=vonbis;
				summary_old=summary; tagline_old=tagline
		title = unescape(title)	
		title = title.replace('JETZT:', '')					# 'JETZT:' hier überflüssig
		title = title.decode(encoding="utf-8", errors="ignore")	
		summary = unescape(summary)	
		summary = summary.decode(encoding="utf-8", errors="ignore")			
		tagline = tagline.decode(encoding="utf-8", errors="ignore")	
						
		img = stringextract('<thumbnail>', '</thumbnail>', element) 
		if img.find('://') == -1:	# Logo lokal? -> wird aus Resources geladen, Unterverz. leider n.m.
			img = R(img)
			
		geo = stringextract('<geoblock>', '</geoblock>', element)
		Log(geo)
		if geo:
			tagline = 'Livestream nur in Deutschland zu empfangen! %s'	% tagline
			
		Log(link); Log(img); Log(summary); Log(tagline[0:80]);
		Resolution = ""; Codecs = ""; duration = ""
	
		# if link.find('rtmp') == 0:				# rtmp-Streaming s. CreateVideoStreamObject
		# Link zu master.m3u8 erst auf Folgeseite? - SenderLiveResolution reicht an  Parseplaylist durch  
		oc.add(DirectoryObject(key=Callback(SenderLiveResolution, path=link, title=title, thumb=img),
			title=title, summary=summary,  tagline=tagline, thumb=img))
	Log(len(oc))
	return oc
		
#-----------------------------------------------------------------------------------------------------
#	17.02.2018 Video-Sofort-Format wieder entfernt (V3.1.6 - V3.5.0)
#		Forum:  https://forums.plex.tv/discussion/comment/1606010/#Comment_1606010
#		Funktionen: remoteVideo, Parseplaylist, SenderLiveListe, TestOpenPort
#-----------------------------------------------------------------------------------------------------
			
###################################################################################################
@route(PREFIX + '/SenderLiveResolution')	# Auswahl der Auflösungstufen des Livesenders
	#	Die URL der gewählten Auflösung führt zu weiterer m3u8-Datei (*.m3u8), die Links zu den 
	#	Videosegmenten (.ts-Files enthält). Diese  verarbeitet der Plexserver im Videoobject. 
	#	10.08.2017: Video-Sofort-Format beschränkt die Auswahl auf 1 Element (der autom. Start funktioniert
	#		aber nicht im Webplayer)
	#	17.02.2018 Video-Sofort-Format wieder entfernt
def SenderLiveResolution(path, title, thumb, include_container=False):
	#page = HTML.ElementFromURL(path)
	url_m3u8 = path
	Log(title); Log(url_m3u8);

	title = title.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(view_group="InfoList", title1=title + ' Live', art=ICON)
	oc = home(cont=oc, ID=NAME)					# Home-Button
	
	Codecs = 'H.264'	# dummy-Vorgabe für PHT (darf nicht leer sein)	
										
	# Spezialbehandlung für N24 - Test auf Verfügbarkeit der Lastserver (1-4),
	#	  m3u8-Datei für Parseplaylist inkompatibel, nur 1 Videoobjekt
	if title.find('N24') >= 0:
		url_m3u8 = N24LastServer(url_m3u8)
		oc.add(CreateVideoStreamObject(url=url_m3u8, title=title, 		
			summary='Bandbreite unbekannt', tagline=title, meta=Codecs, thumb=thumb, 	
			rtmp_live='nein', resolution='unbekannt'))								
		return oc
		
	if url_m3u8.find('rtmp') == 0:		# rtmp, nur 1 Videoobjekt
		oc.add(CreateVideoStreamObject(url=url_m3u8, title=title, 
			summary='rtmp-Stream', tagline=title, meta=Codecs, thumb=thumb, 
			rtmp_live='ja', resolution='unbekannt'))
		return oc
		
	# alle übrigen (i.d.R. http-Links), Videoobjekte für einzelne Auflösungen erzeugen
	if url_m3u8.find('.m3u8') >= 0:				# häufigstes Format
		Log(url_m3u8)
		if url_m3u8.find('http') == 0:			# URL (auch https) oder lokale Datei? (lokal entfällt Eintrag "autom.")			
			oc.add(CreateVideoStreamObject(url=url_m3u8, title=title + ' | Bandbreite und Auflösung automatisch', 
				summary='automatische Auflösung | Auswahl durch den Player', tagline=title,
				meta=Codecs, thumb=thumb, rtmp_live='nein', resolution=''))
				
		# Auswertung *.m3u8-Datei  (lokal oder extern), Auffüllung Container mit Auflösungen. geoblock bei 
		# TV-Live nicht verwendet:	
		oc = Parseplaylist(oc, url_m3u8, thumb, geoblock='')	# (-> CreateVideoStreamObject pro Auflösungstufe)
		return oc							
	else:	# keine oder unbekannte Extension - Format unbekannt
		return ObjectContainer(header='SenderLiveResolution: ', message='unbekanntes Format in ' + url_m3u8)

#-----------------------------
# Spezialbehandlung für N24 - Test auf Verfügbarkeit der Lastserver (1-4): wir prüfen
# 	die Lastservers durch, bis einer Daten liefert
def N24LastServer(url_m3u8):	
	Log('N24LastServer: ' + url_m3u8)
	url = url_m3u8
	
	pos = url.find('index_')	# Bsp. index_1_av-p.m3u8
	nr_org = url[pos+6:pos+7]
	Log(nr_org) 
	for nr in [1,2,3,4]:
		# Log(nr)
		url_list = list(url)
		url_list[pos+6:pos+7] = str(nr)
		url_new = "".join(url_list)
		# Log(url_new)
		try:
			# playlist = HTTP.Request(url).content   # wird abgewiesen
			req = urllib2.Request(url_new)
			r = urllib2.urlopen(req)
			playlist = r.read()			
		except:
			playlist = ''
			
		Log(playlist[:20])
		if 	playlist:	# playlist gefunden - diese url verwenden
			return url_new	
	
	return url_m3u8		# keine playlist gefunden, weiter mit Original-url
				
####################################################################################################
@route(PREFIX + '/CreateVideoStreamObject')	# <- SenderLiveListe, SingleSendung (nur m3u8-Dateien)
											# **kwargs - s. CreateVideoClipObject
def CreateVideoStreamObject(url, title, summary, tagline, meta, thumb, rtmp_live, resolution, include_container=False, **kwargs):
  # Zum Problem HTTP Live Streaming (HLS): Redirecting des Video-Callbacks in einen HTTPLiveStreamURL
  # s.https://forums.plex.tv/index.php/topic/40532-bug-http-live-streaming-doesnt-work-when-redirected/
  # s.a. https://forums.plex.tv/discussion/88056/httplivestreamurl
  # HTTPLiveStreamURL takes the url for an m3u8 playlist as the key argument
  # Ablauf: videoclip_obj -> MediaObject -> PlayVideo
  # HTTPLiveStreamURL: für m3u8-Links, Metadaten (container, codec,..) werden nicht gesetzt
  # ab 03.04.2016: ohne Redirect - die vorh. Infos reichen bei der Mediathek, auch bei den Live-Sendern
  #		Redirect wurde von manchen Playern kommentarlos verweigert bzw. führte zum Crash (Logfiles Otto Kerner)  
  
  # Einstellung im Plex-Web-Client: Direkte Wiedergabe, Direct Stream (Experimenteller Player auf Wunsch)
  #		andernfalls Fehler: HTTP Error 503: Service Unavailable
  #		Aber: keine Auswirkung auf andere Player im Netz
  
  #	resolution = [720, 540, 480] # Parameter bei HTTPLivestream nicht akzeptiert +  auch nicht nötig
  #				bisherige Erfahrung: Clients skalieren besser selbst. Anders bei rtmp!
  # rtmp_live: Steuerung via False/True nicht möglich. Bei zweiten Durchlauf gehen Bool-Parameter verloren
  #				DAF (auch anderes Streams?) benötigt mindestens 1 resolution-Parameter - sonst Fehler.
  #				resolution ohne Auswirkung auf Player-Einstellungen
  #				Die CRITICAL Meldung CreateVideoStreamObject() takes at least 7 arguments (7 given) führt
  #				nicht zum Abbruch des Streams.
  # 
  # 01.03.2017: kein DirectPlay mehr mit neuen Web-Player-Versionen. Lokaler Workaround: Austausch WebClient.bundle gegen
  #			WebClient.bundle aus PMS-Version 1.0.0. Siehe auch Post sander1:
  #			https://forums.plex.tv/discussion/260454/no-directplay-with-httplivestreamurl-in-the-latest-web-players
  # 		Bei Web-Player-Meldung ohne Plugin-Änderung 'dieses medium unterstützt kein streaming' Browser neu starten
  #			(offensichtlich Problem mit dem Javascriptcode)
  
	url = url.replace('%40', '@')	# Url kann Zeichen @ enthalten
	Log('CreateVideoStreamObject: '); Log(url); Log(rtmp_live) 
	Log('include_container: '); Log(include_container)
	Log(Client.Platform)
	Log('Plattform: ' + sys.platform)
	Log(Client.Product)

	random.seed()								# 23.08.2017 Zufallswert für eindeutigen rating_key 				
	rating_id = random.randint(1,10000)			# 	(wie CreateTrackObject) - title verursacht Error
	rating_key = 'rating_key-' + str(rating_id) #	im Server-Log
	Log(rating_key)

	if url.find('rtmp:') >= 0:	# rtmp = Protokoll für flash, Quellen: rtmpdump, shark, Chrome/Entw.-Tools
		if rtmp_live == 'ja':
			Log('rtmp_live: '); Log(rtmp_live) 
			mo = MediaObject(parts=[PartObject(key=RTMPVideoURL(url=url,live=True))]) # live=True nur Streaming
			
			videoclip_obj = VideoClipObject(
				key = Callback(CreateVideoStreamObject, url=url, title=title, summary=summary, tagline=tagline,
				meta=meta, thumb=thumb, rtmp_live='ja', resolution=[720, 540, 480], include_container=True), 
				rating_key=rating_key,
				title=title,
				summary=summary,
				tagline=tagline,
				thumb=thumb,)  
		else:
			mo = MediaObject(parts=[PartObject(key=RTMPVideoURL(url=url))])
			
			videoclip_obj = VideoClipObject(
				key = Callback(CreateVideoStreamObject, url=url, title=title, summary=summary,  tagline=tagline,
				meta=meta, thumb=thumb, rtmp_live='nein', resolution='', include_container=True), 
				rating_key=rating_key,
				title=title,
				summary=summary,
				tagline=tagline,
				thumb=thumb,) 			 

	else:
		if url.find('artelive-lh')  >= 0:		# Sonderbehandlung für ARTE - s.a. def Parseplaylist. Plex macht kein bzw. kein
			url = url.replace('https', 'http')	# kompatibles SSL-Handshake. Die Streaming-Links funktionieren mit http.
		
		# Auflösungsstufen - s. SenderLiveResolution -> Parseplaylist
		resolution=[1280, 1024, 960, 720, 540, 480] # wie VideoClipObject: Vorgabe für Webplayer entbehrlich, für PHT erforderlich
		meta=url									# leer (None) im Webplayer OK, mit PHT:  Server: Had trouble breaking meta
		mo = MediaObject(parts=[PartObject(key=HTTPLiveStreamURL(url=url))]) 
				
		videoclip_obj = VideoClipObject(					# Parameter wie MovieObject
			key = Callback(CreateVideoStreamObject, url=url, title=title, summary=summary,  tagline=tagline,
			meta=meta, thumb=thumb, rtmp_live='nein', resolution=resolution, include_container=True), 
			rating_key=rating_key,
			title=title,
			summary=summary,
			tagline=tagline,
			thumb=thumb,)
			
	videoclip_obj.add(mo)

	Log(url); Log(title); Log(summary); Log(tagline);
	Log(resolution); Log(meta); Log(thumb); Log(rating_key); 
	
	if include_container:
		return ObjectContainer(objects=[videoclip_obj])				
	else:
		return videoclip_obj
		
#####################################################################################################
@route(PREFIX + '/CreateVideoClipObject')	# <- SingleSendung Qualitätsstufen
	# Plex-Warnung: Media part has no streams - attempting to synthesize | keine Auswirkung
	# **kwargs erforderlich bei Fehler: CreateVideoClipObject() got an unexpected keyword argument 'checkFiles'
	#	beobachtet bei Firefox (Suse Leap) + Chrome (Windows7)
	#	s.a. https://github.com/sander1/channelpear.bundle/tree/8605fc778a2d46243bb0378b0ab40a205c408da4
def CreateVideoClipObject(url, title, summary, tagline, meta, thumb, duration, resolution, include_container=False, **kwargs):
	Log('CreateVideoClipObject')
	Log(url); Log(duration); Log(tagline); Log(resolution)
	Log(Client.Platform)
	Log('Plattform: ' + sys.platform)
	Log(Client.Product)
	
	# resolution = ''					# leer - Clients skalieren besser selbst
	resolution=[720, 540, 480]			# wie VideoClipObject: Vorgabe für Webplayer entbehrlich, für PHT erforderlich
	tagline = tagline.replace('leer', ' ') # leer = Stammhalter für PHT

	mo = MediaObject(parts=[PartObject(key=Callback(PlayVideo, url=url))],
		container = Container.MP4,  	# weitere Video-Details für Chrome nicht erf., aber Firefox 
		video_codec = VideoCodec.H264,	# benötigt VideoCodec + AudioCodec zur Audiowiedergabe
		audio_codec = AudioCodec.AAC,)	# 
		
	videoclip_obj = VideoClipObject(
		key = Callback(CreateVideoClipObject, url=url, title=title, summary=summary, tagline=tagline,
		meta=meta, thumb=thumb, duration=duration, resolution=resolution, include_container=True),
		# rating_key = url,				# eindeutiger rating_key als url bei ARD-Videos nicht gewährleistet 
		rating_key = title,
		title = title,
		summary = summary,
		tagline = tagline,
		thumb = thumb,)
	
	videoclip_obj.add(mo)	

	if include_container:						# Abfrage anscheinend verzichtbar, schadet aber auch nicht 
		return ObjectContainer(objects=[videoclip_obj])
	else:
		return videoclip_obj
	
#-----------------------------
# PlayVideo: falls HTTPLiveStreamURL hier verarbeitet wird (nicht in diesem Plugin), sollte die Route der
#	Endung (i.d.R. .m3u8) entsprechen. Siehe Post sander1 28.02.2017: 
#	https://forums.plex.tv/discussion/260046/what-is-the-right-way-to-use-httplivestreamurl-without-url-services#latest
#	
# 
@route(PREFIX + '/PlayVideo')  
#def PlayVideo(url, resolution, **kwargs):	# resolution übergeben, falls im  videoclip_obj verwendet
def PlayVideo(url, **kwargs):	
	Log('PlayVideo: ' + url); 		# Log('PlayVideo: ' + resolution)
	return Redirect(url)

####################################################################################################
# path = ARD_RadioAll = http://www.ardmediathek.de/radio/live?genre=Alle+Genres&kanal=Alle
#	Bei Änderungen der Sender Datei livesenderRadio.xml anpassen (Sendernamen, Icons)
@route(PREFIX + '/RadioLiveListe')  
def RadioLiveListe(path, title):
	Log('RadioLiveListe');
	oc = ObjectContainer(view_group="InfoList", title1=title, art=ICON)
	oc = home(cont=oc, ID=NAME)					# Home-Button
	
	#page = HTML.ElementFromURL(path)
	#Log(page)
	playlist = Resource.Load(PLAYLIST_Radio) 
	#Log(playlist)					
	
	doc = HTML.ElementFromString(playlist)		# unterschlägt </link>	
	liste = doc.xpath('//item')					# z.Z. nur 1 Channel (ARD). Bei Bedarf Schleife erweitern
	Log(len(liste))
	
	# Unterschied zur TV-Playlist livesenderTV.xml: Liste  der Radioanstalten mit Links zu den Webseiten.
	#	Ab 11.10.2917: die Liste + Reihenfolge der Sender wird in der jew. Webseite ermittelt. Die Sender-Liste
	#		wird aus LivesenderRadio.xml geladen und gegen die Sendernamen abgeglichen. Die Einträge sind paarweise
	#		angelegt (Sendername:Icon).
	#		Ohne Treffer beim  Abgleich wird ein Ersatz-Icon verwendet (im Watchdog-PRG führt dies zur Fehleranzeige). 
	#		Die frühere Icon-Liste in <thumblist> entfällt.
	#	Nach Auswahl einer Station wird in RadioLiveSender der Audiostream-Link ermittelt und
	#	in CreateTrackObject endverarbeitet.
	#

	for element in liste:
		s = HTML.StringFromElement(element) 		# Ergebnis wie XMML.StringFromElement
		# Log(s)					# bei Bedarf
		title = stringextract('<title>', '</title>', s)
		title = title.decode(encoding="utf-8", errors="ignore")
		link = stringextract('<link>', '<thumbnail>', s) 	# HTML.StringFromElement unterschlägt </link>
		link = link.strip()							# \r + Leerz. am Ende entfernen
		link = repl_char('amp;',link)				# amp; entfernen! Herkunft: HTML.ElementFromString bei &-Zeichen
		img = stringextract('<thumbnail>', '</thumbnail>', s) 
		if img.find('://') == -1:	# Logo lokal? -> wird aus Resources geladen, Unterverz. leider n.m.
			img = R(img)
		else:
			img = img
			
		sender = stringextract('<sender>', '</sender>', s)			# Auswertung sender + thumbs in RadioAnstalten
			
		Log(title); Log(link); Log(img); 												
		oc.add(DirectoryObject(key=Callback(RadioAnstalten, path=link, title=title, sender=sender), 
			title=title, summary='einzelne Sender', tagline='Radio', thumb=img))
	return oc
#-----------------------------
@route(PREFIX + '/RadioAnstalten')  
def RadioAnstalten(path, title,sender):
	Log('RadioAnstalten: ' + path);
	entry_path = path	# sichern
	oc = ObjectContainer(view_group="InfoList",  title1='Radiosender von ' + title, art=ICON)
	Log(Client.Platform)
	client = Client.Platform
	if client == None:
		client = ''
	if client.find ('Plex Home Theater'): 
		oc = home(cont=oc, ID=NAME)							# Home-Button macht bei PHT die Trackliste unbrauchbar 
			
	page, msg = get_page(path=path)				# Absicherung gegen Connect-Probleme
	if page == '':
		return ObjectContainer(header='Error', message=msg)
	entries = blockextract('class=\"teaser\"', page)	
	
	del entries[0:2]								# "Javascript-Fehler" überspringen (2 Elemente)
	Log(len(entries))

	for element in entries:
		pos = element.find('class=\"socialMedia\"')			# begrenzen
		if pos >= 0:
			element = element[0:pos]
		# Log(element[0:80])						#  nur bei Bedarf)	
		
		img_src = ""						
			
		headline = ''; subtitel = ''				# nicht immer beide enthalten
		if element.find('headline') >= 0:			# h4 class="headline" enthält den Sendernamen
			headline = stringextract('\"headline\">', '</h4>', element)
			headline = headline .decode('utf-8')		# tagline-Attribute verlangt Unicode
		if element.find('subtitle') >= 0:	
			subtitel = stringextract('\"subtitle\">', '</p>', element)
		Log(headline); Log(subtitel);				
			
		href = stringextract('<a href=\"', '\"', element)
		sid = href.split('documentId=')[1]
		
		path = BASE_URL + '/play/media/' + sid + '?devicetype=pc&features=flash'	# -> Textdatei mit Streamlink
		Log('Streamlink: ' + path)
		path_content = HTTP.Request(path).content
		Log(path_content[0:80])			# enthält nochmal Bildquelle + Auflistung Streams (_quality)
										# Streamlinks mit .m3u-Ext. führen zu weiterer Textdatei - Auswert. folgt 
		#slink = stringextract('_stream\":\"', '\"}', path_content) 		# nur 1 Streamlink? nicht mehr aktuell
		link_path,link_img, m3u8_master, geoblock = parseLinks_Mp4_Rtmp(path_content)	# mehrere Streamlinks auswerten,
																						# geoblock hier nicht verwendet
		
		if headline:						# Zuordnung zu lokalen Icons, Quelle livesenderRadio.xml
			senderlist = sender.split('|')
			# Log(senderlist); 		# bei Bedarf
			for i in range (len(senderlist)):
				sname = ''; img = ''
				try:								# try gegen Schreibfehler in  livesenderRadio.xml
					pair =  mystrip(senderlist[i]) 	# mystrip wg. Zeilenumbrüchen in livesenderRadio.xml
					pair = pair.split(':')			# Paarweise, Bsp.: B5 aktuell:radio-b5-aktuell.png
					sname 	= pair[0].strip()
					sname	= sname.decode('utf-8') # wie headline
					img 	= pair[1].strip()
				except:
					break								# dann bleibt es bei img_src (Fallback)
				# Log('headline:' + headline.upper()); Log(sname.upper());
				if sname.upper() == headline.upper():	# lokaler Sendername in  <sender> muss Sendernahme aus headline entspr.
					# if img:
					img_path = os.path.join(Dict['R'], img)
					Log(img_path)
					if os.path.exists(img_path):
						img_src = img
					else:
						img_src = link_img	# Fallback aus parseLinks_Mp4_Rtmp, ev. nur Mediathek-Symbol
					# Log(img_src); 			# bei Bedarf
					break

		Log(link_path); Log(link_img); Log(img_src);Log(m3u8_master); 
		headline_org =  headline	# sichern		
		for i in range(len(link_path)):
			s = link_path[i]
			Log(s)
			mark = s[0]
			slink = s[2:]
			Log(s); Log(mark); Log(slink); 
			if slink.find('.m3u') > 9:		# der .m3u-Link führt zu weiterer Textdatei, die den Streamlink enthält
				try:						# Request kann fehlschlagen, z.B. bei RBB, SR, SWR
					#slink_content = HTTP.Request(slink).content	# 
					slink_content = HTTP.Request(slink,timeout=float(1)).content	# timeout 0,5 für RBB + SR zu klein
					z = slink_content.split()
					Log(z)
					slink = z[-1]				# Link in letzter Zeile
				except:
					slink = ""
			
			Log(img_src); Log(headline); Log(subtitel); Log(sid); Log(slink);	# Bildquelle: z.Z. verwenden wir nur img_src
			if subtitel == '':		# OpenPHT parsing Error, wenn leer
				subtitel = headline
			if mark == '0':						#  Titel kennz. (0=64kb, 1=128kb, 2=128kb), bisher nur diese gesehen
				headline = headline_org + ' (64 KByte)'
			if mark == '1' or mark == '2':					
				headline = headline_org + ' (128 KByte)'
			headline = headline.decode(encoding="utf-8", errors="ignore")
			subtitel = unescape(subtitel)	
			subtitel = subtitel.decode(encoding="utf-8", errors="ignore")
			Log(subtitel)
				
			if slink:						# normaler Link oder Link über .m3u ermittelt
				# msg = ', Stream ' + str(i + 1) + ': OK'		# Log in parseLinks_Mp4_Rtmp ausreichend
				msg = ''
				if img_src.find('http') >= 0:	# Bildquelle Web
					oc.add(CreateTrackObject(url=slink, title=headline + msg, summary=subtitel, 
						 thumb=img_src, fmt='mp3'))				# funktioniert hier auch mit aac
				else:							# Bildquelle lokal
					# OpenPHT scheitert, falls hier CreateTrackObject direkt angesteuert wird und sich in der
					#	Liste andere als Trackobjekte befinden (z.B. Homebutton) Webplayer dagegen OK
					Log(img_src) # Log hilft hier gegen (seltenes) "Verschlucken" des Caches (Bild fehlt)
					oc.add(CreateTrackObject(url=slink, title=headline, summary=subtitel, thumb=R(img_src), fmt='mp3',))							 	
			else:
				msg = ' Stream ' + str(i + 1) + ': nicht verfügbar'	# einzelnen nicht zeigen - verwirrt nur
	
	if len(oc) < 1:	      		# keine Radiostreams gefunden		
		Log('oc = 0, keine Radiostreams gefunden') 		 
		msgHg = 'keine Radiostreams bei ' + title + ' gefunden/verfuegbar' 
		msg =  'keine Radiostreams bei ' + title + ' gefunden/verfuegbar, ' + 'Seite: ' + path
		return ObjectContainer(header=msgH, message=msg)	# bricht Auswertung für Anstalt komplett ab							
				
	return oc
	
#-----------------------------
# Umleitung, falls PHT in RadioAnstalten scheitert (1 Klick mehr erforderlich, keine Liste), z.Z. nicht benötigt
@route(PREFIX + '/RadioEinzel')  
def RadioEinzel(url, title, summary, fmt, thumb,):
	oc = ObjectContainer(view_group="InfoList", title1=title, art=ICON)
	oc.add(CreateTrackObject(url=url, title=title, summary=summary, fmt='mp3', thumb=thumb))	
	return oc
	
#-----------------------------
@route(PREFIX + '/CreateTrackObject')
# 	@route('/music/ardmediathek2016/CreateTrackObject')  # funktioniert nicht, dto. in PlayAudio
# tagline im TrackObject nicht erlaubt.
# 15.03.2017: die Parameter location und includeBandwidths werden für die Android-App benötigt 	
# 26.03.2017: **kwargs - siehe Funktion PlayAudio
#	 **kwargs als Parameter früher für PHT hier nicht geeignet - Test 26.03.2017: OK
# trotz **kwargs werden hier die None-Parameter im Kopf verwendet, um die Abfrage in der Funktion zu ermöglichen,
#	dto. in PlayAudio
# 08.04.2017: eindeutige ID für rating_key via random - url führte zu Error bei Client BRAVIA 2015 Android 5.1.1
#

# def CreateTrackObject(url, title, summary, fmt, thumb, include_container=False, **kwargs):
def CreateTrackObject(url, title, summary, fmt, thumb, include_container=False, location=None, includeBandwidths=None, autoAdjustQuality=None, hasMDE=None, **kwargs):
	Log('CreateTrackObject: ' + url); Log(include_container)
	Log(summary);Log(fmt);Log(thumb);
	
	if location is not None: 
		Log(location); 
	if includeBandwidths is not None: 
		Log(includeBandwidths); 
	if autoAdjustQuality is not None : 
		Log(autoAdjustQuality); 
	if hasMDE is not None: 
		Log(hasMDE); 

	if fmt == 'mp3':
		container = Container.MP3
		# container = 'mp3'
		audio_codec = AudioCodec.MP3
	elif fmt == 'aac':
		container = Container.MP4
		# container = 'aac'
		audio_codec = AudioCodec.AAC
	elif fmt == 'hls':
		protocol = 'hls'
		container = 'mpegts'
		audio_codec = AudioCodec.AAC	

	title = title.decode(encoding="utf-8", errors="ignore")
	summary = summary.decode(encoding="utf-8", errors="ignore")
	
	random.seed()						
	rating_id = random.randint(1,10000)
	rating_key = 'rating_key-' + str(rating_id)
	Log(rating_key)
	
	track_object = TrackObject(
		key = Callback(CreateTrackObject, url=url, title=title, summary=summary, fmt=fmt, thumb=thumb, include_container=True, 
				location=None, includeBandwidths=None, autoAdjustQuality=None, hasMDE=None),
		rating_key = rating_key,	
		title = title,
		summary = summary,
		thumb=thumb,
		items = [
			MediaObject(
				parts = [
					PartObject(key=Callback(PlayAudio, url=url, ext=fmt)) # runtime- Aufruf PlayAudio.mp3
				],
				container = container,
				audio_codec = audio_codec,
				# bitrate = 128,		# bitrate entbehrlich
				audio_channels = 2		# audio_channels entbehrlich
			)
		]
	)


	if include_container:
		return ObjectContainer(objects=[track_object])
	else:
		return track_object

#-----------------------------
@route(PREFIX + '/PlayAudio') 
# # runtime-Aufruf PlayAudio.mp3 
# 15.03.2017: die Parameter location, includeBandwidths usw. werden für die Android-App benötigt.	
# 26.03.2017: **kwargs für eventuelle weitere Extra-Parameter angefügt, siehe
#		https://forums.plex.tv/discussion/comment/1405423/#Comment_1405423
#		https://forums.plex.tv/discussion/comment/1417389#Comment_1417389
#		http://stackoverflow.com/questions/36901/what-does-double-star-and-star-do-for-parameters
#		**kwargs allein würde reichen - None-Parameter verbleiben zunächst zum Debuggen
def PlayAudio(url, location=None, includeBandwidths=None, autoAdjustQuality=None, hasMDE=None, **kwargs):	
	Log('PlayAudio')
	Log(url)	
	if location is not None: 
		Log(location); 					# Bsp. lan
	if includeBandwidths is not None: 
		Log(includeBandwidths); 		
	if autoAdjustQuality is not None: 
		Log(autoAdjustQuality);			# Bsp. 0
	if hasMDE is not None: 
		Log(hasMDE); 					# Bsp. 1
		
	if url is None or url == '':		# sollte hier nicht vorkommen
		Log('Url fehlt!')
		return ObjectContainer(header='Error', message='Url fehlt!') # Web-Player: keine Meldung
	
	try:
		req = urllib2.Request(url)						# Test auf Existenz, SSLContext für HTTPS erforderlich,
		gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)  	#	Bsp.: SWR3 https://pdodswr-a.akamaihd.net/swr3
		ret = urllib2.urlopen(req, context=gcontext)
		Log('PlayAudio: ' + str(ret.code))
	except Exception as exception:	
		error_txt = 'Server meldet: ' + str(exception)
		error_txt = error_txt + '\r\n' + url			 			 	 
		msgH = 'Error'; msg = error_txt
		msg =  msg.decode(encoding="utf-8", errors="ignore")
		Log(msg)
		return ObjectContainer(header=msgH, message=msg) # Framework fängt ab - keine Ausgabe
			
	return Redirect(url)
		
####################################################################################################
#									ZDF-Funktionen
#
@route(PREFIX + '/ZDF_Search')	# Suche - Verarbeitung der Eingabe. Neu ab 28.10.2016 (nach ZDF-Relaunch)
# 	Voreinstellungen: alle ZDF-Sender, ganze Sendungen, sortiert nach Datum
#	Anzahl Suchergebnisse: 25 - nicht beeinflussbar
# def ZDF_Search(query=None, title=L('Search'), s_type=None, pagenr='', **kwargs):
def ZDF_Search(query=None, title=L('Search'), s_type=None, pagenr='', **kwargs):
	query = query.strip()
	query = query.replace(' ', '+')		# Leer-Trennung bei ZDF-Suche mit +
	query = urllib2.quote(query, "utf-8")
	Log('ZDF_Search'); Log(query); Log(pagenr); Log(s_type)

	ID='Search'
	ZDF_Search_PATH	 = 'https://www.zdf.de/suche?q=%s&from=&to=&sender=alle+Sender&attrs=&contentTypes=episode&sortBy=date&page=%s'
	if s_type == 'Bilderserien':	# 'ganze Sendungen' aus Suchpfad entfernt:
		ZDF_Search_PATH	 = 'https://www.zdf.de/suche?q=%s&from=&to=&sender=alle+Sender&attrs=&contentTypes=&sortBy=date&page=%s'
		ID=s_type
	
	if pagenr == '':		# erster Aufruf muss '' sein
		pagenr = 1
	path = ZDF_Search_PATH % (query, pagenr) 
	Log(path)	
	# page = HTTP.Request(path, cacheTime=1).content 		# Debug: cacheTime=1 
	page = HTTP.Request(path).content 
	searchResult = stringextract('data-loadmore-result-count="', '"', page)	# Anzahl Ergebnisse
	Log(searchResult);
	
	# Log(page)	# bei Bedarf		
	NAME = 'ZDF Mediathek'
	name = 'Suchergebnisse zu: %s (Gesamt: %s), Seite %s'  % (urllib.unquote(query), searchResult, pagenr)
	name = name.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=name, art = ObjectContainer.art)

	if searchResult == '0':
		msg_notfound = 'Kein Ergebnis für >%s<' % query
		title = msg_notfound.decode(encoding="utf-8", errors="ignore")
		summary = 'zurück zu ' + NAME
		summary = summary.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(Main_ZDF, name=NAME), title=title, 
			summary=summary, tagline='TV', thumb=R(ICON_MAIN_ZDF)))
		return oc
	
	oc = home(cont=oc, ID='ZDF')							# Home-Button	
				
	# offset=0: anders als bei den übrigen ZDF-'Mehr'-Optionen gibt der Sender Suchergebnisse bereits
	#	seitenweise aus, hier umgesetzt mit pagenr - offset entfällt	
	oc, offset, page_cnt = ZDF_get_content(oc=oc, page=page, ref_path=path, ID=ID, offset=0)
	
	# auf mehr prüfen (Folgeseite auf content-link = Ausschlusskriterum prüfen):
	#	im Gegensatz zu anderen ZDF-Seiten gibt  der Sender hier die Resultate seitenweise aus.
	# 	Daher entfällt die offset-Variante wiez.B. in BarriereArmSingle.
	pagenr = int(pagenr) + 1
	path = ZDF_Search_PATH % (query, pagenr)
	Log(pagenr); Log(path)
	page = HTTP.Request(path, cacheTime=1).content
	content =  blockextract('class="artdirect"', page)
	if len(content) > 0:
		title = "Weitere Beiträge".decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(ZDF_Search, query=query, s_type=s_type, pagenr=pagenr), 
			title=title, thumb=R(ICON_MEHR), summary=''))	
 
	return oc
	
#-------------------------
@route(PREFIX + '/ZDF_Verpasst')
def ZDF_Verpasst(title, zdfDate, offset=0):
	Log('ZDF_Verpasst'); Log(title); Log(zdfDate)
	oc = ObjectContainer(title2=title, view_group="List")
	oc = home(cont=oc, ID='ZDF')							# Home-Button

	path = ZDF_SENDUNG_VERPASST % zdfDate
	page = HTTP.Request(path).content 
	Log(path);	# Log(page)	# bei Bedarf

	oc, offset, page_cnt = ZDF_get_content(oc=oc, page=page, ref_path=path, ID='VERPASST', offset=offset)
	summ_mehr = 'Mehr zu >Verpasst<, Gesamt: %s' % page_cnt
	
	Log(offset)
	if offset:
		summ_mehr = summ_mehr.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(ZDF_Verpasst, title=title, zdfDate=zdfDate, offset=offset), 
			title='Mehr...', summary=summ_mehr,  thumb=R(ICON_MEHR)))	
			
	return oc
	
####################################################################################################
@route(PREFIX + '/ZDFSendungenAZ')
def ZDFSendungenAZ(name):
	Log('ZDFSendungenAZ')
	oc = ObjectContainer(title2=name, view_group="List")
	oc = home(cont=oc, ID='ZDF')							# Home-Button
	
	azlist = list(string.ascii_uppercase)
	azlist.append('0-9')
	title = "Sendungen A-Z"

	# Menü A to Z
	for element in azlist:
		oc.add(DirectoryObject(key=Callback(SendungenAZList, title=title, element=element), 
			title='Sendungen mit ' + element, thumb=R(ICON_ZDF_AZ)))

	return oc

####################################################################################################
@route(PREFIX + '/SendungenAZList')
def SendungenAZList(title, element, offset=0):	# Sendungen zm gewählten Buchstaben
	Log('SendungenAZList')
	title2='Sendungen mit ' + element
	oc = ObjectContainer(title2=title2, view_group="List")
	oc = home(cont=oc, ID='ZDF')							# Home-Button

	group = element	
	if element == '0-9':
		group = '0+-+9'		# ZDF-Vorgabe
	azPath = ZDF_SENDUNGEN_AZ % group
	page = HTTP.Request(azPath).content 
	Log(azPath);	

	oc, offset, page_cnt = ZDF_get_content(oc=oc, page=page, ref_path=azPath, ID='DEFAULT', offset=offset)
	Log(page_cnt)  
	if page_cnt == 0:	# Fehlerbutton bereits in ZDF_get_content
		return oc
		
	summ_mehr = 'Mehr zu >%s<, Gesamt: %s' % (title2, page_cnt)
	if offset:
		summ_mehr = summ_mehr.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(SendungenAZList, title=title, element=element, offset=offset), 
			title='Mehr...', summary=summ_mehr,  thumb=R(ICON_MEHR)))	

	return oc
	
####################################################################################################
# 	wrapper für Mehrfachseiten aus ZDF_get_content (multi=True). Dort ist kein rekursiver Aufruf
#	möglich (Übergabe Objectcontainer in Callback nicht möglich - kommt als String an)
@route(PREFIX + '/ZDF_Sendungen')	
def ZDF_Sendungen(url, title, ID, offset=0):
	Log('ZDFSendungen')
	
	title = title.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(title2=title, view_group="List")
	oc = home(cont=oc, ID='ZDF')						# Home-Button
	
	try:												# Sicherung, s.a. 
		page = HTTP.Request(url).content 				# https://www.zdf.de/zdfunternehmen/drei-stufen-test-100.html
	except:
		page = ''
	if page == '':
			msg = 'Seite kann nicht geladen werden. URL:\r'
			msg = msg + url
			return ObjectContainer(message=msg)	  # header=... ohne Wirkung	(?)	
					
	oc, offset, page_cnt = ZDF_get_content(oc=oc, page=page, ref_path=url, ID='VERPASST', offset=offset)

	Log(offset)
	summ_mehr = 'Mehr zu >%s<, Gesamt: %s' % (title, page_cnt)
	if offset:
		summ_mehr = summ_mehr.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(ZDF_Sendungen, url=url, title=title, ID=ID, offset=offset), 
			title='Mehr...', summary=summ_mehr,  thumb=R(ICON_MEHR)))	

	return oc
  
####################################################################################################
@route(PREFIX + '/Rubriken')
def Rubriken(name):
	Log('Rubriken')
	oc = ObjectContainer(title2='ZDF: ' + name, view_group="List")
	oc = home(cont=oc, ID='ZDF')							# Home-Button

	# zuerst holen wir uns die Rubriken von einer der Rubrikseiten:
	path = 'https://www.zdf.de/doku-wissen'
	page = HTTP.Request(path).content 

	listblock =  stringextract('<li class=\"dropdown-block x-left\">', 'link js-track-click icon-104_live-tv', page)
	rubriken =  blockextract('class=\"dropdown-item', listblock)
	
	for rec in rubriken:											# leider keine thumbs enthalten
		path = stringextract('href=\"', '\"', rec)
		path = ZDF_BASE + path
		title = stringextract('class=\"link-text\">', '</span>', rec)
		title = mystrip(title)
		if title == "Sendungen A-Z":	# Rest nicht mehr relevant
			break
		oc.add(DirectoryObject(key=Callback(RubrikSingle, title=title, path=path), 
			title=title, summary=title,  thumb=R(ICON_ZDF_RUBRIKEN)))	
	
	return oc
#-------------------------
@route(PREFIX + '/RubrikSingle')
def RubrikSingle(title, path, offset=0):
	Log('RubrikSingle'); 
	oc = ObjectContainer(title2=title, view_group="List")
	oc = home(cont=oc, ID='ZDF')							# Home-Button
	
	page = HTTP.Request(path).content 			
	oc, offset, page_cnt = ZDF_get_content(oc=oc, page=page, ref_path=path, ID='Rubriken', offset=offset)
	
	Log(offset)
	if offset:
		summ_mehr = 'Mehr zu >%s<, Gesamt: %s' % (title, page_cnt)
		summ_mehr = summ_mehr.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(RubrikSingle, title=title, path=path, offset=offset), 
			title='Mehr...', summary=summ_mehr,  thumb=R(ICON_MEHR)))	
	return oc
	
####################################################################################################
@route(PREFIX + '/MeistGesehen')
def MeistGesehen(name, offset=0):
	Log('MeistGesehen'); 
	oc = ObjectContainer(title2=name, view_group="List")
	oc = home(cont=oc, ID='ZDF')							# Home-Button
	
	path = ZDF_SENDUNGEN_MEIST
	page = HTTP.Request(path).content 			
	oc, offset, page_cnt = ZDF_get_content(oc=oc, page=page, ref_path=path, ID='MeistGesehen', offset=offset)
	
	Log(offset)
	if offset:
		# Log(name); Log(page_cnt)
		summ_mehr = 'Mehr zu >%s<, Gesamt: %s' % (name, page_cnt)
		summ_mehr = summ_mehr.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(RubrikSingle, title=name, path=path, offset=offset), 
			title='Mehr...', summary=summ_mehr,  thumb=R(ICON_MEHR)))	
	
	return oc
		
####################################################################################################
@route(PREFIX + '/NeuInMediathek')
def NeuInMediathek(name, offset=0):
	Log('NeuInMediathek'); 
	oc = ObjectContainer(title2=name, view_group="List")
	oc = home(cont=oc, ID='ZDF')							# Home-Button
	
	path = ZDF_BASE
	page = HTTP.Request(path).content
	Log(len(page))
	#  1. Block extrahieren (Blöcke: Neu, Nachrichten, Sport ...)
	page = stringextract('>Neu in der Mediathek<','<h2 class="cluster-title"', page)
	Log(len(page))
	 			
	oc, offset, page_cnt = ZDF_get_content(oc=oc, page=page, ref_path=path, ID='NeuInMediathek', offset=offset)
	
	Log(offset)
	if offset:
		summ_mehr = 'Mehr zu >%s<, Gesamt: %s' % (name, page_cnt)
		summ_mehr = summ_mehr.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(NeuInMediathek, name=name, offset=offset), 
			title='Mehr...', summary=summ_mehr,  thumb=R(ICON_MEHR)))	
	
	return oc
		
####################################################################################################
@route(PREFIX + '/BarriereArm')		# z.Z. nur Hörfassungen, Rest ausgeblendet, da UT in Plex-Channels n.m.
def BarriereArm(name):				# Vorauswahl: 1. Infos, 2. Hörfassungen, 3. Videos mit Untertitel
	Log('BarriereArm')
	oc = ObjectContainer(title2='ZDF: ' + name, view_group="List")
	oc = home(cont=oc, ID='ZDF')								# Home-Button

#	title='Barrierefreie Angebote'							# freischalten, falls UT in Plex verfügbar
#	title=title.decode(encoding="utf-8", errors="ignore")
#	oc.add(DirectoryObject(key=Callback(BarriereArmSingle, title=title, ID='Infos'), 
#		title=title, summary='Infos zu den barrierefreie Angeboten', thumb=R(ICON_ZDF_INFOS)))	
		
	title='Hörfassungen'
	title=title.decode(encoding="utf-8", errors="ignore")
	summary='verfügbare Videos mit reinen Hörfassugen'
	summary=summary.decode(encoding="utf-8", errors="ignore")
	oc.add(DirectoryObject(key=Callback(BarriereArmSingle, title=title, ID='Voice'), 
		title=title, summary=summary, thumb=R(ICON_ZDF_HOERFASSUNGEN)))	
		
#	title='Untertitel'										# freischalten, falls UT in Plex verfügbar
#	title=title.decode(encoding="utf-8", errors="ignore")
#	# summary='Verfügbare Videos mit Untertitel'
#	summary='in Plex noch nicht verfügbar'
#	summary=summary.decode(encoding="utf-8", errors="ignore")
#	oc.add(DirectoryObject(key=Callback(BarriereArmSingle, title=title, ID='UT'), 
#		title=title, summary=summary, thumb=R(ICON_ZDF_UNTERTITEL)))		
		
	return oc
	
#-------------------------
@route(PREFIX + '/BarriereArmSingle')
def BarriereArmSingle(title, ID, offset=0):	# Aufruf: 1. Infos, 2. Hörfassungen, 3. Videos mit Untertitel
	Log('BarriereArmSingle: ' + ID)
	Log(offset)
	
	title = title.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(title2='ZDF: ' + title, view_group="List")
	oc = home(cont=oc, ID='ZDF')								# Home-Button

	path = ZDF_BARRIEREARM
	page = HTTP.Request(path).content 
	
	# Dreiteilung: 1. Infos, 2. Hörfassungen, 3. Videos mit Untertitel
	cont1 =  stringextract('title\" >Barrierefreie Angebote', 'Hörfassungen</h2>', page)
	cont2 =  stringextract('Hörfassungen</h2>', 'Die neuesten Videos mit Untertitel</h2>', page)
	pos = page.find('Die neuesten Videos mit Untertitel</h2>')   # nur 1 x vorh, bis Rest
	cont3 = page[pos:]
	Log(len(cont3))
	
	if ID == 'Infos':
		oc, offset, page_cnt  = ZDF_get_content(oc=oc, page=cont1, ref_path=path, ID='BARRIEREARM', offset=offset)	
		summ_mehr = 'Infos zu >Barrierefreie Angebote<, Gesamt: %s' % page_cnt
	if ID == 'Voice':
		oc, offset, page_cnt = ZDF_get_content(oc=oc, page=cont2, ref_path=path, ID='BARRIEREARM', offset=offset)	
		summ_mehr = 'Mehr zu >Hörfassungen<, Gesamt: %s' % page_cnt
	if ID == 'UT':
		oc, offset, page_cnt  = ZDF_get_content(oc=oc, page=cont3, ref_path=path, ID='BARRIEREARM', offset=offset)	
		summ_mehr = 'Mehr zu >Videos mit Untertitel<, Gesamt: %s' % page_cnt
	
	Log(offset)
	if offset:
		summ_mehr = summ_mehr.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(BarriereArmSingle, title=title, ID=ID, offset=offset), 
			title='Mehr...', summary=summ_mehr,  thumb=R(ICON_MEHR)))	
		
	return oc
	
####################################################################################################
@route(PREFIX + '/International')
def International(name, offset=0):
	Log('International'); 
	oc = ObjectContainer(title2=name, view_group="List")
	oc = home(cont=oc, ID='ZDF')							# Home-Button
	
	if name == 'ZDFenglish':
		path = 'https://www.zdf.de/international/zdfenglish'
	if name == 'ZDFarabic':
		path = 'https://www.zdf.de/international/zdfarabic'
		
	page = HTTP.Request(path).content
	Log(len(page))
	 			
	oc, offset, page_cnt = ZDF_get_content(oc=oc, page=page, ref_path=path, ID='International', offset=offset)
	
	Log(offset);Log(page_cnt)
	if offset:
		summ_mehr = 'Mehr zu >%s<, Gesamt: %s' % (name, page_cnt)
		summ_mehr = summ_mehr.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(International, name=name, offset=offset), 
			title='Mehr...', summary=summ_mehr,  thumb=R(ICON_MEHR)))	
	
	return oc	
	
####################################################################################################
# @route(PREFIX + '/ZDF_get_content')	# Auswertung aller ZDF-Seiten
#	 
#	offset: für übergroße Seiten, die nicht wie die Suchergebn. als Folgeseiten mit pagenr organisiert sind.
#		Bsp. für übergroße Seite: Hörfassungen (145 am 28.9.2017)
#
# 	ID='Search' od. 'VERPASST' - Abweichungen zu Rubriken + A-Z

def ZDF_get_content(oc, page, ref_path, offset=0, ID=None):	
	Log('ZDF_get_content'); Log(ID); Log(ref_path); Log(offset)					
	Log(len(page));			
	max_count = int(Prefs['pref_maxZDFContent'])				# max. Anzahl Einträge ab offset
	offset = int(offset)
	
	Bilderserie = False	
	if ID == 'Bilderserien':									# Aufruf: ZDF_Search
		Bilderserie = True										# für Titelergänzung (Anz. Bilder)
		ID='DEFAULT'											# Sätze ohne aufnehmen														
	
	img_alt = teilstring(page, 'class=\"m-desktop', '</picture>') # Bildsätze für b-playerbox
		
	page_title = stringextract('<title>', '</title>', page)  # Seitentitel
	page_title = page_title.strip()
	msg_notfound = ''
	if 'Leider kein Video verfügbar' in page:				# Verfügbarkeit vor class="artdirect"
		msg_notfound = 'Leider kein Video verfügbar'		# z.B. Ausblick auf Sendung
		if page_title:
			msg_notfound = 'Leider kein Video verfügbar zu: ' + page_title
		
	pos = page.find('class="content-box"')					# ab hier verwertbare Inhalte 
	Log('pos: ' + str(pos))
	if pos >= 0:
		page = page[pos:]
				
	content =  blockextract('class="artdirect"', page)
	if ID == 'NeuInMediathek':									# letztes Element entfernen (Verweis Sendung verpasst)
		content.pop()	
	page_cnt = len(content)
	Log('content_Blocks: ' + str(page_cnt));
	
	if page_cnt == 0:											# kein Ergebnis oder allg. Fehler
		if 'class="b-playerbox' not in page and 'class="item-caption' not in page: # Einzelvideo?
			s = 'Es ist leider ein Fehler aufgetreten.'				# ZDF-Meldung Server-Problem
			if page.find('\"title\">' + s) >= 0:
				msg_notfound = s + ' Bitte versuchen Sie es später noch einmal.'
			else:
				msg_notfound = 'Leider keine Inhalte verfügbar.' 	# z.B. bei A-Z für best. Buchstaben 
				if page_title:
					msg_notfound = 'Leider keine Inhalte verfügbar zu: ' + page_title
			
		Log('msg_notfound: ' + str(page_cnt))
		# kann entfallen - Blockbildung mit class="content-box" inzw. möglich. Modul zdfneo.py entfernt.
		#	Zeilen hier ab 1.1.2018 löschen:
		#if ref_path.startswith('https://www.zdf.de/comedy/neo-magazin-mit-jan-boehmermann'): # neue ZDF-Seite
		#	import zdfneo
		#	oc = zdfneo.neo_content(path=ref_path, ID=ID)		# Abschluss dort
		#	return oc, offset, page_cnt 		
		
	if msg_notfound:											# gesamte Seite nicht brauchbar
		title = msg_notfound.decode(encoding="utf-8", errors="ignore")					
		summary = 'zurück zur ' + NAME.decode(encoding="utf-8", errors="ignore")		
		oc.add(DirectoryObject(key=Callback(Main_ZDF, name=NAME), title=title, 
			summary=summary, tagline='TV', thumb=R(ICON_MAIN_ZDF)))
		return oc, offset, page_cnt
		
	if page.find('class="b-playerbox') > 0 and page.find('class="item-caption') > 0:  # mehrspaltig: Video gesamte Sendung?
		first_rec = img_alt +  stringextract('class="item-caption', 'data-tracking=', page) # mit img_alt
		content.insert(0, first_rec)		# an den Anfang der Liste
		# GNNLog(content[0]) # bei Bedarf
					
	
	if 	max_count:								# 0 = 'Mehr..'-Option ausgeschaltet
		delnr = min(page_cnt, offset)
		del content[:delnr]						# Sätze bis offset löschen (bzw. bis Ende records)
	Log(len(content))
	for rec in content:	
		pos = rec.find('</article>')		   # Satz begrenzen - bis nächsten Satz nicht verwertbare Inhalte möglich
		if pos > 0:
			rec = rec[0:pos]
		# Log(rec)  # bei Bedarf
			
		if ID <> 'DEFAULT':					 			# DEFAULT: Übersichtsseite ohne Videos, Bsp. Sendungen A-Z
			if 'title-icon icon-502_play' not in rec:  	# Videobeitrag?
				if '>Videolänge:<' not in rec : 
					continue		
		multi = False			# steuert Mehrfachergebnisse 
		
		meta_image = stringextract('<meta itemprop=\"image\"', '>', rec)
		#Log('meta_image: ' + meta_image)
		# thumb  = stringextract('class=\"m-8-9\"  data-srcset=\"', ' ', rec)    # 1. Bild im Satz m-8-9 (groß)
		thumb_set = stringextract('class=\"m-8-9\"  data-srcset=\"', '/>', rec) 
		thumb_set = thumb_set.split(' ')		
		
		for thumb in thumb_set:				# kleine Ausgabe 240x270 suchen
			if thumb.find('240x270') >= 0:
				break		
		# Log(thumb_set); Log(thumb)

		if thumb == '':											# 1. Fallback thumb	
			thumb  = stringextract('class=\"b-plus-button m-small', '\"', meta_image)
		if thumb == '':											# 2. Fallback thumb (1. Bild aus img_alt)
			thumb = stringextract('data-srcset=\"', ' ', img_alt) 	# img_alt s.o.	
		Log('thumb: ' + thumb)
			
		if thumb.find('https://') == -1:	 # Bsp.: "./img/bgs/zdf-typical-fallback-314x314.jpg?cb=0.18.1787"
				thumb = ZDF_BASE + thumb[1:] # 	Fallback-Image  ohne Host
						
		teaser_label = stringextract('class=\"teaser-label\"', '</div>', rec)
		teaser_typ =  stringextract('<strong>', '</strong>', teaser_label)
		if teaser_typ == 'Beiträge':		# Mehrfachergebnisse ohne Datum + Uhrzeit
			multi = True
			summary = dt1 + teaser_typ 		# Anzahl Beiträge
		#Log('teaser_typ: ' + teaser_typ)			
			
		subscription = stringextract('is-subscription=\"', '\"', rec)	# aus plusbar-Block	
		Log(subscription)
		if subscription == 'true':						
			multi = True
			teaser_count = stringextract('</span>', '<strong>', teaser_label)	# bei Beiträgen
			stage_title = stringextract('class=\"stage-title\"', '</h1>', rec)  
			summary = teaser_count + ' ' + teaser_typ 

		# Titel	
		href_title = stringextract('<a href="', '>', rec)		# href-link hinter teaser-cat kann Titel enthalten
		href_title = stringextract('title="', '"', href_title)
		href_title = unescape(href_title)
		Log('href_title: ' + href_title)
		if 	href_title == 'ZDF Livestream' or href_title == 'Sendung verpasst':
			continue
			
		# Pfad				
		plusbar_title = stringextract('plusbar-title=\"', '\"', rec)	# Bereichs-, nicht Einzeltitel, nachrangig
		# plusbar_path = stringextract('plusbar-path=\"', '\"', rec)    # path ohne http(s)
		path =  stringextract('plusbar-url=\"', '\"', rec)				# plusbar nicht vorh.? - sollte nicht vorkommen
		Log('path: ' + path); Log('ref_path: ' + ref_path)	
		if path == '' or path == ref_path:					# kein Pfad oder Selbstreferenz
			continue
		
		# Datum, Uhrzeit Länge	
		if 'icon-301_clock icon' in rec:						# Uhrsymbol  am Kopf mit Datum/Uhrzeit
			teaser_label = stringextract('class="teaser-label"', '</div>', rec)	
			Log('teaser_label: ' + teaser_label)
			video_datum =  stringextract('</span>', '<strong>', teaser_label)   
			video_time =  stringextract('<strong>', '</strong>', teaser_label)
		else:
			if '<time datetime="' in rec:						# Datum / Zeit können fehlen
				datum_line =  stringextract('<time datetime="', '/time>', rec) # datetime="2017-11-15T20:15:00.000+01:00">15.11.2017</time>
				video_datum =  stringextract('">', '<', datum_line)
				video_time = datum_line.split('T')[1]
				video_time = video_time[:5] 
			else:
				video_datum=''; video_time=''			
		Log(video_datum); Log(video_time);
					
		duration = stringextract('Videolänge:', 'Datum', rec) 		# Länge - 1. Variante 
		duration = stringextract('m-border">', '</', duration)		# Ende </dd> od. </dt>
		if duration == '':
			duration = stringextract('Videolänge:', '</dl>', rec) 	# Länge - 2. Variante bzw. fehlend
			duration = stringextract('">', '</', duration)			
		Log('duration: ' + duration);
		
		pic_cnt = stringextract('Anzahl Bilder:', '<dt class', rec)	# Bilderzahl bei Bilderserien
		pic_cnt = stringextract('">', '</', pic_cnt)				# Ende </dd> od. </dt>
		Log('Bilder: ' + pic_cnt);
			
		title = href_title 
		if title == '':
			title = plusbar_title
		if Bilderserie == True:
			title = title + " | %s"   % pic_cnt
		if title.startswith(' |'):
			title = title[2:]				# Korrektur
			
		category = stringextract('teaser-cat-category">', '</span>', rec)
		category = mystrip(category)
		brand = stringextract('teaser-cat-brand">', '</span>', rec)
		brand = mystrip(brand)	
			
		tagline = video_datum
		video_time = video_time.replace('00:00', '')		# ohne Uhrzeit
		if video_time:
			tagline = tagline + ' | ' + video_time
		if duration:
			tagline = tagline + ' | ' + duration
		if category:
			tagline = tagline + ' | ' + category
		if brand:
			tagline = tagline + ' | ' + brand
		if tagline.startswith(' |'):
			tagline = tagline[2:]			# Korrektur
			
		descr = stringextract('description">', '<', rec)
		descr = mystrip(descr)
		# Log('descr:' + descr)		# UnicodeDecodeError möglich
		if descr:
			summary = descr
		else:
			summary = href_title
			
		if 	'title-icon icon-502_play' in rec == False and 'icon-301_clock icon' in rec == False:
			Log('icon-502_play und icon-301_clock nicht gefunden')
			if ID == 'Bilderserien': 	# aber Bilderserien aufnehmen
				Log('Bilderserien')
			if plusbar_title.find(' in Zahlen') > 0:	# Statistik-Seite, voraus. ohne Galeriebilder 
				continue
			if plusbar_title.find('Liveticker') > 0:	#   Liveticker und Ergebnisse
				continue
			if plusbar_path.find('-livestream-') > 0:	#   Verweis Livestreamseite
				continue
			multi = True			# weitere Folgeseiten mit unbekanntem Inhalt, ev. auch Videos
			tagline = 'Folgeseiten'
		
		if multi == True:			
			tagline = 'Folgeseiten'
		
		title = title.strip()
		title = unescape(title)
		summary = unescape(summary)
		summary = cleanhtml(summary)
		tagline = unescape(tagline)
		tagline = cleanhtml(tagline)
		client = Client.Platform
		if client == None:
			client = ''
		Log(client)									# für PHT: Austausch Titel / Tagline
		if  client == 'Plex Home Theater':
			title, tagline = tagline, title
			
		Log('neuer Satz')
		Log(thumb);	Log(path);Log(title);Log(summary);Log(tagline); Log(multi);
		title = title.decode(encoding="utf-8", errors="ignore")
		summary = summary.decode(encoding="utf-8", errors="ignore")
		tagline = tagline.decode(encoding="utf-8", errors="ignore")
		 
		if multi == True:
			oc.add(DirectoryObject(key=Callback(ZDF_Sendungen, url=path, title=title, ID=ID, offset=0), 
				title=title, thumb=thumb, summary=summary, tagline=tagline))
		else:							
			oc.add(DirectoryObject(key=Callback(GetZDFVideoSources, title=title, url=path, tagline=tagline, thumb=thumb), 
					title=title, thumb=thumb, summary=summary, tagline=tagline))

		if max_count:
			# Mehr Seiten anzeigen:		# 'Mehr...'-Callback durch Aufrufer	
			cnt = len(oc) + offset		# 
			# Log('Mehr-Test'); Log(len(oc)); Log(cnt); Log(page_cnt)
			if cnt > page_cnt:			# Gesamtzahl erreicht - Abbruch
				offset=0
				break					# Schleife beenden
			elif len(oc) >= max_count:	# Mehr, wenn max_count erreicht
				offset = offset + max_count-1
				break					# Schleife beenden
		# break # Test 1. Satz
		
	return oc, offset, page_cnt 
	
#-------------

####################################################################################################
# Subtitles: im Kopf der videodat-Datei enthalten (Endung .vtt). Leider z.Z. keine Möglichkeit
#	bekannt, diese einzubinden
@route(PREFIX + '/GetZDFVideoSources')						# 4 Requests bis zu den Quellen erforderlich!				
def GetZDFVideoSources(url, title, thumb, tagline, segment_start=None, segment_end=None):	
	Log('GetVideoSources'); Log(url); Log(tagline); 
	title = title.decode(encoding="utf-8", errors="ignore")					
	oc = ObjectContainer(title2=title.decode(encoding="utf-8", errors="ignore"), view_group="InfoList")
	urlSource = url 		# für ZDFotherSources

	page, msg = get_page(url)
	if page == '':
		return ObjectContainer(header='Error', message=msg)
			
	# -- Start Vorauswertungen: Bildgalerie u.ä. 
	if segment_start and segment_end:				# Vorgabe Ausschnitt durch ZDF_get_content 
		pos1 = page.find(segment_start); pos2 = page.find(segment_end);  # bisher: b-group-persons
		Log(pos1);Log(pos2);
		page = page[pos1:pos2]
		oc = ZDF_Bildgalerie(oc=oc, page=page, mode=segment_start, title=title)
		return oc

	if page.find('data-module=\"zdfplayer\"') == -1:		# Vorprüfung auf Videos
		if page.find('class=\"b-group-contentbox\"') > 0:	# keine Bildgalerie, aber ähnlicher Inhalt
			oc = ZDF_Bildgalerie(oc=oc, page=page, mode='pics_in_accordion-panels', title=title)		
			return oc		
		if page.find('class=\"content-box gallery-slider-box') >= 0:		# Bildgalerie
			oc = ZDF_Bildgalerie(oc=oc, page=page, mode='is_gallery', title=title)
			return oc
		
	# ab 08.10.2017 dyn. ermitteln (wieder mal vom ZDF geändert)
	# 12.01.2018: ZDF verwendet nun 2 verschiedene Token - s. get_formitaeten: 1 x profile_url, 1 x videodat_url
	apiToken1 = stringextract('apiToken: \'', '\'', page) 
	apiToken2 = stringextract('"apiToken": "', '"', page)
	Dict['apiToken1'] = apiToken1
	Dict['apiToken2'] = apiToken2
	Log('apiToken1: ' + apiToken1); Log('apiToken2: ' + apiToken2)
					
	# -- Ende Vorauswertungen
			
	oc = home(cont=oc, ID='ZDF')	# Home-Button - nach Bildgalerie (PhotoObject darf keine weiteren Medienobjekte enth.)
	# key = 'page_GZVS'											# entf., in get_formitaeten nicht mehr benötigt
	# Dict[key] = page	
	docId = stringextract("docId: \'", "\'", page)				# Bereich window.zdfsite
	formitaeten,duration,geoblock = get_formitaeten(sid=docId)	# Video-URL's ermitteln
	# Log(formitaeten)
	if formitaeten == '':										# Nachprüfung auf Videos
		msg = 'Video nicht vorhanden / verfügbar'  + ' Seite:\r' + url
		msg = msg.decode(encoding="utf-8", errors="ignore")		
		return ObjectContainer(header='Error', message=msg)
				
	if tagline:
		if 'min' in tagline == False:	# schon enthalten (aus ZDF_get_content)?
			tagline = tagline + " | " + duration
	else:
		tagline = duration

	only_list = ["h264_aac_ts_http_m3u8_http"]
	oc, download_list = show_formitaeten(oc=oc, title_call=title, formitaeten=formitaeten, tagline=tagline,
		thumb=thumb, only_list=only_list,geoblock=geoblock)		  
		
	title_oc='weitere Video-Formate'
	if Prefs['pref_use_downloads']:	
		title_oc=title_oc + ' und Download'
	# oc = Parseplaylist(oc, videoURL, thumb)	# hier nicht benötigt - das ZDF bietet bereits 3 Auflösungsbereiche
	oc.add(DirectoryObject(key=Callback(ZDFotherSources, title=title, tagline=tagline, thumb=thumb, docId=docId),
		title=title_oc, summary='', thumb=R(ICON_MEHR)))

	return oc	
	
#-------------------------
@route(PREFIX + '/ZDFotherSources')		# weitere Videoquellen - Übergabe der Webseite in Dict[key]
def ZDFotherSources(title, tagline, thumb, docId):
	Log('OtherSources'); 
	title_org = title		# Backup für Textdatei zum Video
	summary_org = tagline	# Tausch summary mit tagline (summary erstrangig bei Wiedergabe)

	title = title.decode(encoding="utf-8", errors="ignore")					
	oc = ObjectContainer(title2=title, view_group="InfoList")
	oc = home(cont=oc, ID='ZDF')								# Home-Button
		
	formitaeten,duration,geoblock = get_formitaeten(sid=docId)	# Video-URL's ermitteln
	# Log(formitaeten)
	if formitaeten == '':										# Nachprüfung auf Videos
		msg = 'Video nicht vorhanden / verfügbar'  + ' Seite:\r' + url
		msg = msg.decode(encoding="utf-8", errors="ignore")		
		return ObjectContainer(header='Error', message=msg)
	
	if tagline:
		if 'min' in tagline == False:	# schon enthalten (aus ZDF_get_content)?
			tagline = tagline + " | " + duration
	else:
		tagline = duration

	only_list = ["h264_aac_mp4_http_na_na", "vp8_vorbis_webm_http_na_na", "vp8_vorbis_webm_http_na_na"]
	oc, download_list = show_formitaeten(oc=oc, title_call=title_org, formitaeten=formitaeten, tagline=tagline,
		thumb=thumb, only_list=only_list, geoblock=geoblock)		  
					
	# high=0: 	1. Video bisher höchste Qualität:  [progressive] veryhigh
	oc = test_downloads(oc,download_list,title_org,summary_org,tagline,thumb,high=0)  # Downloadbutton(s)
	return oc
	
#-------------------------
#	Ladekette für Videoquellen ab 30.05.2017:
#		1. Ermittlung des apiToken (in configuration.json), nur anfangs 2016 (unverändert), Verwendung in header
#		2. Sender-ID sid ermitteln für profile_url (durch Aufrufer)
#		3. Playerdaten ermitteln via profile_url (Basis bisher unverändert, injiziert: sid)
#		4. Videodaten ermitteln via videodat_url (Basis bisher unverändert, injiziert: videodat)
#	Bei Änderungen durch das ZDF Ladekette mittels chrome neu ermitteln (network / HAR-Auswertung)
#
def get_formitaeten(sid, ID=''):
	Log('get_formitaeten')
	Log('sid/docId: ' + sid)
	Log('Client: '); Log(Client.Platform);								# Client.Platform: None möglich
	Log('Plattform: ' + sys.platform)
	
	# bei Änderung profile_url neu ermitteln - ZDF: zdfplayer-Bereich, NEO: data-sophoraid
	profile_url = 'https://api.zdf.de/content/documents/%s.json?profile=player'	% sid
	Log(profile_url)
	if sid == '':														# Nachprüfung auf Videos
		return '','',''
	
	# apiToken (Api-Auth) : bei Änderungen des  in configuration.json neu ermitteln (für NEO: HAR-Analyse mittels chrome)
	#		ab 08.10.2017 für ZDF in GetZDFVideoSources ermittelt + als Dict gespeichert + hier injiziert (s.u.)
	# Api-Auth + Host reichen manchmal, aber nicht immer! 
	if ID == 'NEO':
		headers = {'Api-Auth': "Bearer d90ed9b6540ef5282ba3ca540ada57a1a81d670a",'Host':"api.zdf.de", 'Accept-Encoding':"gzip, deflate, sdch, br", 'Accept':"application/vnd.de.zdf.v1.0+json"}
	else:
		apiToken1 = 'Bearer ' + str(Dict['apiToken1'])		# s. GetZDFVideoSources. str falls None
		# headers = {'Api-Auth': "Bearer d2726b6c8c655e42b68b0db26131b15b22bd1a32",'Host':"api.zdf.de", 'Accept-Encoding':"gzip, deflate, sdch, br", 'Accept':"application/vnd.de.zdf.v1.0+json"}
		headers = {'Api-Auth': apiToken1,'Host':"api.zdf.de", 'Accept-Encoding':"gzip, deflate, sdch, br", 'Accept':"application/vnd.de.zdf.v1.0+json"}
		Log('apiToken1: ' + apiToken1)
	# Log(headers)		# bei Bedarf
	
	# Bei Anforderung von profile_url mittels urllib2.urlopen ssl.SSLContext erforderlich - entf. bei JSON.ObjectFromURL
	request = JSON.ObjectFromURL(profile_url, headers=headers)				# 3. Playerdaten ermitteln
	request = json.dumps(request, sort_keys=True, indent=2, separators=(',', ': '))  # sortierte Ausgabe
	Log(request[:20])	# "additionalPaths ...
	request = str(request)				# json=dict erlaubt keine Stringsuche, json.dumps klappt hier nicht
	request = request.decode('utf-8', 'ignore')	
	# Log(request)		# bei Bedarf, ev. reicht nachfolg. mainVideoContent
	
	pos = request.rfind('mainVideoContent')				# 'mainVideoContent' am Ende suchen
	request_part = request[pos:]
	# Log(request_part)			# bei Bedarf
	video_ptmd = stringextract('http://zdf.de/rels/streams/ptmd": "', '",', request_part)	
	# Bsp.: /tmd/2/portal/vod/ptmd/mediathek/161021_hsh_hsh'
	# Log(video_ptmd)	
	old_videodat_url = 'https://api.zdf.de' + video_ptmd					# 4. Videodaten ermitteln
	Log(old_videodat_url)	
	# neu ab 20.1.2016: uurl-Pfad statt ptmd-Pfad ( ptmd-Pfad fehlt bei Teilvideos)
	# neu ab19.04.2018: Videos ab heute auch ohne uurl-Pfad möglich, Code einschl. Abbruch entfernt - s.a. KIKA_und_tivi.
	
	ptmd_player = 'ngplayer_2_3'
	videodat_url = stringextract('ptmd-template": "', '",', request_part)
	videodat_url = videodat_url.replace('{playerId}', ptmd_player) 				# ptmd_player injiziert 
	videodat_url = 'https://api.zdf.de' + videodat_url
	# videodat_url = 'https://api.zdf.de/tmd/2/portal/vod/ptmd/mediathek/'  	# unzuverlässig
	# videodat_url = videodat_url + videodat
	Log('old_videodat_url: ' + old_videodat_url); Log('videodat_url: ' + videodat_url); 	

	# ab 28.05.2017: Verwendung JSON.ObjectFromURL - Laden mittels urllib2.urlopen + ssl.SSLContext entbehrlich
	#	damit entfällt auch die Plattformunterscheidung Linux/Windows sowie die Nutzung einer Zertifikatsdatei (V3.0.2. 15.05.2017)
	#	Falls erneut erforderlich s. https://stackoverflow.com/questions/1087227/validate-ssl-certificates-with-python/28325763#28325763
	apiToken2 = 'Bearer ' + str(Dict['apiToken2'])		# s. GetZDFVideoSources. str falls None
	# headers = {'Api-Auth': "Bearer d2726b6c8c655e42b68b0db26131b15b22bd1a32",'Host':"api.zdf.de", 'Accept-Encoding':"gzip, deflate, sdch, br", 'Accept':"application/vnd.de.zdf.v1.0+json"}
	headers = {'Api-Auth': apiToken2,'Host':"api.zdf.de", 'Accept-Encoding':"gzip, deflate, sdch, br", 'Accept':"application/vnd.de.zdf.v1.0+json"}
	Log('apiToken2: ' + apiToken2)
	try:
		request = JSON.ObjectFromURL(videodat_url, headers=headers)				
		request = json.dumps(request, sort_keys=True, indent=2, separators=(',', ': '))  # sortierte Ausgabe
		request = str(request)				# json=dict erlaubt keine Stringsuche, json.dumps klappt hier nicht
		page = request.decode('utf-8', 'ignore')
	except:
		page = ""

	if page == '':	# Alternative ngplayer_2_3 versuchen
		try:
			request = JSON.ObjectFromURL(old_videodat_url, headers=headers)				
			request = json.dumps(request, sort_keys=True, indent=2, separators=(',', ': '))  # sortierte Ausgabe
			request = str(request)				# json=dict erlaubt keine Stringsuche, json.dumps klappt hier nicht
			page = request.decode('utf-8', 'ignore')
		except:
			page = ""
		
		Log('videodat_url: Laden fehlgeschlagen')
		return '', '', ''
	Log(page[:20])	# "{..attributes" ...
		
	'''
	subtitles = stringextract('\"captions\"', '\"documentVersion\"', page)	# Untertitel ermitteln, bisher in Plex-
	subtitles = blockextract('\"class\"', subtitles)						# Channels nicht verwendbar
	Log('subtitles: ' + str(len(subtitles)))
	if len(subtitles) == 2:
		sub_xml = subtitles[0]
		sub_vtt = subtitles[1]
		#Log(sub_xml);Log(sub_vtt);
		sub_xml_path = stringextract('\"uri\": \"', '\"', sub_xml)
		sub_vtt_path = stringextract('\"uri\": \"', '\"', sub_vtt)
		Log('Untertitel xml + vtt:');Log(sub_xml_path);Log(sub_vtt_path);
	'''
	# Fehler "crossdomain access denied" bei .m3u8-Dateien: Ursache https-Verbindung - konkrete Wechselwirkung n.b.
	#	div. Versuche mit Änderungen der crossdomain.xml in Plex erfolglos,
	#	dto. Eintrag des Servers zdfvodnone-vh.akamaihd.net in der hosts-Datei.
	#	Abhilfe: https -> http beim m3u8-Link in show_formitaeten - klappt bei allen angebotenen Formaten
	#	
	duration = stringextract('duration',  'fsk', page)	# Angabe im Kopf, sec/1000
	duration = stringextract('"value":',  '}', duration).strip()
	Log(duration)	
	if duration:
		duration = (int(duration) / 1000) / 60			# Rundung auf volle Minuten reicht hier 
		duration = str(duration) + " min"	
	Log('duration: ' + duration)		
	formitaeten = blockextract('formitaeten', page)		# Video-URL's ermitteln
	geoblock =  stringextract('geoLocation',  '}', page) 
	geoblock =  stringextract('"value": "',  '"', geoblock).strip()
	Log('geoblock: ' + geoblock)									# i.d.R. "none", sonst "de" - wie bei ARD verwenden
	if geoblock == 'de':			# Info-Anhang für summary 
		geoblock = ' | Geoblock!'
	else:
		geoblock = ''

	return formitaeten, duration, geoblock 

#-------------------------
# 	Ausgabe der Videoformate
#	
def show_formitaeten(oc, title_call, formitaeten, tagline, thumb, only_list, geoblock):	
	Log('show_formitaeten')
	Log(only_list)
	# Log(formitaeten)		# bei Bedarf
	
	i = 0 	# Titel-Zähler für mehrere Objekte mit dem selben Titel (manche Clients verwerfen solche)
	download_list = []		# 2-teilige Liste für Download: 'summary # url'	
	for rec in formitaeten:									# Datensätze gesamt
		# Log(rec)		# bei Bedarf
		typ = stringextract('"type": "', '"', rec)
		typ = typ.replace('[]', '').strip()
		facets = stringextract('"facets": ', ',', rec)	# Bsp.: "facets": ["progressive"]
		facets = facets.replace('"', '').replace('\n', '').replace(' ', '') 
		Log(typ); Log(facets)
		
		# Log(typ in only_list)
		if (typ in only_list) == True:								
			audio = blockextract('"audio":', rec)			# Datensätze je Typ
			# Log(audio)	# bei Bedarf
			for audiorec in audio:					
				url = stringextract('"uri": "',  '"', audiorec)			# URL
				url = url.replace('https', 'http')
				quality = stringextract('"quality": "',  '"', audiorec)
				Log(url); Log(quality);
				i = i +1
				if url:			
					if url.find('master.m3u8') > 0:		# 
						title=str(i) + '. ' + title_call + ' | ' + quality + ' [m3u8]'
						summary = 'Qualität: ' + quality + ' | Typ: ' + typ + ' [m3u8-Streaming]'
						summary = summary.decode(encoding="utf-8", errors="ignore")
						oc.add(CreateVideoStreamObject(url=url, title=title, rtmp_live='nein', summary=summary+geoblock, 
							tagline=tagline, meta=Plugin.Identifier + str(i), thumb=thumb, resolution='unbekannt'))	
					else:
						title=str(i) + '. ' + title_call + ' | ' + quality	
						summary = 'Qualität: ' + quality + ' | Typ: ' + typ + ' ' + facets 
						summary = summary.decode(encoding="utf-8", errors="ignore")
						download_list.append(summary + '#' + url)					# Download-Liste füllen				
						oc.add(CreateVideoClipObject(url=url, title=title, summary=summary+geoblock,
							meta= Plugin.Identifier + str(i), tagline=tagline, thumb=thumb, 
							duration='duration', resolution='unbekannt'))
					
	return oc, download_list
#-------------------------
def ZDF_Bildgalerie(oc, page, mode, title):	# keine Bildgalerie, aber ähnlicher Inhalt
	Log('ZDF_Bildgalerie'); Log(mode); Log(title)
	
	if mode == 'is_gallery':							# "echte" Bildgalerie
		content =  stringextract('class=\"content-box gallery-slider-box', 'title=\"Bilderserie schließen\"', page)
		content =  blockextract('class=\"img-container', content)   					# Bild-Datensätze
	if mode == 'pics_in_accordion-panels':				# Bilder in Klappboxen	
		content =  stringextract('class=\"b-group-contentbox\"', '</section>', page)
		content =  blockextract('class=\"accordion-panel\"', content)
	if mode == '<article class="b-group-persons">':		# ZDF-Korrespondenten, -Mitarbeiter,...	
		content = page	
		content =  blockextract('guest-info m-clickarea', content)
			
	Log(len(content))
	# neuer Container mit neuem Titel
	title = title.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(title2=title, view_group="InfoList")

	image = 1
	for rec in content:
		# Log(rec)  # bei Bedarf
		summ = ''; 
		if mode == 'is_gallery':				# "echte" Bildgalerie
			img_src =  stringextract('data-srcset="', ' ', rec)			
			item_title = stringextract('class="item-title', 'class="item-description">', rec)  
			teaser_cat =  stringextract('class="teaser-cat">', '</span>', item_title)  
			teaser_cat = teaser_cat.strip()			# teaser_cat hier ohne itemprop
			if teaser_cat.find('|') > 0:  			# über 3 Zeilen verteilt
				tclist = teaser_cat.split('|')
				teaser_cat = str.strip(tclist[0]) + ' | ' + str.strip(tclist[1])			# zusammenführen
			#Log(teaser_cat)					
			descript = stringextract('class=\"item-description\">', '</p', rec)
			pos = descript.find('<span')			# mögliche Begrenzer: '</p', '<span'
			if pos >= 0:
				descript = descript[0:pos]
			descript = descript.strip()
			#Log(descript)					

			title_add = stringextract('data-plusbar-title=\"', ('\"'), rec)	# aus Plusbar - im Teaser schwierig
			title = teaser_cat
			if title_add:
				title = title + ' |' + title_add
			if title.startswith(' |'):
				title = title[2:]				# Korrektur
			if descript:		
				summ = descript
				
		if mode == 'pics_in_accordion-panels':				# Bilder in Klappboxen
			img_src =  stringextract('data-srcset=\"', ' ', rec)
			title =  stringextract('class=\"shorter\">', '<br/>', rec) 
			summ = stringextract('p class=\"text\">', '</p>', rec) 		
			summ = cleanhtml(summ)
		
		if mode == '<article class=\"b-group-persons\">':
			img_src = stringextract('data-src=\"', '\"', rec)
			
			guest_name =  stringextract('trackView\": true}\'>', '</button>', rec)
			guest_name = guest_name.strip()
			guest_title =  stringextract('guest-title\"><p>', '</p>', rec)
			guest_title = unescape(guest_title)
			title = guest_name + ': ' + guest_title						
			summ = stringextract('desc-text\">', '</p>', rec)
			summ = summ.strip()
			summ = cleanhtml(summ)
			
		if img_src == '':									# Sicherung			
			msgH = 'Error'; msg = 'Problem in Bildgalerie: Bild nicht gefunden'
			Log(msg)
			msg =  msg.decode(encoding="utf-8", errors="ignore")
			return ObjectContainer(header=msgH, message=msg)
					
		title = unescape(title); title = cleanhtml(title)
		title = title.decode(encoding="utf-8", errors="ignore")
		summ = unescape(summ)
		summ = summ .decode(encoding="utf-8", errors="ignore")
		Log('neu');Log(title);Log(img_src);Log(summ[0:40]);
		oc.add(PhotoObject(
			key=img_src,
			rating_key='%s.%s' % (Plugin.Identifier, 'Bild ' + str(image)),	# rating_key = eindeutige ID
			summary=summ,
			title=title,
			thumb = img_src
			))
		image += 1
	return oc	
	
#-------------------------
####################################################################################################
#									Hilfsfunktionen
####################################################################################################
def Parseplaylist(container, url_m3u8, thumb, geoblock, **kwargs):	# master.m3u8 auswerten, Url muss komplett sein
#													# container muss nicht leer ein (siehe SingleSendung)
#  1. Besonderheit: in manchen *.m3u8-Dateien sind die Pfade nicht vollständig,
#	sondern nur als Ergänzung zum Pfadrumpf (ohne Namen + Extension) angegeben, Bsp. (Arte):
#	delive/delive_925.m3u8, url_m3u8 = http://delive.artestras.cshls.lldns.net/artestras/contrib/delive.m3u8
#	Ein Zusammensetzen verbietet sich aber, da auch in der ts-Datei (z.B. delive_64.m3u8) nur relative 
#	Pfade angegeben werden. Beim Redirect des Videoplays zeigt dann der Pfad auf das Plugin und Plex
#	versucht die ts-Stücke in Dauerschleife zu laden.
#	Wir prüfen daher besser auf Pfadbeginne mit http:// und verwerfen Nichtpassendes - auch wenn dabei ein
#	Sender komplett ausfällt.
#	Lösung ab April 2016:  Sonderbehandlung Arte in Arteplaylists.						
#	ARTE ab 10.03.2017:	 die m3u8-Links	enthalten nun komplette Pfade. Allerdings ist SSL-Handshake erforderlich zum
#		Laden der master.m3u8 erforderlich (s.u.). Zusätzlich werden in	CreateVideoStreamObject die https-Links durch 
#		http ersetzt (die Streaming-Links funktionieren auch mit http).	
#		SSL-Handshake für ARTE ist außerhalb von Plex nicht notwendig!
#  2. Besonderheit: fast identische URL's zu einer Auflösung (...av-p.m3u8, ...av-b.m3u8) Unterschied n.b.
#  3. Besonderheit: für manche Sendungen nur 1 Qual.-Stufe verfügbar (Bsp. Abendschau RBB)
#  4. Besonderheit: manche Playlists enthalten zusätzlich abgeschaltete Links, gekennzeichnet mit #. Fehler Webplayer:
#		 crossdomain access denied. Keine Probleme mit OpenPHT und VLC
#  10.08.2017 Filter für Video-Sofort-Format - wieder entfernt 17.02.2018

  Log ('Parseplaylist: ' + url_m3u8)
  playlist = ''
  # seit ZDF-Relaunch 28.10.2016 dort nur noch https
  if url_m3u8.find('http://') == 0 or url_m3u8.find('https://') == 0:		# URL oder lokale Datei?	
	try:
		if url_m3u8.find('https://') == 0:						# HTTPS: mit SSL-Handshake laden (für Arte erforderlich)	
			req = urllib2.Request(url_m3u8)
			gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)		
			r = urllib2.urlopen(req, context=gcontext)
			playlist = r.read()			
		else:
			playlist = HTTP.Request(url_m3u8).content  			# HTTP: konventionell laden			
	except Exception as exception:
			msg = 'Playlist kann nicht geladen werden. URL: | %s | %s'	% (url_m3u8, str(exception))
			msg = msg + url_m3u8
			Log(msg)
			return ObjectContainer(header=L('Error'), message=msg)	  	# header=... ohne Wirkung	(?)			
  else:													
	playlist = Resource.Load(url_m3u8) 
	 
  # Log(playlist)		# bei Bedarf
  lines = playlist.splitlines()
  lines.pop(0)		# 1. Zeile entfernen (#EXTM3U)
  BandwithOld 	= ''	# für Zwilling -Test (manchmal 2 URL für 1 Bandbreite + Auflösung) 
  thumb_org		= thumb # sichern
  i = 0
  #for line in lines[1::2]:	# Start 1. Element, step 2
  for line in lines:	
 	line = lines[i].strip()
 	# Log(line)		# bei Bedarf
	if line.startswith('#EXT-X-STREAM-INF'):# tatsächlich m3u8-Datei?
		url = lines[i + 1].strip()	# URL in nächster Zeile
		Log(url)

		Bandwith = GetAttribute(line, 'BANDWIDTH')
		Resolution = GetAttribute(line, 'RESOLUTION')
		try:
			BandwithInt	= int(Bandwith)
		except:
			BandwithInt = 0
		if Resolution:	# fehlt manchmal (bei kleinsten Bandbreiten)
			Resolution = 'Auflösung ' + Resolution
		else:
			Resolution = 'Auflösung unbekannt'	# verm. nur Ton? CODECS="mp4a.40.2"
		Codecs = GetAttribute(line, 'CODECS')
		# als Titel wird die  < angezeigt (Sender ist als thumb erkennbar)
		title='Bandbreite ' + Bandwith
		if url.find('#') >= 0:	# Bsp. SR = Saarl. Rundf.: Kennzeichnung für abgeschalteten Link
			Resolution = 'zur Zeit nicht verfügbar!'
		if url.startswith('http') == False:   		# relativer Pfad? 
			pos = url_m3u8.rfind('/')				# m3u8-Dateinamen abschneiden
			url = url_m3u8[0:pos+1] + url 			# Basispfad + relativer Pfad
		if Bandwith == BandwithOld:	# Zwilling -Test
			title = 'Bandbreite ' + Bandwith + ' (2. Alternative)'
			
		Log(thumb); Log(Resolution); Log(BandwithInt); 
		thumb=thumb_org
		if BandwithInt and BandwithInt <=  100000: 		# vermutl. nur Audio (Bsp. ntv 48000, ZDF 96000)
			Resolution = Resolution + ' (vermutlich nur Audio)'
			thumb=R(ICON_SPEAKER)
		container.add(CreateVideoStreamObject(url=url, title=title, 		
			summary=Resolution+geoblock, tagline=title, meta=Codecs, thumb=thumb, 	
			rtmp_live='nein', resolution=''))
						
		BandwithOld = Bandwith												

  	i = i + 1	# Index für URL
  #Log (len(container))	# Anzahl Elemente
  if len(container) == 0:	# Fehler, zurück zum Hauptmenü
  		container.add(DirectoryObject(key=Callback(Main),  title='inkompatible m3u8-Datei', 
			tagline='Kennung #EXT-X-STREAM-INF fehlt oder den Pfaden fehlt http / https', thumb=thumb)) 
	
  return container

#----------------------------------------------------------------  
def GetAttribute(text, attribute, delimiter1 = '=', delimiter2 = ','):
# Bsp.: #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=61000,CODECS="mp4a.40.2"

    if attribute == 'CODECS':	# Trenner = Komma, nur bei CODEC ist Inhalt 'umrahmt' 
    	delimiter1 = '="'
    	delimiter2 = '"'
    x = text.find(attribute)
    if x > -1:
        y = text.find(delimiter1, x + len(attribute)) + len(delimiter1)
        z = text.find(delimiter2, y)
        if z == -1:
            z = len(text)
        return unicode(text[y:z].strip())
    else:
        return ''

#----------------------------------------------------------------  
def NotFound(msg):
	msg = msg.decode(encoding="utf-8", errors="ignore")
	return ObjectContainer(
		header=u'%s' % L('Error'),
		message=u'%s' % (msg)
	)

#----------------------------------------------------------------  
def CalculateDuration(timecode):
	milliseconds = 0
	hours        = 0
	minutes      = 0
	seconds      = 0
	d = re.search('([0-9]{1,2}) min', timecode)
	if(None != d):
		minutes = int( d.group(1) )
	else:
		d = re.search('([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2}).([0-9]{1,3})', timecode)
		if(None != d):
			hours = int ( d.group(1) )
			minutes = int ( d.group(2) )
			seconds = int ( d.group(3) )
			milliseconds = int ( d.group(4) )
	milliseconds += hours * 60 * 60 * 1000
	milliseconds += minutes * 60 * 1000
	milliseconds += seconds * 1000
	return milliseconds
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
	#	blockmark bleibt Bestandteil der Rückgabe - im Unterschied zu split()
	#	Rückgabe in Liste. Letzter Block reicht bis Ende mString (undefinierte Länge),
	#		Variante mit definierter Länge siehe Plex-Plugin-TagesschauXL (extra Parameter blockendmark)
	#	Verwendung, wenn xpath nicht funktioniert (Bsp. Tabelle EPG-Daten www.dw.com/de/media-center/live-tv/s-100817)
	rlist = []				
	if 	blockmark == '' or 	mString == '':
		Log('blockextract: blockmark or mString leer')
		return rlist
	
	pos = mString.find(blockmark)
	if 	mString.find(blockmark) == -1:
		Log('blockextract: blockmark <%s> nicht in mString enthalten' % blockmark)
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
def repl_dop(liste):	# Doppler entfernen, im Python-Script OK, Problem in Plex - s. PageControl
	mylist=liste
	myset=set(mylist)
	mylist=list(myset)
	mylist.sort()
	return mylist
#----------------------------------------------------------------  
def transl_umlaute(line):	# Umlaute übersetzen, wenn decode nicht funktioniert
	line_ret = line
	line_ret = line_ret.replace("Ä", "Ae", len(line_ret))
	line_ret = line_ret.replace("ä", "ae", len(line_ret))
	line_ret = line_ret.replace("Ü", "Ue", len(line_ret))
	line_ret = line_ret.replace('ü', 'ue', len(line_ret))
	line_ret = line_ret.replace("Ö", "Oe", len(line_ret))
	line_ret = line_ret.replace("ö", "oe", len(line_ret))
	line_ret = line_ret.replace("ß", "ss", len(line_ret))	
	return line_ret
#----------------------------------------------------------------  
def repl_char(cut_char, line):	# problematische Zeichen in Text entfernen, wenn replace nicht funktioniert
	line_ret = line				# return line bei Fehlschlag
	pos = line_ret.find(cut_char)
	while pos >= 0:
		line_l = line_ret[0:pos]
		line_r = line_ret[pos+len(cut_char):]
		line_ret = line_l + line_r
		pos = line_ret.find(cut_char)
		#Log(cut_char); Log(pos); Log(line_l); Log(line_r); Log(line_ret)	# bei Bedarf	
	return line_ret
#----------------------------------------------------------------  	
def unescape(line):	# HTML-Escapezeichen in Text entfernen, bei Bedarf erweitern. ARD auch &#039; statt richtig &#39;
#					# s.a.  ../Framework/api/utilkit.py
	line_ret = (line.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
		.replace("&#39;", "'").replace("&#039;", "'").replace("&quot;", '"').replace("&#x27;", "'")
		.replace("&ouml;", "ö").replace("&auml;", "ä").replace("&uuml;", "ü").replace("&szlig;", "ß")
		.replace("&Ouml;", "Ö").replace("&Auml;", "Ä").replace("&Uuml;", "Ü").replace("&apos;", "'"))
		
	# Log(line_ret)		# bei Bedarf
	return line_ret	
#----------------------------------------------------------------  	
def cleanhtml(line): # ersetzt alle HTML-Tags zwischen < und >  mit 1 Leerzeichen
	cleantext = line
	cleanre = re.compile('<.*?>')
	cleantext = re.sub(cleanre, ' ', line)
	return cleantext
#----------------------------------------------------------------  	
def mystrip(line):	# eigene strip-Funktion, die auch Zeilenumbrüche innerhalb des Strings entfernt
	line_ret = line	
	line_ret = line.replace('\t', '').replace('\n', '').replace('\r', '')
	line_ret = line_ret.strip()	
	# Log(line_ret)		# bei Bedarf
	return line_ret
#---------------------------------------------------------------- 
def make_filenames(title):
	# erzeugt - hoffentlich - sichere Dateinamen (ohne Extension)
	# zugeschnitten auf Titelerzeugung in meinen Plugins 
	
	fname = transl_umlaute(title)		# Umlaute
	# Ersatz: 	Leerz., Pipe, mehrf. Unterstriche -> 1 Unterstrich, Doppelp. -> Bindestrich	
	#			+ /  -> Bindestrich	
	# Entferne: Frage-, Ausrufez., Hochkomma, Komma und #@!%^&*()
	fname = (fname.replace(' ','_').replace('|','_').replace('___','_').replace('.','_')) 
	fname = (fname.replace('__','_').replace(':','-'))
	fname = (fname.replace('?','').replace('!','').replace('"','').replace('#','')
		.replace('*','').replace('@','').replace('%','').replace('^','').replace('&','')
		.replace('(','').replace(')','').replace(',','').replace('+','-').replace('/','-'))	
	
	# Die Variante .join entfällt leider, da die Titel hier bereits
	# in Unicode ankommen -	Plex code/sandbox.py:  
	# 		'str' object has no attribute '__iter__': 
	# valid_chars = "-_ %s%s" % (string.ascii_letters, string.digits)
	# fname = ''.join(c for c in fname if c in valid_chars)
	return fname
#----------------------------------------------------------------  
		
####################################################################################################
# Directory-Browser - Verzeichnis-Listing
#	Vorlage: Funktion DirectoryNavigator aus Caster (https://github.com/MrHistamine/Caster - nur Windows)
#	Blättert in Verzeichnissen, filtert optional nach Dateinamen
#	Für Filterung nach Dateitypen ev. Filterung nach Mimetypen nachrüsten (hier nicht benötigt)
#		S. http://stackoverflow.com/questions/10263436/better-more-accurate-mime-type-detection-in-python
#	 	Die plattformübergreifende Python-Lösung mimetypes steht unter Plex nicht zur Verfügung. 
#	fileFilter = 'DIR'  = Verzeichnissuche	(alle Plattformen)
#	fileFilter = 'Muster' = Suche nach Muster im Dateinamen (z.B. 'curl') 
#	 
@route(PREFIX + '/DirectoryNavigator')
def DirectoryNavigator(settingKey, newDirectory = None, fileFilter=None):
	Log('settingKey: ' + settingKey); Log('newDirectory: ' + str(newDirectory)); 
	Log('fileFilter: ' + str(fileFilter))
	Log('Plattform: ' + sys.platform)

	# Bei leerer Verz.-Angabe setzen wir abhängig vom System / bzw. c:\ 
	# Windows?: http://stackoverflow.com/questions/1325581/how-do-i-check-if-im-running-on-windows-in-python
	ROOT_DIRECTORY = os.path.abspath(os.sep)	# s. http://stackoverflow.com/questions/12041525
	if sys.platform.startswith('win'):			
		ROOT_DIRECTORY = get_sys_exec_root_or_drive() 
		 
	if(newDirectory is not None or newDirectory is ''):
		containerTitle = newDirectory
	else:
		containerTitle = ROOT_DIRECTORY
		newDirectory = ROOT_DIRECTORY
	Log('ROOT_DIRECTORY: ' + ROOT_DIRECTORY)
		
	oc = ObjectContainer(view_group = 'InfoList', art = R(ART), title1 = containerTitle, no_cache = True)
	oc= home(cont=oc, ID=NAME)						# Home-Button - Rücksprung Pluginstart 
		
	ParentDir = os.path.dirname(newDirectory)		# übergeordnetes Verz. ermitteln
	if os.path.isdir(newDirectory) == False:		# 	dto. bei Pfad/Datei
		ParentDir = os.path.dirname(ParentDir)
	Log('ParentDir: ' + ParentDir)

	# DirSep = os.sep	# Log(DirSep)				# Seperatoren nicht benötigt
	if newDirectory:								# Button Back
		Log.Debug('Button Back: ' + ParentDir)
		summary = 'zum übergeordneten Ordner wechseln: ' + ParentDir
		summary = summary.decode(encoding="utf-8", errors="ignore")
		title = summary
		oc.add(DirectoryObject(key = Callback(DirectoryNavigator, settingKey = settingKey, newDirectory = ParentDir, 
			fileFilter = fileFilter), title =title, summary=summary, thumb = R(ICON_DIR_BACK)))
	else:
		newDirectory = ROOT_DIRECTORY
    
	basePath = newDirectory
	Log('basePath: ' + basePath)
	try:
		if os.path.isdir(basePath):
			subItems = os.listdir(basePath)			# Verzeichnis auslesen
		else:										# Dateiname -> Verz. ermitteln
			Dir = os.path.dirname(os.path.abspath(basePath)) 
			subItems = os.listdir(Dir)
		subItems.sort()
		# Log.Debug(subItems)						# bei Bedarf
		Log.Debug(len(subItems))					# Windows: ohne .Debug hier keine Ausgabe
	except Exception as exception:
		error_txt = 'Verzeichnis-Problem | ' + str(exception)			 			 	 
		msgH = 'Fehler'; msg = error_txt
		msg =  msg.decode(encoding="utf-8", errors="ignore")
		Log(msg)
		return ObjectContainer(header=msgH, message=msg)
	
	# Beim Filter 'DIR' wird ein Button zum Speichern des akt. Verz. voran gestellt, 
	#	die emthaltenen Unterverz. gelistet. Jedes Unterverz erhält einen Callback.
	# 
	Log(fileFilter)
	if fileFilter == 'DIR':							# bei Verzeichnissuche akt. Verz. zum Speichern anbieten
		summary = 'Klicken zum Speichern | Ordner: ' + basePath
		title = summary
		Log(summary);Log(basePath);
		oc.add(DirectoryObject(key = Callback(SetPrefValue, key = settingKey, value = basePath),
			title=title, summary=summary, thumb = R(ICON_DIR_SAVE)))

	for item in subItems:							# Verzeichniseinträge mit Filter listen
		fullpath = os.path.join(basePath, item)
		isDir = os.path.isdir(fullpath)
		# Log(isDir); Log(fullpath)
		if fileFilter != 'DIR':						# nicht Verzeichnissuche
			if isDir == False:						# und kein Unterverzeichnis -> Suche nach Eintrag
				# Log.Debug('Suche nach: ' + fileFilter + ' in ' + basePath + item)
				filterlist = fileFilter.split('|')
				for ffilter in filterlist:
					if item.find(ffilter) >= 0:			# Filter passt
						summary = 'Klicken zum Speichern | Datei: ' + item
						title = summary
						value = os.path.join(basePath, item) 
						oc.add(DirectoryObject(key = Callback(SetPrefValue, key = settingKey, value = value),
							title = item, summary=summary, thumb = R(ICON_DIR_SAVE)))
			else:									# Button für Unterverzeichnisse
				Log.Debug('Setze Verzeichniseintrag:  ' + basePath + item)
				newDirectory = os.path.join(basePath, item)  # + DirSep
				oc.add(DirectoryObject(key = Callback(DirectoryNavigator, settingKey = settingKey, 
					newDirectory = newDirectory, fileFilter=fileFilter), title=item, 
					thumb =R(ICON_DIR_FOLDER)))			
						
		else:										# Verzeichnissuche: Unterverzeichnis -> neuer Button
			if isDir == True:	
				# Log.Debug('Setze Verzeichniseintrag:  ' + basePath + item)
				newDirectory = os.path.join(basePath, item)  # + DirSep
				oc.add(DirectoryObject(key = Callback(DirectoryNavigator, settingKey = settingKey, 
					newDirectory = newDirectory, fileFilter = fileFilter), title = item, 
					thumb = R(ICON_DIR_FOLDER)))			
	return oc

#-------------------
def get_sys_exec_root_or_drive():
    path = sys.executable
    while os.path.split(path)[1]:
        path = os.path.split(path)[0]
    return path
    
####################################################################################################
# allgemeine Funktion zum Setzen von Einstellungen
#
@route(PREFIX + '/SetPrefValue')
def SetPrefValue(key, value):
    if((key is not "") and (value is not "")):
		# Dict[key] = value
		# Dict.Save() 		# funktioniert nicht
		HTTP.Request("%s/:/plugins/%s/prefs/set?%s=%s" % (myhost, Plugin.Identifier, key, value), immediate=True)
		Log.Debug('Einstellung  >' + key  + '< gespeichert. Neuer Wert: ' + value)
    return Main()

