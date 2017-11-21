from pathlib import Path

from setuptools import find_packages, setup

requirements = Path(__file__).parent / 'requirements/core.txt'

with requirements.open(mode='rt', encoding='utf-8') as fp:
    install_requires = [line.strip() for line in fp]

setup(
    name='lexrank',
    maintainer='Ocean S.A.',
    maintainer_email='support@ocean.io',
    version='0.0.1a',
    description='LexRank text summarization.',
    license='Closed source',
    packages=find_packages(include=['lexrank.*']),
    py_modules=['lexrank.settings'],
    python_requires='>=3.6.0',
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'assemble_stopwords = lexrank.tools.assemble_stopwords:assemble_stopwords',  # noqa
        ]
    }
)
