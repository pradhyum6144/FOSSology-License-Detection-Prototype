# Quick Start Guide

## Installation (5 minutes)

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify installation:**
   ```bash
   python test_detector.py
   ```

## Running the Application

1. **Start the server:**
   ```bash
   python app.py
   ```

2. **Open browser:**
   Navigate to `http://localhost:5000`

## Quick Test

1. Go to "Analyze Text" tab
2. Paste this text:
   ```
   Permission is hereby granted, free of charge, to any person obtaining a copy of this software
   ```
3. Click "Analyze License"
4. Should detect: **MIT License** with high confidence

## Sample Workflow

1. **Batch Analysis:**
   - Go to "Batch Analysis" tab
   - Click "Load Sample Data"
   - Review results

2. **Triage Review:**
   - Go to "Triage View" tab
   - Review ambiguous detections
   - Accept or reject each one

3. **Export:**
   - After batch analysis, use export buttons
   - Try JSON, CSV, and SPDX formats

4. **Evaluate:**
   - Go to "Evaluate" tab
   - Click "Run Evaluation"
   - View precision/recall metrics

## Troubleshooting

- **Port already in use?** Change port in `app.py` (line 126)
- **Module not found?** Make sure you're in the project directory and dependencies are installed
- **Data files missing?** Check that `data/` directory contains JSON files

## Next Steps

See `README.md` for full documentation and advanced usage.

