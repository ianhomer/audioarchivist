from setuptools import setup
setup(
    name='audio-helpers',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'ameta=ameta:run',
            'aconvert=aconvert:run',
            'atest=atest:run'
        ]
    }
)
