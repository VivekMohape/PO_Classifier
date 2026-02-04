import json
import streamlit as st

from classifier import classify_po, MODEL

st.set_page_config(page_title="PO Category Classifier", layout="centered")

st.title("PO L1-L2-L3 Classifier")
st.caption(
    "Classify purchase order descriptions into the L1/L2/L3 taxonomy. "
    "Provide a concise description and an optional supplier."
)
st.caption(f"Model: {MODEL}")

if "po_description" not in st.session_state:
    st.session_state["po_description"] = ""
if "supplier" not in st.session_state:
    st.session_state["supplier"] = ""

with st.form("po_form", clear_on_submit=False):
    po_description = st.text_area(
        "PO Description",
        height=120,
        placeholder="e.g., Annual subscription for project management software",
        help="Include product/service, scope, and any keywords that clarify the purchase.",
        key="po_description",
    )
    supplier = st.text_input(
        "Supplier (optional)",
        placeholder="e.g., Acme Corp",
        help="Supplier name helps disambiguate the category when the description is vague.",
        key="supplier",
    )

    col_classify, col_clear = st.columns(2)
    with col_classify:
        submitted = st.form_submit_button("Classify PO")
    with col_clear:
        clear_clicked = st.form_submit_button("Clear")

if clear_clicked:
    st.session_state["po_description"] = ""
    st.session_state["supplier"] = ""
    st.info("Cleared inputs.")

if submitted:
    if not po_description.strip():
        st.warning("Please enter a PO description before classifying.")
    else:
        with st.spinner("Classifying..."):
            result = classify_po(po_description, supplier)

        st.subheader("Result")
        try:
            parsed = json.loads(result)
            if "po_description" not in parsed:
                parsed["po_description"] = po_description
            st.json(parsed)
        except Exception:
            st.error("Model response was not valid JSON. Showing raw output below.")
            st.text(result)
