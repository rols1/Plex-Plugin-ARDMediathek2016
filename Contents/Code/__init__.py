# -*- coding: utf-8 -*-
import string
import random			# Zufallswerte für rating_key
import urllib			# urllib.quote(), 
import urllib2			# urllib2.Request
import ssl				# HTTPS-Handshake
import os, subprocess 	# u.a. Behandlung von Pfadnamen
import sys				# Plattformerkennung
import shutil			# Dateioperationen
import re				# u.a. Reguläre Ausdrücke, z.B. in CalculateDuration
import time
import datetime
import json				# json -> Textstrings

import locale
import updater
import EPG


# +++++ ARD Mediathek 2016 Plugin for Plex +++++

VERSION =  '3.3.1'		
VDATE = '07.11.2017'

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
ICON_MAIN_TVLIVE 		= 'tv-livestreams.png'		
ICON_MAIN_RADIOLIVE 	= 'radio-livestreams.png' 	
ICON_MAIN_UPDATER 		= 'plugin-update.png'		
ICON_UPDATER_NEW 		= 'plugin-update-new.png'
ICON_PREFS 				= 'plugin-preferences.png'


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
ICON_ARD_NEUESTE 		= 'ard-neueste-videos.png' 	
ICON_ARD_BEST 			= 'ard-am-besten-bewertet.png' 	

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
ICON_WARNING 			= "icon-warning.png"
ICON_NEXT 				= "icon-next.png"
ICON_CANCEL 			= "icon-error.png"
ICON_MEHR 				= "icon-mehr.png"
ICON_DOWNL 				= "icon-downl.png"
ICON_DOWNL_DIR			= "icon-downl-dir.png"
ICON_DELETE 			= "icon-delete.png"
ICON_STAR 				= "icon-star.png"
ICON_NOTE 				= "icon-note.png"

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



BASE_URL 		= 'http://www.ardmediathek.de'
ARD_VERPASST 	= '/tv/sendungVerpasst?tag='								# ergänzt mit 0, 1, 2 usw.
ARD_AZ 			= '/tv/sendungen-a-z?buchstabe='							# ergänzt mit 0-9, A, B, usw.
ARD_Suche 		= '/tv/suche?searchText=%s&words=and&source=tv&sort=date'	# Vorgabe UND-Verknüpfung
ARD_Live 		= '/tv/live'

# Aktualisierung der ARD-ID's in Update_ARD_Path
ARD_Rubriken 	= 'http://www.ardmediathek.de/tv/Rubriken/mehr?documentId=21282550'
ARD_Themen 		= 'http://www.ardmediathek.de/tv/Themen/mehr?documentId=21301810'
ARD_Serien 		= 'http://www.ardmediathek.de/tv/Serien/mehr?documentId=26402940'
ARD_Dokus 		= 'http://www.ardmediathek.de/tv/Ausgew%C3%A4hlte-Dokus/mehr?documentId=33649086'
ARD_DokusAll	= 'http://www.ardmediathek.de/tv/Alle-Dokus-Reportagen/mehr?documentId=29897594'
ARD_Filme 		= 'http://www.ardmediathek.de/tv/Ausgew%C3%A4hlte-Filme/mehr?documentId=33649088'
ARD_FilmeAll 	= 'http://www.ardmediathek.de/tv/Alle-Filme/mehr?documentId=31610076'
ARD_Meist 		= 'http://www.ardmediathek.de/tv/Meistabgerufene-Videos/mehr?documentId=23644244'
ARD_Neu 		= 'http://www.ardmediathek.de/tv/Neueste-Videos/mehr?documentId=21282466'
ARD_Best 		= 'http://www.ardmediathek.de/tv/Am-besten-bewertet/mehr?documentId=21282468'
ARD_RadioAll 	= 'http://www.ardmediathek.de/radio/live?genre=Alle+Genres&kanal=Alle'

# ARD-Podcasts
POD_SEARCH  = '/suche?source=radio&sort=date&searchText=%s&pod=on&playtime=all&words=and&to=all='
POD_AZ 		= 'http://www.ardmediathek.de/radio/sendungen-a-z?sendungsTyp=podcast&buchstabe=' 
POD_RUBRIK 	= 'http://www.ardmediathek.de/radio/Rubriken/mehr?documentId=37981136'
POD_FEATURE = 'http://www.ardmediathek.de/radio/das-ARD-radiofeature/Sendung?documentId=3743362&bcastId=3743362'
POD_TATORT 	= 'http://www.ardmediathek.de/radio/ARD-Radio-Tatort/Sendung?documentId=1998988&bcastId=1998988'
POD_NEU 	= 'http://www.ardmediathek.de/radio/Neueste-Audios/mehr?documentId=23644358'
POD_MEIST 	= 'http://www.ardmediathek.de/radio/Meistabgerufene-Audios/mehr?documentId=23644364'
POD_REFUGEE = 'http://www1.wdr.de/radio/cosmo/programm/refugee-radio/refugee-radio-112.html'	# z.Z. Refugee Radio via Suche

# Relaunch der Mediathek beim ZDF ab 28.10.2016: xml-Service abgeschaltet
ZDF_BASE				= 'https://www.zdf.de'
# ZDF_Search_PATH: siehe ZDF_Search, ganze Sendungen, sortiert nach Datum, bei Bilderserien ohne ganze Sendungen
ZDF_SENDUNG_VERPASST 	= 'https://www.zdf.de/sendung-verpasst?airtimeDate=%s'  # Datumformat 2016-10-31
ZDF_SENDUNGEN_AZ		= 'https://www.zdf.de/sendungen-a-z?group=%s'			# group-Format: a,b, ... 0-9: group=0+-+9
ZDF_WISSEN				='https://www.zdf.de/doku-wissen'						# Basis für Ermittlung der Rubriken
ZDF_SENDUNGEN_MEIST		= 'https://www.zdf.de/meist-gesehen'
ZDF_BARRIEREARM			= 'https://www.zdf.de/barrierefreiheit-im-zdf'
# 26.02.2017 alternative Seiten (vollständig im Vergleich mit Web-Version?): 
#	https://config-cdn.cellular.de/zdf/mediathek/config/android/4_0/zdf_mediathek_android_live_4_0.json
#	Siehe https://github.com/raptor2101/Mediathek/issues/85 Kodi-Plugin Mediathek

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
	# folgendes DirectoryObject ist Deko für das nicht sichtbare InputDirectoryObject dahinter:
	oc.add(DirectoryObject(key=Callback(Main_ARD, name="ARD Mediathek"), title="ARD Mediathek",
		summary='', tagline='TV', thumb=R(ICON_MAIN_ARD)))
		
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
	if call_update == False:							# Update-Button "Suche" zeigen	
		title = 'Plugin-Update | akt. Version: ' + VERSION + ' vom ' + VDATE	
		summary='Suche nach neuen Updates starten'
		tagline='Bezugsquelle: ' + repo_url			
		oc.add(DirectoryObject(key=Callback(SearchUpdate, title='Plugin-Update'), 
			title=title, summary=summary, tagline=tagline, thumb=R(ICON_MAIN_UPDATER)))
		
	oc.add(DirectoryObject(key = Callback(Main_Options, title='Einstellungen'), title = 'Einstellungen', 
		summary = 'Live-TV-Sender: EPG-Daten verwenden, verfuegbare Bandbreiten anzeigen', 
		tagline = 'Die Downloadeinstellungen bitte im Webplayer vornehmen',
		thumb = R(ICON_PREFS)))
					
	return oc
	
#----------------------------------------------------------------
@route(PREFIX + '/Main_ARD')
def Main_ARD(name):
	Log('Funktion Main_ARD'); Log(PREFIX); Log(VERSION); Log(VDATE)	
	oc = ObjectContainer(view_group="InfoList", art=ObjectContainer.art)	
	oc = home(cont=oc, ID=NAME)							# Home-Button
		
	
	# Web-Player: folgendes DirectoryObject ist Deko für das nicht sichtbare InputDirectoryObject dahinter:
	oc.add(DirectoryObject(key=Callback(Main_ARD, name=name),title='Suche: im Suchfeld eingeben', 
		summary='', tagline='TV', thumb=R(ICON_SEARCH)))
	oc.add(InputDirectoryObject(key=Callback(Search,  channel='ARD', s_type='video', title=u'%s' % L('Search Video')),
		title=u'%s' % L('Search'), prompt=u'%s' % L('Search Video'), thumb=R(ICON_SEARCH)))
		
	title = 'Sendung verpasst (1 Woche)'
	oc.add(DirectoryObject(key=Callback(VerpasstWoche, name='ARD', title='Sendung verpasst', sender='DAS ERSTE', 
		kanal='208'), title=title, summary=title, tagline='TV', thumb=R(ICON_ARD_VERP)))
	title = 'Sendungen A-Z'
	oc.add(DirectoryObject(key=Callback(SendungenAZ, name='Sendungen 0-9 | A-Z', ID='ARD'), 
		title='Sendungen A-Z', summary=title, tagline='TV', thumb=R(ICON_ARD_AZ)))
						
		
	title = 'Ausgewählte Filme'.decode(encoding="utf-8", errors="ignore")
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Filme, next_cbKey='SingleSendung', ID='ARD'),
		title=title,summary=title, tagline='TV', thumb=R(ICON_ARD_Filme)))
	title = 'Alle Filme'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_FilmeAll, next_cbKey='SingleSendung', ID='ARD'),
		title=title,summary=title, tagline='TV', thumb=R(ICON_ARD_FilmeAll)))
	title = 'Ausgewählte Dokus'.decode(encoding="utf-8", errors="ignore")
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Dokus, next_cbKey='SingleSendung', ID='ARD'), 
		title=title,summary=title, tagline='TV', thumb=R(ICON_ARD_Dokus)))
	title = 'Alle Dokus'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_DokusAll, next_cbKey='SingleSendung', ID='ARD'),
		title=title,summary=title, tagline='TV', thumb=R(ICON_ARD_DokusAll)))
	title = 'Themen'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Themen, next_cbKey='SinglePage', ID='ARD'),
		 title=title, summary=title, tagline='TV', thumb=R(ICON_ARD_Themen)))
	title = 'Serien'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Serien, next_cbKey='SinglePage', ID='ARD'), 
		title=title, summary=title, tagline='TV', thumb=R(ICON_ARD_Serien)))
	title = 'Rubriken'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Rubriken, next_cbKey='SinglePage', ID='ARD'),
		 title=title, summary=title, tagline='TV', thumb=R(ICON_ARD_RUBRIKEN)))
	title = 'Meist Gesehen'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Meist, next_cbKey='SingleSendung', ID='ARD'), 
		title=title, summary=title, tagline='TV', thumb=R(ICON_ARD_MEIST)))
	title = 'neueste Videos'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Neu, next_cbKey='SingleSendung', ID='ARD'), 
		title=title, summary=title, tagline='TV', thumb=R(ICON_ARD_NEUESTE)))
	title = 'am besten bewertet'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Best, next_cbKey='SingleSendung', ID='ARD'),
		 title=title, summary=title, tagline='TV', thumb=R(ICON_ARD_BEST)))
	return oc	
	
