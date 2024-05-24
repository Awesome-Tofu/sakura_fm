from setuptools import setup, find_packages

VERSION = "0.0.4"

setup(
    name='sakura_fm',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    long_description_content_type='text/markdown',
    author='Aditya',
    author_email='adityaraj6311@gmail.com',
    description='A simple scraper package for chatting with bots from sakura.fm',
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pymongo'
    ],
    keywords=['sakura', 'sakura.fm', 'sakura scraper', 'sakurai'],
    entry_points="""
        [console_scripts]
        sakura=sakura.sakura:main
    """
)