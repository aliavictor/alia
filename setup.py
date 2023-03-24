from setuptools import setup, find_packages

setup(
    name="alia",
    version="0.1.3",
    description="A collection of random helper tools to make life easier",
    author="Alia",
    author_email="alia.jo.victor@gmail.com",
    url="https://github.com/aliavictor/alia",
    packages=find_packages(),
    install_requires=[
        # i.e. 'numpy>=1.18.0'
        "numpy",
        "pandas",
        "requests",
        "python-dotenv",
        "sty",
        "pyperclip",
        "python-dateutil",
        "ipython"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
