# coding=utf-8
import sys
from urllib import urlencode
from urlparse import parse_qsl
import requests
import xbmcgui
import xbmcplugin
import xbmcaddon


URL = sys.argv[0]
HANDLE = int(sys.argv[1])
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36'
API_CONFIG = requests.get("https://twl-prod-static.s3.amazonaws.com/configs/projectConfig_smartclip.json", headers={'USER-AGENT':USER_AGENT}).json()
API_VERSION = requests.get(API_CONFIG['ivms']['version'], headers={'USER-AGENT':USER_AGENT}).json()['version_name']
VIDEO_API = API_CONFIG['ivms']['restapi'].replace("[version]", API_VERSION)


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.
    """
    return '{0}?{1}'.format(URL, urlencode(kwargs))


def list_pages():
    my_addon = xbmcaddon.Addon('plugin.video.tierweltlive')
    xbmcplugin.setPluginCategory(HANDLE, 'Start')
    xbmcplugin.setContent(HANDLE, 'videos')
    pages = {"Themen":"56", "Kanäle":"57", "Tiere":"58"}
    for page in pages:
        list_item = xbmcgui.ListItem(label=page)
        list_item.setArt({
            'thumb': my_addon.getAddonInfo('fanart'),
            'fanart': my_addon.getAddonInfo('fanart')
        })
        list_item.setInfo('video', {
            'plot': my_addon.getAddonInfo('description')
        })
        url = get_url(action='list_categories', page=pages[page], childs=False)
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, True)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(HANDLE)


def list_categories(page, childs):
    """
    Create the list of video categories in the Kodi interface.
    """
    xbmcplugin.setPluginCategory(HANDLE, 'Kategorien')
    xbmcplugin.setContent(HANDLE, 'videos')
    if childs == 'False':
        categories = requests.get(VIDEO_API + "containers/" + page + ".json", headers={'USER-AGENT':USER_AGENT}).json()['items']
    else: 
        categories = list(childs[1:-1].split(", "))
    for category in categories:
        if childs == 'False':
            category_module = category['module']
            category_id = category['id']
        else:
            category_module = "channel"
            category_id = category
        category_info = requests.get(VIDEO_API + category_module + "s/" + str(category_id) + ".json", headers={'USER-AGENT':USER_AGENT}).json()
        if childs == 'False':
            category_title = category['unicode']
        else:
            category_title = category_info['title']
        list_item = xbmcgui.ListItem(label=category_title)
        list_item.setInfo('video', {
            'title': category_title, 
            'plot': category_info['description'],
            'tag': category_info['tags'],
            'dateadded': category_info['created']
        })
        if 'web_airdate' in category_info:
            list_item.setInfo('video', {
                'premiered': category_info['web_airdate'],
                'aired': category_info['web_airdate']
            })
        list_item.setArt({
            'thumb': category_info['images'][1]['url'],
            'fanart': category_info['images'][1]['url']
        })
        url = get_url(action='list_videos', id=category_id, category=category_module)
        if 'child_channels' in category_info and len(category_info['child_channels']) > 0:
            url = get_url(action='list_categories', page=0, childs=category_info['child_channels'])
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, True)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(HANDLE)


def list_videos(id, page):
    """
    Create the list of playable videos in the Kodi interface.
    """
    xbmcplugin.setPluginCategory(HANDLE, "Videos")
    xbmcplugin.setContent(HANDLE, 'videos')
    category = requests.get(VIDEO_API + page + "s/" + id + ".json", headers={'USER-AGENT':USER_AGENT}).json()
    if page == 'animal':
        category = requests.get(VIDEO_API + "containers/" + str(category['containers'][0]) + ".json", headers={'USER-AGENT':USER_AGENT}).json()
        videos = category['items']
    else:
        videos = category['contains_media']
    for video in videos:
        if page == 'animal':
            list_item = xbmcgui.ListItem(label=video['unicode'])
            url = get_url(action='play_video', id=video['id'])
            media = requests.get(VIDEO_API + "media/" + str(video['id']) + ".json", headers={'USER-AGENT':USER_AGENT}).json()
            list_item.setInfo('video', {
                'duration': int(round(media['duration_in_ms']/1000)),
                'title': media['title'], 
                'mediatype': 'video',
                'plot': media['teaser'],
                'premiered': media['web_airdate'],
                'aired': media['web_airdate'],
                'tag': media['tags'],
                'dateadded': media['created']
            })
            list_item.setArt({
                'thumb': media['images'][0]['url'],
                'fanart': media['images'][0]['url']
            })
        else:
            list_item = xbmcgui.ListItem(label=video['title'])
            list_item.setInfo('video', {
                'duration': int(round(video['duration_in_ms']/1000)),
                'title': video['title'], 
                'mediatype': 'video',
                'plot': video['teaser'],
                'premiered': category['web_airdate'],
                'aired': category['web_airdate'],
                'tag': category['tags'],
                'dateadded': category['created']
            })
            list_item.setArt({
                'thumb': video['images'][0]['url'],
                'fanart': video['images'][0]['url']
            })
            url = get_url(action='play_video', id=video['pk'])
        list_item.addStreamInfo('video', {
            'width': unicode(1280),
            'height': unicode(720)
        })
        list_item.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, False)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(HANDLE)


def play_video(id):
    """
    Play a video by the provided path.
    """
    uuid = requests.get(VIDEO_API + "media/" + id + ".json", headers={'USER-AGENT':USER_AGENT}).json()['uuid']
    play_item = xbmcgui.ListItem(path="https://cdn-segments.tierwelt-live.de/" + uuid + "_twl_720p.m4v/playlist.m3u8")
    xbmcplugin.setResolvedUrl(HANDLE, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions depending on the provided paramstring
    """
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'list_categories':
            list_categories(params['page'],params['childs'])
        elif params['action'] == 'list_videos':
            list_videos(params['id'],params['category'])
        elif params['action'] == 'play_video':
            play_video(params['id']) 
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        list_pages()


if __name__ == '__main__':
    router(sys.argv[2][1:])
