# Scheme Saathi — Project Submission

## Student details

- **Name:** [Enter your name]
- **Roll number:** [Enter your roll number]
- **Subject:** Python Programming
- **Sector:** Government Scheme Assistant

## Project overview

Citizens can have difficulty finding government schemes that may fit their situation, understanding eligibility language, preparing required documents, and locating the correct application page. Scheme Saathi is a student-built guidance tool for citizens and service desks. It keeps scheme information linked to official sources and displays a clear reminder that a preliminary match is not a government eligibility decision.

## Main features

- Optional citizen profile and keyword search.
- Scheme summary, listed criteria, document checklist, application steps, source URL, and source-check date.
- Service desk form to add sourced records, with validation.
- Search, CSV report download, and non-destructive archiving.
- Local SQLite storage; no demo scheme claims or invented scheme data are preloaded.

## Technologies

Python, Streamlit, SQLite, pandas, and Python `unittest`.

## Source links

- [myScheme — official scheme discovery portal](https://www.myscheme.gov.in/)
- [National Portal of India — Government Schemes](https://www.india.gov.in/my-government/schemes)

## Submission links

- **GitHub repository:** [ADD AFTER CREATING REPOSITORY]
- **Live app:** [ADD IF DEPLOYED]
- **YouTube demo video (under 5 minutes):** [ADD AFTER UPLOADING VIDEO]

## How to run

From PowerShell in the project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_app.py
```

See `README.md` for full setup, test, GitHub upload, optional deployment, and demo recording steps.

## Important limitation

This is a student project, not an official government service. It does not submit applications or guarantee eligibility. Verify every scheme rule, document, and deadline with the linked responsible government source. Service desk mode has no sign-in and is intended for demonstration only.

