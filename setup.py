from setuptools import setup
import randfilter

setup(
    name = randfilter.NAME,
    version = randfilter.VERSION,
    description = randfilter.DESCRIPTION,
    long_description = open("README.rst").read(),
    url = randfilter.URL,
    license = randfilter.LICENSE,
    author = randfilter.AUTHOR,
    author_email = randfilter.AUTHOR_EMAIL,
    install_requires = open("requirements.txt").read().splitlines(),
    py_modules = ['randfilter'],
    entry_points = {
        "console_scripts": ["randfilter = randfilter:main"]
    },
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Utilities',
    ]
)

