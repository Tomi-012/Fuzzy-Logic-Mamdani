import pandas as pd
import numpy as np

class UMKMDataProcessor:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = None
        self.process_data()
    
    def process_data(self):
        """Process the UMKM credit data from CSV"""
        # Read CSV with proper handling
        self.data = pd.read_csv(self.csv_file, header=None, skiprows=2)
        
        # Extract relevant data
        self.business_fields = {}
        self.scales = {}
        self.usage_types = {}
        
        # Find the sections in the CSV
        lapangan_usaha_start = None
        jenis_penggunaan_start = None
        skala_usaha_start = None
        
        for idx, row in self.data.iterrows():
            if pd.notna(row[0]) and 'Lapangan Usaha' in str(row[0]):
                lapangan_usaha_start = idx + 1
            elif pd.notna(row[0]) and 'Jenis Penggunaan' in str(row[0]):
                jenis_penggunaan_start = idx + 1
            elif pd.notna(row[0]) and 'Skala Usaha' in str(row[0]):
                skala_usaha_start = idx + 1
        
        # Process business fields
        if lapangan_usaha_start:
            for idx in range(lapangan_usaha_start, len(self.data)):
                if pd.notna(self.data.iloc[idx, 0]) and pd.notna(self.data.iloc[idx, 1]):
                    field = self.data.iloc[idx, 0].strip('"')
                    amount = self.data.iloc[idx, 1]
                    if amount != '-' and pd.notna(amount):
                        self.business_fields[field] = int(amount)
                elif pd.notna(self.data.iloc[idx, 0]) and 'Jenis Penggunaan' in str(self.data.iloc[idx, 0]):
                    break
        
        # Process usage types
        if jenis_penggunaan_start:
            for idx in range(jenis_penggunaan_start, len(self.data)):
                if pd.notna(self.data.iloc[idx, 0]) and pd.notna(self.data.iloc[idx, 1]):
                    usage = self.data.iloc[idx, 0].strip()
                    amount = self.data.iloc[idx, 1]
                    if amount != '-' and pd.notna(amount):
                        self.usage_types[usage] = int(amount)
                elif pd.notna(self.data.iloc[idx, 0]) and 'Skala Usaha' in str(self.data.iloc[idx, 0]):
                    break
        
        # Process business scales
        if skala_usaha_start:
            for idx in range(skala_usaha_start, len(self.data)):
                if pd.notna(self.data.iloc[idx, 0]) and pd.notna(self.data.iloc[idx, 1]):
                    scale = self.data.iloc[idx, 0].strip()
                    amount = self.data.iloc[idx, 1]
                    if amount != '-' and pd.notna(amount):
                        self.scales[scale] = int(amount)
        
        # Calculate risk levels based on credit amounts
        self.calculate_risk_levels()
    
    def calculate_risk_levels(self):
        """Calculate risk levels for business fields"""
        total_credit = sum(self.business_fields.values())
        
        # Risk level: Lower credit amount = Higher risk (less established)
        # Higher credit amount = Lower risk (more established)
        self.risk_levels = {}
        
        for field, amount in self.business_fields.items():
            percentage = (amount / total_credit) * 100
            if percentage > 20:  # Very established
                risk = 0.2  # Low risk
            elif percentage > 10:  # Well established
                risk = 0.4  # Medium-low risk
            elif percentage > 5:  # Moderately established
                risk = 0.6  # Medium-high risk
            else:  # Less established
                risk = 0.8  # High risk
            
            self.risk_levels[field] = risk
    
    def get_business_field_risk(self, field):
        """Get risk level for a specific business field"""
        return self.risk_levels.get(field, 0.5)  # Default medium risk
    
    def get_scale_credit_range(self, scale):
        """Get credit range for business scale"""
        if scale == "Mikro":
            return (0, 500)  # 0-500 million
        elif scale == "Kecil":
            return (500, 5000)  # 500 million - 5 billion
        elif scale == "Menengah":
            return (5000, 50000)  # 5 billion - 50 billion
        else:
            return (0, 100)  # Default range
    
    def get_usage_priority(self, usage_type):
        """Get approval priority for usage type"""
        if usage_type == "Modal Kerja":
            return 0.7  # Higher priority (working capital)
        elif usage_type == "Investasi":
            return 0.5  # Medium priority (investment)
        else:
            return 0.3  # Lower priority
    
    def get_all_business_fields(self):
        """Get list of all business fields"""
        return list(self.business_fields.keys())
    
    def get_all_scales(self):
        """Get list of all business scales"""
        return list(self.scales.keys())
    
    def get_all_usage_types(self):
        """Get list of all usage types"""
        return list(self.usage_types.keys())
