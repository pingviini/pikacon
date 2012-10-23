from setuptools import setup, find_packages

version = "0.1"

setup(name="pikacon",
      version=version,
      description="Helper library for using pika.",
      long_description=open("README.rst").read() + "\n" +
                       open("docs/HISTORY.rst").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
      ],
      keywords="",
      author="Jukka Ojaniemi",
      author_email="jukka.ojaniemi@jyu.fi",
      url="https://github.com/pingviini/pikacon",
      license="GPL",
      packages=find_packages("src", exclude=["ez_setup"]),
      package_dir={"": "src"},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "setuptools",
          "pika",
      ],
      test_suite="tests",
      )
