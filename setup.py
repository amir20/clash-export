from setuptools import find_packages, setup


setup(
    name='clashleaders',
    packages=find_packages(),
    version='1.0',
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'scheduler=clashleaders.scheduler:main',
            'worker=clashleaders.worker:main',
            'player_worker=clashleaders.player_worker:main',
            'update_all=clashleaders.cli:update_all_calculations'
        ],
    }
)
