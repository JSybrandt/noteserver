#!/usr/bin/env python

from setuptools import setup, find_packages

def parse_requirements(deps_path):
  res = []
  with open(deps_path) as req_file:
    for line in req_file:
      line = line.strip()
      if len(line) > 0 and line[0] != '#':
        res.append(line)
  return res

setup(
    name="Noteserver",
    version="0.0.1",
    description="A backend for personal wikis.",
    author="Justin Sybrandt",
    author_email="justin@sybrandt.com",
    url="https://github.com/JSybrandt/noteserver",
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=parse_requirements("requirements.txt"),
)
