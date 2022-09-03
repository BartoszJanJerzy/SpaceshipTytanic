# README

This is repository for my kaggle competition code.
Make /data dir with data from kaggle (https://www.kaggle.com/c/spaceship-titanic/data) to run scripts.

Modules:
* `my_utils/` - helpful scripts

Notebooks:
* `00_install.ipynb` - notebook with individual instalations 
* `01_preprocessing.ipynb` - EDA and data preprocessing
* `02_clustering.ipynb` - KMeans use to get new feature
* `03_lazy_predict.ipynb` - searching for best models
* `04_adaboost_feature.ipynb` - adaboost tuning to get new feature
* `05_svc_optimization.ipynb` - svc tuning to get new feature
* `06_lgbm_optimization.ipynb` - lgbm tuning to get new feature
* `07_neural_optimization.ipynb` - neural network tuning to get new feature
* `08_lgbm_optimization.ipynb` - final model tuning
* `09_prepare_values.ipynb` - preparing values needed to preprocess and valdiate data
* `10_run_prediction.ipynb` - example prediction using pipeline

Scripts:
* `data_valdiation.py` - pandera validation schemas for pandas DataFrames
* `preprocessor.py` - class with preprocessing needed in prediction pipeline
* `prediction_pipeline.py` - pipeline of tuned models