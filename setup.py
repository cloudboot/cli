from setuptools import setup, find_packages

setup(
    name='cloudboot',
    version='0.1.0-beta',
    description='A example Python package',
    url='https://github.com/lpsandaruwan',
    author='Lahiru Pathirage',
    author_email='lpsandaruwan@gmail.com',
    license='MIT',
    scripts=['./bin/cloudboot'],
    packages=find_packages(),
)
