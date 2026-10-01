import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

st.set_page_config(page_title="Tianrun Unified Costing & Nesting", page_icon="🧪", layout="wide")

# --- PASSWORD PROTECTION ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "asuwaris36":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.subheader("🔒 Secure Access Required")
        st.text_input("Enter company password:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.subheader("🔒 Secure Access Required")
        st.text_input("Enter company password:", type="password", on_change=password_entered, key="password")
        st.error("😕 Incorrect password. Please try again.")
        return False
    else:
        return True

if not check_password():
    st.stop()

# --- FULL DATABASE & PRICING MATRICES ---
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
        "20mm": {"4' x 8'": 1110.00, "4' x 10'": 1380.00, "4' x 12'": 1620.00, "1.3M x 10'": 1450.00, "5' x 10'": 1870.00, "5' x 12'": 2080.00, "6' x 8'": 1870.00, "6' x 12'": 2550.00}
    }
}

board_dimensions = {
    "4' x 8'": {"w": 1219.2, "l": 2438.4, "stock": "Ex-Stock"},
    "4' x 10'": {"w": 1219.2, "l": 3048.0, "stock": "Indent"},
    "4' x 12'": {"w": 1219.2, "l": 3657.6, "stock": "Indent"},
    "1.3M x 10'": {"w": 1300.0, "l": 3048.0, "stock": "Indent"},
    "5' x 10'": {"w": 1524.0, "l": 3048.0, "stock": "Ex-Stock"},
    "5' x 12'": {"w": 1524.0, "l": 3657.6, "stock": "Ex-Stock"},
    "6' x 8'": {"w": 1828.8, "l": 2438.4, "stock": "Ex-Stock"},
    "6' x 12'": {"w": 1828.8, "l": 3657.6, "stock": "Ex-Stock"}
}

# --- ALGORITHMS ---
def pack_pieces(board_w, board_l, piece_list, kerf=5.0):
    items = []
    for p in piece_list:
        w, l, qty, label = p['width'], p['length'], p['qty'], p['label']
        for _ in range(qty):
            items.append({'w': min(w, l), 'l': max(w, l), 'label': label})
    items.sort(key=lambda x: (x['w'] * x['l'], max(x['w'], x['l'])), reverse=True)

    boards = []
    for item in items:
        placed = False
        w_i, l_i, lbl = item['w'], item['l'], item['label']
        if not ((w_i <= board_w and l_i <= board_l) or (l_i <= board_w and w_i <= board_l)):
            return None 

        for b in boards:
            for pw, pl in [(w_i, l_i), (l_i, w_i)]:
                if pw <= board_w and pl <= board_l:
                    for shelf in b['shelves']:
                        if shelf['y'] + pl <= board_l and shelf['x'] + pw <= board_w:
                            b['placements'].append((shelf['x'], shelf['y'], pw, pl, lbl))
                            shelf['x'] += pw + kerf
                            shelf['max_h'] = max(shelf['max_h'], pl)
                            placed = True
                            break
                    if placed: break
                    
                    new_y = b['current_y']
                    if new_y + pl <= board_l and pw <= board_w:
                        b['placements'].append((0, new_y, pw, pl, lbl))
                        b['shelves'].append({'x': pw + kerf, 'y': new_y, 'max_h': pl})
                        b['current_y'] += pl + kerf
                        placed = True
                        break
            if placed: break

        if not placed:
            new_board = {'placements': [], 'shelves': [], 'current_y': 0}
            best_pw, best_pl = (w_i, l_i) if (w_i <= board_w and l_i <= board_l) else (l_i, w_i)
            if board_l >= board_w:
                if l_i <= board_l and w_i <= board_w: best_pw, best_pl = w_i, l_i
                elif w_i <= board_l and l_i <= board_w: best_pw, best_pl = l_i, w_i
            
            new_board['placements'].append((0, 0, best_pw, best_pl, lbl))
            new_board['shelves'].append({'x': best_pw + kerf, 'y': 0, 'max_h': best_pl})
            new_board['current_y'] = best_pl + kerf
            boards.append(new_board)
    return boards

