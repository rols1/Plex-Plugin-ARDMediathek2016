# -*- coding: utf-8 -*-
################################################################################
#			ARD_Bildgalerie.py - Part of Pex-Plugin-ARDMediathek2016
#
################################################################################

PREFIX		 	= "/video/ardmediathek2016/ARD_Bildgalerie"


# ----------------------------------------------------------------------			
@route(PREFIX + '/page')	# Bilderserien ARD - Seitenübersicht
def page(name, path, offset):		
	Log('page:');
	oc = ObjectContainer(title2=name.decode(encoding="utf-8"), art = ObjectContainer.art)
	oc = home(cont=oc, ID='ARD')							# Home-Button
	
	page = HTTP.Request(path).content
	Log(len(page))
				
	entries = blockextract('div class="teaser',  page)
	Log(len(entries))
	if len(entries) == 0:
		err = 'keine weitere Bilderserie gefunden'
		return ObjectContainer(header='Fehler', message=err)
					
	for rec in entries:
		headline =  stringextract('class="headline">', '</h3>', rec)
		href =  stringextract('href="', '"', headline)
		title =  cleanhtml(headline)
		Log(href[:44])
		teasertext =  stringextract('class="teasertext">', '</a></p>', rec)
		# Log(teasertext)
		teasertext = cleanhtml(teasertext)
		teasertext = unescape(teasertext)
		teasertext = teasertext.replace('Bild lädt...', '')
		summ = teasertext
		title = cleanhtml(title)
		# Log(teasertext); Log(title)
		tag = ''
		if 'zur  Bildergalerie' in teasertext:
			summ = teasertext.split('zur  Bildergalerie')[0]
			tag = teasertext.split('zur  Bildergalerie')[1]
				
		title = title.decode(encoding="utf-8")
		summ = summ.decode(encoding="utf-8")
		tag = tag.decode(encoding="utf-8")
		Log(title); Log(summ); Log(tag) 
		
		oc.add(DirectoryObject(key=Callback(Hub,title=title, path=href), 
			title=title, summary=summ, tagline=tag, thumb=R('ard-bilderserien.png')))	# keine thumbs in den Übersichten				
		
	return oc
#-----------------------
@route(PREFIX + '/Hub')	# einzelne Bilderserie ARD
# 02.09.2018 SSL-Fehler mit HTTP.Request - Umstellung auf get_page mit urllib2.Request.
#	Dafür get_page um Alternative mit urllib2.Request + SSLContext erweitert.
# 
def Hub(title, path):		
	Log('Hub: %s' % path)
	title = title.decode(encoding="utf-8")
	oc = ObjectContainer(title2=title.decode(encoding="utf-8"), art = ObjectContainer.art)
	
	page, msg = get_page(path)						# 1. Seite laden	
	if page == '':	
		return 	ObjectContainer(header='Error', message=msg)
									
	Log(len(page))
	
	if '//www.hessenschau.de' in path:			# Schema Hessenschau
		href_rec, summ_rec, picnr_rec, cr_rec = get_pics_hessenschau(page)
	if '//www.ard.de' in path:					# Schema ARD
		href_rec, summ_rec, picnr_rec, cr_rec = get_pics_ard(page)
	if '//www.br.de' in path:					# Schema BR
		href_rec, summ_rec, picnr_rec, cr_rec = get_pics_br(page)
	if '//www.radiobremen.de' in path:			# Schema Bremen
		href_rec, summ_rec, picnr_rec, cr_rec = get_pics_bremen(page)
	if 'swr.de' in path:						# Schema Südwestfunk	//www.swr.de, //swr.de
		href_rec, summ_rec, picnr_rec, cr_rec = get_pics_swr(page)
	if '//www.daserste.de' in path:			# Schema Das Erste
		href_rec, summ_rec, picnr_rec, cr_rec = get_pics_daserste(page)
		
	if len(href_rec) == 0:
		err = 'keine Bilder gefunden zu: %s' % title
		return ObjectContainer(header='Fehler', message=err)	
		
	for i in range (len(href_rec)):
		href=href_rec[i]; summ=summ_rec[i]; picnr=picnr_rec[i]; cr=cr_rec[i]							
		# Log(href); Log(summ); Log(picnr); Log(cr)
		if href:
			oc.add(PhotoObject(
				key=href,
				rating_key='%s.%s' % (Plugin.Identifier, 'Bild ' + str(i)),	# rating_key = eindeutige ID
				summary=summ,
				title="Bild %s | %s" % (picnr, cr),
				thumb = href			# wie key
				))
	
	return oc

