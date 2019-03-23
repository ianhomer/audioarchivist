from setuptools import setup
setup(
    name='audio-helpers',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'aconvert=aconvert:run',
            'ameta=ameta:run',
            'amove=amove:run',
            'atest=atest:run'
        ]
    }
)
