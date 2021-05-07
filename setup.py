# -*- coding: utf-8 -*-
"""Installer for the collective.venue package."""
from setuptools import find_packages
from setuptools import setup


version = "4.2.dev0"

long_description = "\n\n".join([open("README.rst").read(), open("CHANGES.rst").read()])


setup(
    name="collective.venue",
    version=version,
    description="An add-on for Plone",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: Addon",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="plone collective event geo location",
    author="Johannes Raggam",
    author_email="raggam-nl@adm.at",
    url="https://github.com/collective/collective.venue",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["collective"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "collective.address",
        "plone.api",
        "plone.app.content",
        "plone.app.dexterity",
        "plone.app.event",
        "plone.browserlayer",
        "plone.event",
        "plone.registry >= 1.1.0.dev0",  # implicit dependency, see PR #10
        "plone.resource",
        "Products.CMFPlone",
        "Products.GenericSetup",
    ],
    extras_require={
        "geolocation": [
            "collective.geolocationbehavior",
            "plone.formwidget.geolocation",
            "geopy",
            "six",
        ],
        "test": [
            "plone.app.testing",
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            "plone.testing>=5.0.0",
            "plone.app.contenttypes",
            "plone.app.robotframework[debug]",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = collective.venue.locales.update:update_locale
    """,
)
