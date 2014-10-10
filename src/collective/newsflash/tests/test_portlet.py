# -*- coding: utf-8 -*-

import unittest

from collective.newsflash.testing import INTEGRATION_TESTING

from zope.component import getUtility, getMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletAssignmentMapping

from plone.app.portlets.storage import PortletAssignmentMapping

from collective.newsflash.portlet import newsportlet

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles


class PortletTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        portal_setup = self.portal.portal_setup
        portal_setup.runAllImportStepsFromProfile('profile-collective.newsflash.tests:test-remove-portlet')
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_portlet_type_registered(self):
        portlet = getUtility(
            IPortletType,
            name='collective.newsflash.newsportlet.NewsPortlet')
        self.assertEqual(
            portlet.addview, 'collective.newsflash.newsportlet.NewsPortlet')

    def test_interfaces(self):
        # TODO: Pass any keyword arguments to the Assignment constructor
        portlet = newsportlet.Assignment()
        self.assertTrue(IPortletAssignment.providedBy(portlet))
        self.assertTrue(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_add_view(self):
        portlet = getUtility(
            IPortletType,
            name='collective.newsflash.newsportlet.NewsPortlet')
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        # TODO: Pass a dictionary containing dummy form inputs from the add
        # form.
        # Note: if the portlet has a NullAddForm, simply call
        # addview() instead of the next line.
        addview.createAndAdd(data={})

        self.assertEqual(len(mapping), 1)
        self.assertTrue(isinstance(mapping.values()[0],
                                   newsportlet.Assignment))

    def test_invoke_edit_view(self):
        # NOTE: This test can be removed if the portlet has no edit form
        mapping = PortletAssignmentMapping()
        request = self.request

        mapping['foo'] = newsportlet.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.assertTrue(isinstance(editview, newsportlet.EditForm))

    def test_obtain_renderer(self):
        context = self.portal
        request = self.request
        view = context.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn',
                             context=self.portal)

        # TODO: Pass any keyword arguments to the Assignment constructor
        assignment = newsportlet.Assignment()

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)
        self.assertTrue(isinstance(renderer, newsportlet.Renderer))

    def test_remove_portlet(self):
        manager_name = "plone.leftcolumn"
        manager = getUtility(IPortletManager, name=manager_name, context=self.portal)
        mapping = getMultiAdapter((self.portal, manager), IPortletAssignmentMapping)
        self.assertIn('newsflash', [id for id, assignment in mapping.items()])
        portal_setup = self.portal.portal_setup
        portal_setup.runAllImportStepsFromProfile('profile-collective.newsflash:remove-portlet')
        mapping = getMultiAdapter((self.portal, manager), IPortletAssignmentMapping)
        self.assertNotIn('newsflash', [id for id, assignment in mapping.items()])


class RenderTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.portal
        request = request or self.request
        view = view or self.portal.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)

        # TODO: Pass any default keyword arguments to the Assignment
        # constructor.
        assignment = assignment or newsportlet.Assignment()
        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def test_render(self):
        # TODO: Pass any keyword arguments to the Assignment constructor.
        r = self.renderer(context=self.portal,
                          assignment=newsportlet.Assignment())
        r = r.__of__(self.portal)
        r.update()
        # output = r.render()
        # TODO: Test output
