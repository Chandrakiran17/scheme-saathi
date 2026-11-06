from datetime import date
from urllib.parse import urlparse

import pandas as pd
import streamlit as st

from app.database import DEFAULT_DB, initialize, list_schemes, match_profile, save_scheme, set_active

st.set_page_config(page_title="Scheme Saathi", page_icon="🇮🇳", layout="wide")
initialize(DEFAULT_DB)

st.markdown("""
<style>
.stApp {background: linear-gradient(140deg,#f6f8ff 0%,#fff 48%,#f1fbf7 100%);}
.block-container {max-width: 1180px; padding-top: 2rem;}
.hero {padding: 1.7rem 2rem; border-radius: 20px; background: linear-gradient(110deg,#173f5f,#206a5d); color:white; margin-bottom:1.2rem;}
.hero h1 {color:white; margin:0;} .hero p {font-size:1.05rem; margin:.5rem 0 0;}
.notice {background:#fff7df; border-left:5px solid #e6a700; padding:1rem; border-radius:8px;}
</style>
<div class="hero"><h1>Scheme Saathi</h1><p>Clear, source-linked guidance to help people find government schemes.</p></div>
""", unsafe_allow_html=True)

st.caption("A student project for scheme discovery. It is not a government service or an application portal.")
mode = st.sidebar.radio("Choose a workspace", ["Citizen finder", "Service desk"])
schemes = list_schemes()

if mode == "Citizen finder":
    st.subheader("Find schemes to explore")
    st.markdown('<div class="notice">Eligibility results are a preliminary checklist only. The department makes the final decision. Confirm every detail and deadline on the linked official source before applying.</div>', unsafe_allow_html=True)
    with st.form("citizen_profile_form"):
        a, b = st.columns(2)
        age = a.number_input("Age (optional)", min_value=0, max_value=120, value=None, step=1, help="Leave blank to skip age matching.", key="citizen_age")
        income = b.number_input("Annual household income in ₹ (optional)", min_value=0, value=None, step=1000, key="citizen_income")
        c, d = st.columns(2)
        state = c.text_input("State / Union Territory (optional)", key="citizen_state")
        occupation = d.selectbox("Occupation (optional)", ["", "Student", "Farmer", "Job seeker", "Small-business owner", "Other"], key="citizen_occupation")
        query = st.text_input("Search keyword (optional)", placeholder="education, agriculture, employment…", key="citizen_query")
        submitted = st.form_submit_button("Find relevant records", type="primary")
    if submitted:
        profile = {"age": age, "annual_income": income, "state": state.strip(), "occupation": occupation}
        st.session_state["matched_profile_data"] = profile
        st.session_state["matched_query_text"] = query.strip().casefold()
    if "matched_profile_data" in st.session_state:
        profile = st.session_state["matched_profile_data"]
        query = st.session_state.get("matched_query_text", "")
        shown = [s for s in schemes if not query or query in " ".join(str(s.get(k) or "") for k in ("name", "department", "category", "summary", "eligibility")).casefold()]
        if not shown:
            st.info("No scheme records match this search yet. Try another word or ask a service desk to add an officially sourced record.")
        for scheme in shown:
            matched, reasons = match_profile(scheme, profile)
            with st.expander(f"{'🟢' if matched else '🟠'} {scheme['name']} · {scheme['jurisdiction']} · {scheme['category']}", expanded=True):
                st.write(scheme["summary"])
                if reasons:
                    st.warning("Possible criteria to check: " + " ".join(reasons))
                else:
                    st.success("No mismatch found among the criteria entered. This does not confirm eligibility.")
                st.markdown(f"**Department:** {scheme['department']}  ·  **Information checked:** {scheme['verified_on']}")
                st.markdown(f"**Eligibility stated by record editor:** {scheme['eligibility']}")
                st.markdown(f"**Documents listed:** {scheme['documents']}")
                st.markdown(f"**How to apply:** {scheme['application_steps']}")
                st.link_button("Open official source", scheme["official_url"])
    else:
        st.info(f"There are {len(schemes)} published record(s). Enter optional details and select **Find relevant records** to review them.")
    st.divider()
    st.markdown("**Official starting point:** [myScheme — Government scheme discovery](https://www.myscheme.gov.in/) · [National Portal of India — Schemes](https://www.india.gov.in/my-government/schemes)")

