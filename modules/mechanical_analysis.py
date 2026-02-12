"""Modul untuk analisis kondisi mechanical (agregasi dari vibrasi)"""
from typing import Dict
from src.modules.vibration_analysis import generate_vibration_report


def analyze_mechanical_conditions(
    vibration_driver: Dict,
    vibration_driven: Dict,
    foundation_type: str = "rigid",
    product_type: str = "Diesel"
) -> Dict:
    """
    Analisis kondisi mechanical pompa & motor
    
    Args:
        vibration_driver: Data vibrasi Driver (motor)
        vibration_driven: Data vibrasi Driven (pump)
        foundation_type: Tipe fondasi
        product_type: Jenis produk
        
    Returns:
        Dict dengan hasil analisis mechanical
    """
    # Analyze driver (motor)
    driver_report = generate_vibration_report(
        vibration_driver,
        foundation_type,
        product_type
    )
    
    # Analyze driven (pump)
    driven_report = generate_vibration_report(
        vibration_driven,
        foundation_type,
        product_type
    )
    
    # Determine primary component issue
    driver_max = driver_report["averages"]["Overall_Max"]
    driven_max = driven_report["averages"]["Overall_Max"]
    
    if driver_max > driven_max:
        primary_component = "Motor (Driver)"
        primary_component_report = driver_report
    else:
        primary_component = "Pump (Driven)"
        primary_component_report = driven_report
    
    # Overall mechanical status
    overall_zone = max(
        driver_report["overall_zone"],
        driven_report["overall_zone"],
        key=lambda z: ["A", "B", "C", "D"].index(z)
    )
    
    # Recommendations
    recommendations = []
    
    if driver_report["overall_zone"] in ["C", "D"]:
        recommendations.append(
            f"⚠️ Motor vibration Zone {driver_report['overall_zone']} - check coupling alignment & rotor balance"
        )
    
    if driven_report["overall_zone"] in ["C", "D"]:
        recommendations.append(
            f"⚠️ Pump vibration Zone {driven_report['overall_zone']} - check impeller balance & bearing condition"
        )
    
    if primary_component_report["faults"]["primary_fault"] == "Misalignment":
        recommendations.append(
            "🔧 Primary fault: Misalignment - perform laser alignment"
        )
    elif primary_component_report["faults"]["primary_fault"] == "Unbalance":
        recommendations.append(
            "🔧 Primary fault: Unbalance - perform dynamic balancing"
        )
    elif primary_component_report["faults"]["primary_fault"] == "Mechanical Looseness / Foundation Issue":
        recommendations.append(
            "🔧 Primary fault: Mechanical looseness - check foundation bolts & grouting"
        )
    
    if not recommendations:
        recommendations.append("✅ Mechanical vibration within acceptable limits")
    
    return {
        "driver": driver_report,
        "driven": driven_report,
        "primary_component": primary_component,
        "overall_zone": overall_zone,
        "overall_severity": primary_component_report["severity"],
        "primary_fault": primary_component_report["faults"]["primary_fault"],
        "recommendations": recommendations,
        "has_issue": overall_zone in ["C", "D"]
    }
