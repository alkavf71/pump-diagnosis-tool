"""Konfigurasi aplikasi & constants"""
import os

# App metadata
APP_TITLE = "Pump Diagnosis Tool - Pertamina Patra Niaga"
APP_VERSION = "1.0.0"
COMPANY_NAME = "PT Pertamina Patra Niaga"

# ISO 10816-3 Limits (mm/s RMS) - Class III Machines
ISO_LIMITS = {
    "rigid": {
        "zone_a_max": 2.8,
        "zone_b_max": 4.5,
        "zone_c_max": 7.1,
        "zone_d_min": 7.1
    },
    "flexible": {
        "zone_a_max": 4.5,
        "zone_b_max": 7.1,
        "zone_c_max": 11.2,
        "zone_d_min": 11.2
    }
}

# Product properties
PRODUCT_PROPERTIES = {
    "Gasoline": {"density": 740, "default_temp": 30, "risk_factor": 5},
    "Diesel": {"density": 840, "default_temp": 25, "risk_factor": 3},
    "Avtur": {"density": 780, "default_temp": 28, "risk_factor": 4},
    "Naphtha": {"density": 700, "default_temp": 32, "risk_factor": 5}
}

# Pump size class defaults
PUMP_SIZE_DEFAULTS = {
    "Small": {"npshr": 3.0, "bep_flow": 30, "fla": 15},
    "Medium": {"npshr": 4.5, "bep_flow": 100, "fla": 30},
    "Large": {"npshr": 6.0, "bep_flow": 250, "fla": 60}
}

# Fault mapping per direction
FAULT_MAPPING = {
    "H": "Unbalance",
    "V": "Mechanical Looseness / Foundation Issue",
    "A": "Misalignment / Coupling Issue"
}

# Priority order for diagnosis
DIAGNOSIS_PRIORITY = [
    "HYDRAULIC",      # Cavitation/Recirculation
    "ELECTRICAL",     # Imbalance/Overload
    "MECHANICAL",     # Misalignment/Unbalance
    "THERMAL"         # Overheat
]

# Path configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(os.path.dirname(BASE_DIR), "assets")
