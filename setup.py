from pathlib import Path

from setuptools import find_packages, setup

requirements = Path(__file__).parent / 'requirements/core.txt'

with requirements.open(mode='rt', encoding='utf-8') as fp:
    install_requires = [line.strip() for line in fp]

top_packages = [
    'algorithms',
    'assets',
    'mappings',
    'tools',
    'utils',
]

packages_pattern = top_packages + [p + '.*' for p in top_packages]

setup(
    name='lexrank',
    maintainer='Ocean S.A.',
    maintainer_email='support@ocean.io',
    version='0.0.1a',
    description='LexRank text summarization.',
    license='Closed source',
    packages=find_packages(include=packages_pattern),
    py_modules=['settings'],
    python_requires='>=3.6.0',
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'assemble_stopwords = tools.assemble_stopwords:assemble_stopwords',
        ]
    }
)
