import os
import pickle
import pandas as pd
from app_utils.data_validation import PreprocessedData
import tensorflow as tf


class PredictionPipeline:
    '''
    Loads & uses models, makes endemble data and retrun final prediction
    '''
    MODELS_PATH = os.path.join('models')
    STANDARD_FEATURES = ['is_g734s', 'CryoSleep', 'VIP', 'Europa', 'Mars', 'PSO J318.5-22',
    'TRAPPIST-1e', 'Age', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck',
    'segment']
    FINAL_FEATURES = ['ada_boost', 'mean', 'lgbm', 'neural', 'svc', 'segment',
    'CryoSleep', 'Spa', 'RoomService', 'VRDeck', 'FoodCourt', 'ShoppingMall', 'Europa',
    'Age', 'TRAPPIST-1e','PSO J318.5-22', 'Mars', 'VIP', 'is_g734s']
    PROBAS_COLS = ['ada_boost', 'lgbm', 'svc', 'neural', 'mean']

    def __init__(
        self,
        data: pd.DataFrame,
        visible: bool = False
    ):  
        self.data = PreprocessedData.validate(data)
        self.visible = visible
        self.__prediction_ready = False
    
    def get_prediction(self) -> float:
        error_text = 'Run run_prediction() before you get prediction!'
        assert self.__prediction_ready, error_text
        return self.final_proba[0][0]

    def run_model(self):
        self.__prediction_ready = False
        self._pre_pipeline()
        self._predict_final_nn()
        self.__prediction_ready = True

    def _pre_pipeline(self):
        self._predict_kmeans()
        self._predict_adaboost()
        self._predict_svc()
        self._predict_lgbm()
        self._predict_nn()
        self._prepare_mean()

    def _get_final_nn(self):
        path = os.path.join(self.MODELS_PATH, 'final_model')
        model = tf.keras.models.load_model(path)

        if self.visible:
            print('Loaded final model.')

        return model

    def _predict_final_nn(self):
        model = self._get_final_nn()
        x = self.data[self.FINAL_FEATURES].to_numpy()
        predictions = model.predict(x)
        self.final_proba = predictions
                        
        if self.visible:
            print('Final prediction ready.')
            
    def _get_kmeans(self):
        filename = 'kmeans.pickle'
        model = self.__load_model_dict(filename)
        
        if self.visible:
            print('Loaded kmeans.')

        return model

    def _predict_kmeans(self):
        model = self._get_kmeans()
        segments = model.predict(self.data)
        self.data['segment'] = segments
        
        if self.visible:
            print('KMeans ready.')

    def _get_adaboost(self):
        filename = 'adaboost.pickle'
        model_dict = self.__load_model_dict(filename)
                
        if self.visible:
            print('Loaded adaboost.')

        return model_dict

    def _predict_adaboost(self):
        model_dict = self._get_adaboost()
        model = model_dict['model']
        features = model_dict['features']
        
        x = self.data[features].to_numpy()
        predictions = model.predict_proba(x)
        self.data['ada_boost'] = predictions[0][0]
                
        if self.visible:
            print('Adaboost ready.')

    def _get_svc(self):
        filename = 'svc.pickle'
        model_dict = self.__load_model_dict(filename)
                        
        if self.visible:
            print('Loaded svc.')
            
        return model_dict

    def _predict_svc(self):
        model_dict = self._get_svc()
        model = model_dict['model']
        features = model_dict['features']
        
        x = self.data[features].to_numpy()
        predictions = model.predict_proba(x)
        self.data['svc'] = predictions[0][0]
                
        if self.visible:
            print('SVC ready.')

    def _get_lgbm(self):
        filename = 'lgbm.pickle'
        model_dict = self.__load_model_dict(filename)
                        
        if self.visible:
            print('Loaded lgbm.')
            
        return model_dict

    def _predict_lgbm(self):
        model_dict = self._get_lgbm()
        model = model_dict['model']
        features = model_dict['features']
        
        x = self.data[features].to_numpy()
        predictions = model.predict_proba(x)
        self.data['lgbm'] = predictions[0][0]
                
        if self.visible:
            print('LGBM ready.')

    def _get_nn(self):
        path = os.path.join(self.MODELS_PATH, 'neural_model')
        model = tf.keras.models.load_model(path)
                        
        if self.visible:
            print('Loaded neural.')
            
        return model

    def _predict_nn(self):
        model = self._get_nn()
        x = self.data[self.STANDARD_FEATURES].to_numpy()
        predictions = model.predict(x)
        self.data['neural'] = predictions[0][0]
                
        if self.visible:
            print('Neural ready.')

    def _prepare_mean(self):
        cols = ['ada_boost', 'svc', 'lgbm', 'neural']
        self.data['mean'] = self.data[cols].mean(axis=1)

    def __load_model_dict(self, filename: str) -> dict:
        path = os.path.join(self.MODELS_PATH, filename)
        with open(path, 'rb') as file:
            model_dict = pickle.load(file)

        return model_dict