import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

st.set_page_config(page_title="Tianrun Multi-Cut Nesting & Cost Optimizer", page_icon="📐", layout="wide")

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

# --- CONSTANTS & DATABASE ---
BOARD_SIZES = {
    "6' x 8'": {"w": 1828.8, "l": 2438.4},
    "6' x 10'": {"w": 1828.8, "l": 3048.0},
    "6' x 12'": {"w": 1828.8, "l": 3657.6},
    "6' x 14'": {"w": 1828.8, "l": 4267.2},
}

# --- SIDEBAR & INPUTS ---
st.sidebar.header("Job Settings")
kerf_mm = st.sidebar.number_input("Blade Kerf (mm)", min_value=1.0, max_value=10.0, value=5.0, step=1.0)
manual_board_choice = st.sidebar.selectbox("Option 2: Force Board Size", list(BOARD_SIZES.keys()), index=2)

st.sidebar.markdown("---")
st.sidebar.header("Pricing Settings (Any Thickness)")
st.sidebar.markdown("Update prices below based on your required thickness to calculate accurate costs.")
price_6x8 = st.sidebar.number_input("Price for 6' x 8' (RM)", value=1300.0)
price_6x10 = st.sidebar.number_input("Price for 6' x 10' (RM)", value=1600.0)
price_6x12 = st.sidebar.number_input("Price for 6' x 12' (RM)", value=1890.0)
price_6x14 = st.sidebar.number_input("Price for 6' x 14' (RM)", value=2200.0)

BOARD_PRICES = {
    "6' x 8'": price_6x8,
    "6' x 10'": price_6x10,
    "6' x 12'": price_6x12,
    "6' x 14'": price_6x14
}

# --- 2D GUILLOTINE / SHELF PACKING ALGORITHM ---
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

        can_fit_normal = (w_i <= board_w and l_i <= board_l)
        can_fit_rot = (l_i <= board_w and w_i <= board_l)
        if not can_fit_normal and not can_fit_rot:
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
                    if placed:
                        break
                    
                    new_y = b['current_y']
                    if new_y + pl <= board_l and pw <= board_w:
                        b['placements'].append((0, new_y, pw, pl, lbl))
                        b['shelves'].append({'x': pw + kerf, 'y': new_y, 'max_h': pl})
                        b['current_y'] += pl + kerf
                        placed = True
                        break
            if placed:
                break

        if not placed:
            new_board = {'placements': [], 'shelves': [], 'current_y': 0}
            best_pw, best_pl = (w_i, l_i) if (w_i <= board_w and l_i <= board_l) else (l_i, w_i)
            if board_l >= board_w:
                if l_i <= board_l and w_i <= board_w:
                    best_pw, best_pl = w_i, l_i
                elif w_i <= board_l and l_i <= board_w:
                    best_pw, best_pl = l_i, w_i
            
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

    board_area = board_w * board_l
    utilization = (used_area / board_area) * 100

    ax.set_xlim(-50, board_l + 50)
    ax.set_ylim(-50, board_w + 50)
    ax.set_aspect('equal')
    ax.set_title(f"Board #{board_index} of {total_boards} — {board_name} ({int(board_w)}mm x {int(board_l)}mm) | Utilization: {utilization:.1f}%", fontsize=11, weight='bold', pad=10)
    ax.set_xlabel("Length (mm)", fontsize=9)
    ax.set_ylabel("Width (mm)", fontsize=9)
    plt.grid(color='#E0E0E0', linestyle=':', linewidth=0.6)
    plt.tight_layout()
    return fig, utilization

st.title("✂️ Multi-Cut Nesting & Cost Optimizer")
st.markdown("Enter multiple panel sizes below. The tool will calculate both the **Automatic Best Board** and your **Manually Selected Board**, complete with 2D visual layouts and total cost based on your custom thickness pricing.")

st.subheader("1. Enter Cutting List")
st.markdown("Add as many pieces as you need:")

