import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tianrun Lab Costing Calculator", page_icon="🧪", layout="centered")

# --- PASSWORD PROTECTION ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "asuwaris36": # Default secure password
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.subheader("🔒 Secure Access Required")
        st.text_input("Please enter company password:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.subheader("🔒 Secure Access Required")
        st.text_input("Please enter company password:", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect. Please try again.")
        return False
    else:
        return True

if not check_password():
    st.stop()

# --- APP CODE BELOW ---

# --- DATABASE & PRICING MATRICES ---
pricing_data = {
    "Own Price": {
        "3mm": {"6' x 12'": 542.00},
        "4mm": {"6' x 12'": 623.00},
        "5mm": {"4' x 8'": 307.00, "4' x 10'": 382.00, "4' x 12'": 467.00, "1.3M x 10'": 411.00, "5' x 10'": 437.00, "5' x 12'": 505.00, "6' x 8'": 476.00, "6' x 12'": 669.00},
        "6mm": {"4' x 8'": 370.00, "5' x 12'": 590.00},
        "12mm": {"4' x 8'": 505.00, "4' x 10'": 621.00, "4' x 12'": 713.00, "1.3M x 10'": 650.00, "5' x 10'": 794.00, "5' x 12'": 932.00, "6' x 8'": 806.00, "6' x 12'": 1149.00},
        "15mm": {"4' x 8'": 601.00, "4' x 10'": 745.00, "4' x 12'": 869.00, "1.3M x 10'": 778.00, "5' x 10'": 926.00, "5' x 12'": 1099.00, "6' x 8'": 955.00, "6' x 12'": 1385.00},
        "16mm": {"4' x 8'": 633.00, "4' x 10'": 783.00, "4' x 12'": 913.00, "1.3M x 10'": 817.00, "5' x 10'": 1014.00, "5' x 12'": 1174.00, "6' x 8'": 1019.00, "6' x 12'": 1450.00},
        "18mm": {"4' x 8'": 692.00, "4' x 10'": 864.00, "4' x 12'": 1020.00, "1.3M x 10'": 903.00, "5' x 10'": 1101.00, "5' x 12'": 1303.00, "6' x 8'": 1103.00, "6' x 12'": 1601.00},
        "20mm": {"4' x 8'": 760.00, "4' x 10'": 945.00, "4' x 12'": 1107.00, "1.3M x 10'": 989.00, "5' x 10'": 1278.00, "5' x 12'": 1426.00, "6' x 8'": 1277.00, "6' x 12'": 1744.00},
        "25mm": {"5' x 10'": 1647.00}
    },
    "Max Discount": {
        "3mm": {"6' x 12'": 660.00},
        "4mm": {"6' x 12'": 750.00},
        "5mm": {"4' x 8'": 370.00, "4' x 10'": 460.00, "4' x 12'": 570.00, "1.3M x 10'": 500.00, "5' x 10'": 530.00, "5' x 12'": 610.00, "6' x 8'": 580.00, "6' x 12'": 810.00},
        "6mm": {"4' x 8'": 450.00, "5' x 12'": 710.00},
        "12mm": {"4' x 8'": 610.00, "4' x 10'": 750.00, "4' x 12'": 860.00, "1.3M x 10'": 790.00, "5' x 10'": 960.00, "5' x 12'": 1120.00, "6' x 8'": 970.00, "6' x 12'": 1380.00},
        "15mm": {"4' x 8'": 730.00, "4' x 10'": 900.00, "4' x 12'": 1050.00, "1.3M x 10'": 940.00, "5' x 10'": 1120.00, "5' x 12'": 1320.00, "6' x 8'": 1150.00, "6' x 12'": 1670.00},
        "16mm": {"4' x 8'": 760.00, "4' x 10'": 940.00, "4' x 12'": 1100.00, "1.3M x 10'": 990.00, "5' x 10'": 1220.00, "5' x 12'": 1410.00, "6' x 8'": 1230.00, "6' x 12'": 1750.00},
        "18mm": {"4' x 8'": 840.00, "4' x 10'": 1040.00, "4' x 12'": 1230.00, "1.3M x 10'": 1090.00, "5' x 10'": 1330.00, "5' x 12'": 1570.00, "6' x 8'": 1330.00, "6' x 12'": 1930.00},
        "20mm": {"4' x 8'": 920.00, "4' x 10'": 1140.00, "4' x 12'": 1330.00, "1.3M x 10'": 1190.00, "5' x 10'": 1540.00, "5' x 12'": 1720.00, "6' x 8'": 1540.00, "6' x 12'": 2100.00}
    },
    "Astonbina": {
        "3mm": {"6' x 12'": 700.00},
        "4mm": {"6' x 12'": 800.00},
        "5mm": {"4' x 8'": 400.00, "4' x 10'": 490.00, "4' x 12'": 600.00, "1.3M x 10'": 530.00, "5' x 10'": 560.00, "5' x 12'": 650.00, "6' x 8'": 610.00, "6' x 12'": 860.00},
        "6mm": {"4' x 8'": 480.00, "5' x 12'": 760.00},
        "12mm": {"4' x 8'": 650.00, "4' x 10'": 800.00, "4' x 12'": 910.00, "1.3M x 10'": 830.00, "5' x 10'": 1020.00, "5' x 12'": 1190.00, "6' x 8'": 1030.00, "6' x 12'": 1470.00},
        "15mm": {"4' x 8'": 770.00, "4' x 10'": 960.00, "4' x 12'": 1110.00, "1.3M x 10'": 1000.00, "5' x 10'": 1190.00, "5' x 12'": 1410.00, "6' x 8'": 1220.00, "6' x 12'": 1770.00},
        "16mm": {"4' x 8'": 810.00, "4' x 10'": 1000.00, "4' x 12'": 1170.00, "1.3M x 10'": 1050.00, "5' x 10'": 1300.00, "5' x 12'": 1500.00, "6' x 8'": 1300.00, "6' x 12'": 1850.00},
        "18mm": {"4' x 8'": 890.00, "4' x 10'": 1110.00, "4' x 12'": 1310.00, "1.3M x 10'": 1160.00, "5' x 10'": 1410.00, "5' x 12'": 1670.00, "6' x 8'": 1410.00, "6' x 12'": 2050.00},
        "20mm": {"4' x 8'": 970.00, "4' x 10'": 1210.00, "4' x 12'": 1420.00, "1.3M x 10'": 1270.00, "5' x 10'": 1640.00, "5' x 12'": 1820.00, "6' x 8'": 1630.00, "6' x 12'": 2230.00}
    },
    "Regular Customer": {
        "3mm": {"6' x 12'": 740.00},
        "4mm": {"6' x 12'": 850.00},
        "5mm": {"4' x 8'": 420.00, "4' x 10'": 520.00, "4' x 12'": 640.00, "1.3M x 10'": 560.00, "5' x 10'": 600.00, "5' x 12'": 690.00, "6' x 8'": 650.00, "6' x 12'": 920.00},
        "6mm": {"4' x 8'": 510.00, "5' x 12'": 810.00},
        "12mm": {"4' x 8'": 690.00, "4' x 10'": 850.00, "4' x 12'": 980.00, "1.3M x 10'": 890.00, "5' x 10'": 1090.00, "5' x 12'": 1270.00, "6' x 8'": 1100.00, "6' x 12'": 1570.00},
        "15mm": {"4' x 8'": 820.00, "4' x 10'": 1020.00, "4' x 12'": 1190.00, "1.3M x 10'": 1060.00, "5' x 10'": 1260.00, "5' x 12'": 1500.00, "6' x 8'": 1300.00, "6' x 12'": 1890.00},
        "16mm": {"4' x 8'": 870.00, "4' x 10'": 1070.00, "4' x 12'": 1250.00, "1.3M x 10'": 1120.00, "5' x 10'": 1380.00, "5' x 12'": 1600.00, "6' x 8'": 1390.00, "6' x 12'": 1980.00},
        "18mm": {"4' x 8'": 950.00, "4' x 10'": 1180.00, "4' x 12'": 1390.00, "1.3M x 10'": 1230.00, "5' x 10'": 1500.00, "5' x 12'": 1780.00, "6' x 8'": 1510.00, "6' x 12'": 2180.00},
        "20mm": {"4' x 8'": 1040.00, "4' x 10'": 1290.00, "4' x 12'": 1510.00, "1.3M x 10'": 1350.00, "5' x 10'": 1740.00, "5' x 12'": 1950.00, "6' x 8'": 1740.00, "6' x 12'": 2380.00}
    },
    "New Customer": {
        "3mm": {"6' x 12'": 800.00},
        "4mm": {"6' x 12'": 910.00},
        "5mm": {"4' x 8'": 450.00, "4' x 10'": 560.00, "4' x 12'": 690.00, "1.3M x 10'": 600.00, "5' x 10'": 640.00, "5' x 12'": 740.00, "6' x 8'": 700.00, "6' x 12'": 980.00},
        "6mm": {"4' x 8'": 540.00, "5' x 12'": 870.00},
        "12mm": {"4' x 8'": 740.00, "4' x 10'": 910.00, "4' x 12'": 1040.00, "1.3M x 10'": 950.00, "5' x 10'": 1160.00, "5' x 12'": 1360.00, "6' x 8'": 1180.00, "6' x 12'": 1680.00},
        "15mm": {"4' x 8'": 880.00, "4' x 10'": 1090.00, "4' x 12'": 1270.00, "1.3M x 10'": 1140.00, "5' x 10'": 1350.00, "5' x 12'": 1610.00, "6' x 8'": 1400.00, "6' x 12'": 2020.00},
        "16mm": {"4' x 8'": 930.00, "4' x 10'": 1150.00, "4' x 12'": 1340.00, "1.3M x 10'": 1200.00, "5' x 10'": 1480.00, "5' x 12'": 1720.00, "6' x 8'": 1490.00, "6' x 12'": 2120.00},
        "18mm": {"4' x 8'": 1010.00, "4' x 10'": 1260.00, "4' x 12'": 1490.00, "1.3M x 10'": 1320.00, "5' x 10'": 1610.00, "5' x 12'": 1900.00, "6' x 8'": 1610.00, "6' x 12'": 2340.00},
        "20mm": {"4' x 8'": 1110.00, "4' x 10'": 1380.00, "4' x 12'": 1620.00, "1.3M x 10'": 1450.00, "5' x 10'": 1870.00, "5' x 12'": 2080.00, "6' x 8'": 1870.00, "6' x 2'": 2550.00}
    }
}

board_dimensions = {
    "4' x 8'": (1219.2, 2438.4, "Ex-Stock"),
    "4' x 10'": (1219.2, 3048.0, "Indent"),
    "4' x 12'": (1219.2, 3657.6, "Indent"),
    "1.3M x 10'": (1300.0, 3048.0, "Indent"),
    "5' x 10'": (1524.0, 3048.0, "Ex-Stock"),
    "5' x 12'": (1524.0, 3657.6, "Ex-Stock"),
    "6' x 8'": (1828.8, 2438.4, "Ex-Stock"),
    "6' x 12'": (1828.8, 3657.6, "Ex-Stock")
}

st.title("🧪 Tianrun Lab Costing Calculator")
st.markdown("Web version of your offline cost calculator. Share this app link with anyone on your team!")

# --- SIDEBAR INPUTS ---
st.sidebar.header("Configuration Inputs")
tier = st.sidebar.selectbox("Pricing Tier", list(pricing_data.keys()), index=2) # Default Astonbina
thickness = st.sidebar.selectbox("Thickness", ["3mm", "4mm", "5mm", "6mm", "12mm", "15mm", "16mm", "18mm", "20mm", "25mm"], index=7) # Default 18mm
stock_filter = st.sidebar.selectbox("Stock Filter", ["Ex-Stock Only", "All Sizes"], index=0)

part_w = st.sidebar.number_input("Part Width (mm)", min_value=10, max_value=3000, value=750)
part_l = st.sidebar.number_input("Part Length (mm)", min_value=10, max_value=5000, value=2550)
quantity = st.sidebar.number_input("Quantity (pcs)", min_value=1, max_value=1000, value=1)
include_bs = st.sidebar.checkbox("Include Backsplash?", value=False)

# --- CALCULATION ENGINE ---
best_board = None
min_cost_per_piece = float('inf')
board_base_price = 0
board_yield = 0

tier_prices = pricing_data.get(tier, {}).get(thickness, {})

for b_name, (b_w, b_l, b_stock) in board_dimensions.items():
    if stock_filter == "Ex-Stock Only" and b_stock != "Ex-Stock":
        continue
    if b_name not in tier_prices:
        continue
        
    price = tier_prices[b_name]
    
    # Calculate yield in both orientations
    yield_1 = (int(b_w // part_w) * int(b_l // part_l))
    yield_2 = (int(b_w // part_l) * int(b_l // part_w))
    max_yield = max(yield_1, yield_2)
    
    if max_yield > 0:
        cost_per_pc = price / max_yield
        if cost_per_pc < min_cost_per_piece:
            min_cost_per_piece = cost_per_pc
            best_board = b_name
            board_base_price = price
            board_yield = max_yield

# --- DISPLAY RESULTS ---
st.subheader("Calculation Results")

if best_board is None:
    st.error("No eligible board found matching your dimensions and stock filter restrictions.")
else:
    total_boards = int(-(-quantity // board_yield)) # ceiling division
    total_material_cost = min_cost_per_piece * quantity
    
    # Backsplash calculation logic
    bs_cost = 0
    if include_bs:
        if part_l <= 3048:
            bs_cost = 100.00 * quantity
        elif part_l <= 3657.6:
            bs_cost = 120.00 * quantity
        else:
            # Multiples
            m1 = int(-(-part_l // 3048)) * 100.00
            m2 = int(-(-part_l // 3657.6)) * 120.00
            bs_cost = min(m1, m2) * quantity

    grand_total = total_material_cost + bs_cost

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Optimal Board Size", best_board)
        st.metric("Board Base Price", f"RM {board_base_price:,.2f}")
        st.metric("Yield Per Board", f"{board_yield} pcs")
        st.metric("Total Boards Required", f"{total_boards} boards")
    with col2:
        st.metric("Prorated Cost / Piece", f"RM {min_cost_per_piece:,.2f}")
        st.metric("Total Material Cost", f"RM {total_material_cost:,.2f}")
        st.metric("Total Backsplash Cost", f"RM {bs_cost:,.2f}")
        st.metric("GRAND TOTAL", f"RM {grand_total:,.2f}")

    st.success("Calculation complete based on your active pricing tier and cutting logic rules!")
