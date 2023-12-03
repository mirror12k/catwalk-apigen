from distutils.core import setup
setup(
  name = 'catwalk_apigen',
  packages = ['catwalk_apigen'],
  version = '0.1',
  license='MIT',
  description = 'Cross-language API generator for simple REST and GraphlQL apis',
  author = 'mirror12k',
  url = 'https://github.com/mirror12k/catwalk-apigen',
  download_url = 'https://github.com/mirror12k/catwalk-apigen/releases/latest/download/release.zip',
  keywords = ['api', 'code-generator'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
  ],
)