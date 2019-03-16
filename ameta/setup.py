from setuptools import setup
setup(
    name='ameta',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'ameta=ameta:run'
        ]
    }
)
