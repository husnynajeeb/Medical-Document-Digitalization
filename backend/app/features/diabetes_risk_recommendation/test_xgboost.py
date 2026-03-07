# backend/test_xgboost.py
"""
Test script to verify XGBoost model loading
"""
import sys
import os

print("Testing XGBoost installation and model loading...")
print("=" * 50)

# Try to import XGBoost
try:
    import xgboost as xgb
    print(f"✅ XGBoost version: {xgb.__version__}")
except ImportError as e:
    print(f"❌ XGBoost not installed: {e}")
    print("💡 Install with: pip install xgboost==2.0.3")
    sys.exit(1)

# Check for model file
model_path = os.path.join("models", "best_model.pkl")
if os.path.exists(model_path):
    print(f"✅ Model file found: {model_path}")
    
    # Try to load the model
    try:
        import joblib
        model = joblib.load(model_path)
        print(f"✅ Model loaded successfully!")
        print(f"   Model type: {type(model).__name__}")
        
        # Check model attributes
        if hasattr(model, 'feature_names_in_'):
            print(f"   Features: {len(model.feature_names_in_)}")
            print(f"   Feature names: {list(model.feature_names_in_)[:5]}...")
        
        if hasattr(model, 'n_classes_'):
            print(f"   Classes: {model.n_classes_}")
            
    except Exception as e:
        print(f"❌ Error loading model: {type(e).__name__}: {e}")
        
else:
    print(f"❌ Model file not found: {model_path}")
    print("   Place your XGBoost model at: models/best_model.pkl")

print("=" * 50)
print("Test complete!")