#---------------------------------------------------------------- 
@route(PREFIX + '/Main_ZDF')
def Main_ZDF(name):
	Log('Funktion Main_ZDF'); Log(PREFIX); Log(VERSION); Log(VDATE)
	oc = ObjectContainer(view_group="InfoList", art=ObjectContainer.art, title1=name)	
	oc = home(cont=oc, ID=NAME)								# Home-Button	
	
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
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=POD_RUBRIK, next_cbKey='SinglePage', ID='PODCAST'),
		title=title, summary=title, thumb=R(ICON_POD_RUBRIK)))
	title="Radio-Feature"	 
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=POD_FEATURE, next_cbKey='SingleSendung', ID='PODCAST'),
		title=title, summary=title, thumb=R(ICON_POD_FEATURE)))
	title="Radio-Tatort"	 
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=POD_TATORT, next_cbKey='SingleSendung', ID='PODCAST'),
		title=title, summary=title, thumb=R(ICON_POD_TATORT)))
	title="Neueste Audios"	 
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=POD_NEU, next_cbKey='SingleSendung', ID='PODCAST'),
		title=title, summary=title, thumb=R(ICON_POD_NEU)))
	title="Meist abgerufen"	 
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=POD_MEIST, next_cbKey='SingleSendung', ID='PODCAST'),
		title=title, summary=title, thumb=R(ICON_POD_MEIST)))
	
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
	if ID == 'PODCAST':
		name = "Radio-Podcasts"
		cont.add(DirectoryObject(key=Callback(Main_POD,name=name),title=title, summary=summary, tagline=name, 
			thumb=R(ICON_MAIN_POD)))

	return cont
	
####################################################################################################
@route(PREFIX + '/Main_Options')
# DumbTools (https://github.com/coder-alpha/DumbTools-for-Plex) getestet, aber nicht verwendet - wiederholte 
#	Aussetzer bei Aufrufen nach längeren Pausen (mit + ohne secure-Funktion) - Textfelder werden daher hier in
#		den Main_Options nicht unterstützt (Eingabe aber Plex-intern z.B. im Web-Player möglich)
#	Framework: code/preferences.py

def Main_Options(title):
	Log('Funktion Main_Options')	
	# Log(Prefs['pref_use_epg']); 
	
	# hier zeigt Plex die Einstellungen (Entwicklervorgabe in DefaultPrefs.json):
	# 	http://127.0.0.1:32400/:/plugins/com.plexapp.plugins.ardmediathek2016/prefs
	#	geänderte Daten legt Plex persistent ab (nicht in DefaultPrefs.json) - Löschen nur 
	#	möglich mit Löschen des Caches (Entfernen ../Caches/com.plexapp.plugins.ardmediathek2016)
	myplugin = Plugin.Identifier
	data = HTTP.Request("%s/:/plugins/%s/prefs" % (myhost, myplugin), # als Text, nicht als HTML-Element
						immediate=True).content 
	
	# Zeilenaufbau
	#	1. Zeile "<?xml version='1.0' encoding='utf-8'?>"
	#	2. Zeile (..identifier="com.plexapp.plugins.ardmediathek2016"..) 
	#   ab 3.Zeile Daten
	# Log(data)
	myprefs = data.splitlines() 
	Log(myprefs)
	myprefs = myprefs[2:-1]		# letzte Zeile + Zeilen 1-2 entfernen 
		
	oc = ObjectContainer(no_cache=True, view_group="InfoList", title1='Einstellungen')
	oc = home(cont=oc, ID=NAME)				# Home-Button - in den Untermenüs Rücksprung hierher zu Einstellungen 
	for i in range (len(myprefs)):
		do = DirectoryObject()
		summary = ''
		element = myprefs[i]		# Muster: <Setting secure="false" default="true" value="true" label=...
		Log(element)
		secure = stringextract('secure=\"', '\"', element)		# nicht verwendet
		default = stringextract('default=\"', '\"', element)	# Vorgabe
		id = stringextract('id=\"', '\"', element)
		value = stringextract('value=\"', '\"', element)		# akt. Wert (hier nach dem Setzen nicht mehr aktuell)
		pref_value = Prefs[id]									# akt. Wert via Prefs - OK
		label = stringextract('label=\"', '\"', element)
		values = stringextract('values=\"', '\"', element)
		mytype = stringextract('type=\"', '\"', element)
		Log(secure);Log(default);Log(label);Log(values);Log(mytype); Log(id);
		Log(pref_value);
		if mytype == 'bool':										# lesbare Anzeige (statt bool, true, false)
			#oc_type = '| JA / NEIN | aktuell: '
			if str(pref_value).lower() == 'true':
				oc_wert = 'JA'
				oc_type = '| für NEIN  klicken | aktuell: '
			else:
				oc_wert = 'NEIN'
				oc_type = '| für JA  klicken | aktuell: '
		if mytype == 'enum':
			#oc_type = '|  Aufzählung | aktuell: '
			oc_type = '|  für Liste klicken | aktuell: '
			oc_wert = pref_value
		if mytype == 'text':
			oc_type = '| aktuell: '
			oc_wert = pref_value
		title = u'%s  %s  %s' % (label, oc_type, oc_wert)
		title = title.decode(encoding="utf-8", errors="ignore")
		summary = 'zum Ändern bitte Webplayer benutzen (Zahnradsymbol)'
		summary = summary.decode(encoding="utf-8", errors="ignore")
		tagline = 'an dieser Stelle ist keine Texteingabe möglich'
		tagline = tagline.decode(encoding="utf-8", errors="ignore")
		Log(title); Log(mytype)

		if mytype == 'bool':
			Log('mytype == bool')	
			do.key = Callback(Set, key=id, value=not Prefs[id], oc_wert=not Prefs[id]) 	# Wert direkt setzen (groß/klein egal)		
		if mytype == 'enum':
			do.key = Callback(ListEnum, id=id, label=label, values=values)			# Werte auflisten
		elif mytype == 'text':
			Log(title); Log(id)									# Eingabefeld für neuen Wert (Player-abhängig)
			#continue											# Textfelder hier nicht unterstützt			
			do.key = Callback(Main_Options, title='Einstellungen')  # nur Anzeige
			do.summary = summary
			do.tagline = tagline
			
		do.title = title		
		oc.add(do)			
		
	return oc
#------------
@route(PREFIX + '/ListEnum')
def ListEnum(id, label, values):
	Log(ListEnum); Log(id); 
	label = label.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(no_cache=True, view_group="InfoList", title1=label)	
	title = 'zurück zu den Einstellungen'.decode(encoding="utf-8", errors="ignore")		# statt Home-Button	
	oc.add(DirectoryObject(key = Callback(Main_Options, title=title), title = title, 
		summary = title, 
		thumb = R(ICON_PREFS)))
	values = values.split('|') 
	Log(values);
	for i in range(len(values)):
		pref = values[i]
		pref = unescape(pref)
		oc_wert = pref
		Log('value: ' + str(i) + ' Wert: ' + oc_wert)
		oc.add(DirectoryObject(key=Callback(Set, key=id, value=i, oc_wert=oc_wert), title = u'%s' % (pref)))				
	return oc
#------------
@route(PREFIX + '/SetText')
def SetText(query, id):
	if query == None:
		query=''
	return Set(key=id, value=query, oc_wert=query)
#------------
@route(PREFIX + '/Set')
def Set(key, value, oc_wert):
	Log('Set: key, value ' + key + ', ' + value); 
	#oc_wert = value
	if str(value).lower() == 'true':
		oc_wert = 'JA'
	if str(value).lower() == 'false':
		oc_wert = 'NEIN'

	oc = ObjectContainer(no_cache=True, view_group="InfoList", title1='eingestellt auf: ' + oc_wert)	
	title = 'zurück zu den Einstellungen'.decode(encoding="utf-8", errors="ignore")		# statt Home-Button	
	oc.add(DirectoryObject(key = Callback(Main_Options, title=title), title = title, 
		summary = title, 
		thumb = R(ICON_PREFS)))
	
	# Bsp.: http://127.0.0.1:32400/:/plugins/com.plexapp.plugins.ardmediathek2016/prefs/set?pref_use_epg=True
	HTTP.Request("%s/:/plugins/%s/prefs/set?%s=%s" % (myhost, Plugin.Identifier, key, value), immediate=True)
	#return ObjectContainer()
	return oc
