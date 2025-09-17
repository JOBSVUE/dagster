from unittest.mock import Mock, patch

import dagster as dg
import pytest
from project_prompt_eng.defs.assets import (
    InputLocation,
    UserInputSchema,
    nearest_fuel_stations,
    user_input_prompt,
)
from project_prompt_eng.defs.resources import NRELResource


@pytest.fixture
def nrel_resource():
    return NRELResource(api_key="test")


@pytest.fixture
def anthropic_resource():
    class AnthropicResource(dg.ConfigurableResource):
        def get_client(self, context):
            return Mock()

    return AnthropicResource()


@pytest.fixture
def example_response():
    return {
        "fuel_stations": [
            {"latitude": 40.7128, "longitude": -74.0060, "access_days_time": "24 hours daily"}
        ]
    }


@patch("requests.get")
def test_nrel_resource(mock_get, example_response, nrel_resource):
    mock_response = Mock()
    mock_response.json.return_value = example_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    assert nrel_resource.alt_fuel_stations(latitude=40.7128, longitude=-74.0060)


@patch("project_prompt_eng.defs.assets.AnthropicResource")
def test_user_input_prompt(mock_anthropic, anthropic_resource, nrel_resource):
    # Mock the Anthropic client response
    mock_client = Mock()
    mock_response = Mock()
    mock_response.content = [Mock()]
    mock_response.content[
        0
    ].text = '{"latitude": 41.8796, "longitude": -87.6237, "fuel_type": "ELEC"}'
    mock_client.messages.create.return_value = mock_response
    mock_anthropic.return_value.get_client.return_value.__enter__.return_value = mock_client

    config = InputLocation(
        location="I'm near the The Art Institute of Chicago and driving a Kia EV9"
    )

    # Create a mock context
    context = Mock()
    context.log = Mock()

    # Get the result from the materialization
    materialization_result = result.output_for_node("user_input_prompt")
    assert materialization_result.latitude == 41.8796
    assert materialization_result.longitude == -87.6237
    assert materialization_result.fuel_type == "ELEC"


@patch("requests.get")
def test_nearest_fuel_stations(mock_get, example_response, nrel_resource):
    mock_response = Mock()
    mock_response.json.return_value = example_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    config = UserInputSchema(latitude=41.8796, longitude=-87.6237, fuel_type="ELEC")

    result = nearest_fuel_stations(nrel_resource, config)

    # Should return a list of fuel stations with access_days_time
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["latitude"] == 40.7128
    assert result[0]["longitude"] == -74.0060
    assert result[0]["access_days_time"] == "24 hours daily"