def plot_nesting_diagram(board_w, board_l, board_data, board_index, total_boards, board_name):
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    ax.add_patch(patches.Rectangle((0, 0), board_l, board_w, linewidth=2, edgecolor='#1F4E78', facecolor='#F8F9FA'))
    colors = ['#2E75B6', '#70AD47', '#ED7D31', '#FFC000', '#9E480E', '#4BACC6', '#8064A2', '#C00000']
    used_area = 0
    
    for idx, (x, y, pw, pl, label) in enumerate(board_data['placements']):
        col = colors[idx % len(colors)]
        rect = patches.Rectangle((y, x), pl, pw, linewidth=1.2, edgecolor='#1E395B', facecolor=col, alpha=0.9)
        ax.add_patch(rect)
        used_area += pw * pl
        font_sz = 8 if pw >= 150 else 6
        ax.text(y + pl/2, x + pw/2, f"{label}\n{int(pw)}x{int(pl)}", ha='center', va='center', 
                color='white' if col in ['#2E75B6', '#70AD47', '#9E480E', '#8064A2', '#C00000'] else '#111111', 
                fontsize=font_sz, weight='bold')

    utilization = (used_area / (board_w * board_l)) * 100
    ax.set_xlim(-50, board_l + 50)
    ax.set_ylim(-50, board_w + 50)
    ax.set_aspect('equal')
    ax.set_title(f"Board #{board_index} of {total_boards} — {board_name} | Utilization: {utilization:.1f}%", fontsize=11, weight='bold')
    ax.set_xlabel("Length (mm)", fontsize=9)
    ax.set_ylabel("Width (mm)", fontsize=9)
    return fig

def get_own_price(b_name, thick):
    return pricing_data.get("Own Price", {}).get(thick, {}).get(b_name, 0)

def generate_piece_breakdown(res_data, pieces_list, tier_name, thick):
    if not res_data: return None
    total_cost_tier = res_data['cost']
    own_unit = get_own_price(res_data['name'], thick)
    total_cost_own = own_unit * res_data['count']
    total_area = sum(p['width'] * p['length'] * p['qty'] for p in pieces_list)
    breakdown = []
    for p in pieces_list:
        w, l, qty, lbl = p['width'], p['length'], p['qty'], p['label']
        area_share = (w * l * qty) / total_area if total_area > 0 else 0
        tier_line_cost = total_cost_tier * area_share
        tier_unit_cost = tier_line_cost / qty if qty > 0 else 0
        own_line_cost = total_cost_own * area_share
        own_unit_cost = own_line_cost / qty if qty > 0 else 0
        breakdown.append({
            "Label": lbl,
            "Size (mm)": f"{w} x {l}",
            "Qty": qty,
            f"Unit Cost ({tier_name})": f"RM {tier_unit_cost:,.2f}",
            f"Total ({tier_name})": f"RM {tier_line_cost:,.2f}",
            "Unit Cost (Own Price)": f"RM {own_unit_cost:,.2f}",
            "Total (Own Price)": f"RM {own_line_cost:,.2f}"
        })
    return pd.DataFrame(breakdown)

# --- UI & LOGIC ---
st.title("✂️ Tianrun Unified Costing & Nesting Optimizer")

st.sidebar.header("Job Configuration")
tier = st.sidebar.selectbox("Pricing Tier", list(pricing_data.keys()), index=0)
thickness = st.sidebar.selectbox("Thickness", ["3mm", "4mm", "5mm", "6mm", "12mm", "15mm", "16mm", "18mm", "20mm", "25mm"], index=5)
stock_filter = st.sidebar.selectbox("Stock Filter", ["Ex-Stock Only", "All Sizes"], index=0)
kerf_mm = st.sidebar.number_input("Blade Kerf (mm)", min_value=1.0, value=5.0)