#-----------------------
def get_pics_hessenschau(page):		# extrahiert Bildergalerie aus Hessenschau-Seite
	Log('get_pics_hessenschau')
	href_rec=[]; summ_rec=[]; picnr_rec=[]; cr_rec=[]
	
	slider = stringextract('data-hr-slider-dynamic', '<div class', page)
	# Log(slider)
	href_items =  stringextract('url":"', '"', slider)
	# Log(href_items)
	try:
		inline = HTTP.Request(href_items).content		# Bildbeschreibungen ausgelagert, können fehlen
		inline_items = blockextract('gallery__imageHeadline', inline)
	except:
		inline_items = ''
	Log(len(inline_items))
	
	href_next = '123'					#  href in control enthält Link der Folgeseite, Schluss: #
	i=0
	while href_next:					# 1. Seite + Folgeseiten auswerten
		control =  stringextract('gallery__control--right', '</div>', page)
		href_next =  stringextract('href="', '#', control)	# endet mit #
		Log(href_next)
		# pic_16to9 	= stringextract('twitter:image" content="', '"', page)
		pic_pre		= stringextract('centerHorizontal--absolute" src="', '"', page)	# orig. Vorschau
		pic_retina	= ''
		data_set	= stringextract('data-srcset=', '</div>', page)		# dahinter mehr Sets (Verweise)
		data_set	= blockextract('http', data_set)
		pic_href = ''
		for pic in data_set:
			# Alternativen: "medium.jpg", "v-Xto9.jpg" 
			if "retina.jpg" in pic: 		# beste Darst. in  Webclient 2.7.0
				pic_href = pic.split(' ')[0]# Bsp. ..Xto9.jpg 646w
				Log(pic_href)
				break
				
		if 	pic_href == '':
			pic_href = data_set[-1]			# Fallback: letztes Bild aus dem Set, Alternative:
			pic_href = pic_href.split(' ')[0]	#  twitter-pic aus head (meta)
			
		descr = inline_items[i]			# 4 Zeilen + Leerzeilen dazwischen
		# Log(descr)
		pic_nr =  stringextract('headline">', '</h3>',descr)
		pic_nr = pic_nr.strip()
		summ   =  stringextract('copytext">', '</p>',descr)
		summ   =  cleanhtml(summ)
		summ   =  unescape(summ)
		summ = summ.decode(encoding="utf-8")		
		cr = 'Bildrechte: ' + stringextract('&copy;', '</p>',descr)		# Copyright
								
		Log(pic_nr); Log(summ); Log(pic_href);
		href_rec.append(pic_href); summ_rec .append(summ); picnr_rec.append(pic_nr); cr_rec.append(cr)
		if href_next == '':
			break
		page = HTTP.Request(href_next).content		# nächste Seite laden				
		i=i+1
	
	return href_rec, summ_rec, picnr_rec, cr_rec

#-----------------------
def get_pics_ard(page):		# extrahiert Bildergalerie aus ARD-Seite
	Log('get_pics_ard')
	href_rec=[]; summ_rec=[]; picnr_rec=[]; cr_rec=[]
	
	page =  stringextract('data-ctrl-slidable=', 'controls sliding',page)
	records = blockextract('img hideOnNoScript',  page)
	
	i=0
	for rec in records:	
		pic_href =  'http://www.ard.de'+ stringextract('img" src="', '"', rec)
		pic_href = pic_href.replace('/512', '/1024') # man. Anpassung möglich
		pic_nr = "%s/%s" % (str(i+1), str(len(records)))
		summ   =  stringextract('alt="', '"',rec) 	 # cr in summ enthalten
		summ   =  unescape(summ)
		summ = summ.decode(encoding="utf-8")		
		cr = summ							# Titel: "Bild %s | %s" % (picnr, cr)
								
		Log(pic_nr); Log(summ); Log(pic_href);
		href_rec.append(pic_href); summ_rec .append(summ); picnr_rec.append(pic_nr); cr_rec.append(cr)
		i=i+1
	
	return href_rec, summ_rec, picnr_rec, cr_rec