else:
    st.subheader("Service desk · maintain sourced records")
    st.warning("This demonstration has no sign-in or role security. Do not enter sensitive personal information. For real deployment, add organization-managed authentication and access controls.")
    st.metric("Published scheme records", len(schemes))
    st.caption("Only enter information checked against an official department or government portal. Put its direct URL and the date you checked it.")
    with st.form("scheme_form", clear_on_submit=True):
        st.markdown("#### Add a scheme record")
        name = st.text_input("Scheme name *")
        department = st.text_input("Responsible department / ministry *")
        cols = st.columns(3)
        jurisdiction = cols[0].selectbox("Jurisdiction *", ["Central", "State / UT"])
        category = cols[1].selectbox("Category *", ["Education", "Agriculture", "Employment", "Business", "Health", "Social welfare", "Housing", "Other"])
        state_record = cols[2].text_input("State / UT (if state scheme)")
        summary = st.text_area("Short plain-language summary *")
        eligibility = st.text_area("Eligibility wording from the source *")
        docs = st.text_area("Documents listed by source (separate with commas) *")
        steps = st.text_area("Application steps *")
        url = st.text_input("Official source URL *", placeholder="https://...")
        check_date = st.date_input("Date verified against source", value=date.today())
        st.markdown("**Optional matching limits** — leave blank if the official source does not specify them.")
        x, y, z = st.columns(3)
        min_age = x.number_input("Minimum age", 0, 120, value=None, step=1)
        max_age = y.number_input("Maximum age", 0, 120, value=None, step=1)
        max_income = z.number_input("Maximum annual income (₹)", 0, value=None, step=1000)
        x, y = st.columns(2)
        state_criterion = x.text_input("State criterion (if any)")
        occupation_criterion = y.selectbox("Occupation criterion (if any)", ["", "Student", "Farmer", "Job seeker", "Small-business owner", "Other"])
        submitted = st.form_submit_button("Save published record", type="primary")
    if submitted:
        required = [name, department, summary, eligibility, docs, steps, url]
        valid_url = urlparse(url).scheme == "https" and bool(urlparse(url).netloc)
        if not all(v.strip() for v in required):
            st.error("Fill in every field marked with *.")
        elif not valid_url:
            st.error("Enter a full HTTPS source URL from an official government or responsible department site.")
        elif min_age is not None and max_age is not None and min_age > max_age:
            st.error("Minimum age cannot be greater than maximum age.")
        elif jurisdiction == "State / UT" and not state_record.strip():
            st.error("Enter the State / UT for a state scheme.")
        else:
            save_scheme({"name": name.strip(), "department": department.strip(), "jurisdiction": f"{jurisdiction}{': ' + state_record.strip() if jurisdiction == 'State / UT' else ''}", "category": category, "summary": summary.strip(), "eligibility": eligibility.strip(), "documents": docs.strip(), "application_steps": steps.strip(), "official_url": url.strip(), "verified_on": check_date.isoformat(), "min_age": min_age, "max_age": max_age, "max_income": max_income, "state": state_criterion.strip() or None, "occupation": occupation_criterion or None, "active": 1})
            st.success("Record saved to the local SQLite database.")
            st.rerun()
    if schemes:
        st.markdown("#### Current records")
        keyword = st.text_input("Filter records by name or category")
        filtered = [s for s in schemes if keyword.casefold() in (s["name"] + " " + s["category"]).casefold()]
        st.dataframe(pd.DataFrame([{k: s[k] for k in ("id", "name", "department", "jurisdiction", "category", "verified_on", "official_url")} for s in filtered]), use_container_width=True, hide_index=True)
        export = pd.DataFrame([{k: s[k] for k in ("id", "name", "department", "jurisdiction", "category", "summary", "eligibility", "documents", "application_steps", "official_url", "verified_on")} for s in filtered]).to_csv(index=False).encode("utf-8")
        st.download_button("Download filtered report (CSV)", export, "scheme_records.csv", "text/csv")
        for scheme in filtered:
            with st.expander(f"Manage: {scheme['name']} (record #{scheme['id']})"):
                st.write(f"Source checked {scheme['verified_on']} · {scheme['official_url']}")
                if st.button("Archive this record", key=f"archive_{scheme['id']}"):
                    set_active(scheme["id"], False)
                    st.rerun()

