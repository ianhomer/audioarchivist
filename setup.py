from setuptools import setup
setup(
    name='audioarchivist',
    version='0.0.1',
    description='Audio Archivist',
    packages=['audioarchivist'],
    entry_points={
        'console_scripts': [
            'aconvert=audioarchivist.aconvert:run',
            'ameta=audioarchivist.ameta:run',
            'amove=audioarchivist.amove:run',
            'atest=audioarchivist.atest:run'
        ]
    }
)