#-----------------------
def get_pics_br(page):		# extrahiert Bildergalerie aus Bayern-Seite
	Log('get_pics_br')
	href_rec=[]; summ_rec=[]; picnr_rec=[]; cr_rec=[]
	
	json_url = 'http://www.br.de' + stringextract('data-gallery-json-url="', '"', page)	
	page = HTTP.Request(json_url).content			# Bilder-Links von json-Seite laden
	records = blockextract('permalink":',  page)
	
	i=0
	for rec in records:	
		urls = 	blockextract('"url":',  rec)	# versch. Bildformate
		url  = 	urls[-1]						# größtes Format am Schluss
		pic_href =  'http:'+ stringextract('url": "', '"', url)	# Bsp. "url": "//www.br.de/presse/..
		pic_nr = "%s/%s" % (str(i+1), str(len(records)))
		summ   =  stringextract('"textAlt": "', '"',rec)
		summ   =  unescape(summ)
		summ = summ.decode(encoding="utf-8")		
		cr = summ							# Titel: "Bild %s | %s" % (picnr, cr),
								
		Log(pic_nr); Log(summ); Log(pic_href);
		href_rec.append(pic_href); summ_rec .append(summ); picnr_rec.append(pic_nr); cr_rec.append(cr)
		i=i+1
	
	return href_rec, summ_rec, picnr_rec, cr_rec
#-----------------------
def get_pics_bremen(page):		# extrahiert Bildergalerie aus Bremen-Seite
	Log('get_pics_bremen')
	href_rec=[]; summ_rec=[]; picnr_rec=[]; cr_rec=[]

	page =  stringextract('bildgalerie-scroll-box', '</ul>',page)
	records = blockextract('<li><img',  page)
	
	i=0
	for rec in records:	
		pic_href =  'http://www.radiobremen.de'+ stringextract('src="', '"', rec)
		pic_href = pic_href.replace('-bildergaleriethumb.jpg', '-slideshow.jpg') # s. id="grosses_bild"
		pic_nr = "%s/%s" % (str(i+1), str(len(records)))
		summ   =  stringextract('alt="', '"',rec) 	 # cr in summ enthalten
		summ   =  unescape(summ)
		summ = summ.decode(encoding="utf-8")		
		cr = summ							# Titel: "Bild %s | %s" % (picnr, cr)
								
		Log(pic_nr); Log(summ); Log(pic_href);
		href_rec.append(pic_href); summ_rec .append(summ); picnr_rec.append(pic_nr); cr_rec.append(cr)
		i=i+1
	
	return href_rec, summ_rec, picnr_rec, cr_rec

