from setuptools import setup, find_packages

setup(
    name='sakura',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pymongo'
    ],
    entry_points="""
        [console_scripts]
        sakura=sakura.sakura:main
    """,
)