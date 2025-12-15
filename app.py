from flask import Flask, render_template, request, jsonify, send_file
from data_processor import UMKMDataProcessor
from fuzzy_logic import UMKMFuzzyLogic
import json
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize components
try:
    csv_file = 'Posisi Kredit Usaha Mikro, Kecil, dan Menengah (UMKM) pada Bank Umum__, 2023.csv'
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file not found: {csv_file}")
    
    data_processor = UMKMDataProcessor(csv_file)
    fuzzy_logic = UMKMFuzzyLogic()
    logger.info("Application initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize application: {str(e)}")
    data_processor = None
    fuzzy_logic = None

@app.route('/')
def index():
    """Main page with the fuzzy logic interface"""
    return render_template('index.html')

@app.route('/api/get_options')
def get_options():
    """Get all available options for dropdowns"""
    try:
        if not data_processor:
            return jsonify({'error': 'Data processor not initialized'}), 500
            
        options = {
            'business_fields': data_processor.get_all_business_fields(),
            'scales': data_processor.get_all_scales(),
            'usage_types': data_processor.get_all_usage_types()
        }
        return jsonify(options)
    except Exception as e:
        logger.error(f"Error getting options: {str(e)}")
        return jsonify({'error': 'Failed to load options'}), 500

@app.route('/api/calculate', methods=['POST'])
def calculate():
    """Calculate fuzzy logic approval score"""
    try:
        if not data_processor or not fuzzy_logic:
            return jsonify({'error': 'System not properly initialized'}), 500
            
        data = request.get_json()
        
        # Get input values
        business_field = data.get('business_field')
        scale = data.get('scale')
        usage_type = data.get('usage_type')
        
        # Validate inputs
        if not all([business_field, scale, usage_type]):
            return jsonify({'error': 'Semua field harus diisi'}), 400
        
        # Validate that inputs exist in data
        if business_field not in data_processor.get_all_business_fields():
            return jsonify({'error': f'Lapangan usaha "{business_field}" tidak valid'}), 400
        if scale not in data_processor.get_all_scales():
            return jsonify({'error': f'Skala usaha "{scale}" tidak valid'}), 400
        if usage_type not in data_processor.get_all_usage_types():
            return jsonify({'error': f'Jenis penggunaan "{usage_type}" tidak valid'}), 400
        
        # Get fuzzy values
        scale_value = fuzzy_logic.scale_to_fuzzy_value(scale)
        risk_value = fuzzy_logic.risk_to_fuzzy_value(data_processor.get_business_field_risk(business_field))
        priority_value = fuzzy_logic.priority_to_fuzzy_value(data_processor.get_usage_priority(usage_type))
        
        # Calculate approval score
        approval_score = fuzzy_logic.calculate_approval_score(scale_value, risk_value, priority_value)
        
        # Get approval category and color
        approval_category, approval_color = fuzzy_logic.get_approval_category(approval_score)
        
        # Get recommendations
        recommendations = fuzzy_logic.get_recommendations(approval_score, scale_value, risk_value, priority_value)
        
        # Get detailed analysis
        detailed_analysis = fuzzy_logic.get_detailed_analysis(scale_value, risk_value, priority_value, approval_score)
        
        # Generate visualization
        visualization = fuzzy_logic.generate_fuzzy_visualization(scale_value, risk_value, priority_value, approval_score)
        
        # Get additional info
        credit_range = data_processor.get_scale_credit_range(scale)
        field_credit = data_processor.business_fields.get(business_field, 0)
        usage_credit = data_processor.usage_types.get(usage_type, 0)
        
        # Prepare response
        result = {
            'approval_score': round(approval_score, 2),
            'approval_category': approval_category,
            'approval_color': approval_color,
            'recommendations': recommendations,
            'input_values': {
                'business_field': business_field,
                'scale': scale,
                'usage_type': usage_type
            },
            'analysis': {
                'scale_value': round(scale_value, 2),
                'risk_value': round(risk_value, 2),
                'priority_value': round(priority_value, 2),
                'credit_range_million': f"{credit_range[0]} - {credit_range[1]} Juta",
                'field_credit_billion': f"{field_credit:,} Miliar",
                'usage_credit_billion': f"{usage_credit:,} Miliar",
                'detailed_analysis': detailed_analysis
            },
            'visualization': visualization,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in calculation: {str(e)}")
        return jsonify({'error': f'Terjadi kesalahan dalam perhitungan: {str(e)}'}), 500

@app.route('/api/statistics')
def get_statistics():
    """Get UMKM statistics for display"""
    try:
        if not data_processor:
            return jsonify({'error': 'Data processor not initialized'}), 500
            
        total_credit = sum(data_processor.business_fields.values())
        
        stats = {
            'total_credit': f"{total_credit:,} Miliar",
            'total_business_fields': len(data_processor.business_fields),
            'scales_distribution': {
                'Mikro': f"{data_processor.scales.get('Mikro', 0):,} Miliar",
                'Kecil': f"{data_processor.scales.get('Kecil', 0):,} Miliar",
                'Menengah': f"{data_processor.scales.get('Menengah', 0):,} Miliar"
            },
            'usage_distribution': {
                'Modal Kerja': f"{data_processor.usage_types.get('Modal Kerja', 0):,} Miliar",
                'Investasi': f"{data_processor.usage_types.get('Investasi', 0):,} Miliar"
            },
            'top_business_fields': sorted(data_processor.business_fields.items(),
                                        key=lambda x: x[1], reverse=True)[:5],
            'risk_distribution': {
                'low_risk': sum(1 for field in data_processor.business_fields.keys()
                              if data_processor.get_business_field_risk(field) <= 0.4),
                'medium_risk': sum(1 for field in data_processor.business_fields.keys()
                                 if 0.4 < data_processor.get_business_field_risk(field) <= 0.7),
                'high_risk': sum(1 for field in data_processor.business_fields.keys()
                               if data_processor.get_business_field_risk(field) > 0.7)
            }
        }
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        return jsonify({'error': 'Failed to load statistics'}), 500

@app.route('/api/chart_data')
def get_chart_data():
    """Get data for charts visualization"""
    try:
        if not data_processor:
            return jsonify({'error': 'Data processor not initialized'}), 500
            
        chart_data = {
            'business_fields': {
                'labels': list(data_processor.business_fields.keys()),
                'values': list(data_processor.business_fields.values())
            },
            'scales': {
                'labels': list(data_processor.scales.keys()),
                'values': list(data_processor.scales.values())
            },
            'usage_types': {
                'labels': list(data_processor.usage_types.keys()),
                'values': list(data_processor.usage_types.values())
            }
        }
        return jsonify(chart_data)
    except Exception as e:
        logger.error(f"Error getting chart data: {str(e)}")
        return jsonify({'error': 'Failed to load chart data'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
