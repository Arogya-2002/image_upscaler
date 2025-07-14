from src.exceptions import CustomException
from src.logger import logging
from src.constants import MODEL_NAME, MAX_SIZE, TILE_OVERLAP, OUTPUT_DIR

import os
import sys


class ConfigEntity:
    def __init__(self):
        self.model_name = MODEL_NAME
        self.max_size = MAX_SIZE
        self.tile_overlap = TILE_OVERLAP
        self.output_dir = OUTPUT_DIR

   
class ImageUpscalerConfig:
    def __init__(self,config: ConfigEntity):
        self.model_name = config.model_name
        self.max_size = config.max_size
        self.tile_overlap = config.tile_overlap
        self.output_dir = config.output_dir     