import pandas as pd
import numpy as np

class DataPreprocessor:
    def __init__(self):
        # Mappings derived from training logic (LabelEncoder alphabetical sort)
        self.education_map = {'Graduate': 0, 'Not Graduate': 1}
        self.self_employed_map = {'No': 0, 'Yes': 1}
        
    def preprocess(self, data: dict) -> np.ndarray:
        """
        Preprocesses a dictionary of input data into a format suitable for the model.
        
        Expected keys:
        - no_of_dependents
        - education ('Graduate' or 'Not Graduate')
        - self_employed ('Yes' or 'No')
        - income_annum
        - loan_amount
        - loan_term
        - cibil_score
        - residential_assets_value
        - commercial_assets_value
        - luxury_assets_value
        - bank_asset_value
        """
        try:
            # Map categorical variables
            education_encoded = self.education_map.get(data['education'], 1) # Default to 1 (Not Graduate) if unknown
            self_employed_encoded = self.self_employed_map.get(data['self_employed'], 0) # Default to 0 (No)
            
            # Create feature vector in the specific order the model expects
            features = [
                data['no_of_dependents'],
                education_encoded,
                self_employed_encoded,
                data['income_annum'],
                data['loan_amount'],
                data['loan_term'],
                data['cibil_score'],
                data['residential_assets_value'],
                data['commercial_assets_value'],
                data['luxury_assets_value'],
                data['bank_asset_value']
            ]
            
            # Convert to 2D numpy array (1 sample)
            return np.array([features])
            
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}")
            
    def get_feature_names(self):
        return [
            'no_of_dependents', 'education', 'self_employed', 'income_annum', 
            'loan_amount', 'loan_term', 'cibil_score', 'residential_assets_value', 
            'commercial_assets_value', 'luxury_assets_value', 'bank_asset_value'
        ]
