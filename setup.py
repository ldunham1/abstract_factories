from setuptools import setup


with open("README.md") as f:
    long_description = f.read()


setup(
    name='abstract_factories',
    packages=['abstract_factories'],
    version='0.2.2',
    license='MIT',
    description='Abstract Factory design pattern classes for scalable data in dynamic environments.',
    long_description=long_description,
    author='Lee Dunham',
    author_email='leedunham@gmail.com',
    url='https://github.com/ldunham1/abstract_factories',
    classifiers=[
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
)
