from setuptools import setup, find_packages

setup(
    name='cloudboot',
    version='0.1.0-beta',
    description='A groovy collection of easy-peasy scripts and serverless ready templates for Google Cloud serverless computing!',
    url='https://cloudboot.github.io',
    author='Lahiru Pathirage',
    author_email='lpsandaruwan@gmail.com',
    license='MIT',
    scripts=['./bin/cloudboot'],
    packages=find_packages(),
    install_requires=['click', 'inquirerpy', 'requests', 'termcolor', 'pyfiglet']
)