#--------------------------------
def ValidatePrefs():
	Log('ValidatePrefs')
	# Dict.Save()	# n.b. - Plex speichert in Funktion Set, benötigt trotzdem Funktion ValidatePrefs im Plugin
	return
	
####################################################################################################
@route(PREFIX + '/SearchUpdate')
def SearchUpdate(title):		#
	oc = ObjectContainer(view_group="InfoList", art=ObjectContainer.art)	

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
		oc.add(DirectoryObject(
			#key = Callback(updater.menu, title='Update Plugin'), 
			key = Callback(Main), 
			title = 'Plugin ist aktuell | weiter zum aktuellen Plugin',
			summary = 'Plugin Version ' + VERSION + ' ist aktuell (kein Update vorhanden)',
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
def Search(query=None, title=L('Search'), channel='ARD', s_type='video', offset=0, **kwargs):
	Log('Search'); Log(query); Log(channel)
	query = query.replace(' ', '+')			# Leer-Trennung = UND-Verknüpfung bei Podcast-Suche 
	query = urllib2.quote(query, "utf-8")
	Log(query)
	
	name = 'Suchergebnis zu: ' + urllib2.unquote(query)
	name = name.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=name, art = ObjectContainer.art)
	next_cbKey = 'SinglePage'	# cbKey = Callback für Container in PageControl
			
	if channel == 'ARD':		
		path =  BASE_URL +  ARD_Suche 
		path = path % query
		ID='ARD'
	if channel == 'PODCAST':	
		path =  BASE_URL  + POD_SEARCH
		path = path % query
		ID=channel
	Log(path) 
	page = HTTP.Request(path).content
	Log(len(page))
	
	err = test_fault(page, path)		# ARD-spezif. Error-Test
	if err:
		return err		
		
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
		oc = PageControl(title=name, path=path, cbKey=next_cbKey, mode='Suche', ID=ID) 	# wir springen direkt
	 
	return oc
 
#-----------------------
def test_fault(page, path):	# testet geladene ARD-Seite auf ARD-spezif. Error-Test
 	error_txt = '<title>Leider liegt eine Störung vor | ARD Mediathek</title>'
	if page.find(error_txt) >= 0:
		error_txt = 'Leider liegt eine Störung vor | ARD Mediathek | interne Serverprobleme'			 			 	 
		msgH = 'Fehler'; msg = error_txt + ' | Seite: ' + path
		Log(msg)
		msg =  msg.decode(encoding="utf-8", errors="ignore")
		return ObjectContainer(header=msgH, message=msg)	
	else:
		return ''
#-----------------------
def get_page(path, cTimeout=None):		# holt kontrolliert raw-Content, cTimeout für cacheTime
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
		error_txt = 'Seite nicht erreichbar oder nicht mehr vorhanden'			 			 	 
		msgH = 'Fehler'; msg = error_txt + ' | Seite: ' + path
		Log(msg)
		msg =  msg.decode(encoding="utf-8", errors="ignore")
#		err = ObjectContainer(header=msgH, message=msg)

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
def ARDMore(title, morepath, next_cbKey, ID):	# next_cbKey: Vorgabe für nächsten Callback in SinglePage
	Log('ARDMore'); Log(morepath)
	title2=title.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=title2, art = ObjectContainer.art)
	oc = home(cont=oc, ID=ID)							# Home-Button
					 
	path = morepath
	path = Update_ARD_Path(morepath)		# Pfad aktualisieren - bei Podcast i.d.R. unverändert
	page = HTTP.Request(path).content
	err = test_fault(page, path)			# ARD-spezif. Error-Test: 'Leider liegt eine..'
	if err:
		return err		
							
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

	mode = 'Sendereihen'						# steuert Ausschnitt in SinglePage + bei Podcast Kopfauswertung 1.Satz
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
@route(PREFIX + '/PageControl')	# kontrolliert auf Folgeseiten. Mehrfache Verwendung.
	# Wir laden beim 1. Zugriff alle Seitenverweise in eine Liste. Bei den Folgezugriffen können die Seiten-
	# verweise entfallen - der Rückschritt zur Liste ist dem Anwender nach jedem Listenelement  möglich.
	# Dagegen wird in der Mediathek geblättert.
def PageControl(cbKey, title, path, mode, ID, offset=0):  # ID='ARD', 'POD', mode='Suche', 'VERPASST', 'Sendereihen'
	Log('PageControl'); Log('cbKey: ' + cbKey); Log(path)
	Log('mode: ' + mode); Log('ID: ' + str(ID))
	title1='Folgeseiten: ' + title.decode(encoding="utf-8", errors="ignore")
	
	oc = ObjectContainer(view_group="InfoList", title1=title1, title2=title1, art = ObjectContainer.art)
	oc = home(cont=oc, ID=ID)							# Home-Button
	
	page = HTTP.Request(path).content
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
	list = blockextract('class=\"entry\"', page)  # sowohl in A-Z, als auch in Verpasst, 1. Element
	del list[-1]				# letzten Eintrag entfernen - wie in pagenr_path
	Log(len(list))


	first_site = True								# falls 1. Aufruf ohne Seitennr.: im Pfad ergänzen für Liste		
	if (pagenr_suche) or (pagenr_andere) or (pagenr_einslike) :		# re.findall s.o.  		
		if path_page1.find('mcontents=page') == -1: 
			path_page1 = path_page1 + 'mcontents=page.1'
		if path_page1.find('mresults=page') == -1:
			path_page1 = path_page1 + '&mresults=page.1'
		if path_page1.find('searchText=') >= 0:			#  kommt direkt von Suche
			path_page1 = path + '&source=tv&mresults=page.1'
		if path_page1.find('mcontent=page') >= 0:			#  einslike oder Themen
			path_page1 = path_page1 + 'mcontent=page.1'
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
			if href.find('=page.') >=0:
				title = 'Weiter zu Seite ' + pagenr[0]
				href = BASE_URL + href
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
		sendungen = blockextract('class=\"teaser\"', page) 
	if mode == 'Verpasst':								
		page = stringextract('"boxCon isCollapsible', '<!-- **** END **** -->', page)	
		sendungen = blockextract('<h3 class="headline"', page) 
	if mode == 'Sendereihen':	
		if ID == 'PODCAST':						       # auch A-Z 
			# Filter nach next_cbKey (PageControl, 	SinglePage, SingleSendung) hier nicht erforderlich	
			page = stringextract('class=\"section onlyWithJs sectionA\">', '<!-- content -->', page)
		else:
			page = stringextract('data-ctrl-layoutable', '<!-- **** END **** -->', page)	
	sendungen = blockextract('class=\"teaser\"', page)	# Sendungsblöcke in PODCAST: 1. teaser=Sendungskopf, 
														#   Rest Beiträge - Auswertung in get_sendungen	
	if len(sendungen) == 0:								# Fallback 	
		sendungen = blockextract('class=\"entry\"', page) 				
	Log(len(sendungen))
	
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
			#if subtitel == '':	# ohne subtitel verm. keine EinzelSendung, sondern Verweis auf Serie o.ä.
			#	continue		#   11.10.2017: Rubrik "must see" ohne subtitel
			if subtitel == summary or subtitel == '':
				subtitel = img_alt.decode(encoding="utf-8", errors="ignore")
			
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
			if url.find('.m3u8') >= 9:
				del link_path[i]			# 1. master.m3u8 entfernen, oben bereits abgehandelt
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
						summary=summary+geoblock, meta=path, thumb=thumb, tagline='', duration=duration, resolution=''))
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
				tagline = 'Der Download erfolgt durch im Hintergrund | ' + quality
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
#
def DownloadExtern(url, title, dest_path, key_detailtxt):  # Download mittels curl/wget
	Log('DownloadExtern: ' + title)
	Log(url); Log(dest_path); Log(key_detailtxt)
	title=title.decode(encoding="utf-8", errors="ignore")	
	
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
			
	try:
		Core.storage.save(pathtextfile, storetxt)			# Text speichern
		
		AppPath = Prefs['pref_curl_path']
		i = os.path.exists(AppPath)					# Existenz curl/wget prüfen
		Log(AppPath); Log(i)
		if AppPath == '' or i == False:
			msg='Pfad zu curl/wget fehlt oder curl/wget nicht gefunden'
			return ObjectContainer(header='Error', message=msg)
			
		# i = os.access(curl_dest_path, os.W_OK)		# Zielverz. prüfen - nicht relevant für curl/wget
														# 	Anwender muss Schreibrecht sicherstellen
		curl_fullpath = os.path.join(dest_path, dfname)	# kompl. Speicherpfad für Video/Podcast
		Log(curl_fullpath)

		# 08.06.2017 wget-Alternative wg. curl-Problem auf Debian-System (Forum: 
		#	https://forums.plex.tv/discussion/comment/1454827/#Comment_1454827
		#
		# http://stackoverflow.com/questions/3516007/run-process-and-dont-wait
		#	creationflags=DETACHED_PROCESS nur unter Windows
		if AppPath.find('curl') > 0:									# curl-Call
			Log('%s %s %s %s' % (AppPath, url, "-o", curl_fullpath))	
			sp = subprocess.Popen([AppPath, url, "-o", curl_fullpath])	# OK, wartet nicht (ohne p.communicate())
			# sp = subprocess.Popen([AppPath, url, "-N", "-o", curl_fullpath])	# Buffering für curl abgeschaltet
		else:															# wget-Call
			Log('%s %s %s %s %s' % (AppPath, "--no-use-server-timestamps", "-qO", curl_fullpath, url))	
			sp = subprocess.Popen([AppPath, "--no-use-server-timestamps", "-qO", curl_fullpath, url])
			
		msgH = 'curl/wget: Download erfolgreich gestartet'
		Log('sp = ' + str(sp))
	
		if str(sp).find('object at') > 0:  				# subprocess.Popen object OK
			tagline = 'Zusatz-Infos in Textdatei gespeichert:' + textfile
			summary = 'Ablage: ' + curl_fullpath
			summary = summary.decode(encoding="utf-8", errors="ignore")				
			oc.add(DirectoryObject(key = Callback(DownloadsTools), title = 'Download-Tools', summary=summary, 
				thumb=R(ICON_OK), tagline=tagline))						
			return oc				
		else:
			raise Exception('Start von curl/wget fehlgeschlagen')
			
	except Exception as exception:
		msgH = 'Fehler'; 
		summary = str(exception)
		summary = summary.decode(encoding="utf-8", errors="ignore")
		Log(summary)		
		tagline='Download fehlgeschlagen'
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
				tagline = 'Sammeldownload  oder Beschreibung gelöscht'
				thumb = R(ICON_NOTE)
				
			Log(httpurl); Log(tagline); Log(quality); # Log(txt); 			
			if httpurl.endswith('mp3'):
				oc_title = 'Bearbeiten: Podcast | ' + title
			else:
				oc_title='Bearbeiten: ' + title
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
			meta=httpurl, thumb=thumb, tagline=tagline, duration='leer', resolution='leer'))
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
		if img_src.startswith('http://') == False:		# Base ergänzen
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
	return oc
	
