# -*- coding: utf-8 -*-
from collective.newsflash import config
from collective.newsflash.controlpanel import INewsFlashSettings
from collective.newsflash.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry import Registry
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest

BASE_REGISTRY = 'collective.newsflash.controlpanel.INewsFlashSettings.%s'


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.registry = Registry()
        self.registry.registerInterface(INewsFlashSettings)

    def test_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name='newsflash-settings')
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                          '@@newsflash-settings')

    def test_action_in_controlpanel(self):
        cp = api.portal.get_tool('portal_controlpanel')
        actions = [a.getAction(self)['id'] for a in cp.listActions()]
        self.assertIn('newsflash', actions)


class RegistryTestCase(unittest.TestCase):
    """Ensure registry is properly uninstalled"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.registry = getUtility(IRegistry)

    def test_controls_record(self):
        record_controls = self.registry.records[
            BASE_REGISTRY % 'controls']
        self.assertTrue('controls' in INewsFlashSettings)
        self.assertEqual(record_controls.value, config.CONTROLS)

    def test_pauseOnItems_record(self):
        record_pauseOnItems = self.registry.records[
            BASE_REGISTRY % 'pauseOnItems']
        self.assertTrue('pauseOnItems' in INewsFlashSettings)
        self.assertEqual(record_pauseOnItems.value, 2000)

    def test_speed_record(self):
        record_speed = self.registry.records[
            BASE_REGISTRY % 'speed']
        self.assertTrue('speed' in INewsFlashSettings)
        self.assertEqual(record_speed.value, 0.1)

    def test_titleText_record(self):
        record_titleText = self.registry.records[
            BASE_REGISTRY % 'titleText']
        self.assertTrue('titleText' in INewsFlashSettings)
        self.assertEqual(record_titleText.value, config.TITLE_TEXT)

    def test_records_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[config.PROJECTNAME])

        records = [
            BASE_REGISTRY % 'controls',
            BASE_REGISTRY % 'pauseOnItems',
            BASE_REGISTRY % 'speed',
            BASE_REGISTRY % 'titleText',
        ]

        for r in records:
            self.assertNotIn(r, self.registry)
