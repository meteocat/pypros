import setuptools


setuptools.setup(
    name="pypros",
    version="0.0.1",
    description="pypros: A small example package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 1 - Planning', 'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Cython'
    ],
)
