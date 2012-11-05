# -*- coding: utf-8 -*-
import json

from Products.Five import BrowserView

from zope.component import queryUtility
from zope.interface import Interface

from zope.annotation.interfaces import IAnnotations
from zope.publisher.publish import mapply

from Products.CMFCore.utils import getToolByName

from plone.app.layout.viewlets.interfaces import IAboveContent
from plone.registry.interfaces import IRegistry

from collective.newsflash.controlpanel import INewsFlashSettings
from collective.newsflash.interfaces import INewsFlashLayer

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.layout.viewlets.common import ViewletBase


class NewsFlash_Viewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/newsflash_viewlet.pt')


class NewsFlash_API(BrowserView):

    def __call__(self):
        self.request.response.setHeader('Content-Type', 'text/plain')
        return mapply(self.render, (), self.request)

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

    def can_edit(self):
        portal_membership = getToolByName(self.context, 'portal_membership')
        return portal_membership.checkPermission('Modify portal content', self.context)

    def enabled(self):
        return self.hasItems() or self.can_edit()

    def dumps(self, json_var=None, sort_keys=True, indent=0):
        """ """
        if json_var is None:
            json_var = {}
        return json.dumps(json_var, sort_keys=sort_keys, indent=indent)


class NewsFlash_Viewlet_JS(BrowserView):
    pass


