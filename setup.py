from setuptools import setup, find_packages

LONG_DESCRIPTION = '''Simple Compass integration for Django.'''

CLASSIFIERS = [
                'Development Status :: 5 - Production/Stable',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: Apache Software License',
                'Natural Language :: English',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Topic :: Software Development :: Libraries :: Python Modules'
              ]

KEYWORDS = 'django sass compass css'

setup(name='django-orienteer',
    version='0.3',
    description='Django Compass App',
    long_description=LONG_DESCRIPTION,
    author='Drew Yeaton',
    author_email='drew@sentineldesign.net',
    maintainer='Mikhail Kolesnik',
    maintainer_email='mike@openbunker.org',
    url='https://github.com/mikek/django-orienteer',
    packages=find_packages(),
    platforms = ['Platform Independent'],
    license = 'Apache License, Version 2.0',
    classifiers = CLASSIFIERS,
    keywords = KEYWORDS,
)
