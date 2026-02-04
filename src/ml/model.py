import joblib
import os
import numpy as np

class CreditRiskModel:
    def __init__(self, model_path: str = None):
        if model_path is None:
            # Default to the standard location
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            model_path = os.path.join(base_dir, 'models', 'credit_risk_model.pkl')
            
        self.model_path = model_path
        self.model = None
        self.load_model()

    def load_model(self):
        """Loads the model from disk."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at {self.model_path}")
        
        try:
            self.model = joblib.load(self.model_path)
            print(f"Model loaded successfully from {self.model_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {str(e)}")

    def predict_probability(self, features: np.ndarray) -> float:
        """
        Predicts the probability of default (class 1).
        """
        if self.model is None:
            raise RuntimeError("Model is not loaded.")
        
        # XGBoost predict_proba returns [prob_class_0, prob_class_1]
        try:
            probs = self.model.predict_proba(features)
            return float(probs[0][1]) # Probability of Default
        except Exception as e:
            # Fallback for models that might use predict (if Prob isn't available, though unlikely for XGB)
            raise RuntimeError(f"Prediction failed: {str(e)}")
            
    def predict_class(self, features: np.ndarray) -> int:
        """Predicts the binary class (0 or 1)."""
        if self.model is None:
            raise RuntimeError("Model is not loaded.")
        
        return int(self.model.predict(features)[0])
