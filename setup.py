from pathlib import Path

from setuptools import find_packages, setup

requirements = Path(__file__).parent / 'requirements/core.txt'

with requirements.open(mode='rt', encoding='utf-8') as fp:
    install_requires = [line.strip() for line in fp]

readme = Path(__file__).parent / 'README.rst'

with readme.open(mode='rt', encoding='utf-8') as fp:
    readme_text = fp.read()

setup(
    name='lexrank',
    maintainer='Ocean S.A.',
    maintainer_email='support@ocean.io',
    version='0.0.1b',
    description='LexRank text summarization',
    long_description=readme_text,
    keywords=[
        'lex', 'rank', 'lexrank', 'algorithm', 'text', 'summary',
        'summarization',
    ],
    license='MIT',
    author='Luka Shostenko',
    author_email='luka.shostenko@gmail.com',
    url='https://github.com/wikibusiness/lexrank',
    download_url='https://github.com/wikibusiness/lexrank/archive/0.0.1a.tar.gz',  # noqa
    packages=find_packages(include=['lexrank.*']),
    py_modules=['lexrank.settings'],
    python_requires='>=3.5.0',
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'assemble_stopwords = lexrank.tools.assemble_stopwords:entrypoint',
        ],
    },
)
