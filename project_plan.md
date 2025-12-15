# Fuzzy Logic UMKM Credit Evaluation Project

## Project Overview
Create a professional fuzzy logic system to evaluate UMKM credit eligibility using the Mamdani method with an elegant web interface.

## Data Analysis
Based on the CSV data, we have:
- Total UMKM Credit: 1,457,132 Billion Rupiah
- Business Fields: 17 categories (Pertanian, Perdagangan, Industri, etc.)
- Usage Types: Modal Kerja (1,053,972), Investasi (403,160)
- Business Scales: Mikro (662,293), Kecil (460,773), Menengah (334,066)

## Fuzzy Logic Variables
### Input Variables:
1. **Business Scale** (Mikro, Kecil, Menengah) → Credit Amount Range
2. **Business Field** (17 categories) → Risk Level
3. **Usage Type** (Modal Kerja, Investasi) → Approval Priority

### Output Variable:
- **Credit Approval Score** (0-100)

## Project Structure
```
KB_Tugas/
├── app.py                 # Flask web application
├── fuzzy_logic.py         # Mamdani fuzzy logic implementation
├── data_processor.py      # CSV data processing
├── static/
│   ├── css/
│   │   └── style.css      # Modern, clean CSS with animations
│   ├── js/
│   │   └── main.js        # Interactive JavaScript
│   └── assets/
├── templates/
│   ├── index.html         # Main interface
│   └── result.html        # Results display
├── requirements.txt       # Python dependencies
└── Posisi Kredit Usaha Mikro, Kecil, dan Menengah (UMKM) pada Bank Umum__, 2023.csv
```

## Implementation Steps
- [ ] Set up project structure and dependencies
- [ ] Process and analyze UMKM credit data
- [ ] Implement Mamdani fuzzy logic system
- [ ] Create Flask web application backend
- [ ] Design professional frontend with modern UI
- [ ] Add smooth animations and interactions
- [ ] Test the complete system
- [ ] Finalize documentation

## Technology Stack
- **Backend**: Python, Flask, scikit-fuzzy
- **Frontend**: HTML5, CSS3, JavaScript (modern design)
- **Styling**: Clean, minimalist approach with subtle animations
- **Data Processing**: Pandas for CSV handling

## Design Principles
- Clean and minimalist interface
- Professional color scheme (blues, grays, whites)
- Smooth CSS transitions and animations
- Responsive design
- No excessive icons or decorations
- Elegant typography
