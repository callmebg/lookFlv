# services/ai_analyser.py
class StreamAnomalyDetector:
    def __init__(self, model_path='models/lstm_corruption.h5'):
        self.model = tf.keras.models.load_model(model_path)
        self.feature_extractor = FeatureExtractor()
        
    def analyze(self, network_metrics, encoding_metrics):
        # 特征工程
        features = self.feature_extractor.transform(
            network_metrics, 
            encoding_metrics
        )
        # LSTM时序分析
        prediction = self.model.predict(features.reshape(1, 30, -1))
        return self._interpret_prediction(prediction)