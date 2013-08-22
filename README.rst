********************
collective.newsflash
********************

.. contents:: Table of Contents

Life, the Universe, and Everything
----------------------------------

News ticker inspired by the one on the `BBC News`_ website.

Features
^^^^^^^^

- jQuery-based, lightweight and easy to use news ticker.
- Configurable via configlet.

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/collective/collective.newsflash.png?branch=master
    :target: http://travis-ci.org/collective/collective.newsflash

.. image:: https://coveralls.io/repos/collective/collective.newsflash/badge.png?branch=master
    :target: https://coveralls.io/r/collective/collective.newsflash

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

Don't Panic
-----------

Installation
^^^^^^^^^^^^

To enable this product in a buildout-based installation:

1. Edit your buildout.cfg and add ``collective.newsflash`` to the list of eggs
   to install ::

    [buildout]
    ...
    eggs =
        collective.newsflash

2. If you are using Plone 4.1 you may need to extend a five.grok known good
   set (KGS) to make sure that    you get the right versions of the packages
   that make up five.grok::

    [buildout]
    ...
    extends =
        http://good-py.appspot.com/release/five.grok/1.2.0-1

After updating the configuration you need to run ''bin/buildout'', which will
take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``collective.newsflash`` and click the 'Activate'
button.

.. Note::

    You may have to empty your browser cache and save your resource registries
    in order to see the effects of the product installation.

Usage
^^^^^

After installing the product, you should get a viewlet at plone.abovecontent
manager, with a link to manage flashes.

Clicking the " Click here to add one." link, or the pencil at the right, 
you should get a view for adding, modifying or removing news flashes,
in an overlay, if your browser supports Javascript.

After clicking "Save", and reloading your site, you should get the news
flashes rolling over the top section.

.. figure:: https://github.com/collective/collective.newsflash/raw/master/newsflash.png
    :align: center
    :height: 652px
    :width: 1143px
    :scale: 50%
    :target: https://github.com/collective/collective.newsflash/raw/master/newsflash.png

    The News Ticker in action.

Configuring
^^^^^^^^^^^

The product includes a configlet, which allows you to customize the news
flash. Going to "Site Setup" -> "News Flash Settings" you can:

- Change the title text.
- Change the speed in which the text appears.
- Change the time that the text remains in the screen.
- Hide/Show a widget to control the texts flow.

.. _`BBC News`: http://www.bbc.co.uk/news/
.. _`opening a support ticket`: https://github.com/collective/collective.newsflash/issues
