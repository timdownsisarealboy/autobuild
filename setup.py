from setuptools import setup
import os
import distutils.sysconfig
pre = distutils.sysconfig.get_config_var("prefix")
bindir = os.path.join(pre, "bin/activate")

setup(
    name='Autobuild',
    version='0.0.1',
    description='Project Autobuilder',
    author='Tim Downs',
    author_email='tim.downs@mongoosemetrics.com',
    zip_safe=False,
    include_package_data=True,
    url='http://mongoosemetrics.com',
    platforms=["any"],
    dependency_links=[
    ],
    install_requires=[
        'watchdog',
    ]
)
