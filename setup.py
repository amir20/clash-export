from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip
from setuptools import find_packages, setup

pfile = Project(chdir=False).parsed_pipfile
requirements = convert_deps_to_pip(pfile['packages'], r=False)
test_requirements = convert_deps_to_pip(pfile['dev-packages'], r=False)

setup(
    name='clashleaders',
    packages=find_packages(),
    version='1.0',
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    tests_require=test_requirements,
    extras_require={'test': test_requirements},
    entry_points={
        'console_scripts': [
            'scheduler=clashleaders.scheduler:main',
            'worker=clashleaders.worker:main',
            'player_worker=clashleaders.player_worker:main',
            'update_all=clashleaders.cli:update_all_calculations'
        ],
    }
)
