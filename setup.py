from setuptools import setup, find_packages

VERSION = "0.0.8"

def get_long_description():
    with open("README.md", encoding="UTF-8") as f:
        long_description = f.read()
        return long_description

setup(
    name='sakurafm',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    long_description_content_type='text/markdown',
    author='Aditya',
    author_email='adityaraj6311@gmail.com',
    url="https://github.com/awesome-Tofu/sakura_fm",
    description='A simple scraper package for chatting with bots from sakura.fm',
    long_description=get_long_description(),
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