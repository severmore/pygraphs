from setuptools import setup, find_packages

with open('README.md') as rm:
  readme = rm.read()

with open('LICENSE') as li:
  license_ = li.read()

setup(
  name = 'sample',
  version = '0.0.1',
  description = 'Algorithms on graphs',
  long_description = readme,
  author = 'Roman Ivanov',
  auhtor_email = 'iromcorp@gmail.com',
  url = 'https://github.com/severmore/pygraphs.git',
  license = license_,
  packages = find_packages(exclude=('tests', 'docs'))
)
