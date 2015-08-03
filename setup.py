from setuptools import setup

setup(
    name='panda',
    version='0.3.1',
    description='A Python implementation of the Panda REST interface',
    author='pandastream.com',
    author_email='support@pandastream.com',
    url='http://www.pandastream.com',
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
        'requests',
    ],
)
