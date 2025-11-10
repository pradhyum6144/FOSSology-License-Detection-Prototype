"""
License Detection Engine using Text Similarity Heuristics
Uses difflib and regex for text matching
"""

import difflib
import re
import json
import csv
import io
from typing import Dict, List, Tuple, Optional

class LicenseDetector:
    """Detects licenses using text similarity heuristics"""
    
    def __init__(self, license_db_path: str = 'data/license_templates.json'):
        """Initialize with license templates database"""
        self.license_templates = self._load_license_templates(license_db_path)
        self.ambiguous_threshold = 0.6  # Similarity threshold for flagging ambiguity
        self.confidence_threshold = 0.8  # Minimum confidence for positive detection
    
    def _load_license_templates(self, path: str) -> Dict:
        """Load license templates from JSON file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default templates if file doesn't exist
            return self._get_default_templates()
    
    def _get_default_templates(self) -> Dict:
        """Default license templates for common licenses"""
        return {
            'MIT': {
                'name': 'MIT License',
                'spdx_id': 'MIT',
                'keywords': ['MIT', 'Massachusetts Institute of Technology', 'Permission is hereby granted'],
                'template': 'Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files'
            },
            'Apache-2.0': {
                'name': 'Apache License 2.0',
                'spdx_id': 'Apache-2.0',
                'keywords': ['Apache', 'Apache License', 'Version 2.0', 'Licensed under the Apache License'],
                'template': 'Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License'
            },
            'GPL-2.0': {
                'name': 'GNU General Public License v2.0',
                'spdx_id': 'GPL-2.0',
                'keywords': ['GPL', 'GNU General Public License', 'Version 2', 'This program is free software'],
                'template': 'This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License'
            },
            'GPL-3.0': {
                'name': 'GNU General Public License v3.0',
                'spdx_id': 'GPL-3.0',
                'keywords': ['GPL', 'GNU General Public License', 'Version 3', 'This program is free software'],
                'template': 'This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation'
            },
            'BSD-3-Clause': {
                'name': 'BSD 3-Clause License',
                'spdx_id': 'BSD-3-Clause',
                'keywords': ['BSD', '3-Clause', 'Redistribution and use in source and binary forms'],
                'template': 'Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met'
            },
            'LGPL-2.1': {
                'name': 'GNU Lesser General Public License v2.1',
                'spdx_id': 'LGPL-2.1',
                'keywords': ['LGPL', 'Lesser General Public License', 'Version 2.1'],
                'template': 'This library is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License'
            }
        }
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison"""
        # Remove extra whitespace, convert to lowercase
        text = re.sub(r'\s+', ' ', text.strip().lower())
        # Remove common punctuation variations
        text = re.sub(r'[^\w\s]', '', text)
        return text
    
    def _compute_similarity(self, text1: str, text2: str) -> float:
        """Compute text similarity using difflib"""
        normalized1 = self._normalize_text(text1)
        normalized2 = self._normalize_text(text2)
        
        # Use SequenceMatcher for similarity
        similarity = difflib.SequenceMatcher(None, normalized1, normalized2).ratio()
        return similarity
    
    def _keyword_match(self, text: str, keywords: List[str]) -> float:
        """Check keyword presence in text"""
        text_lower = text.lower()
        matches = sum(1 for keyword in keywords if keyword.lower() in text_lower)
        return matches / len(keywords) if keywords else 1
    
    def detect_license(self, text: str) -> Dict:
        """
        Detect license from text fragment
        
        Returns:
            Dictionary with detection results including:
            - detected_license: Best match license name
            - confidence: Confidence score (0-1)
            - is_ambiguous: Boolean flag for ambiguous fragments
            - matches: List of all potential matches with scores
            - spdx_id: SPDX identifier if detected
        """
        if not text or len(text.strip()) < 10:
            return {
                'detected_license': 'Unknown',
                'confidence': 0.0,
                'is_ambiguous': True,
                'matches': [],
                'spdx_id': None,
                'reason': 'Text too short'
            }
        
        matches = []
        
        # Check against each license template
        for license_id, license_info in self.license_templates.items():
            template = license_info.get('template', '')
            keywords = license_info.get('keywords', [])
            
            # Compute similarity with template
            template_similarity = self._compute_similarity(text, template)
            
            # Compute keyword match score
            keyword_score = self._keyword_match(text, keywords)
            
            # Combined score (weighted average)
            combined_score = (template_similarity * 0.7) + (keyword_score * 0.3)
            
            matches.append({
                'license_id': license_id,
                'license_name': license_info.get('name', license_id),
                'spdx_id': license_info.get('spdx_id', license_id),
                'similarity': template_similarity,
                'keyword_score': keyword_score,
                'combined_score': combined_score
            })
        
        # Sort by combined score
        matches.sort(key=lambda x: x['combined_score'], reverse=True)
        
        # Get best match
        best_match = matches[0] if matches else None
        
        if not best_match:
            return {
                'detected_license': 'Unknown',
                'confidence': 0.0,
                'is_ambiguous': True,
                'matches': [],
                'spdx_id': None
            }
        
        confidence = best_match['combined_score']
        detected_license = best_match['license_name']
        spdx_id = best_match['spdx_id']
        
        # Flag as ambiguous if:
        # 1. Confidence is below threshold
        # 2. Multiple licenses have similar scores (top 2 within 0.15)
        is_ambiguous = False
        if confidence < self.confidence_threshold:
            is_ambiguous = True
        elif len(matches) > 1:
            top_score = matches[0]['combined_score']
            second_score = matches[1]['combined_score']
            if top_score - second_score < 0.15:
                is_ambiguous = True
        
        return {
            'detected_license': detected_license,
            'confidence': round(confidence, 3),
            'is_ambiguous': is_ambiguous,
            'matches': matches[:5],  # Top 5 matches
            'spdx_id': spdx_id,
            'license_id': best_match['license_id']
        }
    
    def evaluate_samples(self, samples: List[Dict]) -> Dict:
        """
        Evaluate precision/recall on labeled samples
        
        Args:
            samples: List of dicts with 'text' and 'expected_license' keys
        
        Returns:
            Dictionary with precision, recall, and accuracy metrics
        """
        if not samples:
            return {'error': 'No samples provided'}
        
        true_positives = 0
        false_positives = 0
        false_negatives = 0
        correct = 0
        total = len(samples)
        
        for sample in samples:
            text = sample.get('text', '')
            expected = sample.get('expected_license', '').strip()
            
            result = self.detect_license(text)
            detected = result.get('detected_license', 'Unknown')
            
            # Normalize for comparison
            expected_normalized = expected.lower()
            detected_normalized = detected.lower()
            
            if expected_normalized in detected_normalized or detected_normalized in expected_normalized:
                correct += 1
                true_positives += 1
            else:
                if detected != 'Unknown':
                    false_positives += 1
                if expected:
                    false_negatives += 1
        
        accuracy = correct / total if total > 0 else 0
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            'accuracy': round(accuracy, 3),
            'precision': round(precision, 3),
            'recall': round(recall, 3),
            'f1_score': round(f1_score, 3),
            'total_samples': total,
            'correct': correct,
            'true_positives': true_positives,
            'false_positives': false_positives,
            'false_negatives': false_negatives
        }
    
    def export_to_csv(self, results: List[Dict]) -> str:
        """Export results to CSV format"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['ID', 'Detected License', 'SPDX ID', 'Confidence', 'Is Ambiguous', 'Original Text'])
        
        # Write data
        for result in results:
            writer.writerow([
                result.get('id', ''),
                result.get('detected_license', 'Unknown'),
                result.get('spdx_id', ''),
                result.get('confidence', 0),
                result.get('is_ambiguous', False),
                result.get('original_text', '')[:100]  # Truncate long text
            ])
        
        return output.getvalue()

