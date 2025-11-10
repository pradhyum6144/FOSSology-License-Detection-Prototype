# Project Summary: FOSSology ML Assisted License Detection Prototype

## Overview

This prototype implements a FOSSology-style license detection tool that uses text-similarity heuristics to identify and flag ambiguous license fragments. The system is designed for code compliance scenarios where accurate license identification is critical.

## Architecture

### Backend (Python/Flask)
- **app.py**: Flask REST API server with endpoints for analysis, batch processing, triage, and export
- **license_detector.py**: Core detection engine using `difflib` for text similarity and regex for keyword matching
- **spdx_tagger.py**: SPDX license tagging and document generation module

### Frontend (HTML/CSS/JavaScript)
- **index.html**: Single-page application with tabbed interface
- **styles.css**: Modern, responsive styling with gradient themes
- **app.js**: Client-side logic for API interaction and UI updates

### Data
- **license_templates.json**: Database of license templates with keywords
- **spdx_licenses.json**: SPDX license metadata
- **sample_fragments.json**: Test data with labeled examples

## Key Features Implemented

✅ **Text Similarity Analysis**
- Uses `difflib.SequenceMatcher` for template matching
- Keyword-based scoring for additional confidence
- Combined scoring algorithm (70% similarity + 30% keywords)

✅ **Ambiguity Detection**
- Flags fragments with low confidence (< 0.8)
- Identifies cases where multiple licenses score similarly
- Visual indicators in UI for ambiguous cases

✅ **SPDX Tagging**
- Automatic SPDX identifier generation
- SPDX document export format
- License metadata lookup

✅ **Triage Workflow**
- Dedicated view for reviewing ambiguous detections
- Accept/reject functionality
- Tracks decisions for quality improvement

✅ **Batch Processing**
- JSON/CSV file upload support
- Grid view for multiple results
- Sample data loading

✅ **Export Functionality**
- JSON format for programmatic use
- CSV format for spreadsheet analysis
- SPDX format for compliance documentation

✅ **Evaluation Metrics**
- Precision, recall, accuracy, and F1 score calculation
- Tested on labeled sample data
- Visual metrics dashboard

## Technical Implementation

### Detection Algorithm Flow

1. **Input Normalization**
   - Remove extra whitespace
   - Convert to lowercase
   - Normalize punctuation

2. **Template Matching**
   - Compare against each license template
   - Calculate similarity ratio using SequenceMatcher
   - Score: 0.0 to 1.0

3. **Keyword Analysis**
   - Check for license-specific keywords
   - Calculate keyword match percentage

4. **Combined Scoring**
   - Weighted average: 70% similarity + 30% keywords
   - Sort matches by combined score

5. **Ambiguity Detection**
   - Flag if confidence < threshold (0.8)
   - Flag if top 2 scores within 0.15

### Supported Licenses

- MIT License
- Apache License 2.0
- GNU GPL v2.0
- GNU GPL v3.0
- BSD 3-Clause License
- GNU LGPL v2.1

## API Endpoints

- `POST /api/analyze` - Single text analysis
- `POST /api/batch-analyze` - Batch fragment analysis
- `POST /api/triage` - Record triage decision
- `POST /api/spdx-tag` - Get SPDX information
- `POST /api/export` - Export results (JSON/CSV/SPDX)
- `POST /api/evaluate` - Calculate evaluation metrics

## Usage Scenarios

### Scenario 1: Single Fragment Analysis
1. User pastes license text
2. System analyzes and returns detection
3. User reviews confidence and ambiguity flags

### Scenario 2: Batch Compliance Check
1. Upload file with multiple fragments
2. System processes all fragments
3. Review results in grid view
4. Export report for compliance documentation

### Scenario 3: Triage Workflow
1. System flags ambiguous detections
2. Reviewer examines each case
3. Accept or reject detection
4. Decisions recorded for learning

### Scenario 4: Quality Evaluation
1. Load labeled test samples
2. Run evaluation metrics
3. Review precision/recall scores
4. Identify areas for improvement

## Limitations & Future Work

### Current Limitations
- Template-based only (no ML models)
- Limited license database (6 licenses)
- No context awareness
- Manual triage required
- No persistent storage

### Recommended Enhancements
1. **Expand License Database**: Add 20+ common licenses
2. **Machine Learning**: Train models on larger datasets
3. **Context Analysis**: Consider surrounding code
4. **Database Integration**: Store triage decisions
5. **Performance**: Optimize for large-scale processing
6. **Authentication**: Add user management
7. **API Versioning**: Support multiple API versions

## Deliverables Checklist

- ✅ Working feature/tool with simple UI
- ✅ Short README with setup instructions
- ✅ Sample data for testing
- ✅ Export functionality
- ✅ Evaluation metrics
- ⏳ 2-3 minute demo video (to be created)

## Testing

Run the test script to verify functionality:
```bash
python test_detector.py
```

Expected output: Detection results for sample license texts with confidence scores.

## Deployment

### Development
```bash
python app.py
```

### Production Considerations
- Use production WSGI server (gunicorn, uWSGI)
- Configure reverse proxy (nginx)
- Add environment variables for configuration
- Implement logging and monitoring
- Add rate limiting and authentication

## Project Status

**Status**: ✅ Complete - Ready for demo

All core features implemented and tested. The prototype demonstrates:
- Text similarity-based license detection
- Ambiguity flagging heuristics
- Triage workflow
- SPDX tagging
- Export capabilities
- Evaluation metrics

The tool is ready for demonstration and can be extended for production use.

