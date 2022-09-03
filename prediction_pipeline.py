

class PredictionPipeline:
    '''
    Loads & uses models, makes endemble data and retrun final prediction
    '''

    def __init__(self):
        self.final_proba: float = None
    
    def get_final_prediction(self) -> float:
        self._pre_pipeline()
        self._predict_final_nn()
        return self.final_proba

    def _pre_pipeline(self):
        self._predict_adaboost()
        self._predict_svc()
        self._predict_lgbm()
        self._predict_nn()

    def _get_final_nn(self):
        pass

    def _predict_final_nn(self):
        pass

    def _get_adaboost(self):
        pass

    def _predict_adaboost(self):
        pass

    def _get_svc(self):
        pass

    def _predict_svc(self):
        pass

    def _get_lgbm(self):
        pass

    def _predict_lgbm(self):
        pass

    def _get_nn(self):
        pass

    def _predict_nn(self):
        pass