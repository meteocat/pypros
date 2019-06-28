import datetime
import subprocess

import setuptools

release = (subprocess.check_output(['git', 'describe', '--abbrev=0',
                                    '--tags']).decode('utf-8').strip())
version = ".".join(release.split('.')[0:2])
name = 'pypros'
now = datetime.datetime.now()

setuptools.setup(
    name=name,
    version=release,
    description="pyPROS: Precipitation type calculation, rain or snow",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=['numpy'],
    scripts=['bin/pypros_run'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'],
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'copyright': ('setup.py',
                          str(now.year)+",Servei Meteorològic de Catalunya")
            }
        },
)
