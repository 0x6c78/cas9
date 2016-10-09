# -*- coding: utf-8 -*-
#
# Copyright @ CangTu.
#
# 16-8-29 下午3:55 licangtu@gmail.com
#
# Distributed under terms of the MIT License
import codecs
from setuptools import setup, find_packages


def readme():
    with codecs.open('README.rst', encoding='utf-8') as handle:
        return handle.read()


def requirements():
    with open('requirements.txt') as handle:
        return [line.rstrip() for line in handle]


def get_version():
    return '0.0.1'


setup(
    name='cas9',
    version=get_version(),
    description='CRISPR/Cas9 finder and off target probability evaluator',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='CRISPR/cas9 off_target',
    url='https://github.com/cangtu/cas9',
    author='CangTu',
    author_email='licangtu@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=requirements(),
    entry_points="""
    [console_scripts]
    cas9 = cas9.cli:main
    """,
    include_package_data=True,
    zip_safe=False,
)
