from distutils.core import setup

setup(
    name='cip',
    version='0.0.1',
    package_dir={'cip': 'cip'},
    packages=['cip', 'cip.handlers'],
    url='',
    license='',
    author='MoJ DS Infrastucture Team',
    author_email='webops@digital.justice.gov.uk',
    description='',
    install_requires=[
        'requests',
        'lxml',
        'PyYAML',
        'flask',
        'gunicorn',
        'gevent',
    ],
)
