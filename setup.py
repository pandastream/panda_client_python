from setuptools import setup

setup(
    name='panda',
    version='0.1.2',
    description='A Python implementation of the Panda REST interface',
    author='New Bamboo',
    author_email='info@new-bamboo.co.uk',
    url='http://account.pandastream.com',
    packages=['panda'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
    ],
    keywords='panda rest video encoding stream service',
    license='MIT',
    install_requires=[
        'setuptools',
    ],
)