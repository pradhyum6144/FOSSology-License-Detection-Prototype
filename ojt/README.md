# FOSSology ML Assisted License Detection Prototype

A prototype tool for detecting and classifying software licenses using text-similarity heuristics. This project flags ambiguous license fragments for manual review, similar to FOSSology's license detection capabilities.

## Features

- **Text Similarity Analysis**: Uses `difflib` and regex-based heuristics to match license text against known templates
- **SPDX Tagging**: Automatically generates SPDX-compliant license identifiers
- **Triage Views**: Review and accept/reject ambiguous license detections
- **Batch Processing**: Analyze multiple text fragments from JSON/CSV files
- **Export Reports**: Export results in JSON, CSV, or SPDX format
- **Evaluation Metrics**: Calculate precision, recall, and accuracy on labeled samples

## Project Structure

```
ojt/
├── app.py                 # Flask backend server
├── license_detector.py    # Core license detection engine
├── spdx_tagger.py         # SPDX tagging and document generation
├── requirements.txt       # Python dependencies
├── data/
│   ├── license_templates.json    # License templates database
│   ├── spdx_licenses.json         # SPDX license information
│   └── sample_fragments.json      # Sample test data
├── static/
│   ├── index.html         # Main UI
│   ├── styles.css         # Styling
│   └── app.js             # Frontend logic
└── README.md             # This file
```

## Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Modern web browser

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd ojt
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify data files exist:**
   - `data/license_templates.json`
   - `data/spdx_licenses.json`
   - `data/sample_fragments.json`

## Usage

### Starting the Server

1. **Run the Flask application:**
   ```bash
   python app.py
   ```

2. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

### Using the Application

#### 1. Analyze Single Text
- Paste a license text fragment in the text area
- Click "Analyze License"
- View detection results with confidence scores and ambiguity flags

#### 2. Batch Analysis
- Click "Load Sample Data" to use built-in samples
- Or upload a JSON/CSV file with text fragments
- Review all results in a grid view
- Export results as JSON, CSV, or SPDX format

#### 3. Triage View
- Automatically shows ambiguous detections from batch analysis
- Review each fragment and accept or reject the detection
- Helps improve accuracy through manual review

#### 4. Evaluation
- Click "Run Evaluation" to test on labeled samples
- View precision, recall, accuracy, and F1 score metrics
- Use this to assess detection quality

## How It Works

### Detection Algorithm

1. **Text Normalization**: Removes extra whitespace, converts to lowercase, normalizes punctuation
2. **Template Matching**: Compares input text against known license templates using `difflib.SequenceMatcher`
3. **Keyword Analysis**: Checks for license-specific keywords
4. **Score Calculation**: Combines template similarity (70%) and keyword matching (30%)
5. **Ambiguity Detection**: Flags fragments as ambiguous if:
   - Confidence is below threshold (default: 0.8)
   - Multiple licenses have similar scores (within 0.15)

### Supported Licenses

The prototype includes templates for:
- MIT License
- Apache License 2.0
- GNU GPL v2.0
- GNU GPL v3.0
- BSD 3-Clause License
- GNU LGPL v2.1

## Data Formats

### Input JSON Format
```json
[
  {
    "id": 1,
    "text": "License text fragment here...",
    "expected_license": "MIT"
  }
]
```

### Input CSV Format
```csv
id,text,expected_license
1,"License text...",MIT
```

### Output Format
```json
{
  "detected_license": "MIT License",
  "confidence": 0.85,
  "is_ambiguous": false,
  "spdx_id": "MIT",
  "matches": [...]
}
```

## Limitations

1. **Template-Based**: Relies on predefined license templates; may miss custom or modified licenses
2. **Text Similarity Only**: Does not use machine learning models; uses heuristic matching
3. **Limited License Database**: Includes only 6 common licenses; can be extended
4. **No Context Awareness**: Analyzes text in isolation without code context
5. **Manual Triage Required**: Ambiguous cases require human review

## Next Steps

### Potential Improvements

1. **Expand License Database**: Add more license templates (Mozilla, ISC, etc.)
2. **Machine Learning Integration**: Train ML models for better accuracy
3. **Code Context Analysis**: Consider surrounding code when detecting licenses
4. **Database Storage**: Store triage decisions for learning
5. **API Enhancements**: Add authentication, rate limiting, batch processing optimization
6. **Advanced Export**: Support more formats (XML, YAML, etc.)

### Integration with FOSSology

This prototype demonstrates concepts that could be integrated into FOSSology:
- Similarity-based detection as a pre-filter
- Triage workflow for ambiguous cases
- SPDX export capabilities
- Evaluation metrics for quality assurance

## Development Timeline

- **Week 1**: Setup & Planning ✓
- **Week 2**: Build Core Features ✓
- **Week 3**: Polish UI & Add Extras ✓
- **Week 4**: Test, Document, Demo ✓

## Demo Video

A 2-3 minute demo video should cover:
1. Single text analysis
2. Batch processing with sample data
3. Triage review workflow
4. Export functionality
5. Evaluation metrics

## License

This prototype is provided as-is for educational and demonstration purposes.

## Contributing

This is a prototype project. For production use, consider:
- Adding comprehensive test coverage
- Implementing proper error handling
- Adding logging and monitoring
- Security hardening
- Performance optimization

## Contact

For questions or issues, please refer to the project documentation or create an issue in the repository.

