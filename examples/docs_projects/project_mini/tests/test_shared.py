import dagster as dg
from project_mini.defs.shared_module.shared_module import asset_configurations, my_codespace_assets


def test_asset_configurations():
    expected_assets = ["asset_1", "asset_2", "asset_3"]
    assert asset_configurations == expected_assets
    assert len(asset_configurations) == 3


def test_asset_materialization():
    result = dg.materialize(assets=my_codespace_assets)

    assert result.success

    materialized_asset_keys = {
        event.asset_key for event in result.get_asset_materialization_events()
    }
    expected_keys = {dg.AssetKey(name) for name in asset_configurations}
    assert materialized_asset_keys == expected_keys
