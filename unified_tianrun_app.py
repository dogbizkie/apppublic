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

# --- DATABASE & PRICING MATRICES ---
pricing_data = {
    "Own Price": {
        "3mm": {"6' x 12'": 542.00}, "4mm": {"6' x 12'": 623.00},
        "5mm": {"4' x 8'": 307.0, "4' x 10'": 382.0, "4' x 12'": 467.0, "1.3M x 10'": 411.0, "5' x 10'": 437.0, "5' x 12'": 505.0, "6' x 8'": 476.0, "6' x 12'": 669.0},
        "6mm": {"4' x 8'": 370.00, "5' x 12'": 590.00},
        "12mm": {"4' x 8'": 505.0, "4' x 10'": 621.0, "4' x 12'": 713.0, "1.3M x 10'": 650.0, "5' x 10'": 794.0, "5' x 12'": 932.0, "6' x 8'": 806.0, "6' x 12'": 1149.0},
        "15mm": {"4' x 8'": 601.0, "4' x 10'": 745.0, "4' x 12'": 869.0, "1.3M x 10'": 778.0, "5' x 10'": 926.0, "5' x 12'": 1099.0, "6' x 8'": 955.0, "6' x 12'": 1385.0},
        "16mm": {"4' x 8'": 633.0, "4' x 10'": 783.0, "4' x 12'": 913.0, "1.3M x 10'": 817.0, "5' x 10'": 1014.0, "5' x 12'": 1174.0, "6' x 8'": 1019.0, "6' x 12'": 1450.0},
        "18mm": {"4' x 8'": 692.0, "4' x 10'": 864.0, "4' x 12'": 1020.0, "1.3M x 10'": 903.0, "5' x 10'": 1101.0, "5' x 12'": 1303.0, "6' x 8'": 1103.0, "6' x 12'": 1601.0},
        "20mm": {"4' x 8'": 760.0, "4' x 10'": 945.0, "4' x 12'": 1107.0, "1.3M x 10'": 989.0, "5' x 10'": 1278.0, "5' x 12'": 1426.0, "6' x 8'": 1277.0, "6' x 12'": 1744.0},
        "25mm": {"5' x 10'": 1647.00}
    },
    "Regular Customer": {
        "3mm": {"6' x 12'": 740.00}, "4mm": {"6' x 12'": 850.00},
        "5mm": {"4' x 8'": 420.0, "4' x 10'": 520.0, "4' x 12'": 640.0, "1.3M x 10'": 560.0, "5' x 10'": 600.0, "5' x 12'": 690.0, "6' x 8'": 650.0, "6' x 12'": 920.0},
        "6mm": {"4' x 8'": 510.00, "5' x 12'": 810.00},
        "12mm": {"4' x 8'": 690.0, "4' x 10'": 850.0, "4' x 12'": 980.0, "1.3M x 10'": 890.0, "5' x 10'": 1090.0, "5' x 12'": 1270.0, "6' x 8'": 1100.0, "6' x 12'": 1570.0},
        "15mm": {"4' x 8'": 820.0, "4' x 10'": 1020.0, "4' x 12'": 1190.0, "1.3M x 10'": 1060.0, "5' x 10'": 1260.0, "5' x 12'": 1500.0, "6' x 8'": 1300.0, "6' x 12'": 1890.0},
        "16mm": {"4' x 8'": 870.0, "4' x 10'": 1070.0, "4' x 12'": 1250.0, "1.3M x 10'": 1120.0, "5' x 10'": 1380.0, "5' x 12'": 1600.0, "6' x 8'": 1390.0, "6' x 12'": 1980.0},
        "18mm": {"4' x 8'": 950.0, "4' x 10'": 1180.0, "4' x 12'": 1390.0, "1.3M x 10'": 1230.0, "5' x 10'": 1500.0, "5' x 12'": 1780.0, "6' x 8'": 1510.0, "6' x 12'": 2180.0},
        "20mm": {"4' x 8'": 1040.0, "4' x 10'": 1290.0, "4' x 12'": 1510.0, "1.3M x 10'": 1350.0, "5' x 10'": 1740.0, "5' x 12'": 1950.0, "6' x 8'": 1740.0, "6' x 12'": 2380.0}
    },
    "Astonbina": {
        "3mm": {"6' x 12'": 700.00}, "4mm": {"6' x 12'": 800.00},
        "5mm": {"4' x 8'": 400.0, "4' x 10'": 490.0, "4' x 12'": 600.0, "1.3M x 10'": 530.0, "5' x 10'": 560.0, "5' x 12'": 650.0, "6' x 8'": 610.0, "6' x 12'": 860.0},
        "6mm": {"4' x 8'": 480.00, "5' x 12'": 760.00},
        "12mm": {"4' x 8'": 650.0, "4' x 10'": 800.0, "4' x 12'": 910.0, "1.3M x 10'": 830.0, "5' x 10'": 1020.0, "5' x 12'": 1190.0, "6' x 8'": 1030.0, "6' x 12'": 1470.0},
        "15mm": {"4' x 8'": 770.0, "4' x 10'": 960.0, "4' x 12'": 1110.0, "1.3M x 10'": 1000.0, "5' x 10'": 1190.0, "5' x 12'": 1410.0, "6' x 8'": 1220.0, "6' x 12'": 1770.0},
        "16mm": {"4' x 8'": 810.0, "4' x 10'": 1000.0, "4' x 12'": 1170.0, "1.3M x 10'": 1050.0, "5' x 10'": 1300.0, "5' x 12'": 1500.0, "6' x 8'": 1300.0, "6' x 12'": 1850.0},
        "18mm": {"4' x 8'": 890.0, "4' x 10'": 1110.0, "4' x 12'": 1310.0, "1.3M x 10'": 1160.0, "5' x 10'": 1410.0, "5' x 12'": 1670.0, "6' x 8'": 1410.0, "6' x 12'": 2050.0},
        "20mm": {"4' x 8'": 970.0, "4' x 10'": 1210.0, "4' x 12'": 1420.0, "1.3M x 10'": 1270.0, "5' x 10'": 1640.0, "5' x 12'": 1820.0, "6' x 8'": 1630.0, "6' x 12'": 2230.0}
    },
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

manual_board_choice = st.sidebar.selectbox("Manual Override Board", list(valid_boards.keys()) if valid_boards else ["None"])

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

    # OPTION 1: MOST ECONOMICAL (Full Job Nesting)
    st.header("Option 1: Most Economical (Optimal Full-Job Nesting)")
    st.info("Finds the best single board size to pack ALL pieces, minimizing overall material cost and boards used.")
    
    best_board_name = None
    min_total_cost = float('inf')
    best_packing = None

    for b_name, b_data in valid_boards.items():
        packed = pack_pieces(b_data['w'], b_data['l'], pieces, kerf=kerf_mm)
        if packed:
            cost = len(packed) * b_data['price']
            if cost < min_total_cost:
                min_total_cost = cost
                best_board_name = b_name
                best_packing = packed

    if best_board_name is None:
        st.error("Pieces are too large to fit on any available board!")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Optimal Board", best_board_name)
        c2.metric("Qty Needed", f"{len(best_packing)} boards")
        c3.metric("Total Material Cost", f"RM {min_total_cost:,.2f}")
        for i, b_data in enumerate(best_packing, 1):
            st.pyplot(plot_nesting_diagram(valid_boards[best_board_name]['w'], valid_boards[best_board_name]['l'], b_data, i, len(best_packing), best_board_name))

    st.markdown("---")

    # OPTION 2: LEAST HASSLE (Piece-by-Piece Offline Calculator Logic)
    st.header("Option 2: Least Hassle (Piece-by-Piece Prorated Cost)")
    st.warning("Evaluates each piece independently for the best yield. Easier to fulfill from offcuts/various boards, but results in more raw warehouse waste.")
    
    breakdown = []
    total_prorated_cost = 0
    for p in pieces:
        w, l, qty, lbl = p['width'], p['length'], p['qty'], p['label']
        best_piece_board = None
        min_cpp = float('inf')
        for b_name, b_data in valid_boards.items():
            bw, bl, price = b_data['w'], b_data['l'], b_data['price']
            y1 = (int(bw // w) * int(bl // l))
            y2 = (int(bw // l) * int(bl // w))
            max_y = max(y1, y2)
            if max_y > 0:
                cpp = price / max_y
                if cpp < min_cpp:
                    min_cpp = cpp
                    best_piece_board = b_name
        
        if best_piece_board:
            line_cost = min_cpp * qty
            total_prorated_cost += line_cost
            breakdown.append({"Label": lbl, "Dimensions": f"{w} x {l}", "Qty": qty, "Best Board Source": best_piece_board, "Unit Cost (RM)": round(min_cpp, 2), "Line Total (RM)": round(line_cost, 2)})
        else:
            breakdown.append({"Label": lbl, "Dimensions": f"{w} x {l}", "Qty": qty, "Best Board Source": "OVERSIZED", "Unit Cost (RM)": 0, "Line Total (RM)": 0})
            
    st.dataframe(pd.DataFrame(breakdown), use_container_width=True)
    st.metric("Total Prorated Billed Cost", f"RM {total_prorated_cost:,.2f}")

    st.markdown("---")

    # OPTION 3: MANUAL OVERRIDE
    st.header(f"Option 3: Manual Override ({manual_board_choice})")
    if manual_board_choice and manual_board_choice != "None":
        m_data = valid_boards[manual_board_choice]
        m_packed = pack_pieces(m_data['w'], m_data['l'], pieces, kerf=kerf_mm)
        if m_packed is None:
            st.error("Pieces are too large for this specific board.")
        else:
            m_cost = len(m_packed) * m_data['price']
            c1, c2, c3 = st.columns(3)
            c1.metric("Selected Board", manual_board_choice)
            c2.metric("Qty Needed", f"{len(m_packed)} boards")
            c3.metric("Total Material Cost", f"RM {m_cost:,.2f}")
            for i, b_data in enumerate(m_packed, 1):
                st.pyplot(plot_nesting_diagram(m_data['w'], m_data['l'], b_data, i, len(m_packed), manual_board_choice))
