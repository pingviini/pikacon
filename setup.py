from setuptools import setup, find_packages

version = "0.4.0-dev"

with open("README.rst", "r") as fh:
    readme = fh.read()
with open("CHANGES.rst", "r") as fh:
    changes = fh.read()

setup(name="pikacon",
      version=version,
      description="Ini-style configuration for pika.",
      long_description="%s\n%s" % (readme, changes),
      classifiers=[
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU General Public License (GPLv3)",
          "Operating System :: OS Independent",
      ],
      keywords="pikacon pika ini queue exchange connection amqp",
      author="Jukka Ojaniemi",
      author_email="jukka.ojaniemi@gmail.com",
      url="https://github.com/pingviini/pikacon",
      license="GPLv3",
      packages=find_packages("src", exclude=["ez_setup"]),
      package_dir={"": "src"},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "setuptools",
          "pika>=0.10.0",
      ],
      extras_require={
          'develop': ['Sphinx'],
          'tests': ['pytest', 'tox'],
      },
      test_suite="tests",
)
