# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.component import ComponentLookupError

from zope.interface import directlyProvides

from plone.app.layout.viewlets.interfaces import IAboveContent

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import setRoles
from plone.app.testing import login
from plone.app.testing import logout

from collective.newsflash.interfaces import INewsFlashLayer
from collective.newsflash.browser.newsflash_viewlet import NewsFlash_Viewlet
from collective.newsflash.testing import INTEGRATION_TESTING


class BrowserTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, INewsFlashLayer)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_newsflash_api_view(self):
        view = getMultiAdapter((self.portal, self.request),
                               name='newsflash_api')
        self.assertTrue(view())
        self.assertEqual(view.settings.controls, False)
        speed = "%d.1" % view.settings.speed
        self.assertEqual(speed, "0.1")
        self.assertEqual(view.settings.pauseOnItems, 2000)
        self.assertEqual(view.settings.titleText, u"Latest")

    def test_newsflash_js_view(self):
        view = getMultiAdapter((self.portal, self.request),
                               name='newsflash_viewlet.js')
        self.assertTrue(view())
        default_js = u'$(document).ready(function() {' + \
                     u'\n        var config_data = {' + \
                     u'\n"controls": false, ' + \
                     u'\n"feedType": "xml", ' + \
                     u'\n"htmlFeed": true, ' + \
                     u'\n"pauseOnItems": 2000, ' + \
                     u'\n"speed": 0.1, ' + \
                     u'\n"titleText": "Latest"' + \
                     u'\n}' + \
                     u'\n        if ($(".empty-ticker")[0] !== undefined) {' + \
                     u'\n            config_data["paused"] = true;' + \
                     u'\n        }' + \
                     u'\n        $("#js-news").ticker(config_data);' + \
                     u'\n        });\n'
        self.assertEqual(default_js.strip(' \t\n\r'), view().strip(' \t\n\r'))

    def test_newsflash_viewlet(self):
        view = getMultiAdapter((self.portal, self.request),
                               name='view')
        viewlet = NewsFlash_Viewlet(
            self.portal, self.request, view, IAboveContent)
        self.assertTrue(viewlet.render())

    def test_newsflash_edit_not_accessible_by_anonymous(self):
        logout()

        self.assertRaises(ComponentLookupError,
                          getMultiAdapter,
                          (self.portal, self.request),
                          name='manage-newsflashes')
