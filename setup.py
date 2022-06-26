import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='orm-mysql',
    version='1.0.1',
    description='An ORM for MySql.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/hrushikeshj/mysql-orm',
    author='Hrushikesh J',
    author_email='hrushi2002j@gmail.com',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=['orm'],
    include_package_data=True,
    install_requires=[
            'mysql-connector-python',
            'pyyaml',
        ],
    setup_requires=['wheel'],
    zip_safe=False
    )