#-----------------------------------------------------------------------------------------------------
@route(PREFIX + '/EPG_Sender')		# EPG Vorauswahl, Daten holen in Modul EPG.py, Anzeige in EPG_Show
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
def get_sort_playlist():								# sortierte Playliste der TV-Livesender
	Log('get_sort_playlist')
	playlist = Resource.Load(PLAYLIST)					# lokale XML-Datei (Pluginverz./Resources)
	stringextract('<channel>', '</channel>', playlist)	# ohne Header
	playlist = blockextract('<item>', playlist)
	sort_playlist =  []
	for item in playlist:   
		rec = []
		title = stringextract('<title>', '</title>', item)
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
	today_human = 'ab ' + EPG_rec[0][7]
	
	if len(EPG_rec) == 0:			# kann vorkommen, Bsp. SR
		msg='Sender ' + name + ': keine EPG-Daten gefunden'
		msg = msg.decode(encoding="utf-8", errors="ignore")
		return ObjectContainer(header='Error', message=msg)
		
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
@route(PREFIX + '/EPG_ShowAll')		# EPG: aktuelle Sendungen aller Sender mode='allnow'
def EPG_ShowAll(title):
	Log('EPG_ShowAll')
		
	oc = ObjectContainer(view_group="InfoList", title1='EPG', title2='Aktuelle Sendungen', art = ICON)	
	oc = home(cont=oc, ID=NAME)				# Home-Button	

	# Zeilen-Index: title=rec[0]; EPG_ID=rec[1]; img=rec[2]; link=rec[3];	
	sort_playlist = get_sort_playlist()	
	for rec in sort_playlist:
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
		
	return oc
#-----------------------------------------------------------------------------------------------------
@route(PREFIX + '/SenderLiveListe')	# LiveListe - verwendet lokale Playlist
def SenderLiveListe(title, listname, offset=0):	# 

	# SenderLiveListe -> SenderLiveResolution (reicht nur durch) -> Parseplaylist (Ausw. m3u8)
	#	-> CreateVideoStreamObject 
	Log.Debug('SenderLiveListe')
	
	Log('Dict_Lock: ' + str(Dict['Lock']))
	Dict['Lock'] = False			# schütz bei Back-Schritten vor erneuter Thread-Auslösung -
	Log('Lock_geloest')				# 	siehe Thread remoteVideo
		

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
				tagline = 'Zeit: ' + vonbis
			else:
				tagline = ''			
		title = unescape(title)	
		title = title.replace('JETZT:', '')					# 'JETZT:' hier überflüssig
		title = title.decode(encoding="utf-8", errors="ignore")	
		summary = unescape(summary)	
		summary = summary.decode(encoding="utf-8", errors="ignore")			
		tagline = tagline.decode(encoding="utf-8", errors="ignore")	
						
		img = stringextract('<thumbnail>', '</thumbnail>', element) 
		if img.find('://') == -1:	# Logo lokal? -> wird aus Resources geladen, Unterverz. leider n.m.
			img = R(img)
			
		Log(link); Log(img); Log(summary); Log(tagline[0:80]);
		Resolution = ""; Codecs = ""; duration = ""
	
		# if link.find('rtmp') == 0:				# rtmp-Streaming s. CreateVideoStreamObject
		# Link zu master.m3u8 erst auf Folgeseite? - SenderLiveResolution reicht an  Parseplaylist durch  
		oc.add(DirectoryObject(key=Callback(SenderLiveResolution, path=link, title=title, thumb=img),
			title=title, summary=summary,  tagline=tagline, thumb=img))
	Log(len(oc))
	return oc
		
#-----------------------------------------------------------------------------------------------------
# remote: s. https://github.com/plexinc/plex-media-player/wiki/Remote-control-API
#	TV-Livestreams:
#		Filterung der Videoobjekte gemäß Video-Sofort-Format in Parseplaylist (auto, Bandbreite)
#		Aufruf Thread.Create in SenderLiveResolution - für TV-Livestreams 
#	Thread.Sleep() führt zu unmittelbar wiederholten Aufrufen der Funktion - dto. vom Nutzer 
#		ausgeführte Back-Funktion. Div. negative Versuche mit Thread.Block() + Thread.Lock. Bisher beste 
#		Lösung: globale Variable Dict['Lock'] - Freigabe erst bei Rückkehr in SenderLiveListe
 
def remoteVideo():	# Thread, Problem PHT: esc funktioniert nur 1 x (Video-Abbruch)
	Log('Thread_remoteVideo')
	plextoken = os.environ.get('PLEXTOKEN')	# 	id für diesen channel
	Log('plextoken: ' + plextoken)						
	myproduct = Client.Product					# für pref_setVideoFormatLive, none bei thread-python-Alternative
	Log(myproduct)

	delay = int(Prefs['pref_setVideoFormat_Delay'])	# Verzögerung in sec zwischen den remote-Requests
	Log('delay (sec): ' + str(delay))			# 1-10 (Einstellungen)

#	return		# todo. entfernen nach Konsolentests. DefaultPrefs.json aktualisieren
# todo: delay in Lock_return (2-faches Durchlaufen verhindern, verursacht durch 2. Aufruf CreateVideoStreamObject?
#		

	if Dict['Lock'] == True:
		Log('Lock_return')	
		return		
			
	if myproduct == 'Plex Web' or myproduct == 'Plex Media Player':	# klappt bei beiden garantiert nicht
		Log('remoteVideo nicht in: ' + myproduct)
		return
		
	Dict['Lock']=True								# Global - Freigabe in SenderLiveListe
	Log('Lock_gestartet')
	Dict['remoteStart'] = datetime.datetime.now()	# Global - verhindert Doppel-Durchlauf 
		
#	Ermittlung des Zieldevice via https://plex.tv/devices.xml (Header: X-Plex-Token)
#	Player-Unterschiede:
#		PHT: Steuerungs-Requests reichen - Header, subscribe + unsubscribe nicht erforderlich
#			Steuerungs-Sequenz: moveRight - select - select
#		Android: subscribe mit Header erforderlich, Steuerungs-Requests ohne Header möglich.
#			Steuerungs-Sequenz: moveDown - moveRight - moveRight - select - select
#	Header: token (devices.xml) für X-Plex-Token, X-Plex-Client-Identifier + X-Plex-Target-Client-Identifier,
#			Device name für X-Plex-Device-Name, commandID (1 bei subscribe, 2 bei Requests + unsubscribe)
#	
#	Problem Plex Media Player (PMP, Plex Web ähnlich): subscribe -> commands - unsubscribe
#		Die vom PMP zur Steuerung gesendete timeline führt zum Error im PMP-Log, da wir im Plugin keinen 
#		eigenen HTTP-Server aufspannen. Mit dem subscribe-Port  kann auch der PMS nichts anfangen.
#		Innerhalb der 10sec-Timeout-Frist akzeptiert der PMP trotzdem die
#		Steuerkommandos. Für diese ist jeweils der notwendige Headersatz erforderlich (s. Code).
#		s.a. https://forums.plex.tv/discussion/190372/pmp-control-api-my-feedback
#			 https://github.com/plexinc/plex-media-player/wiki/Remote-control-API

