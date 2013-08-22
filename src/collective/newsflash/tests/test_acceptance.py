# -*- coding: utf-8 -*-

import unittest

import robotsuite

from plone.testing import layered

from collective.newsflash.testing import FUNCTIONAL_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("test_newsflash.txt"),
                layer=FUNCTIONAL_TESTING),
    ])
    return suite
