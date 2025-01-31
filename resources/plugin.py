from future import standard_library
from future.utils import PY2
standard_library.install_aliases()  # noqa: E402

import os
import sys
import urllib.parse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

from resources.lib.vimeo.api import Api
from resources.lib.kodi.cache import Cache
from resources.lib.kodi.items import Items
from resources.lib.kodi.search_history import SearchHistory
from resources.lib.kodi.settings import Settings
from resources.lib.kodi.vfs import VFS
from resources.routes import *

addon = xbmcaddon.Addon()
addon_id = addon.getAddonInfo("id")
addon_base = "plugin://" + addon_id
addon_profile_path = xbmc.translatePath(addon.getAddonInfo("profile"))
if PY2:
    addon_profile_path = addon_profile_path.decode("utf-8")
vfs = VFS(addon_profile_path)
vfs_cache = VFS(os.path.join(addon_profile_path, "cache/"))
settings = Settings(addon)
cache = Cache(settings, vfs_cache)
api = Api(settings, xbmc.getLanguage(xbmc.ISO_639_1), vfs, cache)
search_history = SearchHistory(settings, vfs)
listItems = Items(addon, addon_base, search_history)


def run():
    url = urllib.parse.urlparse(sys.argv[0])
    path = url.path
    handle = int(sys.argv[1])
    args = urllib.parse.parse_qs(sys.argv[2][1:])
    xbmcplugin.setContent(handle, "videos")

    if path == PATH_ROOT:
        action = args.get("action", None)
        if action is None:
            items = listItems.root(api.logged_in(), api.user_name())
            xbmcplugin.addDirectoryItems(handle, items, len(items))
            xbmcplugin.endOfDirectory(handle)
        elif "call" in action:
            collection = listItems.from_collection(api.call(args.get("call")[0]))
            xbmcplugin.addDirectoryItems(handle, collection, len(collection))
            xbmcplugin.endOfDirectory(handle)
        elif "settings" in action:
            addon.openSettings()
            xbmc.executebuiltin("Container.Refresh")
        elif "signin" in action:
            login(handle)
        elif "signout" in action:
            logout(handle)
        else:
            xbmc.log("Invalid root action", xbmc.LOGERROR)

    elif path == PATH_CATEGORIES:
        collection = listItems.from_collection(api.categories())
        xbmcplugin.addDirectoryItems(handle, collection, len(collection))
        xbmcplugin.endOfDirectory(handle)

    elif path == PATH_LIKES:
        collection = listItems.from_collection(api.likes())
        xbmcplugin.addDirectoryItems(handle, collection, len(collection))
        xbmcplugin.endOfDirectory(handle)

    elif path == PATH_PURCHASES:
        collection = listItems.from_collection(api.purchases())
        xbmcplugin.addDirectoryItems(handle, collection, len(collection))
        xbmcplugin.endOfDirectory(handle)

    elif path == PATH_WATCH_LATER:
        collection = listItems.from_collection(api.watch_later())
        xbmcplugin.addDirectoryItems(handle, collection, len(collection))
        xbmcplugin.endOfDirectory(handle)

    elif path == PATH_TRENDING:
        collection = listItems.from_collection(api.trending())
        xbmcplugin.addDirectoryItems(handle, collection, len(collection))
        xbmcplugin.endOfDirectory(handle)

    elif path == PATH_FEATURED:
        action = args.get("action", None)
        if action is None:
            items = listItems.featured()
            xbmcplugin.addDirectoryItems(handle, items, len(items))
            xbmcplugin.endOfDirectory(handle)
        elif "channel" in action:
            channel_id = args.get("id", [""])[0]
            collection = listItems.from_collection(api.channel(channel_id))
            xbmcplugin.addDirectoryItems(handle, collection, len(collection))
            xbmcplugin.endOfDirectory(handle)
        else:
            xbmc.log("Invalid featured action", xbmc.LOGERROR)

    elif path == PATH_PLAY:
        # Public params
        video_id = args.get("video_id", [None])[0]

        # Private params
        media_url = args.get("uri", [None])[0]

        if media_url:
            resolved_url = api.resolve_media_url(media_url)
            item = xbmcgui.ListItem(path=resolved_url)
            subtitles = api.get_subtitles(media_url)
            if subtitles is not None:
                sfiles = []
                for sub in subtitles:
                    txt = api.get_subtitle_file(sub["uri"])
                    cache.add(sub["name"], txt)
                    sfiles.append(os.path.join(vfs_cache.path, sub["name"]))
                item.setSubtitles(sfiles)
            xbmcplugin.setResolvedUrl(handle, succeeded=True, listitem=item)
        elif video_id:
            collection = listItems.from_collection(api.resolve_id(video_id))
            playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            resolve_list_item(handle, collection[0][1])
            playlist.add(url=collection[0][0], listitem=collection[0][1])
        else:
            xbmc.log("Invalid play param", xbmc.LOGERROR)

    elif path == PATH_SEARCH:
        action = args.get("action", None)
        query = args.get("query", [""])[0]
        if query:
            if action is None:
                search(handle, query)
            elif "people" in action:
                xbmcplugin.setContent(handle, "artists")
                collection = listItems.from_collection(api.search(query, "users"))
                xbmcplugin.addDirectoryItems(handle, collection, len(collection))
                xbmcplugin.endOfDirectory(handle)
            elif "channels" in action:
                xbmcplugin.setContent(handle, "albums")
                collection = listItems.from_collection(api.search(query, "channels"))
                xbmcplugin.addDirectoryItems(handle, collection, len(collection))
                xbmcplugin.endOfDirectory(handle)
            elif "groups" in action:
                xbmcplugin.setContent(handle, "albums")
                collection = listItems.from_collection(api.search(query, "groups"))
                xbmcplugin.addDirectoryItems(handle, collection, len(collection))
                xbmcplugin.endOfDirectory(handle)
            else:
                xbmc.log("Invalid search action", xbmc.LOGERROR)
        else:
            if action is None:
                # Search root
                items = listItems.search()
                xbmcplugin.addDirectoryItems(handle, items, len(items))
                xbmcplugin.endOfDirectory(handle)
            elif "new" in action:
                # New search
                query = xbmcgui.Dialog().input(addon.getLocalizedString(30101))
                search_history.add(query)
                search(handle, query)
            else:
                xbmc.log("Invalid search action", xbmc.LOGERROR)

    elif path == PATH_SETTINGS_CACHE_CLEAR:
        vfs_cache.destroy()
        dialog = xbmcgui.Dialog()
        dialog.ok("Vimeo", addon.getLocalizedString(30501))

    else:
        xbmc.log("Path not found", xbmc.LOGERROR)