# Delay erforderlich: 	1. um der Player-App vor dem Steuerkdo. den Aufbau der Objekte zu ermöglichen
#						2. um beim Zurückblättern (Back-Taste) die Steuerkdo. nicht erneut auszulösen

	Log('Thread remoteVideo: Start_Remote')
	# Anmeldung bei https://plex.tv/pin, falls der Client nicht in devices.xml auftaucht
	r=HTTP.Request('https://plex.tv/devices.xml', headers={'X-Plex-Token': plextoken}, cacheTime=0, immediate=True)
	cont = r.content		# Liste devices
	Log(cont[:60]); 	# Log(r.headers) 	r.headers enthält hier keine ID-Merkmale des Clients	

	uri = ''; clientid = ''
	RemoteModel = Prefs['pref_setRemoteModel']				# Voreinstellung
	Log('RemoteModel: ' + RemoteModel)
	devices = blockextract('<Device', cont)
	for device in devices:
		product = stringextract('product="', '"', device)	# Bsp. "Plex Home Theater"
		Log(myproduct); Log(product)
		if myproduct == product:
			client_token = stringextract('token="', '"', device)	# wird Client- und Target-Client-Identifier
			client_id =  stringextract('clientIdentifier="', '"', device)		
			plex_device =  stringextract('Device name="', '"', device)		
			uri =  stringextract('Connection uri="', '"', device)	# Bsp. "http://192.168.0.102:32500"
			if uri:	 # anscheinend  nur steuerbar, falls Connection uri vorhanden 
				Log('client_token: ' + client_token); Log('client_id: ' + client_id); 
				Log('uri: ' + uri); Log('plex_device: ' + plex_device); 
				
				if TestOpenPort(uri) == True:		# IP/Port erreichbar? devices.xml enthält auch inaktive Clients						
					headers={'X-Plex-Token': plextoken, 'X-Plex-Client-Identifier': client_token, 'X-Plex-Device-Name': plex_device,
						'X-Plex-Target-Client-Identifier': client_token, 'commandID' : '1'}
					Log('headers: ' + str(headers)); 
							
					# nur Richtungs-Kommandos, ohne subscribe, unsubscribe, headers 											
					if 	myproduct == "Plex Home Theater" or RemoteModel  == "Plex Home Theater":
						Thread.Sleep(delay)
						# time.sleep(delay) 					# keine Änderungen im Thread-Verhalten
						r = HTTP.Request('%s/player/navigation/moveRight' % (uri), cacheTime=0, immediate=True) 
						Log(r.content)
						Thread.Sleep(delay)	
						r = HTTP.Request('%s/player/navigation/select' % (uri), cacheTime=0, immediate=True) 
						Log(r.content)				
						Thread.Sleep(delay)	
						r = HTTP.Request('%s/player/navigation/select' % (uri), cacheTime=0, immediate=True) 
						Log(r.content)
						return True		
						
					# bisher nur getestet für "Plex for Android"
					#	merkwürdige Rückmeldung im OK-Fall: Failure: 200 OK 
					if 	myproduct == "Plex for Android" or RemoteModel  == "Plex for Android":				
						# 1. Subscribe									
						Thread.Sleep(delay)
						r = HTTP.Request('%s/player/timeline/subscribe?protocol=http&port=32400&commandID=1' % (uri), 
							headers=headers, cacheTime=0, immediate=True) 
						Log(r.content)
						# 2. Richtungs-Kommandos									
						headers={'X-Plex-Token': plextoken, 'X-Plex-Client-Identifier': client_token, 'X-Plex-Device-Name': plex_device,
							'X-Plex-Target-Client-Identifier': client_token, 'commandID' : '2'}
						Thread.Sleep(delay)	
						r = HTTP.Request('%s/player/navigation/moveDown' % (uri), headers=headers, cacheTime=0, immediate=True) 
						Log(r.content)
						Thread.Sleep(delay)	
						r = HTTP.Request('%s/player/navigation/moveRight' % (uri), headers=headers, cacheTime=0, immediate=True) 
						Log(r.content)				
						Thread.Sleep(delay)	
						r = HTTP.Request('%s/player/navigation/moveRight' % (uri), headers=headers, cacheTime=0, immediate=True) 
						Log(r.content)				
						Thread.Sleep(delay)	
						r = HTTP.Request('%s/player/navigation/select' % (uri), headers=headers, cacheTime=0, immediate=True) 
						Log(r.content)
						Thread.Sleep(delay)	
						r = HTTP.Request('%s/player/navigation/select' % (uri), headers=headers, cacheTime=0, immediate=True) 
						Log(r.content)
						# 3. Unsubscribe		# unschädlich, falls vom Player nicht benötigt							
						Thread.Sleep(delay)
						commandID = 3							
						r = HTTP.Request('%s/player/timeline/unsubscribe?protocol=http&port=32400&commandID=%s' % (uri, commandID), 
							headers=headers, cacheTime=0, immediate=True) 
						Log(r.content)				
						Log('Thread remoteVideo: select-request erfolgt')
						return True		
				
	Log('Thread remoteVideo: kein select-request')
	return	

def TestOpenPort(address_port):	# speziell für remoteVideo, Bsp. address_port: http://192.168.0.102:32500
	import socket
	tout = 1		# Timeout
	
	adress_port = address_port.split('://')[1]
	address = adress_port.split(':')[0]; port = adress_port.split(':')[1];
	
	s = socket.socket()
	s.settimeout(tout)
	try:
		s.connect((address, int(port)))
		s.shutdown(1)
		s.close()
		Log("Verbindung zu %s auf Port %s erfolgreich" % (address, port))
		return True
	except socket.error, e:
		Log("Verbindung zu %s auf Port %s fehlgeschlagen: %s" % (address, port, e))
		return False
			
###################################################################################################
@route(PREFIX + '/SenderLiveResolution')	# Auswahl der Auflösungstufen des Livesenders
	#	Die URL der gewählten Auflösung führt zu weiterer m3u8-Datei (*.m3u8), die Links zu den 
	#	Videosegmenten (.ts-Files enthält). Diese  verarbeitet der Plexserver im Videoobject. 
	#	10.08.2017: Video-Sofort-Format beschränkt die Auswahl auf 1 Element (der autom. Start funktioniert
	#		aber nicht im Webplayer)
	#		Bei lokalen m3u8-Dateien müssen die Bandbreiten aufsteiend sortiert sein für Abgleich mit
	#			Video-Sofort-Format (Bsp. liveTV_cbcyoumain.m3u8, liveTV_ntvlive-ipadakamai.m3u8)
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
		if Prefs['pref_setVideoFormatLive']:		
			if Dict['Lock'] != True:		 	# läuft noch ein Thread? (z.B. Aktivierung  durch Back-Taste)
				t=Thread.Create(remoteVideo)		# Thread für Video-Sofort-Format TV-Live (auto)
				Log(t)
		return oc
		
	if url_m3u8.find('rtmp') == 0:		# rtmp, nur 1 Videoobjekt
		oc.add(CreateVideoStreamObject(url=url_m3u8, title=title, 
			summary='rtmp-Stream', tagline=title, meta=Codecs, thumb=thumb, 
			rtmp_live='ja', resolution='unbekannt'))
		if Prefs['pref_setVideoFormatLive']:		
			if Dict['Lock'] != True:		 	# läuft noch ein Thread? (z.B. Aktivierung  durch Back-Taste)
				t=Thread.Create(remoteVideo)		# Thread für Video-Sofort-Format TV-Live (auto)
				Log(t)
		return oc
		
	# alle übrigen (i.d.R. http-Links), Videoobjekte für einzelne Auflösungen erzeugen
	if url_m3u8.find('.m3u8') >= 0:				# häufigstes Format
		Log(url_m3u8)
		if url_m3u8.find('http') == 0:			# URL (auch https) oder lokale Datei? (lokal entfällt Eintrag "autom.")			
			oc.add(CreateVideoStreamObject(url=url_m3u8, title=title + ' | Bandbreite und Auflösung automatisch', 
				summary='automatische Auflösung | Auswahl durch den Player', tagline=title,
				meta=Codecs, thumb=thumb, rtmp_live='nein', resolution=''))
		if Prefs['pref_setVideoFormatLive']:	# Video-Sofort-Format = Qualität: auto (m3u8)
			if 'auto' in Prefs['pref_setVideoFormatLive']:
				if len(oc) == 1:				# lokale Datei i.d.R. ohne 'auto'-Eintrag
					return ObjectContainer(header='Fehler', message='lokale Datei ohne Video-Sofort-Format >auto<: ' + url_m3u8)
				else:					
					if Prefs['pref_setVideoFormatLive']:
						Log(Dict['Lock'])
						if Dict['Lock'] != True:		 	# läuft noch ein Thread? (z.B. Aktivierung  durch Back-Taste)
							t=Thread.Create(remoteVideo)	# Thread für Video-Sofort-Format TV-Live (auto)
							Log(t)
					return oc					# Rückgabe Objekt 'auto' - Fernsteuerung in remoteVideo 
			else:
				# 'auto' entfernen, Ersatz durch gewähltes Format in Parseplaylist:
				oc = ObjectContainer(view_group="InfoList", title1=title + ' Live', art=ICON)
				
		# hier weiter mit Auswertung der m3u8-Datei (lokal oder extern), Berücksichtigung pref_setVideoFormatLive
		if Prefs['pref_setVideoFormatLive']:	# Video-Sofort-Format für andere als 'auto'	
			if Dict['Lock'] != True:			# läuft noch ein Thread? (z.B. Aktivierung  durch Back-Taste)
				t=Thread.Create(remoteVideo)	# Thread für Video-Sofort-Format TV-Live (ausgewählte Bandbreite)
				Log(t)
		 # Auswertung *.m3u8-Datei, Auffüllung Container mit Auflösungen. geoblock bei TV-Live nicht verwendet:	
		oc = Parseplaylist(oc, url_m3u8, thumb, geoblock='')
		return oc							# (-> CreateVideoStreamObject pro Auflösungstufe)
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
  # 01.03.2017: kein DirectPlay mehr neuen Web-Player-Versionen. Lokaler Workaround: Austausch WebClient.bundle gegen
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
	Log(url); Log(duration); Log(tagline)
	Log(Client.Platform)
	Log('Plattform: ' + sys.platform)
	Log(Client.Product)
	
	# resolution = ''					# leer - Clients skalieren besser selbst
	resolution=[720, 540, 480]			# wie VideoClipObject: Vorgabe für Webplayer entbehrlich, für PHT erforderlich

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
					img 	= pair[1].strip()
				except:
					break								# dann bleibt es bei img_src (Fallback)
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
# 	Voreinstellungen: alle DF-Sender, ganze Sendungen, sortiert nach Datum
#	Anzahl Suchergebnisse: 25 - nicht beeinflussbar
# def ZDF_Search(query=None, title=L('Search'), s_type=None, pagenr='', **kwargs):
def ZDF_Search(query=None, title=L('Search'), s_type=None, pagenr='', **kwargs):
#	query = urllib2.quote(query, "utf-8")
	query = query.strip()
	query = query.replace(' ', '+')		# Leer-Trennung bei ZDF-Suche mit +
	Log('ZDF_Search'); Log(query); Log(pagenr); Log(s_type)

	ID='Search'
	ZDF_Search_PATH	 = 'https://www.zdf.de/suche?q=%s&from=&to=&sender=alle+Sender&attrs=&contentTypes=episode&sortBy=date&page=%s'
	if s_type == 'Bilderserien':	# 'ganze Sendungen' aus Suchpfad entfernt:
		ZDF_Search_PATH	 = 'https://www.zdf.de/suche?q=%s&from=&to=&sender=alle+Sender&attrs=&contentTypes=&sortBy=date&page=%s'
		ID=s_type
	
	path = ZDF_Search_PATH % (query, pagenr) 
	Log(path)	
	# page = HTTP.Request(path, cacheTime=1).content 		# Debug: cacheTime=1 
	page = HTTP.Request(path).content 
	searchResult = stringextract('data-loadmore-result-count=\"', '\"', page)	# Anzahl Ergebnisse
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
	
	if pagenr == '':		# erster Aufruf muss '' sein
		pagenr = 1
			
	# offset=0: anders als bei den übrigen ZDF-'Mehr'-Optionen gibt der Sender Suchergebnisse bereits
	#	seitenweise aus, hier umgesetzt mit pagenr - offset entfällt	
	oc, offset, page_cnt = ZDF_get_content(oc=oc, page=page, ref_path=path, ID=ID, offset=0)
	
	# auf mehr prüfen (Folgeseite auf content-link = Ausschlusskriterum prüfen):
	#	im Gegensatz zu anderen ZDF-Seiten gibt  der Sender hier die Resultate seitenweise aus.
	# 	Daher entfällt die offset-Variante wiez.B. in BarriereArmSingle.
	pagenr = int(pagenr) + 1
	path = ZDF_Search_PATH % (query, pagenr)
	Log(pagenr); Log(path)
	page = HTTP.Request(path).content
	pos =  page.find('\"content-link\"')
	if pos >= 0: 
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
	  
	if len(oc) == 1:	# home berücksichtigen
		return NotFound('Leer - keine Sendung(en), die mit  >' + element + '< beginnen')
		
	summ_mehr = 'Mehr zu >%s<, Gesamt: %s' % (title2, page_cnt)
	Log(offset)
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
			title=title, thumb=R(ICON_ZDF_RUBRIKEN)))	
	
	return oc
