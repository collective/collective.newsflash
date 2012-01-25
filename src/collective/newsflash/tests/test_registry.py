# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles

from plone.registry import Registry
from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

from collective.newsflash import config
from collective.newsflash.controlpanel import INewsFlashSettings
from collective.newsflash.testing import INTEGRATION_TESTING

BASE_REGISTRY = 'collective.newsflash.controlpanel.INewsFlashSettings.%s'


class RegistryTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        # set up settings registry
        self.registry = Registry()
        self.registry.registerInterface(INewsFlashSettings)

    def test_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name='newsflash-settings')
        view = view.__of__(self.portal)
        self.failUnless(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                          '@@newsflash-settings')

    def test_action_in_controlpanel(self):
        cp = getToolByName(self.portal, 'portal_controlpanel')
        actions = [a.getAction(self)['id'] for a in cp.listActions()]
        self.failUnless('newsflash' in actions)

    def test_controls_record(self):
        record_controls = self.registry.records[
            BASE_REGISTRY % 'controls']
        self.failUnless('controls' in INewsFlashSettings)
        self.assertEquals(record_controls.value, config.CONTROLS)

    def test_pauseOnItems_record(self):
        record_pauseOnItems = self.registry.records[
            BASE_REGISTRY % 'pauseOnItems']
        self.failUnless('pauseOnItems' in INewsFlashSettings)
        self.assertEquals(record_pauseOnItems.value, 2000)

    def test_speed_record(self):
        record_speed = self.registry.records[
            BASE_REGISTRY % 'speed']
        self.failUnless('speed' in INewsFlashSettings)
        self.assertEquals(record_speed.value, 0.1)

    def test_titleText_record(self):
        record_titleText = self.registry.records[
            BASE_REGISTRY % 'titleText']
        self.failUnless('titleText' in INewsFlashSettings)
        self.assertEquals(record_titleText.value, config.TITLE_TEXT)


class RegistryUninstallTest(unittest.TestCase):
    """Ensure registry is properly uninstalled"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.registry = getUtility(IRegistry)
        qi = getattr(self.portal, 'portal_quickinstaller')
        qi.uninstallProducts(products=[config.PROJECTNAME])

    def test_records_removed(self):
        records = [
            BASE_REGISTRY % 'controls',
            BASE_REGISTRY % 'pauseOnItems',
            BASE_REGISTRY % 'speed',
            BASE_REGISTRY % 'titleText',
            ]
        for r in records:
            self.assertFalse(r in self.registry)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
