# -*- coding: utf-8 -*-
from collective.newsflash.controlpanel import INewsFlashSettings
from collective.newsflash.interfaces import INewsFlashLayer
from five import grok
from plone import api
from plone.app.layout.viewlets.interfaces import IAboveContent
from plone.registry.interfaces import IRegistry
from zope.annotation.interfaces import IAnnotations
from zope.component import queryUtility
from zope.interface import Interface

import json

grok.templatedir("templates")


class NewsFlash_Viewlet(grok.Viewlet):
    grok.context(Interface)
    grok.layer(INewsFlashLayer)
    grok.name('collective.newsflash.viewlet')
    grok.order(0)
    grok.require('zope2.View')
    grok.viewletmanager(IAboveContent)


class NewsFlash_API(grok.View):
    grok.context(Interface)
    grok.layer(INewsFlashLayer)
    grok.require('zope2.View')

    def __call__(self):
        self.response.setHeader('Content-Type', 'text/plain')
        return super(NewsFlash_API, self).__call__()

    def __init__(self, *args, **kwargs):
        super(NewsFlash_API, self).__init__(*args, **kwargs)
        registry = queryUtility(IRegistry)
        self.settings = registry.forInterface(INewsFlashSettings)

    def render(self):
        return self.dumps(self.getSettings())

    def getSettings(self, *args, **kwargs):
        settings = dict(controls=self.settings.controls,
                        titleText=self.settings.titleText,
                        feedType='xml',
                        htmlFeed=True,
                        speed=self.settings.speed,
                        pauseOnItems=self.settings.pauseOnItems,)
        return settings

    def getItems(self):
        site = api.portal.get_tool('portal_url').getPortalObject()
        annotations = IAnnotations(site)
        return annotations.get('collective.newsflash.newsflash', [])

    def hasItems(self):
        items = self.getItems()
        if items:
            return len(items) > 0
        else:
            return False

    def can_edit(self):
        portal_membership = api.portal.get_tool('portal_membership')
        return portal_membership.checkPermission('Modify portal content', self.context)

    def enabled(self):
        return self.hasItems() or self.can_edit()

    def dumps(self, json_var=None, sort_keys=True, indent=0):
        """ """
        if json_var is None:
            json_var = {}
        return json.dumps(json_var, sort_keys=sort_keys, indent=indent)


class NewsFlash_Viewlet_JS(grok.View):
    grok.context(Interface)
    grok.layer(INewsFlashLayer)
    grok.name('newsflash_viewlet.js')
    grok.require('zope2.View')
