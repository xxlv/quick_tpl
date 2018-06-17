import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quick_generator",
    version="0.0.1",
    author="ghost",
    author_email="lvxiang119@gmail.com",
    description="Quickly code generator",
    long_description=long_description,
    packages=setuptools.find_packages(),

    entry_points={
        'console_scripts': ['gen=quick_generator.gen:main'],
    }

)
