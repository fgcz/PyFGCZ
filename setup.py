from setuptools import setup


"""
https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
"""


try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()



setup(name='PyFGCZ',
      version='0.4',
      description="contains BioBeamer and FCC",
      long_description=read_md('README.md'),
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
