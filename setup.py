from setuptools import setup
setup(name='mysql-orm',
    version='0.1.1',
    description='Testing installation of Package',
    url='https://github.com/hrushikeshj',
    author='hrushikesh',
    author_email='hrushi2002j@gmail.com',
    license='MIT',
    packages=['orm'],
    install_requires=[
            'mysql-connector-python',
            'pyyaml',
        ],
    setup_requires=['wheel'],
    zip_safe=False)
