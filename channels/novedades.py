# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para novedades
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

#Propiedades del Canal:
__active__ = False
__adult__ = False
__category__ = "F"
__changes__ = ""
__channel__ = "novedades"
__creationdate__ = ""
__date__ = ""
__language__ = "ES"
__thumbnail__ = ""
__title__ = "Novedades"
__type__ = "generic"
__version__ = 0

import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "novedades"
__category__ = "F"
__type__ = "generic"
__title__ = "Novedades"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item,preferred_thumbnail="squares"):
    logger.info("pelisalacarta.channels.novedades mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="peliculas"            , title="Películas", thumbnail="%sthumb_canales_peliculas.png"))
    itemlist.append( Item(channel=__channel__, action="peliculas_infantiles" , title="Para niños", thumbnail="%sthumb_canales_infantiles.png"))
    itemlist.append( Item(channel=__channel__, action="series"               , title="Episodios de series", thumbnail="%sthumb_canales_series.png"))
    itemlist.append( Item(channel=__channel__, action="anime"                , title="Episodios de anime", thumbnail="%sthumb_canales_anime.png"))
    itemlist.append( Item(channel=__channel__, action="documentales"         , title="Documentales", thumbnail="%sthumb_canales_documentales.png"))

    return itemlist

def peliculas(item):
    logger.info("pelisalacarta.channels.novedades peliculas")

    itemlist = []

    import zpeliculas
    item.url = "http://www.zpeliculas.com"
    itemlist.extend( zpeliculas.peliculas(item) )

    import cinetux
    item.url = "http://www.cinetux.org/"
    itemlist.extend( cinetux.peliculas(item) )

    import divxatope
    item.url = "http://www.divxatope.com/categoria/peliculas-castellano"
    itemlist.extend( divxatope.lista(item) )

    import gnula
    item.url = "http://gnula.nu/peliculas-online/lista-de-peliculas-online-parte-1/"
    itemlist.extend( gnula.peliculas(item)[:20] )

    sorted_itemlist = []

    for item in itemlist:

        if item.extra!="next_page" and not item.title.startswith(">>"):
            item.title = item.title + " ["+item.channel+"]"
            sorted_itemlist.append(item)

    sorted_itemlist = sorted(sorted_itemlist, key=lambda Item: Item.title)    

    return sorted_itemlist

def peliculas_infantiles(item):
    logger.info("pelisalacarta.channels.novedades peliculas_infantiles")

    itemlist = []

    import zpeliculas
    item.url = "http://www.zpeliculas.com/peliculas/p-animacion/"
    itemlist.extend( zpeliculas.peliculas(item) )

    import cinetux
    item.url = "http://www.cinetux.org/genero/infantil"
    itemlist.extend( cinetux.peliculas(item) )

    import gnula
    item.url = "http://gnula.nu/generos/lista-de-peliculas-del-genero-infantil/"
    itemlist.extend( gnula.peliculas(item)[:20] )

    import oranline
    item.url = "http://www.oranline.com/Películas/infantil/"
    itemlist.extend( oranline.peliculas(item) )

    sorted_itemlist = []

    for item in itemlist:

        if item.extra!="next_page" and not item.title.startswith(">>"):
            item.title = item.title + " ["+item.channel+"]"
            sorted_itemlist.append(item)

    sorted_itemlist = sorted(sorted_itemlist, key=lambda Item: Item.title)    

    return sorted_itemlist

def series(item):
    logger.info("pelisalacarta.channels.novedades series")

    itemlist = []

    import divxatope
    item.url = "http://www.divxatope.com/categoria/series"
    itemlist.extend( divxatope.lista(item) )

    import seriesflv
    item.url = "es"
    itemlist.extend( seriesflv.ultimos_episodios(item) )

    sorted_itemlist = []

    for item in itemlist:

        if item.extra!="next_page" and not item.title.startswith(">>"):
            item.title = item.title + " ["+item.channel+"]"
            sorted_itemlist.append(item)

    sorted_itemlist = sorted(sorted_itemlist, key=lambda Item: Item.title)    

    return sorted_itemlist

def anime(item):
    logger.info("pelisalacarta.channels.novedades anime")

    itemlist = []

    import animeid
    item.url = "http://animeid.tv/"
    itemlist.extend( animeid.novedades_episodios(item) )

    import animeflv
    item.url = "http://animeflv.net/"
    itemlist.extend( animeflv.novedades(item) )

    sorted_itemlist = []

    for item in itemlist:

        if item.extra!="next_page" and not item.title.startswith(">>"):
            item.title = item.title + " ["+item.channel+"]"
            sorted_itemlist.append(item)

    sorted_itemlist = sorted(sorted_itemlist, key=lambda Item: Item.title)    

    return sorted_itemlist

def documentales(item):
    logger.info("pelisalacarta.channels.novedades documentales")

    itemlist = []

    import documaniatv
    item.url = "http://www.documaniatv.com/newvideos.html"
    itemlist.extend( documaniatv.novedades(item) )

    import oranline
    item.url = "http://oranline.com/Pel%C3%ADculas/documentales/"
    itemlist.extend( oranline.peliculas(item) )

    sorted_itemlist = []

    for item in itemlist:

        if item.extra!="next_page" and not item.title.startswith(">>"):
            item.title = item.title + " ["+item.channel+"]"
            sorted_itemlist.append(item)

    sorted_itemlist = sorted(sorted_itemlist, key=lambda Item: Item.title)    

    return sorted_itemlist
