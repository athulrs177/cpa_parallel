from setuptools import setup, find_packages

setup(
    name='CPA_parallel',
    version='0.1.0',
    url="https://github.com/athulrs177/CPA",
    author="Athul Rasheeda Satheesh",
    author_email="athulrs177@gmail.com",
    packages=["CPA_parallel"],
    install_requires=[
        'numpy',
        'xarray',
        'uroc @ git+https://github.com/evwalz/urocc.git',
        'dask',
        'progressbar',
    ],
)
