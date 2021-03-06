# -*- coding: utf-8 -*-

import re

from module.plugins.Hook import Hook


class XFileSharingPro(Hook):
    __name__ = "XFileSharingPro"
    __type__ = "hook"
    __version__ = "0.12"

    __config__ = [("activated", "bool", "Activated", True),
                  ("load_default", "bool", "Include default (built-in) hoster list", True),
                  ("include_hosters", "str", "Include hosters (comma separated)", ""),
                  ("exclude_hosters", "str", "Exclude hosters (comma separated)", "")]

    __description__ = """XFileSharingPro hook plugin"""
    __license__ = "GPLv3"
    __authors__ = [("zoidberg", "zoidberg@mujmail.cz")]


    def coreReady(self):
        self.loadPattern()


    def loadPattern(self):
        hoster_list = self.getConfigSet('include_hosters')
        exclude_list = self.getConfigSet('exclude_hosters')

        if self.getConfig('load_default'):
            hoster_list |= set((
                #WORKING HOSTERS:
                "aieshare.com", "asixfiles.com", "banashare.com", "cyberlocker.ch", "eyesfile.co", "eyesfile.com",
                "fileband.com", "filedwon.com", "filedownloads.org", "hipfile.com", "kingsupload.com", "mlfat4arab.com",
                "netuploaded.com", "odsiebie.pl", "q4share.com", "ravishare.com", "uptobox.com", "verzend.be",
                "xvidstage.com", "thefile.me", "sharesix.com", "hostingbulk.com",
                #NOT TESTED:
                "bebasupload.com", "boosterking.com", "divxme.com", "filevelocity.com", "glumbouploads.com",
                "grupload.com", "heftyfile.com", "host4desi.com", "laoupload.com", "linkzhost.com", "movreel.com",
                "rockdizfile.com", "limfile.com", "share76.com", "sharebeast.com", "sharehut.com", "sharerun.com",
                "shareswift.com", "sharingonline.com", "6ybh-upload.com", "skipfile.com", "spaadyshare.com",
                "space4file.com", "uploadbaz.com", "uploadc.com", "uploaddot.com", "uploadfloor.com", "uploadic.com",
                "uploadville.com", "vidbull.com", "zalaa.com", "zomgupload.com", "kupload.org", "movbay.org",
                "multishare.org", "omegave.org", "toucansharing.org", "uflinq.org", "banicrazy.info", "flowhot.info",
                "upbrasil.info", "shareyourfilez.biz", "bzlink.us", "cloudcache.cc", "fileserver.cc", "farshare.to",
                "filemaze.ws", "filehost.ws", "filestock.ru", "moidisk.ru", "4up.im", "100shared.com", "sharesix.com",
                "thefile.me", "filenuke.com", "sharerepo.com", "mightyupload.com",
                #WRONG FILE NAME:
                "sendmyway.com", "upchi.co.il",
                #NOT WORKING:
                "amonshare.com", "imageporter.com", "file4safe.com",
                #DOWN OR BROKEN:
                "ddlanime.com", "fileforth.com", "loombo.com", "goldfile.eu", "putshare.com"
            ))

        hoster_list -= (exclude_list)
        hoster_list -= set(('', u''))

        if not hoster_list:
            self.unload()
            return

        regexp = r"http://(?:[^/]*\.)?(%s)/(?:embed-)?\w{12}" % ("|".join(sorted(hoster_list)).replace('.', '\.'))

        dict = self.core.pluginManager.hosterPlugins['XFileSharingPro']
        dict['pattern'] = regexp
        dict['re'] = re.compile(regexp)
        self.logDebug("Pattern loaded - handling %d hosters" % len(hoster_list))


    def getConfigSet(self, option):
        s = self.getConfig(option).lower().replace('|', ',').replace(';', ',')
        return set([x.strip() for x in s.split(',')])


    def unload(self):
        dict = self.core.pluginManager.hosterPlugins['XFileSharingPro']
        dict['pattern'] = r'^unmatchable$'
        dict['re'] = re.compile(r'^unmatchable$')
