# -*- coding: utf-8 -*-
import json

from five import grok
from zope.component import queryUtility
from zope.interface import Interface

from Products.CMFCore.utils import getToolByName

from plone.app.layout.viewlets.interfaces import IAboveContent
from plone.app.layout.viewlets.interfaces import IHtmlHeadLinks
from plone.registry.interfaces import IRegistry

from collective.newsflash.controlpanel import INewsFlashSettings
from collective.newsflash.interfaces import INewsFlashLayer

from zope.annotation.interfaces import IAnnotations

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
        site = getToolByName(self.context, 'portal_url').getPortalObject()
        annotations = IAnnotations(site)
        return annotations.get('collective.newsflash.newsflash', [])

    def hasItems(self):
        items = self.getItems()
        if items:
            return len(items) > 0
        else:
            return False

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


class HtmlLinks_Viewlet(grok.Viewlet):
    grok.context(Interface)
    grok.layer(INewsFlashLayer)
    grok.name('collective.newsflash.links')
    grok.viewletmanager(IHtmlHeadLinks)
    grok.require('zope2.View')
