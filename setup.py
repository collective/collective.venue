from setuptools import setup
from setuptools import find_packages

version = '1.0dev'


setup(name='collective.venue',
      version=version,
      description="Dexterity venue type for use with events.",
      long_description=open("README.rst").read()
                       + "\n" +
                       open("CHANGES.rst").read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone collective event',
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
          'collective.geolocationbehavior',
          'plone.app.content',
          'plone.app.dexterity',
          'plone.formwidget.geolocation',
          'Products.GenericSetup',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """)