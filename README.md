﻿Plex-Plugin-ARDMediathek2016
===================
#### 09.01.2020 Support ist eingestellt - Nachfolgeplugin ist [Kodi-Addon-ARDundZDF](https://github.com/rols1/Kodi-Addon-ARDundZDF/releases/latest), [Forum Kodinerds.net](https://www.kodinerds.net/index.php/Thread/64244-RELEASE-Kodi-Addon-ARDundZDF)

#### 30.05.2019 bitte den ARD-Hinweis zur Abschaltung beachten. Mit der Abschaltung entfällt derSupport für Plex-Plugin-ARDMediathek2016. Das Repo bleibt voraussichtlich noch ca. für ein Jahr danach aktiv und wird danach gelöscht.

#### 29.05.2019 ab Plexmediaserver-Version 1.15.6.1079 ist auch mit dem Webclient die Unterstützung für Plugins weggefallen (für andere Clients bereits früher).  Es existiert eine ältere noch funktionierende Lösung: https://forums.plex.tv/t/rel-ardundzdf/309751/19

![Abschaltung ](https://aws1.discourse-cdn.com/plex/optimized/3X/4/d/4d01bb24fae46529c0ec120ec35479278022416d_2_690x327.png)


Plex Plugin für die ARD Mediathek - mit Live-TV der ARD + weiteren Sendern
ab Version 2.0.0 mit ZDF Mediathek, ab Version 3.4.8 zusäzlich mit ZDFmobile 

Download aktuelle Version: https://github.com/rols1/Plex-Plugin-ARDMediathek2016/releases/latest
![Downloads](https://img.shields.io/github/downloads/rols1/Plex-Plugin-ARDMediathek2016/total.svg "Downloads")

Das Plugin löst den Vorgänger Plex-Plugin-ARDMediathek2015 ab. Die ZDF Mediathek ist ab Version 2.1.1 integriert.
Der Relaunch des ZDF-Mediathek-Internetangebots vom 28.10.2016 ist eingearbeitet 

#### Rückmeldungen willkommen:
Im Forum: https://forums.plex.tv/discussion/213947/rel-plex-plugin-ardmediathek2016
direkt: rols1@gmx.de 
  
Funktionen ab Version 2.2.0: 
===================

#### ARD Mediathek:  
- Suche nach Sendungen
- Sendung Verpasst (Sendungen der letzten 7 Tage)
- Sendungen A-Z
- Filme
- Dokus
- Serien
- Themen
- Rubriken
- MeistGesehen
- Neueste Videos
- am besten bewertet
- Barrierearm (Hörfassung)
- Bilderserien

#### ZDF Mediathek: 
- Suche nach Sendungen
- Sendung Verpasst (Sendungen der letzten 7 Tage)
- Sendungen A-Z
- Rubriken
- MeistGesehen
- Neu in der Mediathek
- Barrierearm (Hörfassung)
- ZDFenglish
- ZDFarabic
- Bilderserien

#### Radio-Podcasts:
- Sendungen A-Z
- Rubriken
- Radio-Feature
- Radio-Tatort
- Neueste Audios
- Meist abgerufen
- Refugee-Radio
- Podcast-Favoriten (manuell erweiterbar)

#### TV-Live-Streams (30.08.2018: 33 Sender), Aufnahmefunktion: 
- ARD- und ZDF-Sender überregional und regional, einige ausgewählte Privatsender

#### Radio-Live-Streams der ARD:
- alle Radiosender von Bayern, HR, mdr, NDR, Radio Bremen, RBB, SR, SWR, WDR, Deutschlandfunk. Insgesamt 10 Stationen, 63 Sender
 
#### Videobehandlung ARD Mediathek und ZDF Mediathek:
- Videostreams: Auflistung der verfügbaren Angebote an Bandbreiten + Auflösungen (falls verfügbar: Audio ohne Video)
- Videoclips: Auflistung der verfügbaren Angebote an Qualitätstufen sowie zusätzlich verfügbarer Videoformate (Ausnahme HDS + SMIL) 

#### Downloadoption ab Version 2.6.7 (cURL oder wget eforderlich)
- Download von Videos im ARD-Bereich
- Download von Videos im ZDF-Bereich
- Download von Podcasts - bei Podcast-Favoriten zusätzlich Sammeldownloads 
- Tools zum Bearbeiten des Download-Verzeichnisses (Verzeichnisse festlegen, Verschieben, Löschen)

#### Update-Modul
- nach der Erst-Installation können weitere Updates durch das Plugin installiert werden

INSTALLATION:
===================  
Installationshilfe von Otto Kerner (Plex-Forum Mai 2015):
Anleitung zum manuellen Installieren von Plex Software-Bundles (Channels, Agenten, Scanner):
- zip-Datei von Github herunterladen
- zip auspacken, heraus kommt ein Ordner namens "Plex-Plugin-ARDMediathek2016-master"
- Diesen Ordner umbenennen in "ARDMediathek2016.bundle"
- den kompletten Ordner kopieren ins Plex Datenverzeichnis, in den Unterordner /Plug-ins

ein Neustart von Plex oder ein vorheriges Beenden von Plex ist i.d.R. nicht erforderlich
Beim Aktualisieren einfach den .bundle Ordner löschen und die neue Version an seine Stelle kopieren.
Ergänzung:
 
### Ergänzung
beim Download der zip-Datei aus Plex-Plugin-ARDMediathek2016/release entfällt das Umbenennen.

Credits:
===================  
- Credits to [coder-alpha] https://forums.plex.tv/discussion/166602/rel-ccloudtv-channel-iptv/p1): (Channel updater, based on Channel updater by sharkone/BitTorrent.bundle)
- Credits to [Arauco] (https://forums.plex.tv/profile/Arauco): processing of Logos and Icons

Hauptmenü:
===================  
![img](https://us.v-cdn.net/6025034/uploads/editor/t4/xrwomsb0zpaq.png)

Suche in ZDF Mediathek:
===================  
![img](https://us.v-cdn.net/6025034/uploads/editor/d5/lsawdl1xybzq.png)

Videoformate ZDF Mediathek:
===================  
![img](https://us.v-cdn.net/6025034/uploads/editor/pm/8y069jf7ad38.png)

TV Livesender Vorauswahl:
===================  
![img](https://us.v-cdn.net/6025034/uploads/editor/i5/vo1g066f7n9n.jpg)

Radio Livesender:
===================  
![img](https://us.v-cdn.net/6025034/uploads/editor/m7/qibbk5zksgkj.png)

Podcast-Menü:
===================  
![img](https://us.v-cdn.net/6025034/uploads/editor/mx/pgmo59s3layj.png)

Podcast-Favoriten:
===================  
![img](https://us.v-cdn.net/6025034/uploads/editor/as/s2ogw2bx2s5h.png)



