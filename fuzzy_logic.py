import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

class UMKMFuzzyLogic:
    def __init__(self):
        self.setup_fuzzy_variables()
        self.setup_rules()
        self.setup_control_system()
    
    def setup_fuzzy_variables(self):
        """Setup fuzzy variables for Mamdani inference"""
        
        # Input variables
        # Business Scale (0-100 points, where higher = larger scale)
        self.business_scale = ctrl.Antecedent(np.arange(0, 101, 1), 'business_scale')
        self.business_scale['mikro'] = fuzz.trimf(self.business_scale.universe, [0, 0, 40])
        self.business_scale['kecil'] = fuzz.trimf(self.business_scale.universe, [20, 50, 80])
        self.business_scale['menengah'] = fuzz.trimf(self.business_scale.universe, [60, 100, 100])
        
        # Risk Level (0-100, where higher = higher risk)
        self.risk_level = ctrl.Antecedent(np.arange(0, 101, 1), 'risk_level')
        self.risk_level['rendah'] = fuzz.trimf(self.risk_level.universe, [0, 0, 40])
        self.risk_level['sedang'] = fuzz.trimf(self.risk_level.universe, [20, 50, 80])
        self.risk_level['tinggi'] = fuzz.trimf(self.risk_level.universe, [60, 100, 100])
        
        # Usage Priority (0-100, where higher = higher priority)
        self.usage_priority = ctrl.Antecedent(np.arange(0, 101, 1), 'usage_priority')
        self.usage_priority['rendah'] = fuzz.trimf(self.usage_priority.universe, [0, 0, 40])
        self.usage_priority['sedang'] = fuzz.trimf(self.usage_priority.universe, [20, 50, 80])
        self.usage_priority['tinggi'] = fuzz.trimf(self.usage_priority.universe, [60, 100, 100])
        
        # Output variable: Credit Approval Score (0-100)
        self.approval_score = ctrl.Consequent(np.arange(0, 101, 1), 'approval_score')
        self.approval_score['sangat_rendah'] = fuzz.trimf(self.approval_score.universe, [0, 0, 20])
        self.approval_score['rendah'] = fuzz.trimf(self.approval_score.universe, [10, 30, 50])
        self.approval_score['sedang'] = fuzz.trimf(self.approval_score.universe, [40, 60, 80])
        self.approval_score['tinggi'] = fuzz.trimf(self.approval_score.universe, [70, 90, 100])
        self.approval_score['sangat_tinggi'] = fuzz.trimf(self.approval_score.universe, [90, 100, 100])
    
    def setup_rules(self):
        """Setup fuzzy rules for Mamdani inference"""
        
        rules = [
            # Rules for high approval
            ctrl.Rule(self.business_scale['menengah'] & self.risk_level['rendah'] & self.usage_priority['tinggi'], 
                     self.approval_score['sangat_tinggi']),
            ctrl.Rule(self.business_scale['menengah'] & self.risk_level['rendah'] & self.usage_priority['sedang'], 
                     self.approval_score['tinggi']),
            ctrl.Rule(self.business_scale['kecil'] & self.risk_level['rendah'] & self.usage_priority['tinggi'], 
                     self.approval_score['tinggi']),
            
            # Rules for medium-high approval
            ctrl.Rule(self.business_scale['menengah'] & self.risk_level['sedang'] & self.usage_priority['tinggi'], 
                     self.approval_score['tinggi']),
            ctrl.Rule(self.business_scale['kecil'] & self.risk_level['rendah'] & self.usage_priority['sedang'], 
                     self.approval_score['sedang']),
            ctrl.Rule(self.business_scale['menengah'] & self.risk_level['rendah'] & self.usage_priority['rendah'], 
                     self.approval_score['sedang']),
            
            # Rules for medium approval
            ctrl.Rule(self.business_scale['kecil'] & self.risk_level['sedang'] & self.usage_priority['sedang'], 
                     self.approval_score['sedang']),
            ctrl.Rule(self.business_scale['mikro'] & self.risk_level['rendah'] & self.usage_priority['tinggi'], 
                     self.approval_score['sedang']),
            ctrl.Rule(self.business_scale['kecil'] & self.risk_level['tinggi'] & self.usage_priority['tinggi'], 
                     self.approval_score['sedang']),
            
            # Rules for medium-low approval
            ctrl.Rule(self.business_scale['kecil'] & self.risk_level['sedang'] & self.usage_priority['rendah'], 
                     self.approval_score['rendah']),
            ctrl.Rule(self.business_scale['mikro'] & self.risk_level['sedang'] & self.usage_priority['sedang'], 
                     self.approval_score['rendah']),
            ctrl.Rule(self.business_scale['kecil'] & self.risk_level['tinggi'] & self.usage_priority['sedang'], 
                     self.approval_score['rendah']),
            
            # Rules for low approval
            ctrl.Rule(self.business_scale['mikro'] & self.risk_level['tinggi'] & self.usage_priority['rendah'], 
                     self.approval_score['sangat_rendah']),
            ctrl.Rule(self.business_scale['mikro'] & self.risk_level['tinggi'] & self.usage_priority['sedang'], 
                     self.approval_score['rendah']),
            ctrl.Rule(self.business_scale['mikro'] & self.risk_level['sedang'] & self.usage_priority['rendah'], 
                     self.approval_score['rendah']),
        ]
        
        self.rules = rules
    
    def setup_control_system(self):
        """Setup the control system"""
        self.approval_system = ctrl.ControlSystem(self.rules)
        self.approval_simulation = ctrl.ControlSystemSimulation(self.approval_system)
    
    def calculate_approval_score(self, scale_value, risk_value, priority_value):
        """Calculate approval score using Mamdani inference"""
        
        # Reset the simulation
        self.approval_simulation.reset()
        
        # Set input values
        self.approval_simulation.input['business_scale'] = scale_value
        self.approval_simulation.input['risk_level'] = risk_value
        self.approval_simulation.input['usage_priority'] = priority_value
        
        # Compute the result
        self.approval_simulation.compute()
        
        # Get the approval score
        approval_score = self.approval_simulation.output['approval_score']
        
        return approval_score
    
    def get_approval_category(self, score):
        """Get approval category based on score"""
        if score >= 80:
            return "Sangat Disetujui", "#10b981"  # Green
        elif score >= 60:
            return "Disetujui", "#3b82f6"  # Blue
        elif score >= 40:
            return "Pertimbangan", "#f59e0b"  # Orange
        elif score >= 20:
            return "Ditolak Rendah", "#ef4444"  # Red
        else:
            return "Ditolak", "#dc2626"  # Dark Red
    
    def get_recommendations(self, score, scale, risk, priority):
        """Get recommendations based on fuzzy logic results"""
        recommendations = []
        
        if score < 40:
            if risk > 70:
                recommendations.append("Pertimbangkan untuk mengurangi risiko dengan jaminan tambahan")
            if scale < 33:
                recommendations.append("Usahakan untuk meningkatkan skala usaha")
            if priority < 50:
                recommendations.append("Fokus pada penggunaan modal kerja untuk peluang lebih baik")
        
        elif score < 60:
            if risk > 50:
                recommendations.append("Tinjau ulang rencana bisnis untuk mengurangi risiko")
            if priority < 70:
                recommendations.append("Pertimbangkan untuk mengalokasikan dana ke modal kerja")
        
        else:
            recommendations.append("Aplikasi kredit memiliki prospek yang baik")
            if scale > 67:
                recommendations.append("Pertimbangkan untuk meningkatkan jumlah kredit")
        
        return recommendations
    
    def scale_to_fuzzy_value(self, scale):
        """Convert business scale to fuzzy value (0-100)"""
        scale_mapping = {
            "Mikro": 16.5,  # Middle of mikro range
            "Kecil": 50,    # Middle of kecil range  
            "Menengah": 83.5 # Middle of menengah range
        }
        return scale_mapping.get(scale, 50)
    
    def risk_to_fuzzy_value(self, risk_level):
        """Convert risk level (0-1) to fuzzy value (0-100)"""
        return risk_level * 100
    
    def priority_to_fuzzy_value(self, priority):
        """Convert priority (0-1) to fuzzy value (0-100)"""
        return priority * 100
    
    def generate_fuzzy_visualization(self, scale_value, risk_value, priority_value, approval_score):
        """Generate fuzzy logic visualization as base64 image"""
        # Set matplotlib to use non-interactive backend
        plt.switch_backend('Agg')
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Visualisasi Logika Fuzzy - Evaluasi Kredit UMKM', fontsize=16, fontweight='bold', color='black')
        fig.patch.set_facecolor('#ffffff')
        
        # Plot 1: Business Scale
        ax1 = axes[0, 0]
        ax1.set_facecolor('#ffffff')
        ax1.plot(self.business_scale.universe, self.business_scale['mikro'].mf, 'b', linewidth=2, label='Mikro')
        ax1.plot(self.business_scale.universe, self.business_scale['kecil'].mf, 'g', linewidth=2, label='Kecil')
        ax1.plot(self.business_scale.universe, self.business_scale['menengah'].mf, 'r', linewidth=2, label='Menengah')
        ax1.axvline(x=scale_value, color='black', linestyle='--', alpha=0.7, label=f'Input: {scale_value:.1f}')
        ax1.set_title('Variabel Input: Skala Usaha')
        ax1.set_xlabel('Nilai Skala (0-100)')
        ax1.set_ylabel('Derajat Keanggotaan')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim([0, 1.1])
        
        # Plot 2: Risk Level
        ax2 = axes[0, 1]
        ax2.set_facecolor('#ffffff')
        ax2.plot(self.risk_level.universe, self.risk_level['rendah'].mf, 'b', linewidth=2, label='Rendah')
        ax2.plot(self.risk_level.universe, self.risk_level['sedang'].mf, 'g', linewidth=2, label='Sedang')
        ax2.plot(self.risk_level.universe, self.risk_level['tinggi'].mf, 'r', linewidth=2, label='Tinggi')
        ax2.axvline(x=risk_value, color='black', linestyle='--', alpha=0.7, label=f'Input: {risk_value:.1f}')
        ax2.set_title('Variabel Input: Tingkat Risiko')
        ax2.set_xlabel('Nilai Risiko (0-100)')
        ax2.set_ylabel('Derajat Keanggotaan')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim([0, 1.1])
        
        # Plot 3: Usage Priority
        ax3 = axes[1, 0]
        ax3.set_facecolor('#ffffff')
        ax3.plot(self.usage_priority.universe, self.usage_priority['rendah'].mf, 'b', linewidth=2, label='Rendah')
        ax3.plot(self.usage_priority.universe, self.usage_priority['sedang'].mf, 'g', linewidth=2, label='Sedang')
        ax3.plot(self.usage_priority.universe, self.usage_priority['tinggi'].mf, 'r', linewidth=2, label='Tinggi')
        ax3.axvline(x=priority_value, color='black', linestyle='--', alpha=0.7, label=f'Input: {priority_value:.1f}')
        ax3.set_title('Variabel Input: Prioritas Penggunaan')
        ax3.set_xlabel('Nilai Prioritas (0-100)')
        ax3.set_ylabel('Derajat Keanggotaan')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.set_ylim([0, 1.1])
        
        # Plot 4: Approval Score Output
        ax4 = axes[1, 1]
        ax4.set_facecolor('#ffffff')
        ax4.plot(self.approval_score.universe, self.approval_score['sangat_rendah'].mf, 'darkred', linewidth=2, label='Sangat Rendah')
        ax4.plot(self.approval_score.universe, self.approval_score['rendah'].mf, 'red', linewidth=2, label='Rendah')
        ax4.plot(self.approval_score.universe, self.approval_score['sedang'].mf, 'orange', linewidth=2, label='Sedang')
        ax4.plot(self.approval_score.universe, self.approval_score['tinggi'].mf, 'lightgreen', linewidth=2, label='Tinggi')
        ax4.plot(self.approval_score.universe, self.approval_score['sangat_tinggi'].mf, 'green', linewidth=2, label='Sangat Tinggi')
        ax4.axvline(x=approval_score, color='black', linestyle='--', alpha=0.7, label=f'Output: {approval_score:.1f}')
        ax4.set_title('Variabel Output: Skor Persetujuan')
        ax4.set_xlabel('Skor Persetujuan (0-100)')
        ax4.set_ylabel('Derajat Keanggotaan')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        ax4.set_ylim([0, 1.1])
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def get_detailed_analysis(self, scale_value, risk_value, priority_value, approval_score):
        """Get detailed analysis of fuzzy logic results"""
        analysis = {
            'input_analysis': {},
            'rule_activation': [],
            'recommendations': []
        }
        
        # Analyze input values
        analysis['input_analysis']['scale'] = self._analyze_fuzzy_input(scale_value, self.business_scale)
        analysis['input_analysis']['risk'] = self._analyze_fuzzy_input(risk_value, self.risk_level)
        analysis['input_analysis']['priority'] = self._analyze_fuzzy_input(priority_value, self.usage_priority)
        
        # Analyze output
        analysis['output_analysis'] = self._analyze_fuzzy_input(approval_score, self.approval_score)
        
        # Generate rule activation analysis
        for i, rule in enumerate(self.rules):
            # This is a simplified version - in practice you'd need to analyze rule activation
            analysis['rule_activation'].append({
                'rule_id': i + 1,
                'description': f"Rule {i+1} activation",
                'strength': 0.0  # Would need actual computation
            })
        
        return analysis
    
    def _analyze_fuzzy_input(self, value, variable):
        """Analyze fuzzy input and return membership degrees"""
        memberships = {}
        for term in variable.terms:
            memberships[term] = fuzz.interp_membership(variable.universe, variable[term].mf, value)
        return memberships
