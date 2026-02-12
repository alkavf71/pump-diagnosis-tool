"""Modul untuk analisis data listrik (voltage, current, imbalance)"""
from typing import Dict
from utils.calculations import (
    calculate_voltage_imbalance,
    calculate_current_imbalance,
    calculate_load_percentage
)
from utils.lookup_tables import PUMP_SIZE_DEFAULTS


def analyze_electrical_conditions(
    voltage_l1: float,
    voltage_l2: float,
    voltage_l3: float,
    current_l1: float,
    current_l2: float,
    current_l3: float,
    pump_size: str
) -> Dict:
    """
    Analisis kondisi listrik motor
    
    Args:
        voltage_l1, l2, l3: Tegangan per phase (V)
        current_l1, l2, l3: Arus per phase (A)
        pump_size: Ukuran pompa untuk estimasi FLA
        
    Returns:
        Dict dengan hasil analisis listrik
    """
    # Get FLA from pump size
    fla = PUMP_SIZE_DEFAULTS[pump_size]["fla"]
    
    # Calculate voltage imbalance
    v_imbalance, v_status = calculate_voltage_imbalance(voltage_l1, voltage_l2, voltage_l3)
    
    # Calculate current imbalance
    i_imbalance, i_status = calculate_current_imbalance(current_l1, current_l2, current_l3)
    
    # Calculate average current & load
    i_avg = (current_l1 + current_l2 + current_l3) / 3
    load_pct, load_status = calculate_load_percentage(i_avg, fla)
    
    # Overall electrical status
    if v_status == "ALARM" or i_status == "ALARM" or load_status == "OVERLOAD_ALARM":
        overall_status = "CRITICAL"
    elif v_status == "WARNING" or i_status == "WARNING" or load_status == "OVERLOAD_WARNING":
        overall_status = "WARNING"
    elif load_status == "UNDERLOAD":
        overall_status = "WARNING"  # Underload juga bisa masalah
    else:
        overall_status = "NORMAL"
    
    # Recommendations
    recommendations = []
    
    if v_imbalance > 2:
        recommendations.append(
            f"⚠️ Voltage imbalance {v_imbalance}% > 2% - check power supply quality"
        )
    
    if i_imbalance > 5:
        recommendations.append(
            f"⚠️ Current imbalance {i_imbalance}% > 5% - check winding & connections"
        )
    
    if load_status == "OVERLOAD_WARNING":
        recommendations.append(
            f"⚠️ Motor load {load_pct}% > 110% FLA - check pump head & impeller"
        )
    elif load_status == "OVERLOAD_ALARM":
        recommendations.append(
            f"🚨 CRITICAL: Motor load {load_pct}% > 125% FLA - immediate action required"
        )
    elif load_status == "UNDERLOAD":
        recommendations.append(
            f"⚠️ Motor underload {load_pct}% < 80% FLA - check if pump operating below BEP"
        )
    
    if not recommendations:
        recommendations.append("✅ Electrical parameters within normal range")
    
    return {
        "voltage": {
            "l1": voltage_l1,
            "l2": voltage_l2,
            "l3": voltage_l3,
            "average": round((voltage_l1 + voltage_l2 + voltage_l3) / 3, 1),
            "imbalance_pct": v_imbalance,
            "status": v_status
        },
        "current": {
            "l1": current_l1,
            "l2": current_l2,
            "l3": current_l3,
            "average": round(i_avg, 1),
            "imbalance_pct": i_imbalance,
            "status": i_status
        },
        "load": {
            "fla": fla,
            "percentage": load_pct,
            "status": load_status
        },
        "overall_status": overall_status,
        "recommendations": recommendations,
        "has_issue": overall_status != "NORMAL"
    }


def generate_electrical_report(
    electrical_data: Dict,
    spec_data: Dict
) -> Dict:
    """
    Generate laporan analisis listrik
    
    Args:
        electrical_data: Dict dengan voltage & current per phase
        spec_data: Dict dengan pump_size
        
    Returns:
        Dict dengan laporan listrik lengkap
    """
    v1 = electrical_data.get("voltage_l1", 380.0)
    v2 = electrical_data.get("voltage_l2", 380.0)
    v3 = electrical_data.get("voltage_l3", 380.0)
    
    i1 = electrical_data.get("current_l1", 0.0)
    i2 = electrical_data.get("current_l2", 0.0)
    i3 = electrical_data.get("current_l3", 0.0)
    
    pump_size = spec_data.get("pump_size", "Medium")
    
    analysis = analyze_electrical_conditions(
        voltage_l1=v1,
        voltage_l2=v2,
        voltage_l3=v3,
        current_l1=i1,
        current_l2=i2,
        current_l3=i3,
        pump_size=pump_size
    )
    
    return analysis
