# README

This is repository for my dash app with visualziation of kaggle competition model.
See the competition -> https://www.kaggle.com/c/spaceship-titanic

Structure:
* `app.py` - main code for dash app
* `app_pages` - pages for dash app
* `app_utils` - scripts used in dash app
  * `data_valdiation.py` - pandera validation schemas for pandas DataFrames
  * `preprocessor.py` - class with preprocessing needed in prediction pipeline
  * `prediction_pipeline.py` - pipeline of tuned models
* `assets` - styling scripts for dash app
