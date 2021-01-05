from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='leiaquilt',
    version='1.0.0',

    description='Utility for aligning images into a 2x1 or 2x2 quilt',

    long_description=long_description,

    long_description_content_type='text/markdown',

    url='https://github.com/LeiaInc/LeiaQuilt',

    packages=['leiaquilt'],

    python_requires='>=3.5, <4',

    install_requires=['opencv-python==4.4.0.42',
                      'numpy==1.19.5',
                      'joblib==0.17.0'],

    entry_points={
        'console_scripts': [
            'leiaquilt=leiaquilt:main',
        ],
    },
)
