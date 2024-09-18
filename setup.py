from setuptools import setup, find_packages

setup(
    name='autocomplete_project',
    version='0.1',
    packages=find_packages(include=['data_structure', 'text_processor', 'utils', 'ai']),
    install_requires=[],
    include_package_data=True,
    description='Auto-complete search prompt system',
    author='Arbel Hadari',
)
