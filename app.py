from __future__ import annotations

import math
import time
from pathlib import Path
from typing import Dict

import streamlit as st
from PIL import Image


st.set_page_config(page_title="Ethical Learning Toolkit", page_icon="🧠", layout="wide")


def load_css() -> None:
    css_path = Path(__file__).with_name("styles.css")
    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def safe_eval(expr: str):
    allowed = {
        "__builtins__": {},
        "abs": abs,
        "round": round,
        "pow": pow,
        "sqrt": math.sqrt,
        "math": math,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "pi": math.pi,
        "e": math.e,
    }
    return eval(expr, allowed, {})


def dashboard() -> None:
    st.title("🧠 Ethical Learning Toolkit")
    st.caption("A transparent educational workspace for calculations, study tools, and lightweight browser demos.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Calculator", "Ready")
    col2.metric("Converters", "3 modes")
    col3.metric("BMI", "Live")
    col4.metric("Timer", "Start anytime")

    st.markdown("---")

    st.subheader("Quick overview")
    st.info(
        "This project is designed for ethical, educational use only. It focuses on transparent browser-side utilities, study helpers, and safe demonstration tools."
    )


def calculator_section() -> None:
    st.subheader("🧮 Calculator")
    expr = st.text_input("Expression", value="(12 + 8) * 3 / 2")
    if st.button("Calculate"):
        try:
            result = safe_eval(expr)
            st.success(f"Result: {result}")
        except Exception as exc:
            st.error(f"Invalid expression: {exc}")

    st.markdown("**Examples:** `2 + 2`, `sqrt(81)`, `sin(pi/2)`, `(10 * 3) / 2`")


def converter_section() -> None:
    st.subheader("🔄 Unit Converter")
    converter_type = st.selectbox("Type", ["Length", "Weight", "Temperature"])

    if converter_type == "Length":
        units = {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0, "in": 0.0254, "ft": 0.3048, "yd": 0.9144}
    elif converter_type == "Weight":
        units = {"mg": 0.000001, "g": 0.001, "kg": 1.0, "lb": 0.453592, "oz": 0.0283495}
    else:
        units = {"C": "C", "F": "F", "K": "K"}

    if converter_type != "Temperature":
        amount = st.number_input("Amount", value=1.0)
        from_unit = st.selectbox("From", list(units.keys()))
        to_unit = st.selectbox("To", list(units.keys()), index=1)

        value_in_meters = amount * units[from_unit]
        converted = value_in_meters / units[to_unit]
        st.success(f"{amount} {from_unit} = {converted:,.4f} {to_unit}")
    else:
        temp = st.number_input("Temperature", value=25.0)
        src = st.selectbox("From", ["C", "F", "K"])
        dst = st.selectbox("To", ["C", "F", "K"], index=1)

        def to_celsius(value: float, unit: str) -> float:
            if unit == "C":
                return value
            if unit == "F":
                return (value - 32) * 5 / 9
            if unit == "K":
                return value - 273.15
            raise ValueError("Unsupported unit")

        def from_celsius(value: float, unit: str) -> float:
            if unit == "C":
                return value
            if unit == "F":
                return (value * 9 / 5) + 32
            if unit == "K":
                return value + 273.15
            raise ValueError("Unsupported unit")

        c = to_celsius(temp, src)
        converted = from_celsius(c, dst)
        st.success(f"{temp} {src} = {converted:.2f} {dst}")


def bmi_section() -> None:
    st.subheader("📏 BMI Calculator")
    height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
    weight_kg = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=65.0)

    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    if bmi < 18.5:
        status = "Underweight"
        color = "orange"
    elif bmi < 25:
        status = "Healthy"
        color = "green"
    elif bmi < 30:
        status = "Overweight"
        color = "gold"
    else:
        status = "Obese"
        color = "red"

    st.metric("BMI", f"{bmi:.2f}")
    st.markdown(f"<div style='color:{color}; font-weight:600; font-size:1.1rem;'>Category: {status}</div>", unsafe_allow_html=True)


def timer_section() -> None:
    st.subheader("⏱️ Countdown Timer")
    minutes = st.number_input("Minutes", min_value=0, max_value=180, value=1)
    total_seconds = max(int(minutes * 60), 0)

    if "timer_end" not in st.session_state:
        st.session_state.timer_end = None

    if st.button("Start timer"):
        st.session_state.timer_end = time.time() + total_seconds

    if st.session_state.timer_end is not None:
        remaining = max(0, int(st.session_state.timer_end - time.time()))
        mins, secs = divmod(remaining, 60)
        st.metric("Remaining", f"{mins:02d}:{secs:02d}")

        if remaining == 0:
            st.balloons()
            st.success("Time is up!")
            st.session_state.timer_end = None


def notes_section() -> None:
    st.subheader("📝 Notes")
    default = st.session_state.get("study_notes", "")
    note_text = st.text_area("Write something useful", value=default, height=180)
    if st.button("Save note"):
        st.session_state.study_notes = note_text
        st.success("Note saved for this session.")

    st.code(st.session_state.get("study_notes", "No notes saved yet."))


def image_tool_section() -> None:
    st.subheader("🖼️ Image Resize Preview")
    uploaded = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded is not None:
        image = Image.open(uploaded)
        original_size = image.size
        width = st.slider("Width", 100, 1500, min(original_size[0], 800))
        height = st.slider("Height", 100, 1500, min(original_size[1], 600))

        resized = image.resize((width, height))
        col1, col2 = st.columns(2)
        col1.image(image, caption=f"Original: {original_size[0]}x{original_size[1]}")
        col2.image(resized, caption=f"Resized: {width}x{height}")

        buf = __import__("io").BytesIO()
        resized.save(buf, format="PNG")
        st.download_button("Download resized image", data=buf.getvalue(), file_name="resized_image.png", mime="image/png")


def battery_demo() -> None:
    st.subheader("🔋 Animated Battery Demo")
    st.markdown(
        """
        <div class="battery-box">
            <div class="battery-header">
                <div>
                    <div class="mini-title">Battery status</div>
                    <div id="battery-value">78%</div>
                </div>
                <div class="battery-outer">
                    <div class="battery-inner" id="battery-inner"></div>
                </div>
            </div>
            <div class="battery-meta">Charging: Yes • Health: Excellent</div>
        </div>
        <script>
            const value = 78;
            const inner = document.getElementById('battery-inner');
            const label = document.getElementById('battery-value');
            inner.style.width = value + '%';
            label.textContent = value + '%';
        </script>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    load_css()
    dashboard()

    tabs = st.tabs(["Dashboard", "Calculator", "Converters", "BMI", "Timer", "Notes", "Image", "Battery"])

    with tabs[0]:
        dashboard()
    with tabs[1]:
        calculator_section()
    with tabs[2]:
        converter_section()
    with tabs[3]:
        bmi_section()
    with tabs[4]:
        timer_section()
    with tabs[5]:
        notes_section()
    with tabs[6]:
        image_tool_section()
    with tabs[7]:
        battery_demo()


if __name__ == "__main__":
    main()
