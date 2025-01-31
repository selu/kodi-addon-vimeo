from future import standard_library
standard_library.install_aliases()  # noqa: E402

import urllib.parse
import xbmcgui

from resources.lib.kodi.utils import format_bold
from resources.routes import *


class Items:
    def __init__(self, addon, addon_base, search_history):
        self.addon = addon
        self.addon_base = addon_base
        self.search_history = search_history

    def root(self, logged_in, user_name):
        items = []

        # Search
        list_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30101))
        url = self.addon_base + PATH_SEARCH
        items.append((url, list_item, True))

        # Charts
        list_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30102))
        url = self.addon_base + PATH_FEATURED
        items.append((url, list_item, True))

        # Trending
        list_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30103))
        url = self.addon_base + PATH_TRENDING
        items.append((url, list_item, True))

        # Categories
        list_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30104))
        url = self.addon_base + PATH_CATEGORIES
        items.append((url, list_item, True))

        if logged_in:
            # Likes
            list_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30105))
            url = self.addon_base + PATH_LIKES
            items.append((url, list_item, True))

            # Watch Later
            list_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30106))
            url = self.addon_base + PATH_WATCH_LATER
            items.append((url, list_item, True))

            # Purchases
            list_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30107))
            url = self.addon_base + PATH_PURCHASES
            items.append((url, list_item, True))

        # Settings
        list_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30108))
        url = self.addon_base + "/?action=settings"
        items.append((url, list_item, False))

        if not logged_in:
            # Sign in TODO
            list_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30109))
            url = self.addon_base + "/?action=signin"
            items.append((url, list_item, False))

        if logged_in:
            # Sign out TODO
            list_item = xbmcgui.ListItem(label=(self.addon.getLocalizedString(30119) % user_name))
            url = self.addon_base + "/?action=signout"
            items.append((url, list_item, False))

        return items

    def search(self):
        items = []

        # New search
        list_item = xbmcgui.ListItem(label=format_bold(self.addon.getLocalizedString(30201)))
        url = self.addon_base + PATH_SEARCH + "?action=new"
        items.append((url, list_item, True))

        # Search history
        history = self.search_history.get()
        for k in sorted(list(history), reverse=True):
            list_item = xbmcgui.ListItem(label=history[k].get("query"))
            url = self.addon_base + PATH_SEARCH + "?" + urllib.parse.urlencode({
                "query": history[k].get("query")
            })
            items.append((url, list_item, True))

        return items

    def search_sub(self, query):
        items = []

        # People
        list_item = xbmcgui.ListItem(label=format_bold(self.addon.getLocalizedString(30211)))
        url = self.addon_base + PATH_SEARCH + "?" + urllib.parse.urlencode({
            "action": "people",
            "query": query
        })
        items.append((url, list_item, True))

        # Channels
        list_item = xbmcgui.ListItem(label=format_bold(self.addon.getLocalizedString(30212)))
        url = self.addon_base + PATH_SEARCH + "?" + urllib.parse.urlencode({
            "action": "channels",
            "query": query
        })
        items.append((url, list_item, True))

        # Groups
        list_item = xbmcgui.ListItem(label=format_bold(self.addon.getLocalizedString(30213)))
        url = self.addon_base + PATH_SEARCH + "?" + urllib.parse.urlencode({
            "action": "groups",
            "query": query
        })
        items.append((url, list_item, True))

        return items

    def featured(self):
        """
        Channel IDs were retrieved with the following request:
        curl https://api.vimeo.com/users/39723100/channels -H "Authorization: bearer <token>"
        """
        items = []

        # Staff Pics
        list_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30301))
        url = self.addon_base + PATH_FEATURED + "?" + urllib.parse.urlencode({
            "action": "channel",
            "id": "927"
        })
        items.append((url, list_item, True))

        # Premieres
        list_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30302))
        url = self.addon_base + PATH_FEATURED + "?" + urllib.parse.urlencode({
            "action": "channel",
            "id": "1143843"
        })
        items.append((url, list_item, True))

        # Best of the Month
        list_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30303))
        url = self.addon_base + PATH_FEATURED + "?" + urllib.parse.urlencode({
            "action": "channel",
            "id": "1143844"
        })
        items.append((url, list_item, True))

        # Best of the Year
        list_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30304))
        url = self.addon_base + PATH_FEATURED + "?" + urllib.parse.urlencode({
            "action": "channel",
            "id": "1172058"
        })
        items.append((url, list_item, True))

        # A Decade of Staff Picks
        list_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30305))
        url = self.addon_base + PATH_FEATURED + "?" + urllib.parse.urlencode({
            "action": "channel",
            "id": "1354461"
        })
        items.append((url, list_item, True))

        # Vimeo Curation channels
        list_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30306))
        url = self.addon_base + "/?" + urllib.parse.urlencode({
            "action": "call",
            "call": "/users/39723100/channels"
        })
        items.append((url, list_item, True))

        return items

    def from_collection(self, collection):
        items = []

        for item in collection.items:
            items.append(item.to_list_item(self.addon, self.addon_base))

        if collection.next_href:
            next_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30901))
            url = self.addon_base + "/?" + urllib.parse.urlencode({
                "action": "call",
                "call": collection.next_href
            })
            items.append((url, next_item, True))

        return items
