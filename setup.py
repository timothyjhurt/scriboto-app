from setuptools import setup

setup(name='scriboto-app',
      version='0.1',
      description='Using clinical conversations to complete EHR documentation',
      url='http://github.com/storborg/funniest',
      author='Scriboto',
      author_email='scriboto@gmail.com',
      license='MIT',
      packages=['scriboto-app'],
      install_requires=[
          'google-cloud-storage',
          'PyAudio',
          'pandas',
          'multiprocessing',
          'Flask',
      ],
      zip_safe=False)
