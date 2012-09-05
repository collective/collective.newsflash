# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component import ComponentLookupError

from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory

from plone.app.layout.viewlets.interfaces import IAboveContent

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import setRoles
from plone.app.testing import login
from plone.app.testing import logout

from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

from collective.newsflash.interfaces import INewsFlashLayer
from collective.newsflash.browser.newsflash_viewlet import NewsFlash_Viewlet
from collective.newsflash.controlpanel import INewsFlashSettings
from collective.newsflash.testing import INTEGRATION_TESTING


class BrowserTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, INewsFlashLayer)

        registry = getUtility(IRegistry)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_newsflash_api_view(self):
        view = getMultiAdapter((self.portal, self.request),
                               name='newsflash_api')
        self.failUnless(view())
        self.assertEquals(view.settings.controls, False)
        speed = "%d.1" % view.settings.speed
        self.assertEquals(speed, "0.1")
        self.assertEquals(view.settings.pauseOnItems, 2000)
        self.assertEquals(view.settings.titleText, u"Latest")

    def test_newsflash_js_view(self):
        view = getMultiAdapter((self.portal, self.request),
                               name='newsflash_viewlet.js')
        self.failUnless(view())
        default_js = u'jq(document).ready(function() {' + \
                     u'\n        var config_data = {' + \
                     u'\n"controls": false, ' + \
                     u'\n"feedType": "xml", ' + \
                     u'\n"htmlFeed": true, ' + \
                     u'\n"pauseOnItems": 2000, ' + \
                     u'\n"speed": 0.1, ' + \
                     u'\n"titleText": "Latest"' + \
                     u'\n}' + \
                     u'\n        jq("#js-news").ticker(config_data);' + \
                     u'\n        });\n'
        self.assertEquals(default_js, view())

    def test_newsflash_viewlet(self):
        view = getMultiAdapter((self.portal, self.request),
                               name='view')
        viewlet = NewsFlash_Viewlet(self.portal,
                                     self.request,
                                     view,
                                     IAboveContent)
        self.failUnless(viewlet.render())

    def test_newsflash_edit_not_accessible_by_anonymous(self):
        logout()

        self.assertRaises(ComponentLookupError,
                          getMultiAdapter,
                          (self.portal, self.request),
                          name='manage-newsflashes')

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