#-------------------------
@route(PREFIX + '/RubrikSingle')
def RubrikSingle(title, path, offset=0):
	Log('RubrikSingle'); 
	oc = ObjectContainer(title2=title, view_group="List")
	oc = home(cont=oc, ID='ZDF')							# Home-Button
	
	page = HTTP.Request(path).content 			
	oc, offset, page_cnt = ZDF_get_content(oc=oc, page=page, ref_path=path, ID='DEFAULT', offset=offset)
	
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
	oc, offset, page_cnt = ZDF_get_content(oc=oc, page=page, ref_path=path, ID='DEFAULT', offset=offset)
	
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
	page = stringextract('<article class="b-cluster m-filter js-rb-live','<article class="b-cluster m-filter js-rb-live', page)
	Log(len(page))
	 			
	oc, offset, page_cnt = ZDF_get_content(oc=oc, page=page, ref_path=path, ID='DEFAULT', offset=offset)
	
	Log(offset)
	if offset:
		summ_mehr = 'Mehr zu >name<, Gesamt: %s' % (name, page_cnt)
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
		oc, offset, page_cnt  = ZDF_get_content(oc=oc, page=cont1, ref_path=path, ID='DEFAULT', offset=offset)	
		summ_mehr = 'Infos zu >Barrierefreie Angebote<, Gesamt: %s' % page_cnt
	if ID == 'Voice':
		oc, offset, page_cnt = ZDF_get_content(oc=oc, page=cont2, ref_path=path, ID='DEFAULT', offset=offset)	
		summ_mehr = 'Mehr zu >Hörfassungen<, Gesamt: %s' % page_cnt
	if ID == 'UT':
		oc, offset, page_cnt  = ZDF_get_content(oc=oc, page=cont3, ref_path=path, ID='DEFAULT', offset=offset)	
		summ_mehr = 'Mehr zu >Videos mit Untertitel<, Gesamt: %s' % page_cnt
	
	Log(offset)
	if offset:
		summ_mehr = summ_mehr.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(BarriereArmSingle, title=title, ID=ID, offset=offset), 
			title='Mehr...', summary=summ_mehr,  thumb=R(ICON_MEHR)))	
		
	return oc
	
####################################################################################################
# @route(PREFIX + '/ZDF_get_content')	# Auswertung aller ZDF-Seiten
#	Die Erkennung von Mehrfachseiten (multi=true) ist leider nicht allen Fällen möglich. Bsp.:
#	Liveticker, Bilderserien usw. werden ohne bes. Kennung hier angezeigt. Bis auf Weiteres werden
#	die Folgeseiten mit Fehlermeldung abgefangen (nach Test auf Videos) 
#	offset: für übergroße Seiten, die nicht wie die Suchergebn. als Folgeseiten mit pagenr organisiert sind.
#		Bsp. für übergroße Seite: Hörfassungen (145 am 28.9.2017)

