# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para quierodibujosanimados
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

__category__ = "A"
__type__ = "generic"
__title__ = "Quiero dibujos animados"
__channel__ = "quierodibujosanimados"
__language__ = "ES"
__creationdate__ = "20121112"

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.quierodibujosanimados mainlist")

    #itemlist.append( Item(channel=__channel__ , action="novedades"  , title="Novedades" , url="http://www.quierodibujosanimados.com/"))
    return series( Item(channel=__channel__ , action="series"     , title="Series"    , url="http://www.quierodibujosanimados.com/"))

def series(item):
    logger.info("pelisalacarta.channels.quierodibujosanimados series")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<ul class="categorias">(.*?)</ul')
    
    #<a href="http://www.quierodibujosanimados.com/cat/popeye-el-marino/38" title="Popeye el marino">Popeye el marino</a>
    patron = '<a href="([^"]+)"[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="episodios" , title=title , url=url, thumbnail=thumbnail, plot=plot, fanart="http://pelisalacarta.mimediacenter.info/fanart/quierodibujosanimados.jpg"))        

    next_page_url = scrapertools.find_single_match(data,'</span[^<]+<a href="([^"]+)">')
    if next_page_url!="":
        itemlist.append( Item(channel=__channel__, action="episodios", title=">> Página siguiente" , url=urlparse.urljoin(item.url,next_page_url) , folder=True, fanart="http://pelisalacarta.mimediacenter.info/fanart/quierodibujosanimados.jpg") )

    return itemlist

def episodios(item):
    logger.info("pelisalacarta.channels.quierodibujosanimados episodios")

    '''
    <li>
    <div class="info">
    <h2><a href="http://www.quierodibujosanimados.com/Caillou-raton-de-biblioteca/954" title="Caillou ratón de biblioteca">Caillou ratón de biblioteca</a></h2>
    <p>Caillou volvía con su hermanita Rosi y su mamá de la biblioteca y traían un montón de libros que Caillou quería leer, especialmente uno de piratas. Capítulo titulado "Caillou ratón de biblioteca".</p>
    <div class="pie">
    <div class="categoria">
    <span>Categor&iacute;a:</span>
    <a href="http://www.quierodibujosanimados.com/cat/caillou/14" title="Caillou" class="categoria">Caillou</a>
    </div>
    <div class="puntuacion">
    <div class="rating_16 punt_0" data-noticia="954">
    <span>0.5</span>
    <span>1</span>
    <span>1.5</span>
    <span>2</span>
    <span>2.5</span>
    <span>3</span>
    <span>3.5</span>
    <span>4</span>
    <span>4.5</span>
    <span>5</span>
    </div>
    </div>
    </div>
    <span class="pico"></span>
    </div>
    <div class="dibujo">
    <a href="http://www.quierodibujosanimados.com/Caillou-raton-de-biblioteca/954" title="Caillou ratón de biblioteca" class="thumb">
    <img src="http://www.quierodibujosanimados.com/i/thm-Caillou-raton-de-biblioteca.jpg" alt="Caillou ratón de biblioteca" width="137" height="174" />
    </a>
    <h4><a href="http://www.quierodibujosanimados.com/Caillou-raton-de-biblioteca/954" title="Caillou ratón de biblioteca">Caillou ratón de biblioteca</a></h4>
    </div>
    </li>
    '''

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    patron  = '<div class="dibujo"[^<]+'
    patron += '<a href="([^"]+)" title="([^"]+)"[^<]+'
    patron += '<img src="([^"]+)"'

    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, fanart="http://pelisalacarta.mimediacenter.info/fanart/quierodibujosanimados.jpg"))

    next_page_url = scrapertools.find_single_match(data,'</span[^<]+<a href="([^"]+)">')
    if next_page_url!="":
        itemlist.append( Item(channel=__channel__, action="episodios", title=">> Página siguiente" , url=urlparse.urljoin(item.url,next_page_url) , folder=True, fanart="http://pelisalacarta.mimediacenter.info/fanart/quierodibujosanimados.jpg") )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    from servers import servertools

    # mainlist
    serie_itemlist = mainlist(Item())
    
    # Comprueba que todas las opciones tengan algo (excepto el buscador)
    for serie_item in serie_itemlist:
        episodio_itemlist = episodios(serie_item)

        for episodio_item in episodio_itemlist:
            mirrors = servertools.find_video_items(item=episodio_item)

            if len(mirrors)>0:
                return True

    return False