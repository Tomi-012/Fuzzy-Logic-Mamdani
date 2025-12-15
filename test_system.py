#!/usr/bin/env python3
"""
Test script for UMKM Fuzzy Logic System
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_processor import UMKMDataProcessor
from fuzzy_logic import UMKMFuzzyLogic

def test_data_processor():
    """Test data processor functionality"""
    print("=" * 50)
    print("Testing Data Processor")
    print("=" * 50)
    
    try:
        processor = UMKMDataProcessor('Posisi Kredit Usaha Mikro, Kecil, dan Menengah (UMKM) pada Bank Umum__, 2023.csv')
        
        print(f"✓ Business fields loaded: {len(processor.business_fields)}")
        print(f"✓ Scales loaded: {len(processor.scales)}")
        print(f"✓ Usage types loaded: {len(processor.usage_types)}")
        
        # Test sample data
        print(f"\nSample business fields:")
        for i, (field, amount) in enumerate(list(processor.business_fields.items())[:3]):
            print(f"  {i+1}. {field}: {amount:,} Miliar")
        
        print(f"\nScales:")
        for scale, amount in processor.scales.items():
            print(f"  - {scale}: {amount:,} Miliar")
        
        print(f"\nUsage types:")
        for usage, amount in processor.usage_types.items():
            print(f"  - {usage}: {amount:,} Miliar")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in data processor: {str(e)}")
        return False

def test_fuzzy_logic():
    """Test fuzzy logic functionality"""
    print("\n" + "=" * 50)
    print("Testing Fuzzy Logic System")
    print("=" * 50)
    
    try:
        fuzzy = UMKMFuzzyLogic()
        print("✓ Fuzzy system initialized successfully")
        
        # Test sample calculation
        scale_value = fuzzy.scale_to_fuzzy_value("Kecil")
        risk_value = fuzzy.risk_to_fuzzy_value(0.5)
        priority_value = fuzzy.priority_to_fuzzy_value(0.7)
        
        print(f"\nTest inputs:")
        print(f"  Scale (Kecil): {scale_value}")
        print(f"  Risk (0.5): {risk_value}")
        print(f"  Priority (0.7): {priority_value}")
        
        approval_score = fuzzy.calculate_approval_score(scale_value, risk_value, priority_value)
        category, color = fuzzy.get_approval_category(approval_score)
        recommendations = fuzzy.get_recommendations(approval_score, scale_value, risk_value, priority_value)
        
        print(f"\nResults:")
        print(f"  Approval Score: {approval_score:.2f}")
        print(f"  Category: {category}")
        print(f"  Color: {color}")
        print(f"  Recommendations: {len(recommendations)} items")
        
        # Test visualization generation
        try:
            viz = fuzzy.generate_fuzzy_visualization(scale_value, risk_value, priority_value, approval_score)
            print(f"  Visualization: ✓ Generated ({len(viz)} characters)")
        except Exception as e:
            print(f"  Visualization: ✗ Failed - {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in fuzzy logic: {str(e)}")
        return False

def test_integration():
    """Test integration between components"""
    print("\n" + "=" * 50)
    print("Testing System Integration")
    print("=" * 50)
    
    try:
        # Initialize components
        processor = UMKMDataProcessor('Posisi Kredit Usaha Mikro, Kecil, dan Menengah (UMKM) pada Bank Umum__, 2023.csv')
        fuzzy = UMKMFuzzyLogic()
        
        # Test sample evaluation
        business_field = "Perdagangan Besar dan Eceran"
        scale = "Kecil"
        usage_type = "Modal Kerja"
        
        print(f"Test evaluation:")
        print(f"  Business Field: {business_field}")
        print(f"  Scale: {scale}")
        print(f"  Usage Type: {usage_type}")
        
        # Get values
        scale_value = fuzzy.scale_to_fuzzy_value(scale)
        risk_value = fuzzy.risk_to_fuzzy_value(processor.get_business_field_risk(business_field))
        priority_value = fuzzy.priority_to_fuzzy_value(processor.get_usage_priority(usage_type))
        
        # Calculate
        approval_score = fuzzy.calculate_approval_score(scale_value, risk_value, priority_value)
        category, color = fuzzy.get_approval_category(approval_score)
        
        print(f"\nIntegration Results:")
        print(f"  Scale Value: {scale_value:.2f}")
        print(f"  Risk Value: {risk_value:.2f}")
        print(f"  Priority Value: {priority_value:.2f}")
        print(f"  Approval Score: {approval_score:.2f}")
        print(f"  Category: {category}")
        
        return True
        
    except Exception as e:
        print(f"✗ Integration error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("UMKM Fuzzy Logic System - Test Suite")
    print("=" * 50)
    
    results = []
    results.append(test_data_processor())
    results.append(test_fuzzy_logic())
    results.append(test_integration())
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! System is working correctly.")
        return 0
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())