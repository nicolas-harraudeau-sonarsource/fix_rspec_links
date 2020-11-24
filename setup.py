"""A simple tool to fix RSPEC links in Jira"""

from setuptools import setup

test_deps = ['pytest>=6.1.2']

setup(
    name='fix_rspec_links',
    version='0.0.1',
    description='A simple tool to fix RSPEC links in Jira',
    author='SonarSource',
    packages=['fix_rspec_links', ],  # Required
    python_requires='>=3.8, <4',
    install_requires=[
        'click>=7.1.2',
        'requests>=2.25.0',
        'beautifulsoup4>=4.9.3'
    ],
    extras_require={
        'test': test_deps,
    },
    setup_requires=['pytest-runner'],
    tests_require=test_deps,

    entry_points={
        'console_scripts': [
            'fix_rspec_links=fix_rspec_links:cli',
        ],
    },
)