def resolve_list_item(handle, list_item):
    resolved_url = api.resolve_media_url(list_item.getProperty("mediaUrl"))
    list_item.setPath(resolved_url)
    xbmcplugin.setResolvedUrl(handle, succeeded=True, listitem=list_item)


def search(handle, query):
    search_options = listItems.search_sub(query)
    collection = listItems.from_collection(api.search(query, "videos"))
    xbmcplugin.addDirectoryItems(handle, search_options, len(collection))
    xbmcplugin.addDirectoryItems(handle, collection, len(collection))
    xbmcplugin.endOfDirectory(handle)

def login(handle):
    code = api.api_client_device.initiate_device_authentication(['public','private'])
    progress = xbmcgui.DialogProgress()
    progress.create(
        addon.getLocalizedString(30109),
        addon.getLocalizedString(30601) % (
            code['activate_link'].lstrip('https://'),
            code['user_code']
        )
    )
    total = code['expires_in'] / code['interval']
    for i in range(total):
        progress.update(int(100.0*i/total))
        for j in range(code['interval']):
            if progress.iscanceled():
                progress.close()
                return
            xbmc.sleep(1000)

        try:
            token = api.api_client_device.device_authorization(
                code['authorize_link'],
                code['device_code'],
                code['user_code']
            )
            settings.set("api.accesstoken", token)
            progress.close()
            xbmc.executebuiltin("Container.Refresh")
            return
        except Exception as e:
            xbmc.log("token exception: %s" % e, xbmc.LOGERROR)
            pass
    progress.close()

def logout(handle):
    api.api_client.delete_token()
    settings.set("api.accesstoken", None)
    xbmc.executebuiltin("Container.Refresh")
