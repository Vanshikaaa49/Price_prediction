from flask import Flask, request, jsonify
from flask_cors import CORS
import util
from logger_config import setup_logger

app = Flask(__name__)
CORS(app)

# Setup logging
logger = setup_logger(__name__)

def validate_prediction_input(total_sqft, location, bhk, bath):
    """Validate input parameters for home price prediction"""
    errors = []
    
    # Validate total_sqft
    try:
        sqft_val = float(total_sqft)
        if sqft_val <= 0:
            errors.append("Total square feet must be greater than 0")
        elif sqft_val > 100000:
            errors.append("Total square feet seems too large (>100,000)")
    except (ValueError, TypeError):
        errors.append("Total square feet must be a valid number")
    
    # Validate BHK
    try:
        bhk_val = int(bhk)
        if bhk_val < 1 or bhk_val > 10:
            errors.append("BHK must be between 1 and 10")
    except (ValueError, TypeError):
        errors.append("BHK must be a valid integer")
    
    # Validate Bath
    try:
        bath_val = int(bath)
        if bath_val < 1 or bath_val > 10:
            errors.append("Bathrooms must be between 1 and 10")
    except (ValueError, TypeError):
        errors.append("Bathrooms must be a valid integer")
    
    # Validate Location
    if not location or not isinstance(location, str):
        errors.append("Location is required")
    else:
        valid_locations = util.get_location_names()
        location_lower = location.lower().strip()
        valid_location_lower = [loc.lower() for loc in valid_locations]
        if location_lower not in valid_location_lower:
            errors.append(f"Invalid location: {location}")
    
    return errors

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    try:
        response = jsonify({
            'locations': util.get_location_names()
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        logger.info("Location names fetched successfully")
        return response
    except Exception as e:
        logger.error(f"Error fetching locations: {str(e)}")
        return jsonify({'error': 'Failed to fetch locations'}), 500

@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    try:
        total_sqft = request.form.get('total_sqft')
        location = request.form.get('location')
        bhk = request.form.get('bhk')
        bath = request.form.get('bath')
        
        # Validate inputs
        errors = validate_prediction_input(total_sqft, location, bhk, bath)
        if errors:
            logger.warning(f"Validation errors: {errors}")
            return jsonify({'error': 'Validation failed', 'details': errors}), 400
        
        # Convert to appropriate types
        total_sqft = float(total_sqft)
        bhk = int(bhk)
        bath = int(bath)
        
        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        
        logger.info(f"Price predicted - Location: {location}, SqFt: {total_sqft}, BHK: {bhk}, Bath: {bath}, Price: {estimated_price}")
        
        response = jsonify({
            'estimated_price': estimated_price
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to predict price', 'details': str(e)}), 500

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(debug=True)