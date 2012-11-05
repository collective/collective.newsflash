# -*- coding:utf-8 -*-
from zope.interface import implements
from Products.CMFPlone.interfaces import INonInstallable


class HiddenProfiles(object):

    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        profiles = ['collective.newsflash:uninstall', ]
        return profiles
