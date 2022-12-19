"""
SurveyGuru
----------

SurveyGuru is an application for survey data generation.
"""

from setuptools import setup

setup(
    name="SurveyGuru",
    version="0.0.1",
    license="MIT",
    author="John Kyle Alas-as",
    author_email="alasasjohnkyle@gmail.com",
    url="https://github.com/jkalasas/SurveyGuru",
    long_description=__doc__,
    entry_points={
        "console_scripts": [
            "surveyguru = surveyguru.__main__:main",
        ],
    },
)
