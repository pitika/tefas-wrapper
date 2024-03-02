import io
from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="tefas-wrapper",
    version='{{VERSION_PLACEHOLDER}}',
    description="Tefas wrapper to fetch funds data from http://tefas.gov.tr/",
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Serhat Mutlu Durmaz",
    author_email="serhat.md@gmail.com",
    url="https://github.com/semudu/tefas-wrapper",
    download_url="https://github.com/semudu/tefas-wrapper/archive/v{{VERSION_PLACEHOLDER}}.tar.gz",
    keywords=["TEFAS", "WRAPPER", "FUND", "FON"],
    install_requires=["requests", "beautifulsoup4", "js2xml", "marshmallow", "pandas"],
    packages=["tefaswrapper"],
    include_package_data=True,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
