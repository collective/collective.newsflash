# -*- coding: utf-8 -*-
from collective.newsflash.config import PROJECTNAME
from collective.newsflash.testing import INTEGRATION_TESTING
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from Products.GenericSetup.upgrade import listUpgradeSteps
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest


class UpgradesTestCase(unittest.TestCase):

    """Ensure product upgrades work."""

    layer = INTEGRATION_TESTING
    profile = PROJECTNAME + ':default'

    def setUp(self):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']

    def test_latest_version(self):
        self.assertEqual(
            self.setup.getLastVersionForProfile(self.profile)[0], u'1001')

    def _match(self, item, source, dest):
        source, dest = tuple([source]), tuple([dest])
        return item['source'] == source and item['dest'] == dest

    def test_to1001_available(self):
        steps = listUpgradeSteps(self.setup, self.profile, '1000')
        steps = [s for s in steps if self._match(s[0], '1000', '1001')]
        self.assertEqual(len(steps), 1)

    def test_portlet_not_assigned(self):
        manager_name = 'plone.leftcolumn'
        manager = getUtility(
            IPortletManager, name=manager_name, context=self.portal)
        mapping = getMultiAdapter(
            (self.portal, manager), IPortletAssignmentMapping)
        assignments = [id for id, assignment in mapping.items()]
        self.assertNotIn('newsflash', assignments)
