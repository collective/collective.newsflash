# -*- coding: utf-8 -*-

from zope import schema

from zope.interface import Interface, provider
from zope.schema.interfaces import IContextAwareDefaultFactory
from zope.site.hooks import getSite

from plone.app.registry.browser import controlpanel

from collective.newsflash import config
from collective.newsflash import _


@provider(IContextAwareDefaultFactory)
def default_title_text(context):
    site = getSite()
    # HACK: to avoid "AttributeError: translate" on tests
    if hasattr(site, 'translate'):  # runtime
        return site.translate(config.TITLE_TEXT)
    else:  # tests
        return config.TITLE_TEXT


class INewsFlashSettings(Interface):
    """Interface for the form on the control panel.
    """

    titleText = schema.TextLine(
        title=_(u'Title text'),
        description=_(u'To remove the title set this to an empty '
                       'string.'),
        required=True,
        defaultFactory=default_title_text,
        missing_value=u"",
        )

    speed = schema.Float(
        title=_(u'Display speed'),
        description=_(u'The speed at which the news flashes appear on the '
                       'screen. Values go from 0.0 - 1.0.'),
        required=True,
        min=0.0,
        max=1.0,
        default=0.1,
        )

    pauseOnItems = schema.Int(
        title=_(u'Time items appear on screen'),
        description=_(u'The time, in milliseconds (ms), that each news '
                       'flash item appears on the screen.'),
        required=True,
        min=0,
        default=2000,
        )

    controls = schema.Bool(
        title=_(u'Controls'),
        description=_(u'Whether or not to show the ticker controls.'),
        default=config.CONTROLS,
        )


class NewsFlashSettingsEditForm(controlpanel.RegistryEditForm):
    schema = INewsFlashSettings
    label = _(u'News Flash Settings')
    description = _(u'Here you can modify the settings for '
                     'collective.newsflash.')

    def updateFields(self):
        super(NewsFlashSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(NewsFlashSettingsEditForm, self).updateWidgets()


class NewsFlashConfiglet(controlpanel.ControlPanelFormWrapper):
    form = NewsFlashSettingsEditForm
