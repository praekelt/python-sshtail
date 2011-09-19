from setuptools import setup, find_packages

setup(
    name='python-sshtail',
    version='0.0.2',
    description='Python classes to allow for tailing of multiple files via SSH.',
    long_description=open('README.rst', 'rt').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='https://github.com/praekelt/python-sshtail',
    packages=find_packages(),
    install_requires=[
        'paramiko',
    ],
    include_package_data=True,
    classifiers = [
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    zip_safe=False,
)

