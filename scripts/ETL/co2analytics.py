import json

from scripts.ETL.extraction_utils import extract_data_xlsx, extract_data_csv
import os
from pathlib import Path
from scripts.ETL.plots import plot, print_head
from scripts.ETL.transformation_utils import transform_wroclaw_data, transform_world_data


class CO2Analytics:
    def __init__(
            self,
            main_dir: Path = Path('.'),
            config: Path | str = Path('config.json')
    ):
        self._main_dir = Path(main_dir)
        self._config_file = Path(config)
        with self._main_dir.joinpath(self._config_file).open() as f:
            self._config = json.load(f)
        self._data_dir = self._main_dir.joinpath(self._config['data_dir'])
        self.plot_config = self._config.get('plots_configuration')
        self.wroclaw_data = None
        self.world_data = None
        self.transformed_wroclaw_data = None
        self.transformed_world_data = None

    @property
    def config(self):
        return self._config

    def run(self):
        self.wroclaw_data, self.world_data = self._get_data()
        self.transformed_wroclaw_data, self.transformed_world_data \
            = self._get_transformed_data()


    def _get_data(self):
        if self.wroclaw_data is None:
            file_path = self._data_dir.joinpath(self._config['files']['wroclaw'])
            self.wroclaw_data = extract_data_xlsx(file_path)
        if self.world_data is None:
            file_path = self._data_dir.joinpath(self._config['files']['world'])
            self.world_data = extract_data_csv(file_path)
        return self.wroclaw_data, self.world_data


    def _get_transformed_data(self):
        if self.transformed_wroclaw_data is None:
            self.transformed_wroclaw_data = transform_wroclaw_data(self.wroclaw_data)
        if self.transformed_world_data is None:
            self.transformed_world_data = transform_world_data(self.world_data)
        return self.transformed_wroclaw_data, self.transformed_world_data
