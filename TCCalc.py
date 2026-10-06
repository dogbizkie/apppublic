import streamlit as st
import pandas as pd
import math
from rectpack import newPacker

# --- 1. DATABASES & PRICING ---

ASUWARIS_PRICES = {
    "Solid": {"6x8": 646, "6x12": 852, "6x14": 1003},
    "Woodgrain": {"6x8": 656, "6x12": 867, "6x14": 1019}
}
FORMICA_PRICES = {
    "Solid": {"6x9": 1043, "6x12": 1391, "6x14": 1622},
    "Woodgrain": {"6x9": 1070, "6x12": 1427, "6x14": 1665}
}

BOARD_DIMS = {
    "6x8": (1830, 2440), "6x9": (1830, 2745), 
    "6x12": (1830, 3660), "6x14": (1830, 4270)
}

ACCESSORIES = {
    "Nylon Leg - Old": 9.50, "Stainless Steel Leg": 25.00,
    "Nylon Coat Hook - Old": 5.00, "Stainless Steel Coat Hook": 6.90,
    "Nylon Lockset - Old": 8.50, "Stainless Steel Lockset (136)": 29.50,
    "Stainless Steel Hinge - T31 (10mm)": 19.00, "Stainless Steel Hinge - T31 (12/13mm)": 24.20,
    "Nylon L-Bracket": 1.50, "Stainless Steel L-Bracket": 3.00,
    "Aluminium Oval Headrail - Black": 99.00, "Aluminium Square Headrail - Black": 116.00,
    "Aluminium U-Channel - Black (12 & 13mm)": 37.80, "Aluminium Door Frame (New) - Black": 100.00
}

# Transport Database (Sample mapped from upload)
TRANSPORT_DB = {
    "Kuala Lumpur": {"1 Tonne": 120, "3 Tonne": 195},
    "Shah Alam": {"1 Tonne": 135, "3 Tonne": 210},
    "Klang": {"1 Tonne": 155, "3 Tonne": 235},
    "Seremban": {"1 Tonne": 290, "3 Tonne": 360},
    "Melaka": {"1 Tonne": 510, "3 Tonne": 640},
    "Johor Bahru": {"1 Tonne": 780, "3 Tonne": 980},
    "Kuantan Port till Pekan": {"1 Tonne": 680, "3 Tonne": 860},
    "Penang": {"1 Tonne": 790, "3 Tonne": 980}
}

# Labor Database (Sample mapped from upload - Base cost for KL & PJ Area)
# Structure: Area -> Series -> Thickness -> [Measurement Cost, Labor Cost per Cubicle]
LABOR_DB = {
    "KL & PJ": {
        "Scan": {"10mm": [100, 120], "12mm": [100, 125], "13mm": [100, 125], "18mm": [100, 165]},
        "Orient": {"10mm": [100, 137], "12mm": [100, 144], "13mm": [100, 144], "18mm": [100, 186]},
        "Monitor": {"10mm": [100, 200], "12mm": [100, 200], "13mm": [100, 200], "18mm": [100, 245]},
        "Tech 1": {"10mm": [100, 83], "12mm": [100, 90], "13mm": [100, 90], "18mm": [100, 125]},
        "Tech 3": {"10mm": [100, 96], "12mm": [100, 101], "13mm": [100, 101], "18mm": [100, 135]}
    },
    "Shah Alam": {
        "Scan": {"12mm": [100, 130]}, # Add full arrays based on the master sheet
        "Tech 1": {"12mm": [100, 85]}
    }
}

# --- 2. STREAMLIT UI SETUP ---
st.set_page_config(page_title="Cubicle Costing App", layout="wide")
st.title("Full-Fledged Cubicle Costing & Optimization App")

st.sidebar.header("1. Project Settings")
sys_series = st.sidebar.selectbox("System Series", ["Scan", "Orient", "Monitor", "Tech 1", "Tech 3"])
brand = st.sidebar.selectbox("Board Brand", ["ASUWARIS", "Formica"])
finish = st.sidebar.selectbox("Finish Type", ["Solid", "Woodgrain"])
thickness = st.sidebar.selectbox("Thickness", ["10mm", "12mm", "13mm", "18mm"])

st.sidebar.header("2. Hardware Configuration")
leg_type = st.sidebar.selectbox("Adjustable Leg", ["Nylon Leg - Old", "Stainless Steel Leg"])
hook_type = st.sidebar.selectbox("Coat Hook", ["Nylon Coat Hook - Old", "Stainless Steel Coat Hook"])
lock_type = st.sidebar.selectbox("Lockset", ["Nylon Lockset - Old", "Stainless Steel Lockset (136)"])
hinge_type = st.sidebar.selectbox("Hinge", ["Stainless Steel Hinge - T31 (10mm)", "Stainless Steel Hinge - T31 (12/13mm)"])
conn_type = st.sidebar.radio("Connector Style", ["L-Bracket", "U-Channel"])
lb_type = st.sidebar.selectbox("L-Bracket Type", ["Nylon L-Bracket", "Stainless Steel L-Bracket"])
uc_type = st.sidebar.selectbox("U-Channel Type", ["Aluminium U-Channel - Black (12 & 13mm)"])
hr_type = st.sidebar.selectbox("Headrail Type", ["Aluminium Oval Headrail - Black", "Aluminium Square Headrail - Black"])
df_type = st.sidebar.selectbox("Door Frame (Tech 1)", ["Aluminium Door Frame (New) - Black"])