def ZDF_get_content(oc, page, ref_path, offset=0, ID=None):	# ID='Search' od. 'VERPASST' - Abweichungen zu Rubriken + A-Z
	Log('ZDF_get_content'); Log(ID); Log(ref_path); Log(offset)					
	max_count = int(Prefs['pref_maxZDFContent'])				# max. Anzahl Einträge ab offset
	offset = int(offset)																		
	
	img_alt = teilstring(page, 'class=\"m-desktop', '</picture>') # Bildsätze für b-playerbox
	
	if page.find('class=\"content-box gallery-slider-box') >= 0: 	# Bildgalerie (hier aus Folgeseiten)
		title = stringextract('\"big-headline\"  itemprop=\"name\" >', '</h1>', page)
		title = unescape(title)
		Log(title)
		oc = ZDF_Bildgalerie(oc=oc, page=page, mode='is_gallery', title=title)
		return oc
	if page.find('name headline mainEntityOfPage') >= 0:  # spez. Bildgalerie, hier Bares für Rares
		headline = stringextract('name headline mainEntityOfPage\" >', '</h1>', page)
		if headline[0:7] == 'Objekte':		# Bsp.: Objekte vom 6. Dezember 2016
			oc = ZDF_Bildgalerie(oc=oc, page=page, mode='pics_in_accordion-panels', title=headline)
			return oc 		 	
		
	pos = page.find('class=\"content-box\"')					# ab hier verwertbare Inhalte 
	if pos >= 0:
		page = page[pos:]
				
				
	#if ID == 'Search' or ID == 'VERPASST':						# Unterscheidung ab 22.11.16 nicht mehr nötig
	#	content =  blockextract('class=\"content-link\"', page)																			
	content =  blockextract('class=\"artdirect\"', page)
	if ID == 'NeuInMediathek':									# letztes Element entfernen (Verweis Sendung verpasst)
		content.pop()	
	Log(len(page)); 
	page_cnt = len(content)
	Log('content_Blocks: ' + str(page_cnt));
	
	if page_cnt == 0:											# kein Ergebnis oder allg. Fehler
		s = 'Es ist leider ein Fehler aufgetreten.'				# ZDF-Meldung Server-Problem
		if page.find('\"title\">' + s) >= 0:
			msg_notfound = s + ' Bitte versuchen Sie es später noch einmal.'
		else:
			msg_notfound = 'Leider keine Inhalte' 				# z.B. bei A-Z für best. Buchstaben 
			
		if ref_path.startswith('https://www.zdf.de/comedy/neo-magazin-mit-jan-boehmermann'): # neue ZDF-Seite
			import zdfneo
			oc = zdfneo.neo_content(path=ref_path, ID=ID)		# Abschluss dort
			return oc, offset, page_cnt 
			
		title = msg_notfound.decode(encoding="utf-8", errors="ignore")					
		summary = 'zurück zur ' + NAME.decode(encoding="utf-8", errors="ignore")		
		oc.add(DirectoryObject(key=Callback(Main_ZDF, name=NAME), title=title, 
			summary=summary, tagline='TV', thumb=R(ICON_MAIN_ZDF)))
		return oc
		
		
	if page.find('class=\"b-playerbox') > 0 and page.find('class=\"item-caption') > 0:  # Video gesamte Sendung?
		first_rec = img_alt +  stringextract('class=\"item-caption', 'data-tracking=', page) # mit img_alt
		content.insert(0, first_rec)		# an den Anfang der Liste
		# Log(content[0]) # bei Bedarf
	
	if 	max_count:								# 0 = 'Mehr..'-Option ausgeschaltet
		delnr = min(page_cnt, offset)
		del content[:delnr]						# Sätze bis offset löschen (bzw. bis Ende records)
	Log(len(content))
	for rec in content:	
		pos = rec.find('</article>')		# Satz begrenzen - bis nächsten Satz nicht verwertbare Inhalte möglich
		if pos > 0:
			rec = rec[0:pos]
			#Log(rec)  # bei Bedarf
			
		teaser_cat=''; actionDetail=''; genre=''; summary=''; duration='';  title=''; airing=''; 
		tagline=''; thumb =''; vid_content=''; video_datum=''; video_duration=''; other_teaser_label='';
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
		Log(thumb)
			
		if thumb.find('https://') == -1:	 # Bsp.: "./img/bgs/zdf-typical-fallback-314x314.jpg?cb=0.18.1787"
				thumb = ZDF_BASE + thumb[1:] # 	Fallback-Image  ohne Host
			
		# python-Problem beim stringextract des gesamten plusbar-Blocks. Beschränkung auf einzelne strings			
		path =  stringextract('plusbar-url=\"', '\"', rec)	# plusbar nicht vorh.? - sollte nicht vorkommen
		if path == '' or path == ref_path:					# kein Pfad oder Selbstreferenz
			continue
		plusbar_title = stringextract('plusbar-title=\"', '\"', rec)	# Bereichs-, nicht Einzeltitel, nachrangig
		plusbar_path = stringextract('plusbar-path=\"', '\"', rec)

		# multi- und Teaser-Behandlung:	
		teaser_label = stringextract('class=\"teaser-label\"', '</div>', rec)
		teaser_typ =  stringextract('<strong>', '</strong>', teaser_label)
		if 	teaser_label:
			dt1 =  stringextract('</span>', '<strong>', teaser_label)   
			dt2 =  stringextract('<strong>', '</strong>', teaser_label)
			# Log(teaser_label);Log(teaser_typ);
			Log(dt1); Log(dt2);
			
		if teaser_typ == 'Beiträge':		# Mehrfachergebnisse ohne Datum + Uhrzeit
			multi = True
			summary = dt1 + teaser_typ 		# Anzahl Beiträge
		#Log('teaser_typ: ' + teaser_typ)			
			
		if 	teaser_label.find('class=\"icon-301_clock') >= 0:							# Wochentag + Uhrzeit
			airing = dt1 + ' | ' + dt2 + ' Uhr'
		if 	teaser_label.find('class=\"icon-302_countdown') >= 0:						# Countdown
			other_teaser_label = dt1 + ' ' + dt2			
		#Log(airing); Log(other_teaser_label);
			
		subscription = stringextract('is-subscription=\"', '\"', rec)	# aus plusbar-Block	
		Log(subscription)
		if subscription == 'true':						
			multi = True
			teaser_count = stringextract('</span>', '<strong>', teaser_label)	# bei Beiträgen
			stage_title = stringextract('class=\"stage-title\"', '</h1>', rec)  
			summary = teaser_count + ' ' + teaser_typ 

		# Auswertung Datum + Uhrzeit
		if rec.find('class=\"vid-content\"') >= 0:		# Bsp: <dd class="video-duration m-border">55 min</dd>
			if rec.find('<time datetime=') > 0:	# airing ersetzt airing aus teaser_label 
				airing_string = stringextract('<time datetime=\"', '\"', rec)
				Log(airing_string)
				airing = get_airing(airing_string)		# Bsp. airing_list 2016-11-12T21:45:00.000+01:00
				Log(airing)	
			video_datum = stringextract('video-airing\">', '<', rec)		# Video-Datum, kann fehlen	
			video_duration = stringextract('video-duration', '/dd', rec)	# Video-Länge,  "      "	
			duration = stringextract('>', '<', video_duration)			
				
			if video_datum:
				vid_content = video_datum
			if airing:		# aus teaser_label oder vid-content, so.o.
				vid_content = airing 		# Wochentag + Uhrzeit aus teaser_label
			if duration:
				if vid_content == '':
					vid_content = duration
				else:
					vid_content = vid_content + ' | ' + duration

		if duration == '':
			duration = stringextract('class="teaser-info ">', '</dd>', rec) # Länge bei Verpasst
		Log(airing); Log(video_datum); Log(video_duration); Log(duration);  

		# teaser_cat. div. Bezeichner + Textformate,  Bsp.: <span class="teaser-cat" itemprop="genre">
		teaser_cat = stringextract('class=\"teaser-cat\"', '</span>', rec)
		teaser_cat = teaser_cat.replace('>', "")
		teaser_cat = teaser_cat.replace('itemprop=\"genre\"', "")	
		teaser_cat = teaser_cat.strip()
		if teaser_cat.find('|') > 0:  	# häufig über 3 Zeilen verteilt
			tclist = teaser_cat.split('|')
			teaser_cat = str.strip(tclist[0]) + ' | ' + str.strip(tclist[1])			# zusammenführen
		Log('teaser_cat: ' + teaser_cat)
			
		href_title = stringextract('<a href=\"', '>', rec)		# href-link hinter teaser-cat kann Titel enthalten
		href_title = stringextract('title="', '\"', href_title)
		href_title = unescape(href_title)
		Log('href_title: ' + href_title)
		if 	href_title == 'ZDF Livestream':
			continue
		
		genre = stringextract('itemprop=\"genre\">', '</span>', rec)
		genre = mystrip(genre)
		if genre.find('|') > 0:  	# häufig über 3 Zeilen verteilt
			tclist = genre.split('|')
			genre = str.strip(tclist[0]) + ' | ' + str.strip(tclist[1])			# zusammenführen
			
		description = stringextract('itemprop=\"description\">', '</p>', rec)	# 
		if description == '':
			description = stringextract('class=\"item-description\">', '<', rec) 	# Bsp. Satz b-playerbox
		description = description.strip()	
		description = unescape(description)
		Log('description: ' + description)
		
		# Titel + Beschreibung (einschl. Datum + Zeit) zusammenstellen
		if teaser_cat:
			title = teaser_cat
		if href_title:				
			title = title + ' | ' + href_title		
		if title == '':				
			title = plusbar_title 		# nachrangig, z.B. Zeitbereich: Morgens 5:30 - 12:00
		
		if description:
			summary = description

		if multi == True:			
			tagline = 'Folgeseiten'
		else:							# Videos prüfen + Titel kennzeichnen
			if rec.find('title-icon icon-502_play') > 0 or  rec.find('icon-301_clock icon') > 0:
				# title = 'Video' + ' | ' + title 			# kann entfallen, spart Platz
				tagline = plusbar_title + ' | ' + duration 	# z.b. Nachts 0:00 - 05:30 | 43 min
				if vid_content:
					title = title  +  ' | ' + vid_content
					tagline = plusbar_title 
			else:	
				Log('icon-502_play und icon-301_clock nicht gefunden')
				if ID == 'Bilderserien': 	# aber Bilderserien aufnehmen
					Log('Bilderserien')
				if plusbar_title.find(' in Zahlen') > 0:	# Statistik-Seite, voraus. ohne Galeriebilder 
					continue
				if plusbar_title.find('Liveticker') > 0:	#   Liveticker und Ergebnisse
					continue
				if plusbar_path.find('-livestream-') > 0:	#   Verweis Livestreamseite
					continue
					
				multi = True		# weitere Folgeseiten mit unbekanntem Inhalt, ev. auch Videos
				tagline = 'Folgeseiten'
		
		if title[1] == '|':				# Fehlerkorrektur
			title = title[2:]
		Log('tagline: ' + tagline)
		if tagline.strip()[-1] == '|':	# Fehlerkorrektur
			tagline = tagline.strip()[:-1]
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
		Log(teaser_cat);Log(actionDetail);Log(genre);Log(thumb);			
		Log(path);Log(title);Log(summary);Log(tagline);Log(multi);
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

	# Bildstrecken am Fuß des Dokuments anhängen (ZDF-Korrespondenten, -Mitarbeiter,...):
	segment_start='<article class=\"b-group-persons\">'; segment_end = 'class="b-footer">'
	if page.find(segment_start) > 0:  
		rec = stringextract(segment_start, segment_end, page)
		path = ref_path													# aktuelle Seite, Auswertung in Bildgalerie
		title = stringextract('class="big-headline">', '</h2>', rec)	# 1. Titel
		title = unescape(title)
		thumb = stringextract('data-src=\"', '\"', rec)					# 1. Bild
		summary = stringextract('class=\"desc-text\">', '</p>', rec)	# 1. Beschr.
		summary = unescape(summary)
		summary = cleanhtml(summary)
		tagline = 'Bilder und Infos'
		title = title.decode(encoding="utf-8", errors="ignore")
		tagline = tagline.decode(encoding="utf-8", errors="ignore")
		summary = summary.decode(encoding="utf-8", errors="ignore")
		Log('Bildstrecke Footer');Log(thumb);Log(path);
		oc.add(DirectoryObject(key=Callback(GetZDFVideoSources, title=title, url=path, tagline=tagline, thumb=thumb,
			segment_start=segment_start, segment_end=segment_end),  title=title, thumb=thumb, summary=summary,
			tagline=tagline))	
				
	return oc, offset, page_cnt 
