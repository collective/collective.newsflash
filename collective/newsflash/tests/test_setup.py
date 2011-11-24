# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from collective.newsflash.config import PROJECTNAME
from collective.newsflash.testing import INTEGRATION_TESTING

JS = '++resource++collective.newsflash.javascript/jquery.newsflash.js'


class InstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.failUnless(qi.isProductInstalled(PROJECTNAME))

    def test_javascript_installed(self):
        js = getattr(self.portal, 'portal_javascripts')
        self.failUnless(JS in js.getResourceIds(), 'javascript not installed')


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.failIf(self.qi.isProductInstalled(PROJECTNAME))

    def test_javascript_installed(self):
        js = getattr(self.portal, 'portal_javascripts')
        self.failIf(JS in js.getResourceIds(), 'javascript not removed')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
