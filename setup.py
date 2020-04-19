from setuptools import setup, find_packages

packages = find_packages(
    where='.', 
    include=['digits_sequence_generator*']
)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name= "digits-sequence-generator",
    version="1.0",
    author="Jitesh Gosar",
    author_email="gosar95@gmail.com",
    description="Generates sequence of digits using MNIST dataset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jitesh17/digits_sequence_generator",
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy',
        'matplotlib'
    ],
    python_requires='>=3.6',
)
