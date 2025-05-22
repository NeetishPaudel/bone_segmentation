FEMUR AND TIBIA SEGMENTATION, EXPANSION, AND ANATOMICAL LANDMARK EXTRACTION FROM 3D CT IMAGES

This repository contains a reproducible pipeline for segmenting the femur and tibia from 3D CT scans, applying morphological expansions, and extracting key anatomical landmarks. The pipeline is designed for use in biomechanical modeling, orthopedic planning, and medical research.

---

PROJECT OBJECTIVES

- Segment femur and tibia masks from labeled CT volumes.
- Perform fixed and randomized morphological expansions of bone masks.
- Extract anatomical landmarks: medial and lateral lowest tibial surface points.
- Provide reusable and extensible code with preserved spatial accuracy.

---

Bone Segmentation Project/
│
├── code/                          # Core logic and execution scripts
│   ├── config.py
│   ├── main.py
│
├── utils/                         # Utility functions
│   ├── __init__.py
│   ├── io_utils.py
│   ├── mask_utils.py
│   └── processing_utils.py
│
├── Data/                          # Input CT volume
│
├── Results/
│   ├── Output Images/             # Visual outputs for expanded masks, landmarks, etc.
│   ├── Femur_tibia_segmentation_report/   # Saved report documents (e.g., .docx or .pdf)
│   └── Medial and Lateral lowest points/  # Extracted anatomical landmark data
│
├── README.txt                     # Project overview and usage instructions
└── Requirements.txt               # List of Python dependencies

---

INSTALLATION

1. Clone the repository:
   git clone https://github.com/your-username/femur-tibia-segmentation.git
   cd femur-tibia-segmentation

2. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate  (On Windows: venv\\Scripts\\activate)

3. Install dependencies:
   pip install -r requirements.txt


## 📊 Results

- Accurate binary masks for femur and tibia.
- Fixed dilation masks (2mm and 4mm).
- Realistic randomized expansions simulating biological variability.
- Medial/lateral lowest tibial points extracted with spatial fidelity.


