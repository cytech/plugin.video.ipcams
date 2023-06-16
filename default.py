import sys
import os
from urllib.parse import parse_qsl, unquote_plus
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs

__addon__ = xbmcaddon.Addon()
__addonID__ = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__path__ = __addon__.getAddonInfo('path')
__iconpath__ = os.path.join(xbmcvfs.translatePath(__path__), 'resources', 'lib', 'media')
__fanart__ = os.path.join(xbmcvfs.translatePath(__path__), 'fanart.jpg')

__LS__ = __addon__.getLocalizedString


def paramsToDict(parameters):
    return dict(parse_qsl(parameters))


def writeLog(message, level=xbmc.LOGDEBUG):
    xbmc.log('[%s] %s' % (__addonID__, message), level)


arguments = sys.argv

if len(arguments) > 1:
    if arguments[0][0:6] == 'plugin':
        _addonHandle = int(arguments[1])
        arguments.pop(0)
        arguments[1] = arguments[1][1:]

    params = paramsToDict(arguments[1])

    item = [__LS__(30011) % '1', __LS__(30011) % '2', __LS__(30011) % '3', __LS__(30011) % '4', __LS__(30011) % '5', __LS__(30011) % '6']
    cam = [__addon__.getSetting('cam1'), __addon__.getSetting('cam2'), __addon__.getSetting('cam3'),
           __addon__.getSetting('cam4'), __addon__.getSetting('cam5'), __addon__.getSetting('cam6')]
    loc = [__addon__.getSetting('loc1'), __addon__.getSetting('loc2'), __addon__.getSetting('loc3'),
           __addon__.getSetting('loc4'), __addon__.getSetting('loc5'), __addon__.getSetting('loc6')]


_atleast = False
for i in range(int(__addon__.getSetting('numcams'))):
    li = xbmcgui.ListItem(label=loc[i] if loc[i] != '' else item[i], label2=item[i])
    icon = xbmcvfs.translatePath(os.path.join( __iconpath__, 'ipcam_%s.png' % (i + 1)))
    li.setArt({'icon': icon, 'fanart': __fanart__})
    li.setProperty('isPlayable', 'true')
    li.setInfo('video', {'tag': 'Documentary'})

    if cam[i] != '':
        xbmcplugin.addDirectoryItem(_addonHandle, cam[i], li)
        _atleast = True

if _atleast:
    xbmcplugin.endOfDirectory(_addonHandle)
else:
    xbmcgui.Dialog().ok(__addonname__, __LS__(30015))
