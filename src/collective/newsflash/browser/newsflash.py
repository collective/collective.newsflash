# -*- coding: utf-8 -*-

from zope.app.component.hooks import getSite

from zope import interface
from zope import schema
from z3c.form import form
from z3c.form import field
from z3c.form import  button
from plone.z3cform.layout import wrap_form

from zope.annotation.interfaces import IAnnotations

from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

from collective.newsflash import _


class INewsFlash(interface.Interface):
    newsflash = schema.List(value_type=schema.Text(title=_(u'News Flash'),
                                                   default=u''),
                            default=[],
                            required=False)


class NewsFlashEditForm(form.Form):
    fields = field.Fields(INewsFlash)
    ignoreContext = True  # don't use context to get widget data
    label = _("Manage News Flashes")

    def update(self):
        portal = getSite()
        if IPloneSiteRoot.providedBy(portal):
            annotations = IAnnotations(portal)
            field = self.fields['newsflash'].field
            field.default = annotations.get('collective.newsflash.newsflash', [])

        # call the base class version - this is very important!
        super(NewsFlashEditForm, self).update()

    def render(self):
        submitted = self.request.form.get('form.buttons.save', False)
        if submitted:
            data, errors = self.extractData()
            if errors:
                return super(NewsFlashEditForm, self).render()
            else:
                return None
        else:
            return super(NewsFlashEditForm, self).render()

    @button.buttonAndHandler(_(u'Save'))
    def handleApply(self, action):
        portal = getSite()
        if IPloneSiteRoot.providedBy(portal):
            data, errors = self.extractData()
            if errors:
                return
            annotations = IAnnotations(portal)
            if 'newsflash' in data and data['newsflash']:
                annotations['collective.newsflash.newsflash'] = data['newsflash']
            else:
                annotations['collective.newsflash.newsflash'] = []
            return None

NewsFlashEdit = wrap_form(NewsFlashEditForm)
