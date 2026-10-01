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

# -------------------------------------------------------------
# COST PRORATION LOGIC (MATCHING ORIGINAL OFFLINE APP LOGIC)
# -------------------------------------------------------------
def calc_piece_cost_logic(w, l, qty, bw, bl, board_price):
    """
    Calculates cost PER PIECE based strictly on max yield of that specific board size.
    Cost = (Board Price / Max Pieces it yields) * Qty requested.
    """
    y1 = (int(bw // w) * int(bl // l))
    y2 = (int(bw // l) * int(bl // w))
    max_y = max(y1, y2)
    
    if max_y > 0:
        cost_per_piece = board_price / max_y
        total_cost = cost_per_piece * qty
        return max_y, cost_per_piece, total_cost
    return 0, 0, 0

def generate_piece_breakdown(res_data, pieces_list, tier_name, thick):
    breakdown = []
    sum_tier_total = 0
    sum_own_total = 0
    
    if res_data['name'] == 'Mixed Optimized':
        for p_data in res_data['breakdown_data']:
            breakdown.append({
                "Label": p_data['Label'],
                "Size (mm)": p_data['Size (mm)'],
                "Qty": p_data['Qty'],
                "Best Board": p_data['Best Board'],
                f"Yield (pcs/board)": p_data['Yield'],
                f"Unit Cost ({tier_name})": f"RM {p_data['tier_cpp']:,.2f}",
                f"Total ({tier_name})": f"RM {p_data['tier_total']:,.2f}",
                "Unit Cost (Own Price)": f"RM {p_data['own_cpp']:,.2f}",
                "Total (Own Price)": f"RM {p_data['own_total']:,.2f}"
            })
            sum_tier_total += p_data['tier_total']
            sum_own_total += p_data['own_total']
    else:
        b_name = res_data['name']
        bw = res_data['data']['w']
        bl = res_data['data']['l']
        board_price_tier = res_data['data']['price']
        board_price_own = get_own_price(b_name, thick)
        
        for p in pieces_list:
            w, l, qty, lbl = p['width'], p['length'], p['qty'], p['label']
            
            y_tier, cpp_tier, total_tier = calc_piece_cost_logic(w, l, qty, bw, bl, board_price_tier)
            y_own, cpp_own, total_own = calc_piece_cost_logic(w, l, qty, bw, bl, board_price_own)
            
            breakdown.append({
                "Label": lbl,
                "Size (mm)": f"{w} x {l}",
                "Qty": qty,
                "Best Board": b_name,
                f"Yield (pcs/board)": y_tier,
                f"Unit Cost ({tier_name})": f"RM {cpp_tier:,.2f}",
                f"Total ({tier_name})": f"RM {total_tier:,.2f}",
                "Unit Cost (Own Price)": f"RM {cpp_own:,.2f}",
                "Total (Own Price)": f"RM {total_own:,.2f}"
            })
            sum_tier_total += total_tier
            sum_own_total += total_own
            
    breakdown.append({
        "Label": "SUBTOTAL",
        "Size (mm)": "",
        "Qty": "",
        "Best Board": "",
        f"Yield (pcs/board)": "",
        f"Unit Cost ({tier_name})": "",
        f"Total ({tier_name})": f"RM {sum_tier_total:,.2f}",
        "Unit Cost (Own Price)": "",
        "Total (Own Price)": f"RM {sum_own_total:,.2f}"
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

manual_board_choice = st.sidebar.selectbox("Option 2: Manual Override Board", list(valid_boards.keys()) if valid_boards else ["None"])

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

    # -------------------------------------------------------------
    # OPTION 1 LOGIC: INDEPENDENT PIECE-BY-PIECE OPTIMIZATION
    # -------------------------------------------------------------
    opt1_piece_breakdown = []
    opt1_grouped_boards = {}
    opt1_total_tier_cost = 0
    opt1_total_own_cost = 0
    opt1_fits_all = True
    
    for p in pieces:
        w, l, qty, lbl = p['width'], p['length'], p['qty'], p['label']
        best_board_name = None
        min_cpp = float('inf')
        
        for b_name, b_data in valid_boards.items():
            bw, bl = b_data['w'], b_data['l']
            b_price = b_data['price']
            y, cpp, total = calc_piece_cost_logic(w, l, 1, bw, bl, b_price) 
            if y > 0 and cpp < min_cpp:
                min_cpp = cpp
                best_board_name = b_name
                
        if best_board_name:
            if best_board_name not in opt1_grouped_boards:
                opt1_grouped_boards[best_board_name] = []
            opt1_grouped_boards[best_board_name].append(p)
            
            # Tier Cost
            tier_y, tier_cpp, tier_total = calc_piece_cost_logic(w, l, qty, valid_boards[best_board_name]['w'], valid_boards[best_board_name]['l'], valid_boards[best_board_name]['price'])
            opt1_total_tier_cost += tier_total
            
            # Own Cost
            own_price = get_own_price(best_board_name, thickness)
            own_y, own_cpp, own_total = calc_piece_cost_logic(w, l, qty, valid_boards[best_board_name]['w'], valid_boards[best_board_name]['l'], own_price)
            opt1_total_own_cost += own_total
            
            opt1_piece_breakdown.append({
                "Label": lbl, "Size (mm)": f"{w} x {l}", "Qty": qty, "Best Board": best_board_name,
                "Yield": tier_y, "tier_cpp": tier_cpp, "tier_total": tier_total, "own_cpp": own_cpp, "own_total": own_total
            })
        else:
            opt1_fits_all = False
            break

    opt1_res = None
    if opt1_fits_all:
        total_opt1_boards = 0
        opt1_visual_data = []
        for b_name, b_pieces in opt1_grouped_boards.items():
            bw, bl = valid_boards[b_name]['w'], valid_boards[b_name]['l']
            packed = pack_pieces(bw, bl, b_pieces, kerf=kerf_mm)
            if packed:
                total_opt1_boards += len(packed)
                for b_data in packed:
                    opt1_visual_data.append({'name': b_name, 'data': valid_boards[b_name], 'packed_board': b_data})

        opt1_res = {
            'name': 'Mixed Optimized', 
            'count': total_opt1_boards, 
            'cost': opt1_total_tier_cost,
            'cost_own': opt1_total_own_cost,
            'breakdown_data': opt1_piece_breakdown,
            'visuals': opt1_visual_data
        }

    # -------------------------------------------------------------
    # OPTION 2 LOGIC: SINGLE BOARD FULL NESTING (MANUAL)
    # -------------------------------------------------------------
    results = []
    for b_name, b_data in valid_boards.items():
        bw, bl = b_data['w'], b_data['l']
        b_price = b_data['price']
        own_b_price = get_own_price(b_name, thickness)
        
        packed = pack_pieces(bw, bl, pieces, kerf=kerf_mm)
        if not packed: continue 

        prorated_tier_sum = 0
        prorated_own_sum = 0
        fits_all = True
        for p in pieces:
            y, _, total_t = calc_piece_cost_logic(p['width'], p['length'], p['qty'], bw, bl, b_price)
            _, _, total_o = calc_piece_cost_logic(p['width'], p['length'], p['qty'], bw, bl, own_b_price)
            if y == 0: 
                fits_all = False
                break
            prorated_tier_sum += total_t
            prorated_own_sum += total_o
            
        if fits_all:
            results.append({
                'name': b_name, 
                'count': len(packed), 
                'cost': prorated_tier_sum, 
                'cost_own': prorated_own_sum,
                'packed': packed, 
                'data': b_data
            })

    opt2_res = None
    if manual_board_choice and manual_board_choice != "None":
        for r in results:
            if r['name'] == manual_board_choice:
                opt2_res = r
                break

    def get_row_data(strategy_name, res_data):
        if not res_data:
            return {"Strategy": strategy_name, "Board Size(s) Used": "N/A", "Warehouse Boards Pulled": "N/A", f"Total Prorated Invoice ({tier})": "N/A", "Total Prorated (Own Price)": "N/A"}
        
        board_desc = res_data['name']
        if board_desc == 'Mixed Optimized':
            used = list(set([x['Best Board'] for x in res_data['breakdown_data']]))
            board_desc = " + ".join(used)
            
        return {
            "Strategy": strategy_name, 
            "Board Size(s) Used": board_desc, 
            "Warehouse Boards Pulled": f"{res_data['count']} pcs", 
            f"Total Prorated Invoice ({tier})": f"RM {res_data['cost']:,.2f}",
            "Total Prorated (Own Price)": f"RM {res_data['cost_own']:,.2f}"
        }

    # --- COST SUMMARY TABLE ---
    st.header("Executive Cost Summary")
    st.info("Pricing for ALL options is calculated using the strict prorated rule: (Board Price ÷ Max Yield per board) × Qty.")
    summary_data = [
        get_row_data("Option 1: Most Economical (Piece-by-Piece Proration)", opt1_res),
        get_row_data(f"Option 2: Manual Override ({manual_board_choice})", opt2_res)
    ]
    st.table(pd.DataFrame(summary_data))
    st.markdown("---")

    # --- OPTION 1 RENDER ---
    st.header("Option 1: Most Economical (Piece-by-Piece True Optimization)")
    st.info("Logic: Evaluates every piece independently. Mixes and matches different board sizes to guarantee the absolute lowest total RM cost.")
    if opt1_res:
        st.subheader("Itemized Cost Breakdown (Option 1)")
        st.dataframe(generate_piece_breakdown(opt1_res, pieces, tier, thickness), use_container_width=True)
        
        st.subheader("2D Cutting Visuals")
        for i, b_info in enumerate(opt1_res['visuals'], 1):
            st.pyplot(plot_nesting_diagram(b_info['data']['w'], b_info['data']['l'], b_info['packed_board'], i, opt1_res['count'], b_info['name']))
    else:
        st.error("Pieces are too large to fit on any available board!")
    st.markdown("---")
    
    # --- OPTION 2 RENDER (FORMERLY OPTION 3) ---
    st.header(f"Option 2: Manual Override ({manual_board_choice})")
    if opt2_res:
        st.subheader(f"Itemized Cost Breakdown (Option 2)")
        st.dataframe(generate_piece_breakdown(opt2_res, pieces, tier, thickness), use_container_width=True)
        
        st.subheader("2D Cutting Visuals")
        for i, b_data in enumerate(opt2_res['packed'], 1):
            st.pyplot(plot_nesting_diagram(opt2_res['data']['w'], opt2_res['data']['l'], b_data, i, opt2_res['count'], opt2_res['name']))
    else:
        st.error(f"Cannot pack using {manual_board_choice}. Pieces are larger than the board dimensions!")
