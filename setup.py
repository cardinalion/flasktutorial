from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    # what directories to include Python files
    # finds these directories automatically
    packages=find_packages(),
    # includes other files, like static and templates
    # MANIFEST.in is needed to tell what this other data is
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)