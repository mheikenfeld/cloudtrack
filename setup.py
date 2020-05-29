from setuptools import setup

setup(name='tobac',
      use_scm_version=True,
      setup_requires=['setuptools_scm'],
      description='Tracking and object-based analysis of clouds',
      url='http://github.com/climate-processes/tobac',
      author='Max Heikenfeld',
      author_email='max.heikenfeld@web.de',
      license='BSD-3',
      packages=['tobac','tobac.analysis','tobac.plot','tobac.themes','tobac.themes.tobac_v1'],
      install_requires=[],
      zip_safe=False)
