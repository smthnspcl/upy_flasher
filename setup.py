from setuptools import setup, find_packages

setup(
    long_description=open("README.rst", "r").read(),
    name="upy_flasher",
    version="0.42",
    description="micropython flash script",
    author="Pascal Eberlein",
    author_email="pascal@eberlein.io",
    url="https://github.com/smthnspcl/upy_flasher",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords="micropython flasher",
    packages=find_packages(),
)
