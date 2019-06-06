# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages

version = '4.0'


def read(fname):
    with open(fname) as f:
        return f.read()


setup(
    name='collective.venue',
    version=version,
    description="Dexterity venue type for use with events.",
    long_description=read("README.rst")
    + "\n"
    + read("CHANGES.rst"),
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
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
    ],
    extras_require={
        'geolocation': [
            'collective.geolocationbehavior',
            'plone.formwidget.geolocation',
            'geopy',
            'six',
        ]
    },
    entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
