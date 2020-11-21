from setuptools import setup

setup(
    name="cheeseboys",
    version="0.4.0",
    description="An arcade game played in a (humor) post-apocalyptic world",
    url="https://github.com/keul/Cheese-Boys",
    author="keul",
    author_email="lucafbb@gmail.com",
    license="GPL",
    packages=["cheeseboys"],
    classifiers=[
        "Development Status :: 7 - Inactive",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: pygame",
    ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    include_package_data=True,
    install_requires=["pygame>=2", "KezMenu", "KTextSurfaceWriter"],
    zip_safe=False,
)
