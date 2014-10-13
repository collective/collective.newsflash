Changelog
---------

There's a frood who really knows where his towel is.

1.1 (unreleased)
^^^^^^^^^^^^^^^^

.. Warning::
    The upgrade step of this release removes the management portlet from the left column on the root of the site.
    If you added it to the right column you must remove it manually before upgrade.

- Add upgrade step to remove management portlet and cook resources.
  [hvelarde]

- Add support for Plone 4.3 and drop support for Plone 4.1.
  [hvelarde]

- Remove dependency on zope.app.component; depend on plone.api.
  [hvelarde]

- Moving static resources to cssregistry/jsregistry, removing unused viewlet.
  [quimera]

- Remove portlet in favor of a new UI. [jpgimenez]

- Fixing newsflash edit workflow, new icon and style [quimera]


1.0 (2012-09-24)
^^^^^^^^^^^^^^^^

- Updated Spanish translation and added Brazilian Portuguese translation.
  [hvelarde]

- Package license is now GPLv2. [hvelarde]

- bugfix: Do not allow anonymous users to access the edit view for newsflashes
  [frapell]

- bugfix: Do not try to annotate portal object if it's not the portal object
  [frapell]


1.0rc1 (2012-08-16)
^^^^^^^^^^^^^^^^^^^

- Initial release.
