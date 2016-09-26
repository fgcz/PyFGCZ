from setuptools import setup


"""
https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
"""



def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='PyFGCZ',
      version='0.5',
      description="contains BioBeamer and FCC",
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Beta',
        'License :: OSI Approved :: GPLv3',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      url='https://github.com/fgcz/PyFGCZ',
      author='Christian Panse',
      author_email='cp@fgcz.ethz.ch',
      license='GPLv3',
      packages=['fgcz'],
      install_requires=[
        'PyYAML>=3',
        'lxml>=3.4.4' ],
      scripts=[
        'fgcz/scripts/fgcz_biobeamer.py',
        'fgcz/scripts/fgcz_fcc_run_linux.py',
        'fgcz/scripts/fgcz_fcc_run_windows.py'
      ],
      zip_safe=True)
