import os

from setuptools import setup, find_packages
from pip.req import parse_requirements

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements(os.path.join(here, 'requirements.txt'), session=False)

# reqs is a list of requirement
# e.g. ['ringo', 'ringo_printtemplates']
requires = [str(ir.req) for ir in install_reqs]

setup(name='trainable',
      version='0.0',
      description='trainable',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='trainable',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = trainable:main
      [console_scripts]
      trainable-admin = ringo.scripts.admin:main
      [babel.extractors]
      tableconfig = ringo.lib.i18n:extract_i18n_tableconfig
      formconfig = formbar.i18n:extract_i18n_formconfig
      """,
      message_extractors = {'trainable': [
            ('**.py', 'python', None),
            ('templates/**.html', 'mako', None),
            ('templates/**.mako', 'mako', None),
            ('views/**.xml', 'formconfig', None),
            ('views/**.json', 'tableconfig', None),
            ('static/**', 'ignore', None)]},
      )
