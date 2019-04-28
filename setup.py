import setuptools

meta = {}

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("kafkashell/version.py") as f:
    exec(f.read(), meta)

requires = [
    "prompt-toolkit>=2.0.9",
    "pygments>=2.1.3,<3.0.0",
    "fuzzyfinder>=2.0.0",
    "jsonschema>=3.0.1",
    "oyaml>=0.8"
]

setuptools.setup(
    name="kafka-shell",
    version=meta["__version__"],
    author="Shawn Seymour",
    author_email="shawn@devshawn.com",
    description="A supercharged, interactive Kafka shell built on top of the existing Kafka CLI tools.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devshawn/kafka-shell",
    license="Apache License 2.0",
    packages=["kafkashell"],
    package_data={"kafkashell": ["data/*.json", "data/*.yaml", "data/*.schema"]},
    install_requires=requires,
    entry_points={
        "console_scripts": ["kafka-shell=kafkashell.main:main"],
    },
    keywords=("kafka", "shell", "prompt", "apache", "autocomplete", "streams", "cli"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
