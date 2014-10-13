# -*- coding: utf-8 -*-
from collective.newsflash.config import PROJECTNAME
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile

import logging

logger = logging.getLogger(PROJECTNAME)


def remove_portlet(context):
    """Remove management portlet."""
    logger = logging.getLogger(PROJECTNAME)
    profile = 'profile-{}.upgrades.v1001:default'.format(PROJECTNAME)
    loadMigrationProfile(context, profile)
    logger.info('Management portlet was removed')


def cook_css_resources(context):
    """Cook CSS resources."""
    css_tool = api.portal.get_tool('portal_css')
    css_tool.cookResources()
    logger.info('CSS resources were cooked')


def cook_js_resources(context):
    """Cook JS resources."""
    js_tool = api.portal.get_tool('portal_javascripts')
    js_tool.cookResources()
    logger.info('Javascript resources were cooked')