st.sidebar.header("3. Logistics & Labor")
area = st.sidebar.selectbox("Project Area (Labor)", list(LABOR_DB.keys()))
transport_loc = st.sidebar.selectbox("Transport Destination", list(TRANSPORT_DB.keys()))
lorry_type = st.sidebar.radio("Lorry Size", ["1 Tonne", "3 Tonne"])

st.markdown("### Panel Dimensions & Quantities (mm)")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    door_w = st.number_input("Door W", value=600)
    door_h = st.number_input("Door H", value=1800)
    door_qty = st.number_input("Door Qty", value=0, min_value=0)

with col2:
    int_pil_w = st.number_input("Int Pilaster W", value=300)
    int_pil_h = st.number_input("Int Pilaster H", value=1800)
    int_pil_qty = st.number_input("Int Pil Qty", value=0, min_value=0)

with col3:
    end_pil_w = st.number_input("End Pilaster W", value=150)
    end_pil_h = st.number_input("End Pilaster H", value=1800)
    end_pil_qty = st.number_input("End Pil Qty", value=0, min_value=0)

with col4:
    div_pan_w = st.number_input("Div Panel W", value=1500)
    div_pan_h = st.number_input("Div Panel H", value=1800)
    div_pan_qty = st.number_input("Div Panel Qty", value=0, min_value=0)

with col5:
    uri_pan_w = st.number_input("Urinal W", value=450)
    uri_pan_h = st.number_input("Urinal H", value=900)
    uri_pan_qty = st.number_input("Urinal Qty", value=0, min_value=0)

# --- 3. CORE CALCULATION ENGINE ---
if st.button("Calculate Total Project Cost", type="primary"):
    bom = {}
    hw_cost = 0

    # Door Hardware
    hinges_per_door = 4 if door_h > 2100 else 3
    if door_qty > 0:
        bom[hinge_type] = door_qty * hinges_per_door
        bom[hook_type] = door_qty * 1
        bom[lock_type] = door_qty * 1
    
    # Adjustable Legs
    if sys_series == "Scan":
        total_legs = (int_pil_qty * 2) + (end_pil_qty * 1)
        if total_legs > 0: bom[leg_type] = total_legs

    # Connectors
    if conn_type == "L-Bracket":
        total_brackets = (div_pan_qty * (8 if div_pan_h > 2100 else 6)) + \
                         (int_pil_qty * (8 if int_pil_h > 2100 else 6)) + \
                         (end_pil_qty * (4 if end_pil_h > 2100 else 3)) + \
                         (uri_pan_qty * 6)
        if total_brackets > 0: bom[lb_type] = total_brackets
    else:
        total_u_mm = (div_pan_qty * div_pan_h) + (int_pil_qty * int_pil_h) + (end_pil_qty * end_pil_h)
        if total_u_mm > 0: bom[uc_type] = math.ceil(total_u_mm / 6100)
        if uri_pan_qty > 0: bom[lb_type] = (uri_pan_qty * 6)

    # Headrail & Extrusions
    if sys_series in ["Scan", "Orient"]:
        hr_length = ((door_qty * door_w) + (int_pil_qty * int_pil_w) + (end_pil_qty * end_pil_w)) * 1.10
        if hr_length > 0: bom[hr_type] = math.ceil(hr_length / 6100)
        
    if sys_series == "Tech 1" and door_qty > 0:
        frame_mm = door_qty * ((door_h * 2) + door_w)
        bom[df_type] = math.ceil(frame_mm / 4200)

    # Calculate Hardware Cost
    for item, qty in bom.items():
        hw_cost += ACCESSORIES.get(item, 0) * qty

    # Nesting & Board Cost (Simplified Area Heuristic for MVP rendering speed)
    kerf = 5
    total_area = (door_qty * (door_w + kerf) * (door_h + kerf)) + \
                 (int_pil_qty * (int_pil_w + kerf) * (int_pil_h + kerf)) + \
                 (end_pil_qty * (end_pil_w + kerf) * (end_pil_h + kerf)) + \
                 (uri_pan_qty * (uri_pan_w + kerf) * (uri_pan_h + kerf))
                 
    if sys_series not in ["Tech 1", "Tech 3"]:
        total_area += (div_pan_qty * (div_pan_w + kerf) * (div_pan_h + kerf))

    # Assume worst-case board size for estimating max yield cost 
    b_area = 1830 * 4270 
    boards_needed