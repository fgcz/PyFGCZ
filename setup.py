from setuptools import setup


"""
https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html

python setup.py register sdist upload
"""


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='PyFGCZ',
      version='0.5.18',
      description="PyFGCZ contains BioBeamer and FCC python code.",
      long_description=readme(),
      classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Utilities',
      ],
      url='https://github.com/fgcz/PyFGCZ',
      author='Christian Panse',
      author_email='cp@fgcz.ethz.ch',
      license='GPLv3',
      packages=['fgcz'],
      install_requires=[
        'PyYAML>=3',
        'lxml>=3.4.2' ],
      scripts=[
        'fgcz/scripts/fgcz_biobeamer.py',
        'fgcz/scripts/fgcz_fcc_run_linux.py',
        'fgcz/scripts/fgcz_fcc_run_windows.py'
      ],
      zip_safe=True)
