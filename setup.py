# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages

version = '3.0.1'


setup(
    name='collective.venue',
    version=version,
    description="Dexterity venue type for use with events.",
    long_description=open("README.rst").read()
    + "\n" +
    open("CHANGES.rst").read(),
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='plone collective event geo location',
    author='Johannes Raggam',
    author_email='raggam-nl@adm.at',
    url='https://github.com/collective/collective.venue',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'collective.address',
        'plone.api',
        'plone.app.content',
        'plone.app.dexterity',
        'plone.app.event',
        'plone.browserlayer',
        'plone.event',
        'plone.registry >= 1.1.0.dev0',  # implicit dependency, see PR #10
        'plone.resource',
        'Products.CMFPlone',
        'Products.GenericSetup',
        'z3c.unconfigure < 1.1',
    ],
    extras_require={
        'geolocation': [
            'collective.geolocationbehavior',
            'plone.formwidget.geolocation',
            'geopy'
        ],
    },
    entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """
)
