# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.browserlayer.utils import registered_layers

from collective.newsflash.config import PROJECTNAME
from collective.newsflash.testing import INTEGRATION_TESTING

JS = '++resource++collective.newsflash.javascript/newsflash.js'


class InstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_add_permission(self):
        permission = 'collective.newsflash: Add News Flash'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        self.assertEqual(roles, ['Contributor', 'Manager', 'Owner', 'Site Administrator'])

    def test_browserlayer(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('INewsFlashLayer' in layers,
                        'browser layer not installed')

    def test_jsregistry(self):
        portal_javascripts = self.portal.portal_javascripts
        self.assertTrue(JS in portal_javascripts.getResourceIds(),
                        '%s not installed' % JS)


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertTrue(not self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_removed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertFalse('INewsFlashLayer' in layers,
                         'browser layer not removed')

    def test_jsregistry_removed(self):
        portal_javascripts = self.portal.portal_javascripts
        self.assertFalse(JS in portal_javascripts.getResourceIds(),
                         '%s not removed' % JS)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
