from setuptools import setup, find_packages

version = "0.3.2"

setup(name="pikacon",
      version=version,
      description="Ini-style configuration for pika.",
      long_description="%s\n%s" % (
          open("README.rst").read(),
          open("CHANGES.rst").read()),
      classifiers=[
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
      ],
      keywords="pikacon pika ini queue exchange connection amqp",
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
          "pika>=0.9.12",
      ],
      extras_require={
          'develop': ['Sphinx'],
      },
      test_suite="tests",
      )
