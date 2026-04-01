from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data_to_big_query(data, **kwargs) -> None:
    # Load the config you just edited
    config_path = os.path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    
    # Initialize the BigQuery client using Mage's wrapper
    loader = ConfigFileLoader(config_path, config_profile)

    for key, value in data.items():
        
        table_id = f'project-de05ea45-0c4e-455c-806.aus_road_deaths_data_engineering.{key}'
        
        print(f'Exporting {key} to {table_id}...')

        BigQuery.with_config(loader).export(
            DataFrame(value),
            table_id,
            if_exists='replace',
        )