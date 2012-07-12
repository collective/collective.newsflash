********************
collective.newsflash
********************

.. contents:: Table of Contents

Overview
--------

An alternative implementation of the `jQuery News Ticker
<http://www.jquerynewsticker.com/>`_ Plugin for Plone.

Requirements
------------

* Plone >= 4.1.x (http://plone.org/products/plone)
* five.grok >= 1.2 (http://pypi.python.org/pypi/five.grok)
* zope.schema >= 3.8.0 (http://pypi.python.org/pypi/zope.schema)

Features
--------

* Lightweight and easy to use news ticker

Usage
-----

After installing the product, you should get a portlet on the left side of
your site, with a "Manage News Flashes" link. If you want, you can go to
@@manage-portlets, remove it and add it somewhere else.

Clicking this "Manage News Flashes" link, you should get a view for adding,
modifying or removing newsflashes, in an overlay, if your browser supports
Javascript.

After clicking "Save", and reloading your site, you should get the newsflashes
rolling over the top section.

Configuring
-----------

The product includes a configlet, which allows you to customize the newsflash.
Going to "Site Setup" -> "News Flash Settings" you can:

    * Change the title text.
    * Change the speed in which the text appears.
    * Change the time that the text remains in the screen.
    * Hide/Show a widget to control the texts flow.
