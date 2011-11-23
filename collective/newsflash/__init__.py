from zope.i18nmessageid import MessageFactory
NewsPortletMessageFactory = MessageFactory('collective.newsflash')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
