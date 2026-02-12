"""Modul untuk analisis data hidraulis (NPSHa, BEP, dll)"""
from typing import Dict
from src.utils.calculations import (
    calculate_npsha,
    calculate_differential_head,
    calculate_flow_ratio
)
from src.config import PUMP_SIZE_DEFAULTS, PRODUCT_PROPERTIES


def analyze_hydraulic_conditions(
    suction_pressure: float,
    discharge_pressure: float,
    flow_rate: float,
    product_type: str,
    pump_size: str,
    temperature: float = None
) -> Dict:
    """
    Analisis kondisi hidraulis pompa
    
    Args:
        suction_pressure: Tekanan suction (kPa)
        discharge_pressure: Tekanan discharge (kPa)
        flow_rate: Laju alir (m³/h)
        product_type: Jenis produk
        pump_size: Ukuran pompa (Small/Medium/Large)
        temperature: Suhu produk (°C), optional
        
    Returns:
        Dict dengan hasil analisis hidraulis
    """
    # Get pump defaults
    npshr = PUMP_SIZE_DEFAULTS[pump_size]["npshr"]
    bep_flow = PUMP_SIZE_DEFAULTS[pump_size]["bep_flow"]
    
    # Calculate NPSHa
    npsha = calculate_npsha(suction_pressure, product_type, temperature)
    
    # Calculate differential head
    head = calculate_differential_head(discharge_pressure, suction_pressure, product_type)
    
    # Calculate flow ratio
    flow_ratio, flow_status = calculate_flow_ratio(flow_rate, pump_size)
    
    # Assess cavitation risk
    safety_margin = 1.0  # meter (API 610 recommendation)
    npsha_margin = npsha - (npshr + safety_margin)
    
    if npsha_margin < 0:
        cavitation_risk = "HIGH"
        cavitation_status = "⚠️ CRITICAL: NPSHa < NPSHr + safety margin"
    elif npsha_margin < 1.0:
        cavitation_risk = "MEDIUM"
        cavitation_status = "⚠️ WARNING: Low NPSHa margin"
    else:
        cavitation_risk = "LOW"
        cavitation_status = "✅ NPSHa adequate"
    
    # Assess flow condition
    if flow_status == "RECIRCULATION_RISK":
        flow_recommendation = "⚠️ Flow < 60% BEP - risk of recirculation & vibration"
    elif flow_status == "OVERLOAD_CAVITATION_RISK":
        flow_recommendation = "⚠️ Flow > 120% BEP - risk of cavitation & overload"
    else:
        flow_recommendation = "✅ Flow within acceptable range"
    
    return {
        "npsha": npsha,
        "npshr": npshr,
        "npsha_margin": round(npsha_margin, 2),
        "cavitation_risk": cavitation_risk,
        "cavitation_status": cavitation_status,
        "head": head,
        "flow_rate": flow_rate,
        "bep_flow": bep_flow,
        "flow_ratio": flow_ratio,
        "flow_status": flow_status,
        "flow_recommendation": flow_recommendation,
        "has_issue": cavitation_risk != "LOW" or flow_status != "NORMAL"
    }


def generate_hydraulic_report(
    operational_data: Dict,
    spec_data: Dict
) -> Dict:
    """
    Generate laporan analisis hidraulis
    
    Args:
        operational_data: Dict dengan suction_pressure, discharge_pressure, flow_rate
        spec_data: Dict dengan product_type, pump_size
        
    Returns:
        Dict dengan laporan hidraulis lengkap
    """
    suction = operational_data.get("suction_pressure", 0.0)
    discharge = operational_data.get("discharge_pressure", 0.0)
    flow = operational_data.get("flow_rate", 0.0)
    
    product = spec_data.get("product_type", "Diesel")
    pump_size = spec_data.get("pump_size", "Medium")
    
    analysis = analyze_hydraulic_conditions(
        suction_pressure=suction,
        discharge_pressure=discharge,
        flow_rate=flow,
        product_type=product,
        pump_size=pump_size
    )
    
    return analysis