#-----------------------
def get_pics_swr(page):		# extrahiert Bildergalerie aus SWR-Seite
	Log('get_pics_swr')
	href_rec=[]; summ_rec=[]; picnr_rec=[]; cr_rec=[]

	page1 =  stringextract('bildgalerie-scroll-box', '</ul>',page)
	records = blockextract('<li><img',  page1)
	Log('records: ' + str(len(records)))
	
	i=0
	for rec in records:	
		pic_href =  'http://www.swr.de'+ stringextract('src="', '"', rec)
		pic_href = pic_href.replace('-bildergaleriethumb.jpg', '-slideshow.jpg') # s. id="grosses_bild"
		pic_nr = "%s/%s" % (str(i+1), str(len(records)))
		summ   =  stringextract('alt="', '"',rec) 	 # cr in summ enthalten
		summ   =  unescape(summ)
		summ = summ.decode(encoding="utf-8")		
		cr = summ							# Titel: "Bild %s | %s" % (picnr, cr)
								
		Log(pic_nr); Log(summ); Log(pic_href);
		href_rec.append(pic_href); summ_rec .append(summ); picnr_rec.append(pic_nr); cr_rec.append(cr)
		i=i+1
		
	if len(href_rec) == 0:						# 2. Variante, Blöcke data-ctrl-gallerylayoutable
		records = blockextract('data-ctrl-gallerylayoutable',  page)
		Log('records: ' + str(len(records)))		
		for rec in records:	
			pics = stringextract('<img src', '>',rec)
			pics = blockextract('https', pics)			# Set verschied. Größen
			summ = ''
			try:
				Log(pics[-1])							# letztes = größtes
				summ   =  stringextract('teasertext">', '</p>',rec) # kann fehlen, s.o. (alt)
				pic_href = re.search(r'https(.*)jpg',pics[-1]).group(0)
			except:
				continue
			
			pic_nr = "%s/%s" % (str(i+1), str(len(records)))
			if summ == '':
				summ   =  stringextract('alt="', '"', pics[-1]) 
			summ   =  unescape(summ)
			summ = summ.decode(encoding="utf-8")		
			cr = summ							# Titel: "Bild %s | %s" % (picnr, cr)
									
			Log(pic_nr); Log(summ); Log(pic_href);
			href_rec.append(pic_href); summ_rec .append(summ); picnr_rec.append(pic_nr); cr_rec.append(cr)
			i=i+1	
			
	if len(href_rec) == 0:						# 3. Variante, Blöcke class="mediagallery-backlink"
		records = blockextract('class="mediagallery-backlink"',  page)
		Log('records: ' + str(len(records)))
		for rec in records:	
			pic_href = stringextract('itemprop="url" href="', '"', rec)
			pic_nr = "%s/%s" % (str(i+1), str(len(records)))
			summ   =  stringextract('description">', '<',rec) 	
			summ   =  unescape(summ.strip())
			summ = summ.decode(encoding="utf-8")		
			cr = summ							# Titel: "Bild %s | %s" % (picnr, cr)
									
			Log(pic_nr); Log(summ); Log(pic_href);
			href_rec.append(pic_href); summ_rec .append(summ); picnr_rec.append(pic_nr); cr_rec.append(cr)
			i=i+1		
						
	return href_rec, summ_rec, picnr_rec, cr_rec

#-----------------------
def get_pics_daserste(page):		# extrahiert Bildergalerie aus Das Erste-Seite
	Log('get_pics_daserste')
	href_rec=[]; summ_rec=[]; picnr_rec=[]; cr_rec=[]

	page =  stringextract('div data-ctrl-slidable=', 'id="footer">',page)
	records = blockextract('class="mediaLink',  page)
	
	i=0
	for rec in records:	
		pic_href =   'http://www.daserste.de' + stringextract("'xl':{'src':'", "'", rec)	# img data set
		Log(pic_href)
		if  pic_href == 'http://www.daserste.de':
			pic_href =  'http://www.daserste.de' + stringextract('src="', '"', rec)
			pic_href = pic_href.replace('-bildergaleriethumb.jpg', '-slideshow.jpg') # s. id="grosses_bild"
		
		pic_nr = "%s/%s" % (str(i+1), str(len(records)))
		summ   =  stringextract('teasertext">', '</p>',rec) # kann fehlen, s.o. (alt)
		summ   =  summ.strip()
		if summ == '':
			summ   =  stringextract('alt="', '"',rec) 	 
		summ   =  unescape(summ)
		summ = summ.decode(encoding="utf-8")		
		cr = stringextract('title="', '"',rec) 					# Titel: "Bild %s | %s" % (picnr, cr)
								
		Log(pic_nr); Log(summ[:40]); Log(pic_href);
		href_rec.append(pic_href); summ_rec .append(summ); picnr_rec.append(pic_nr); cr_rec.append(cr)
		i=i+1
	
	return href_rec, summ_rec, picnr_rec, cr_rec
