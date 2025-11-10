"""
FOSSology-style ML Assisted License Detection Prototype
Main Flask application for license text similarity analysis
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from license_detector import LicenseDetector
from spdx_tagger import SPDXTagger

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

@app.route('/data/<path:filename>')
def serve_data(filename):
    """Serve data files"""
    return send_from_directory('data', filename)

# Initialize components
detector = LicenseDetector()
spdx_tagger = SPDXTagger()

@app.route('/')
def index():
    """Serve the main UI"""
    return send_from_directory('static', 'index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """Analyze text for license detection"""
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    # Detect license and compute similarity
    results = detector.detect_license(text)
    
    return jsonify(results)

@app.route('/api/batch-analyze', methods=['POST'])
def batch_analyze():
    """Analyze multiple text fragments"""
    data = request.json
    fragments = data.get('fragments', [])
    
    if not fragments:
        return jsonify({'error': 'No fragments provided'}), 400
    
    results = []
    for fragment in fragments:
        result = detector.detect_license(fragment.get('text', ''))
        result['id'] = fragment.get('id', len(results))
        result['original_text'] = fragment.get('text', '')
        results.append(result)
    
    return jsonify({'results': results})

@app.route('/api/triage', methods=['POST'])
def triage_decision():
    """Record triage decision (accept/reject)"""
    data = request.json
    decision = data.get('decision')  # 'accept' or 'reject'
    fragment_id = data.get('id')
    detected_license = data.get('detected_license')
    confidence = data.get('confidence')
    
    # Store decision (in production, this would go to a database)
    triage_record = {
        'id': fragment_id,
        'decision': decision,
        'detected_license': detected_license,
        'confidence': confidence,
        'timestamp': data.get('timestamp')
    }
    
    return jsonify({'status': 'recorded', 'record': triage_record})

@app.route('/api/spdx-tag', methods=['POST'])
def spdx_tag():
    """Generate SPDX tags for detected licenses"""
    data = request.json
    license_name = data.get('license_name', '')
    
    if not license_name:
        return jsonify({'error': 'No license name provided'}), 400
    
    spdx_info = spdx_tagger.get_spdx_info(license_name)
    return jsonify(spdx_info)

@app.route('/api/export', methods=['POST'])
def export_report():
    """Export analysis results as formatted report"""
    data = request.json
    results = data.get('results', [])
    format_type = data.get('format', 'json')  # 'json', 'csv', 'spdx'
    
    if format_type == 'json':
        return jsonify({'format': 'json', 'data': results})
    elif format_type == 'csv':
        # Generate CSV
        csv_content = detector.export_to_csv(results)
        return jsonify({'format': 'csv', 'data': csv_content})
    elif format_type == 'spdx':
        # Generate SPDX format
        spdx_content = spdx_tagger.generate_spdx_document(results)
        return jsonify({'format': 'spdx', 'data': spdx_content})
    else:
        return jsonify({'error': 'Unsupported format'}), 400

@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    """Evaluate precision/recall on sample data"""
    data = request.json
    samples = data.get('samples', [])
    
    if not samples:
        return jsonify({'error': 'No samples provided'}), 400
    
    metrics = detector.evaluate_samples(samples)
    return jsonify(metrics)

if __name__ == '__main__':
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True, port=5000)

