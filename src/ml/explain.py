import shap
import pandas as pd
import numpy as np
import os
import joblib

class ModelExplainer:
    def __init__(self, model_input):
        """
        model_input: Can be the model object itself or path to it.
        """
        if isinstance(model_input, str):
            self.model = joblib.load(model_input)
        else:
            self.model = model_input
            
        # Initialize TreeExplainer (assuming XGBoost/RandomForest)
        try:
            self.explainer = shap.TreeExplainer(self.model)
        except Exception as e:
            print(f"Warning: Could not initialize TreeExplainer: {e}")
            self.explainer = None

    def explain_local(self, features: np.ndarray, feature_names: list):
        """
        Returns top contributing features for a single prediction.
        """
        if self.explainer is None:
            return "Explanation unavailable"

        try:
            # Calculate SHAP values
            shap_values = self.explainer.shap_values(features)
            
            # If binary classification, shap_values might be a list or single array
            # XGBoost usually returns single array for binary
            if isinstance(shap_values, list):
                vals = shap_values[1][0] # Positive class
            else:
                vals = shap_values[0]

            # Pair values with names
            explanation = sorted(zip(feature_names, vals), key=lambda x: abs(x[1]), reverse=True)
            
            # Format as robust strings
            top_factors = []
            for name, val in explanation[:3]:
                direction = "increases risk" if val > 0 else "decreases risk"
                top_factors.append(f"{name} ({direction})")
                
            return ", ".join(top_factors)
            
        except Exception as e:
            return f"Explanation failed: {str(e)}"
