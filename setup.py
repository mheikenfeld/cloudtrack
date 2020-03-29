from setuptools import setup

setup(name='tobac',
      version='1.2',
      description='Tracking and object-based analysis of clouds',
      url='http://github.com/climate-processes/tobac',
      author='Max Heikenfeld',
      author_email='max.heikenfeld@physics.ox.ac.uk',
      license='GNU',
      packages=['tobac','tobac.analysis','tobac.plot','tobac.themes','tobac.themes.tobac_v1'],
      install_requires=[],
      zip_safe=False)
