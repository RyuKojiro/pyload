# -*- coding: utf-8 -*-
#
# Test links:
# http://www.filepup.net/files/k5w4ZVoF1410184283.html
# http://www.filepup.net/files/R4GBq9XH1410186553.html

import re

from module.plugins.internal.SimpleHoster import SimpleHoster, create_getInfo


class FilepupNet(SimpleHoster):
    __name__ = "FilepupNet"
    __type__ = "hoster"
    __version__ = "0.01"

    __pattern__ = r'http://(?:www\.)?filepup\.net/files/\w+'

    __description__ = """Filepup.net hoster plugin"""
    __license__ = "GPLv3"
    __authors__ = [("zapp-brannigan", "fuerst.reinje@web.de"),
                   ("Walter Purcaro", "vuolter@gmail.com")]


    FILE_NAME_PATTERN = r'>(?P<N>.+?)</h1>'
    FILE_SIZE_PATTERN = r'class="fa fa-archive"></i> \((?P<S>[\d.]+) (?P<U>\w+)'

    OFFLINE_PATTERN = r'>This file has been deleted'

    LINK_PATTERN = r'(http://www\.filepup\.net/get/.+?)\''


    def setup(self):
        self.multiDL = False
        self.chunkLimit = 1


    def handleFree(self):
        m = re.search(self.LINK_PATTERN, self.html)
        if m is None:
            self.parseError("Download link not found")

        dl_link = m.group(1)
        self.download(dl_link, post={'task': "download"})

        check = self.checkDownload({'html': re.compile("html")})
        if check == "html":
            self.parseError("Downloaded file is an html file")


getInfo = create_getInfo(FilepupNet)