if "cut_list" not in st.session_state:
    st.session_state.cut_list = pd.DataFrame([
        {"Label": "Bench Top", "Width (mm)": 600, "Length (mm)": 3600, "Qty": 1},
        {"Label": "Backsplash", "Width (mm)": 180, "Length (mm)": 3600, "Qty": 1},
        {"Label": "Panel A", "Width (mm)": 522, "Length (mm)": 700, "Qty": 2},
        {"Label": "Panel B", "Width (mm)": 509, "Length (mm)": 700, "Qty": 2},
        {"Label": "Panel C", "Width (mm)": 592, "Length (mm)": 700, "Qty": 2},
    ])

edited_df = st.data_editor(st.session_state.cut_list, num_rows="dynamic", use_container_width=True)

if st.button("Generate Nesting Plans 🚀"):
    st.markdown("---")
    pieces = []
    for index, row in edited_df.iterrows():
        try:
            w = float(row["Width (mm)"])
            l = float(row["Length (mm)"])
            qty = int(row["Qty"])
            lbl = str(row["Label"])
            if w > 0 and l > 0 and qty > 0:
                pieces.append({'width': w, 'length': l, 'qty': qty, 'label': lbl})
        except:
            continue
            
    if not pieces:
        st.error("Please enter valid width, length, and qty for at least one piece.")
        st.stop()

    st.subheader("Option 1: Automatic Most Efficient Board")
    
    best_board_name = None
    min_total_cost = float('inf')
    best_packing_result = None
    best_board_cost = 0

    for b_name, b_data in BOARD_SIZES.items():
        bw, bl = b_data['w'], b_data['l']
        b_price = BOARD_PRICES.get(b_name, 99999)
        
        packed_boards = pack_pieces(bw, bl, pieces, kerf=kerf_mm)
        if packed_boards is None:
            continue 
            
        total_boards_needed = len(packed_boards)
        total_cost = total_boards_needed * b_price
        
        if total_cost < min_total_cost:
            min_total_cost = total_cost
            best_board_name = b_name
            best_packing_result = packed_boards
            best_board_cost = b_price

    if best_board_name is None:
        st.error("Pieces are too large to fit on any standard board size in the database!")
    else:
        col1, col2 = st.columns(2)
        col1.metric("Optimal Board Size", best_board_name)
        col1.metric("Boards Required", f"{len(best_packing_result)} pcs")
        col2.metric("Base Price per Board", f"RM {best_board_cost:,.2f}")
        col2.metric("Total Material Cost", f"RM {min_total_cost:,.2f}")
        
        for i, b_data in enumerate(best_packing_result, start=1):
            fig, util = plot_nesting_diagram(BOARD_SIZES[best_board_name]['w'], BOARD_SIZES[best_board_name]['l'], b_data, i, len(best_packing_result), best_board_name)
            st.pyplot(fig)

    st.markdown("---")
    st.subheader(f"Option 2: Manual Override ({manual_board_choice})")
    
    mw, ml = BOARD_SIZES[manual_board_choice]['w'], BOARD_SIZES[manual_board_choice]['l']
    m_price = BOARD_PRICES.get(manual_board_choice, 0)
    manual_packed = pack_pieces(mw, ml, pieces, kerf=kerf_mm)
    
    if manual_packed is None:
        st.error(f"Cannot pack using {manual_board_choice}. Some pieces exceed the board dimensions!")
    else:
        m_total_cost = len(manual_packed) * m_price
        
        col3, col4 = st.columns(2)
        col3.metric("Selected Board Size", manual_board_choice)
        col3.metric("Boards Required", f"{len(manual_packed)} pcs")
        col4.metric("Base Price per Board", f"RM {m_price:,.2f}")
        col4.metric("Total Material Cost", f"RM {m_total_cost:,.2f}")
        
        if len(manual_packed) > len(best_packing_result if best_packing_result else []):
            st.warning("⚠️ Notice: Forcing this board size requires more boards than Option 1.")
        elif m_total_cost > min_total_cost:
            st.warning("⚠️ Notice: Forcing this board size is more expensive than Option 1.")
            
        for i, b_data in enumerate(manual_packed, start=1):
            fig, util = plot_nesting_diagram(mw, ml, b_data, i, len(manual_packed), manual_board_choice)
            st.pyplot(fig)