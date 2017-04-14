from setuptools import setup, find_packages


setup(
    name="pyrocket",
    version="0.1.0",
    description="Rocket sync-tracker client",
    long_description=open('README.rst').read(),
    url="https://github.com/Contraz/pyrocket",
    author="Einar Forselv",
    author_email="eforselv@gmail.com",
    maintainer="Einar Forselv",
    maintainer_email="eforselv@gmail.com",
    include_package_data=True,
    keywords=['synchronizing', 'music', 'rocket'],
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics',
        'License :: OSI Approved :: zlib/libpng License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)
