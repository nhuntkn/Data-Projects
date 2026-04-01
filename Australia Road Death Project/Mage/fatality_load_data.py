import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_from_google_cloud_storage(*args, **kwargs):
    """
    Template for loading data from API
    """
    url = 'https://storage.googleapis.com/aus-road-deaths-data-engineering-project/bitre_fatalities_feb2026.csv'
    response = requests.get(url)

    return pd.read_csv(io.StringIO(response.text), sep=',', header = 4)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
