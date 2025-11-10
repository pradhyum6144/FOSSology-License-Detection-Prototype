"""
Simple test script to verify license detection functionality
"""

from license_detector import LicenseDetector

def test_detector():
    """Test the license detector with sample texts"""
    detector = LicenseDetector()
    
    test_cases = [
        {
            'text': 'Permission is hereby granted, free of charge, to any person obtaining a copy',
            'expected': 'MIT'
        },
        {
            'text': 'Licensed under the Apache License, Version 2.0',
            'expected': 'Apache-2.0'
        },
        {
            'text': 'This program is free software; you can redistribute it under the terms of the GNU General Public License',
            'expected': 'GPL'
        },
        {
            'text': 'Redistribution and use in source and binary forms are permitted',
            'expected': 'BSD'
        }
    ]
    
    print("Testing License Detector\n" + "="*50)
    
    for i, test in enumerate(test_cases, 1):
        result = detector.detect_license(test['text'])
        print(f"\nTest {i}:")
        print(f"  Input: {test['text'][:60]}...")
        print(f"  Detected: {result['detected_license']}")
        print(f"  Confidence: {result['confidence']:.2%}")
        print(f"  Ambiguous: {result['is_ambiguous']}")
        print(f"  SPDX ID: {result.get('spdx_id', 'N/A')}")
    
    print("\n" + "="*50)
    print("Test completed!")

if __name__ == '__main__':
    test_detector()

