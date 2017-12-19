################################################################################
#				update_single.py - Part of Pex-Plugin-ARDMediathek2016
#							Update von Einzeldateien
################################################################################
#import  urllib, os		# bereits geladen

PREFIX		 	= "/video/ardmediathek2016"
REPO_BASE 		= 'https://raw.githubusercontent.com/rols1/Plex-Plugin-ARDMediathek2016/master'
TRIGGER_FILE	= '/Contents/Resources/update_single_files'

################################################################################
# Aufruf: 	wie Plugin-Update - bei Pluginstart oder manuell (Einstellungen)
# Ablauf:		Funktion check_repo:
#			1. Repo-TRIGGER_FILE holen
#			2. Zeitstempel Repo-TRIGGER_FILE gegen Plugin-TRIGGER_FILE  vergleichen
#			2.1 Repo-TRIGGER_FILE leer: Abbruch - kein Austausch
#			2.2 Zeitstempel fehlt oder jünger: Rückgabe 1 = Austauschsignal
#				Funktion replace:
#			1. Repo-TRIGGER_FILE erneut holen
#			2. Austausch der gelisteten Dateien
#			3. Abschluss: Austausch Repo-TRIGGER_FILE gegen Plugin-TRIGGER_FILE
#			4. Hinweis: Plugin neu starten | betroffene Dateien 
#
# Austausch erfolgt auch, wenn update_single_files im Plugin fehlt
#
# Format Zeitstempel:  Datum | UTC-Sekunden (Konsole: date " | date +"%s)
#				Bsp.: So 17. Dez 22:32:12 CET 2017 | 1513546328
#				Die UTC-Sekunden ersparen hier Zeitfunktionen
################################################################################

@route(PREFIX + '/check_repo')
# Rückgabe: 
#	Fehler: 0, info-string (exception-string)
#	Erfolg: 1, info-string (ausgetauschte Dateien)
def check_repo():
	Log('update_single: check_repo')
		
	try:									# Repo-TRIGGER_FILE laden
		repo_cont = HTTP.Request(REPO_BASE + TRIGGER_FILE).content
		repo_cont = repo_cont.strip()
	except Exception as exception:
		Log(str(exception))
		repo_cont = ''
		return 0, str(exception) + ' (Github: update_single_files)'		
	Log(repo_cont)
	if repo_cont == '':						# leere Datei: kein Austausch
		Log('update_single_files: leer')
		return 0, 'alles aktuell'
	
	repo_lines = repo_cont.splitlines()
	stamp = repo_lines[0]					# Repo-Zeitstempel
	repo_stamp = stamp.split('|')[1]		# Bsp. 1513584263
	repo_stamp = int(repo_stamp.strip())
	Log('repo_stamp: ' + str(repo_stamp))
	
	# Hinw.: storage.join_path erwartet Liste der Pfadelemente - anders als os.path.join
	plugin_file = Core.storage.join_path(Core.bundle_path, 'Contents', 'Resources', 'update_single_files')
	Log(plugin_file)
	cont = ''
	Log(os.path.exists(plugin_file))
	if os.path.exists(plugin_file):
		try:								# Plugin-TRIGGER_FILE laden		
			cont = 	Core.storage.load(plugin_file)
		except Exceptionn as exception:			
			Log(str(exception))
			cont = ''

	# Austausch erfolgt auch, wenn update_single_files im Plugin fehlt
	if cont:
		lines = cont.splitlines()
		stamp = lines[0]							# Repo-Zeitstempel
		plugin_stamp = stamp.split('|')[1]			# Bsp. 1513584263
		plugin_stamp = int(plugin_stamp.strip())
		Log('plugin_stamp: ' + str(plugin_stamp))
		if repo_stamp <= plugin_stamp:				# Repo-Stempel älter: kein Austausch
			Log('repo_stamp <= plugin_stamp')
			return 0, 'alles aktuell'
		
		del lines[0]
	return 1, "Einzeldateien: " + ', '.join(lines)

#----------------------------------------------------------------

@route(PREFIX + '/replace')
# Rückgabe: ObjectContainer mit Exception- oder Hinweis-String 
def replace():
	Log('update_single: replace')
	
	try:							# Repo-TRIGGER_FILE holen - wie check_repo
		repo_cont = HTTP.Request(REPO_BASE + TRIGGER_FILE).content
	except Exception as exception:
		Log(str(exception))
		msg = str(exception) + ' (Github: update_single_files)'
		return ObjectContainer(header=L('Fehler'), message=msg)			
	Log(repo_cont)

	cnt = 0								# Start Austausch
	repo_lines = repo_cont.splitlines()
	del repo_lines[0]
	for line in repo_lines:
		if line.strip() == '':			# leer?
			continue
		line = line.replace('./', '/')	# ls-Ausgabe bereinigen
		repo_url = REPO_BASE + line
		# Log(repo_url)	
		try:
			cont = HTTP.Request(repo_url).content
			plugin_path = os.path.join(Core.bundle_path + line)
			Log(plugin_path)
			Core.storage.save(plugin_path, cont)
		except Exception as exception:			
			Log(str(exception))
			msg = str(exception) + ' (Plugin: %s)'	% line
			return ObjectContainer(header=L('Fehler'), message=msg)			
			
		cnt = cnt + 1

	plugin_file = Core.storage.join_path(Core.bundle_path, 'Contents', 'Resources', 'update_single_files')
	try:								# zum Schluß neues TRIGGER_FILE speichern
		Core.storage.save(plugin_file, repo_cont)	
	except Exception as exception:
		msg =  str(exception) + ' (Plugin: update_single_files)'
		return ObjectContainer(header=L('Fehler'), message=msg)			
	
	msg = 'Update erfolgreich - Plugin bitte neu starten |\r\n'		
	msg = msg + '%s Datei(en) erneuert | %s'	% (cnt, ', '.join(repo_lines))
	return ObjectContainer(header=L('Info'), message=msg)			

		
