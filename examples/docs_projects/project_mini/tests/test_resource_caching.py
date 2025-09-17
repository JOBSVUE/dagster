from unittest.mock import patch

import dagster as dg
from project_mini.defs.resource_caching.expensive_resource import (
    ExpensiveResource,
    another_expensive_asset,
    expensive_asset,
)
from project_mini.defs.resource_caching.expensive_resource_cache import (
    ExpensiveResourceCache,
    another_expensive_asset_cache,
    expensive_asset_cache,
)
from project_mini.defs.resource_caching.expensive_resource_pickle import (
    ExpensiveResourcePickle,
    another_expensive_asset_pickle,
    expensive_asset_pickle,
)


@patch("time.sleep", return_value=None)
def test_expensive_asset(mock_sleep):
    result = dg.materialize(
        assets=[expensive_asset, another_expensive_asset],
        resources={
            "expensive_resource": ExpensiveResource(),
        },
    )
    assert result.success


@patch("time.sleep", return_value=None)
def test_expensive_asset_cache(mock_sleep):
    result = dg.materialize(
        assets=[expensive_asset_cache, another_expensive_asset_cache],
        resources={
            "expensive_resource_cache": ExpensiveResourceCache(),
        },
    )
    assert result.success


@patch("time.sleep", return_value=None)
def test_expensive_asset_pickle(mock_sleep):
    result = dg.materialize(
        assets=[expensive_asset_pickle, another_expensive_asset_pickle],
        resources={
            "expensive_resource_pickle": ExpensiveResourcePickle(
                cache_file=".tmp/dagster_resource_cache.pkl"
            ),
        },
    )
    assert result.success
