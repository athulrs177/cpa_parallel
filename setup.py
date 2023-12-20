from setuptools import setup, find_packages

setup(
    name='CPA',
    version='0.1.0',
    url="https://github.com/athulrs177/CPA",
    author="Athul Rasheeda Satheesh",
    author_email="athulrs177@gmail.com",
    packages=["CPA_3D"],
    install_requires=[
        'numpy',
        'xarray',
        'urocc @ git+https://github.com/evwalz/urocc.git',
        'dask',
    ],
)
