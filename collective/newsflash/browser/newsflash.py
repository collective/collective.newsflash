# -*- coding: utf-8 -*-

from zope import interface
from zope import schema
from z3c.form import form
from z3c.form import field
from z3c.form import  button
from plone.z3cform.layout import wrap_form

from zope.annotation.interfaces import IAnnotations

from collective.newsflash import _

class INewsFlash(interface.Interface):
    newsflash = schema.List(value_type = schema.Text(title=_(u'Newsflash'),
                                                 default=u''),
                            default=[] )

class NewsFlashEditForm(form.Form):
    fields = field.Fields(INewsFlash)
    ignoreContext = True # don't use context to get widget data
    label = _("Add Newsflash")

    def update(self):
        annotations = IAnnotations(self.context)
        field = self.fields['newsflash'].field
        field.default = annotations.get('collective.newsflash.newsflash', [])
        # call the base class version - this is very important!
        super(NewsFlashEditForm, self).update()

    def render(self):
        if not self.request.form.get('form.buttons.save', False):
            return super(NewsFlashEditForm, self).render()
        else:
            return None

    @button.buttonAndHandler(_(u'Save'))
    def handleApply(self, action):
        data, errors = self.extractData()
        annotations = IAnnotations(self.context)
        annotations['collective.newsflash.newsflash'] = data['newsflash']
        return None

NewsFlashEdit = wrap_form(NewsFlashEditForm)