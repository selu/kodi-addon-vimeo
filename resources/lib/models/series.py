from future import standard_library
standard_library.install_aliases()  # noqa: E402

import urllib.parse
import xbmcgui

from resources.lib.models.list_item import ListItem


class Series(ListItem):
    thumb = ""
    info = {}
    uri = ""

    def to_list_item(self, addon, addon_base):
        list_item = xbmcgui.ListItem(label=self.label, label2=self.label2)
        list_item.setArt({"thumb": self.thumb})
        #list_item.setInfo("video", {
        #    "year": self.info.get("date")[:4]
        #})
        url = addon_base + "/?" + urllib.parse.urlencode({
            "action": "call",
            "call": (self.uri+"?" if "?" not in self.uri else self.uri+"&")+"sort=episode"
        })

        return url, list_item, True
