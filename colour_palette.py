# app.py
import streamlit as st
import colorsys
import csv
import io

st.set_page_config(page_title="Palette Curator — Demo", layout="centered")
st.title("Palette Curator — choose a color, get curated palettes")

# ---------------------------
# Helpers: conversions
# ---------------------------
def hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join([c*2 for c in hex_color])
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r, g, b

def rgb_to_hex(r, g, b):
    return "#{:02X}{:02X}{:02X}".format(int(r), int(g), int(b))

def rgb_to_hls(r, g, b):
    # colorsys uses 0..1
    return colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)

def hls_to_rgb(h, l, s):
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return r*255, g*255, b*255

def clamp01(x):
    return max(0.0, min(1.0, x))

# ---------------------------
# Palette generation methods
# ---------------------------
def generate_analogous(h, s, l, count):
    # spread around hue +/- 30 degrees (0.083 in 0..1 units)
    spread = 0.083
    palette = []
    mid = (count - 1) // 2
    for i in range(count):
        offset = (i - mid) * spread
        hh = (h + offset) % 1.0
        rr, gg, bb = hls_to_rgb(hh, l, s)
        palette.append(rgb_to_hex(rr, gg, bb))
    return palette

def generate_complementary(h, s, l, count):
    # complementary is hue + 0.5
    palette = []
    comp = (h + 0.5) % 1.0
    # include base and some tints/shades of both base and comp
    for i in range(count):
        t = i / max(1, count-1)
        hh = h if i % 2 == 0 else comp
        # vary lightness for interest
        ll = clamp01(l * (1 - 0.15*t) + 0.1*t)
        rr, gg, bb = hls_to_rgb(hh, ll, s)
        palette.append(rgb_to_hex(rr, gg, bb))
    return palette

def generate_triadic(h, s, l, count):
    # triadic hues: +120deg (0.333), -120deg
    hues = [(h + offset) % 1.0 for offset in (0, 1/3, 2/3)]
    palette = []
    for i in range(count):
        hh = hues[i % len(hues)]
        # slight variation in lightness
        ll = clamp01(l * (0.9 + 0.1*(i % 2)))
        rr, gg, bb = hls_to_rgb(hh, ll, s)
        palette.append(rgb_to_hex(rr, gg, bb))
    return palette

def generate_monochrome(h, s, l, count):
    palette = []
    for i in range(count):
        # vary lightness evenly
        ll = clamp01(0.15 + (i / max(1, count-1)) * 0.7)
        rr, gg, bb = hls_to_rgb(h, ll, s * (0.6 + 0.4*(1 - abs(0.5 - i/(count-1)))))
        palette.append(rgb_to_hex(rr, gg, bb))
    return palette

def generate_tints_shades(h, s, l, count):
    # from lighter tints to darker shades
    palette = []
    for i in range(count):
        t = i / max(1, count-1)
        ll = clamp01(0.9 - 0.7 * t)  # 0.9 -> 0.2
        ss = clamp01(s * (0.6 + 0.4*(1-t)))
        rr, gg, bb = hls_to_rgb(h, ll, ss)
        palette.append(rgb_to_hex(rr, gg, bb))
    return palette

def generate_random_harmony(h, s, l, count, seed=42):
    import random
    rnd = random.Random(seed)
    palette = []
    for _ in range(count):
        hh = (h + rnd.uniform(-0.3, 0.3)) % 1.0
        ss = clamp01(s * rnd.uniform(0.6, 1.0))
        ll = clamp01(l * rnd.uniform(0.6, 1.0))
        rr, gg, bb = hls_to_rgb(hh, ll, ss)
        palette.append(rgb_to_hex(rr, gg, bb))
    return palette

# Dispatch mapping
PALETTE_FUNCS = {
    "Analogous": generate_analogous,
    "Complementary": generate_complementary,
    "Triadic": generate_triadic,
    "Monochrome": generate_monochrome,
    "Tints & Shades": generate_tints_shades,
    "Random Harmony": generate_random_harmony
}

# ---------------------------
# UI
# ---------------------------
col1, col2 = st.columns([1,2])
with col1:
    base_color = st.color_picker("Pick base color", "#4B8BBE")
    palette_type = st.selectbox("Palette type", list(PALETTE_FUNCS.keys()), index=0)
    count = st.slider("Number of colors", min_value=3, max_value=8, value=5)
    seed_input = st.number_input("Seed (for Random Harmony)", value=42, step=1)

with col2:
    st.write("**Quick tips**")
    st.write("- Try Analogous for harmonious, calm palettes.")
    st.write("- Complementary for strong contrast.")
    st.write("- Triadic for vivid, colorful combos.")
    st.write("- Tints & Shades to get usable UI palettes.")
    st.write("- Use Random Harmony for creative exploration.")

st.markdown("---")

# ---------------------------
# Generate & Display
# ---------------------------
r, g, b = hex_to_rgb(base_color)
h, l, s = rgb_to_hls(r, g, b)

# call chosen function
if palette_type == "Random Harmony":
    palette = PALETTE_FUNCS[palette_type](h, s, l, count, seed=seed_input)
else:
    palette = PALETTE_FUNCS[palette_type](h, s, l, count)

# Show swatches
st.subheader("Generated Palette")
cols = st.columns(len(palette))
for i, col in enumerate(cols):
    color_hex = palette[i]
    col.markdown(f"<div style='height:120px;background:{color_hex};border-radius:4px'></div>", unsafe_allow_html=True)
    col.write(color_hex)

# Copy / download
def make_csv(palette_list):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["position", "hex"])
    for i, c in enumerate(palette_list, start=1):
        writer.writerow([i, c])
    return output.getvalue().encode("utf-8")

csv_bytes = make_csv(palette)
st.download_button("Download palette CSV", csv_bytes, file_name="palette.csv", mime="text/csv")

st.caption("Demo mode: This algorithm is deterministic and fast. You can swap the generator functions with ML or style-rules later.")
