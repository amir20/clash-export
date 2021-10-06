from setuptools import find_namespace_packages, setup

setup(
    name="clashleaders",
    packages=find_namespace_packages(include=["clashleaders*"]),
    version="1.0",
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "worker=clashleaders.worker:main",
            "rq_worker=clashleaders.rq_worker:main",
            "update_all=clashleaders.cli:update_all_calculations",
            "migrate=clashleaders.cli:migrate_pre_calculated",
            "update_status=clashleaders.model:Status.update_status",
            "delete_outdated=clashleaders.batch.purge:delete_outdated",
            "reset_stats=clashleaders.batch.purge:reset_stats",
            "compute_similar_clans=clashleaders.batch.similar_clan:compute_similar_clans",
            "update_troops=clashleaders.model:AverageTroop.update_all",
            "index_random_war_clan=clashleaders.cli:index_random_war_clan",
            "fetch_clan_leaderboards=clashleaders.cli:fetch_clan_leaderboards",
        ],
    },
)