# Build valid boards dictionary based on selection
tier_prices = pricing_data.get(tier, {}).get(thickness, {})
valid_boards = {}
for b_name, b_info in board_dimensions.items():
    if stock_filter == "Ex-Stock Only" and b_info["stock"] != "Ex-Stock": continue
    if b_name in tier_prices:
        valid_boards[b_name] = {"w": b_info["w"], "l": b_info["l"], "price": tier_prices[b_name]}

manual_board_choice = st.sidebar.selectbox("Option 3: Manual Override Board", list(valid_boards.keys()) if valid_boards else ["None"])

st.subheader("1. Enter Cutting List")
if "cut_list" not in st.session_state:
    st.session_state.cut_list = pd.DataFrame([
        {"Label": "Bench Top", "Width (mm)": 600, "Length (mm)": 3600, "Qty": 1},
        {"Label": "Panel A", "Width (mm)": 522, "Length (mm)": 700, "Qty": 2}
    ])

edited_df = st.data_editor(st.session_state.cut_list, num_rows="dynamic", use_container_width=True)

if st.button("Generate Job Costs & Layouts 🚀"):
    st.markdown("---")
    if not valid_boards:
        st.error(f"No boards available for {tier} - {thickness} under the current stock filter.")
        st.stop()

    pieces = []
    for index, row in edited_df.iterrows():
        try:
            w, l, qty, lbl = float(row["Width (mm)"]), float(row["Length (mm)"]), int(row["Qty"]), str(row["Label"])
            if w > 0 and l > 0 and qty > 0: pieces.append({'width': w, 'length': l, 'qty': qty, 'label': lbl})
        except: continue
            
    if not pieces:
        st.error("Please enter valid dimensions.")
        st.stop()

    # Calculate all packing permutations first
    results = []
    for b_name, b_data in valid_boards.items():
        packed = pack_pieces(b_data['w'], b_data['l'], pieces, kerf=kerf_mm)
        if packed:
            cost = len(packed) * b_data['price']
            results.append({'name': b_name, 'cost': cost, 'count': len(packed), 'packed': packed, 'data': b_data})

    if not results:
        st.error("Pieces are too large to fit on any available board!")
        st.stop()

    # Sort logic for Option 1 (Lowest Cost Priority)
    opt1_res = sorted(results, key=lambda x: (x['cost'], x['count']))[0]
    
    # Sort logic for Option 2 (Fewest Boards Priority / Least Hassle)
    opt2_res = sorted(results, key=lambda x: (x['count'], x['cost']))[0]
    
    # Manual Option 3
    opt3_res = None
    if manual_board_choice and manual_board_choice != "None":
        for r in results:
            if r['name'] == manual_board_choice:
                opt3_res = r
                break

    def get_row_data(strategy_name, res_data):
        if not res_data:
            return {"Strategy": strategy_name, "Board Size": "N/A", "Qty (Boards)": "N/A", f"Unit Price ({tier})": "N/A", f"Total Price ({tier})": "N/A", "Unit Price (Own Price)": "N/A", "Total Cost (Own Price)": "N/A"}
        b_name = res_data['name']
        b_qty = res_data['count']
        tier_unit = res_data['data']['price']
        tier_total = res_data['cost']
        own_unit = get_own_price(b_name, thickness)
        own_total = own_unit * b_qty
        return {
            "Strategy": strategy_name, 
            "Board Size": b_name, 
            "Qty (Boards)": b_qty, 
            f"Unit Price ({tier})": f"RM {tier_unit:,.2f}", 
            f"Total Price ({tier})": f"RM {tier_total:,.2f}",
            "Unit Price (Own Price)": f"RM {own_unit:,.2f}",
            "Total Cost (Own Price)": f"RM {own_total:,.2f}"
        }

    # --- COST SUMMARY TABLE ---
    st.header("Executive Cost Summary & Margin Comparison")
    summary_data = [
        get_row_data("Option 1: Most Economical (Cheapest RM)", opt1_res),
        get_row_data("Option 2: Least Hassle (Fewest Boards Pulled)", opt2_res),
        get_row_data(f"Option 3: Manual Override ({manual_board_choice})", opt3_res)
    ]
    st.table(pd.DataFrame(summary_data))
    
    st.subheader("Itemized Piece Cost Breakdown by Option")
    st.info("Because total material costs vary between strategies, the individual cost attributed to each piece (prorated by its surface area) will also shift depending on which option you choose.")
    tab1, tab2, tab3 = st.tabs(["Option 1 Details", "Option 2 Details", f"Option 3 ({manual_board_choice})"])
    with tab1:
        st.dataframe(generate_piece_breakdown(opt1_res, pieces, tier, thickness), use_container_width=True)
    with tab2:
        st.dataframe(generate_piece_breakdown(opt2_res, pieces, tier, thickness), use_container_width=True)
    with tab3:
        if opt3_res:
            st.dataframe(generate_piece_breakdown(opt3_res, pieces, tier, thickness), use_container_width=True)
        else:
            st.error("N/A - This board choice cannot fit all the pieces.")
            
    st.markdown("---")

    # --- OPTION 1 RENDER ---
    st.header("Option 1: Most Economical (Cheapest Price)")
    st.info("Logic: Finds the board size that yields the lowest absolute material cost, even if it requires pulling more physical boards.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Optimal Board", opt1_res['name'])
    c2.metric("Qty Needed", f"{opt1_res['count']} boards")
    c3.metric(f"Total Material Cost ({tier})", f"RM {opt1_res['cost']:,.2f}")
    for i, b_data in enumerate(opt1_res['packed'], 1):
        st.pyplot(plot_nesting_diagram(opt1_res['data']['w'], opt1_res['data']['l'], b_data, i, opt1_res['count'], opt1_res['name']))
    
    st.markdown("---")

    # --- OPTION 2 RENDER ---
    st.header("Option 2: Least Hassle (Minimum Boards Pulled)")
    st.warning("Logic: Groups all pieces onto the largest board needed so you pull the fewest physical boards from the rack. This may cause more raw offcut waste (higher cost) but saves warehouse handling time.")
    c4, c5, c6 = st.columns(3)
    c4.metric("Optimal Board", opt2_res['name'])
    c5.metric("Qty Needed", f"{opt2_res['count']} boards")
    c6.metric(f"Total Material Cost ({tier})", f"RM {opt2_res['cost']:,.2f}")
    if opt1_res['name'] == opt2_res['name']:
        st.success("The Most Economical option is also the Least Hassle option!")
    for i, b_data in enumerate(opt2_res['packed'], 1):
        st.pyplot(plot_nesting_diagram(opt2_res['data']['w'], opt2_res['data']['l'], b_data, i, opt2_res['count'], opt2_res['name']))

    st.markdown("---")
    
    # --- OPTION 3 RENDER ---
    st.header(f"Option 3: Manual Override ({manual_board_choice})")
    if opt3_res:
        c7, c8, c9 = st.columns(3)
        c7.metric("Selected Board", opt3_res['name'])
        c8.metric("Qty Needed", f"{opt3_res['count']} boards")
        c9.metric(f"Total Material Cost ({tier})", f"RM {opt3_res['cost']:,.2f}")
        for i, b_data in enumerate(opt3_res['packed'], 1):
            st.pyplot(plot_nesting_diagram(opt3_res['data']['w'], opt3_res['data']['l'], b_data, i, opt3_res['count'], opt3_res['name']))
    else:
        st.error(f"Cannot pack using {manual_board_choice}. Pieces are larger than the board dimensions!")