#-------------
def get_airing(airing_string):		# Datum + Uhrzeit, Bsp. airing_string 2016-11-12T21:45:00.000+01:00
	# Log(airing_string)
	airing = ''
	
	airing_date = airing_string.split('T')[0]	# 2016-11-12
	airing_time = airing_string.split('T')[1]
	
	airing_date = airing_date[8:10] + '.' + airing_date[5:7] +  '.' + airing_date[0:4]  # 12.11.2016
	airing_time = airing_time[0:5]  # 21:45
	
	if airing_date and airing_time:
		airing = airing_date + ', ' + airing_time + ' Uhr'
	
	return airing
	
#-------------

####################################################################################################
# Subtitles: im Kopf der videodat-Datei enthalten (Endung .vtt). Leider z.Z. keine Möglichkeit
#	bekannt, diese einzubinden
@route(PREFIX + '/GetZDFVideoSources')						# 4 Requests bis zu den Quellen erforderlich!				
def GetZDFVideoSources(url, title, thumb, tagline, segment_start=None, segment_end=None):	
	Log('GetVideoSources'); Log(url); Log(tagline); 
	title = title.decode(encoding="utf-8", errors="ignore")					
	oc = ObjectContainer(title2=title.decode(encoding="utf-8", errors="ignore"), view_group="InfoList")
	urlSource = url 	# für ZDFotherSources

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
	else:													# vorhanden: data-module="zdfplayer"
		apiToken = stringextract('"apiToken": "', '"', page)# ab 08.10.2017 dyn. ermitteln (wieder mal vom ZDF geändert)
		Dict['apiToken'] = apiToken
					
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
#		1. Ermittlung des apiToken (in configuration.json), bisher  unverändert, Verwendung in header
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
		apiToken = 'Bearer ' + str(Dict['apiToken'])		# s. GetZDFVideoSources. str falls None
		# headers = {'Api-Auth': "Bearer d2726b6c8c655e42b68b0db26131b15b22bd1a32",'Host':"api.zdf.de", 'Accept-Encoding':"gzip, deflate, sdch, br", 'Accept':"application/vnd.de.zdf.v1.0+json"}
		headers = {'Api-Auth': apiToken,'Host':"api.zdf.de", 'Accept-Encoding':"gzip, deflate, sdch, br", 'Accept':"application/vnd.de.zdf.v1.0+json"}
	# Log(headers)		# bei Bedarf
	
	# Bei Anforderung von profile_url mittels urllib2.urlopen ssl.SSLContext erforderlich - entf. bei JSON.ObjectFromURL
	request = JSON.ObjectFromURL(profile_url, headers=headers)				# 3. Playerdaten ermitteln
	request = json.dumps(request, sort_keys=True, indent=2, separators=(',', ': '))  # sortierte Ausgabe
	Log(request[:20])	# "canonical" ...
	request = str(request)				# json=dict erlaubt keine Stringsuche, json.dumps klappt hier nicht
	request = request.decode('utf-8', 'ignore')	
	# Log(request)		# bei Bedarf, ev. reicht nachfolg. mainVideoContent
	
	pos = request.rfind('mainVideoContent')				# 'mainVideoContent' am Ende suchen
	request_part = request[pos:]
	# Log(request_part)			# bei Bedarf
	old_videodat = stringextract('http://zdf.de/rels/streams/ptmd\": \"', '\",', request_part)	
	# Bsp.: /tmd/2/portal/vod/ptmd/mediathek/161021_hsh_hsh'
	# Log(old_videodat)	
	old_videodat_url = 'https://api.zdf.de' + old_videodat					# 4. Videodaten ermitteln
	# neu ab 20.1.2016: uurl-Pfad statt ptmd-Pfad ( ptmd-Pfad fehlt bei Teilvideos)
	videodat = stringextract('"uurl": "', '"', request_part)	# Bsp.: 161118_clip_5_hsh
	if videodat == '':												# fehlt manchmal, dann auch kein Video verfügbar
		Log('videodat: nicht in request_part enthalten')
		return '','',''
	
	ptmd_player = 'ngplayer_2_3'
	videodat_url = stringextract('ptmd-template": "', '",', request_part)
	videodat_url = videodat_url.replace('{playerId}', ptmd_player) 				# ptmd_player injiziert 
	videodat_url = 'https://api.zdf.de' + videodat_url
	# videodat_url = 'https://api.zdf.de/tmd/2/portal/vod/ptmd/mediathek/'  	# unzuverlässig
	# videodat_url = videodat_url + videodat
	Log('old_videodat_url: ' + old_videodat_url); Log('videodat_url: ' + videodat_url); Log('uurl: ' + videodat); 	

	# ab 28.05.2017: Verwendung JSON.ObjectFromURL - Laden mittels urllib2.urlopen + ssl.SSLContext entbehrlich
	#	damit entfällt auch die Plattformunterscheidung Linux/Windows sowie die Nutzung einer Zertifikatsdatei
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
			img_src =  stringextract('data-srcset=\"', ' ', rec)			
			item_title = stringextract('class=\"item-title', 'class=\"item-description\">', rec)  
			teaser_cat =  stringextract('class=\"teaser-cat\">', '</span>', item_title)  
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
#  10.08.2017 Filter für Video-Sofort-Format, für m3u8-auto bereits in SenderLiveResolution erfolgt

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
	except:
		if playlist == '':
			msg = 'Playlist kann nicht geladen werden. URL: \r'
			msg = msg + url_m3u8
			Log(msg.replace('\r', ''))
			return ObjectContainer(message=msg)	  	# header=... ohne Wirkung	(?)			
  else:													
	playlist = Resource.Load(url_m3u8) 
  # Log(playlist)   # bei Bedarf
	 
  lines = playlist.splitlines()
  # Log(lines)
  lines.pop(0)		# 1. Zeile entfernen (#EXTM3U)
  BandwithOld = ''	# für Zwilling -Test (manchmal 2 URL für 1 Bandbreite + Auflösung) 
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
		if Resolution:	# fehlt manchmal (bei kleinsten Bandbreiten)
			Resolution = 'Auflösung ' + Resolution
		else:
			Resolution = 'Auflösung unbekannt'	# verm. nur Ton? CODECS="mp4a.40.2"
		Codecs = GetAttribute(line, 'CODECS')
		# als Titel wird die  < angezeigt (Sender ist als thumb erkennbar)
		if int(Bandwith) >  64000: 	# < 64000 vermutl. nur Audio, als Video keine Wiedergabe 
			title='Bandbreite ' + Bandwith
			if url.find('#') >= 0:	# Bsp. SR = Saarl. Rundf.: Kennzeichnung für abgeschalteten Link
				Resolution = 'zur Zeit nicht verfügbar!'
			if Bandwith == BandwithOld:	# Zwilling -Test
				title = 'Bandbreite ' + Bandwith + ' (2. Alternative)'
			if url.startswith('http') == False:   		# relativer Pfad? 
				pos = url_m3u8.rfind('/')				# m3u8-Dateinamen abschneiden
				url = url_m3u8[0:pos+1] + url 			# Basispfad + relativer Pfad
				
			Log(url); Log(title); Log(thumb); Log('Resolution')	
			# Video-Sofort-Format = Qualität: auto (m3u8) - nur 1 Objekt, auto bereits abgehandelt?	
			BandwithWish = Prefs['pref_setVideoFormatLive']			# leer, auto oder Bandbreitenwert
			Log(BandwithWish); 
			if BandwithWish and BandwithWish.endswith('auto') == False: 
				BandwithWish = BandwithWish.split('>')[1].strip()	# Bsp. "m3u8-Streaming: Bandbreite > 100000"
				Log(Bandwith); Log(BandwithWish);
				if int(Bandwith) > int(BandwithWish):				# Bandbreite größer als Wunschbandbreite?
					container.add(CreateVideoStreamObject(url=url, title=title, 		
						summary=Resolution+geoblock, tagline=title, meta=Codecs, thumb=thumb, 	
						rtmp_live='nein', resolution=''))
					return container					# nur dieser gewünscht
			else:										# Objekte für alle gefundenen Bandbreiten
				container.add(CreateVideoStreamObject(url=url, title=title, 		
					summary=Resolution+geoblock, tagline=title, meta=Codecs, thumb=thumb, 	
					rtmp_live='nein', resolution=''))								
			BandwithOld = Bandwith
				

  	i = i + 1	# Index für URL
  #Log (len(container))	# Anzahl Elemente
  if len(container) == 0:	# Fehler, zurück zum Hauptmenü
  		container.add(DirectoryObject(key=Callback(Main),  title='Problem mit Video-Sofort-Format oder m3u8-Datei', 
			tagline='Video-Sofort-Format nicht gefunden oder fehlerhafte m3u8-Datei', thumb=thumb)) 
	
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
	# Entferne: Frage-, Ausrufez., Hochkomma, Komma und #@!%^&*()+
	fname = (fname.replace(' ','_').replace('|','_').replace('___','_').replace('.','_')) 
	fname = (fname.replace('__','_').replace(':','-'))
	fname = (fname.replace('?','').replace('!','').replace('"','').replace('#','')
		.replace('*','').replace('@','').replace('%','').replace('^','').replace('&','')
		.replace('(','').replace(')','').replace(',','').replace('+','-'))	
	
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

