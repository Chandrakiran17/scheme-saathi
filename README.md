# Scheme Saathi

A beginner-friendly Streamlit application for discovering and maintaining official-source-linked Indian government scheme information. Citizens enter optional profile details to see records whose listed criteria do not conflict. A service desk can add, search, archive, and export sourced records.

## Important accuracy note

This project is not a government service and does not submit applications. A profile match is only a preliminary pointer; it is not an eligibility decision. Confirm eligibility, required documents, application method, and current deadlines with the responsible department. The app starts with an empty scheme database: it does not fabricate scheme details. Staff must enter each record from an official source and record the date it was checked.

The myScheme portal describes itself as a government scheme discovery platform and links users to the relevant application page. See [myScheme](https://www.myscheme.gov.in/) and [National Portal of India: Schemes](https://www.india.gov.in/my-government/schemes).

## Features

- Citizen finder with optional age, income, state, occupation, and keyword filters.
- Plain-language scheme summary, source-entered criteria, document list, and application steps.
- Direct official source link and verification date shown with each record.
- Service desk form with validation and optional matching criteria.
- Search, CSV report download, and archive action. Archiving hides a record without deleting it.
- SQLite local storage; citizen profile details are kept in the Streamlit session, not saved to the database.
- Responsive Streamlit layout.

## Requirements

- Windows 10/11 and Python 3.10 or newer.
- PowerShell.
- Internet connection to open linked official sources (the app itself can run locally offline after dependencies are installed).

## Install and run on Windows PowerShell

Open PowerShell and change to the folder containing this README:

```powershell
cd "C:\path\to\your\project"
```

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation for this terminal, run this temporary command and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install dependencies and start the application:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Streamlit opens a browser tab, usually at `http://localhost:8501`. Use **Service desk** to enter a scheme record verified against an official government site. Then switch to **Citizen finder** to try the filters.

## Database

SQLite file: `schemes.db` in the project folder. It is created automatically and ignored by Git so local records are not accidentally uploaded. Back it up before moving computers. The schema is created with `IF NOT EXISTS`; archiving sets a record inactive and does not erase it.

For Streamlit Community Cloud, the application code is compatible, but its local filesystem is not a reliable persistent database. Use this as a read-only demo or connect a persistent hosted database before relying on records across deployments/restarts. Do not collect personal identifiers or sensitive documents. The Service desk mode is not authenticated; deploy behind organization-managed authentication before real use.

## Tests

```powershell
python -m unittest discover -s tests -v
```

Tests use temporary SQLite files and do not modify the real database.

## Main code walkthrough

- `streamlit_app.py`: draws the citizen and service-desk screens, validates submitted fields, displays source links, and provides CSV export.
- `app/database.py`: initializes SQLite, saves/archives/lists records, and compares profile fields to criteria entered by the service desk.
- `tests/test_database.py`: verifies saving, non-destructive archiving, and profile matching.

The app does not use AI to invent or interpret scheme rules. Record editors enter source-derived information, and the matching code only checks four optional structured fields (age, annual income, state, occupation). It shows the full written criteria and source link so the user can verify the information.

## GitHub upload (beginner steps)

1. Create a GitHub account if you do not already have one, then choose **New repository**. Name it `scheme-saathi` and create it without adding a README (this project already has one).
2. In PowerShell, `cd` to your project folder and run:

   ```powershell
   git init
   git add README.md requirements.txt streamlit_app.py app tests .gitignore
   git commit -m "Build Scheme Saathi scheme assistant"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/scheme-saathi.git
   git push -u origin main
   ```

3. Replace `YOUR-USERNAME` with your GitHub username. If Git asks for a password, sign in through its browser prompt or use GitHub's recommended authentication; never paste a password or token into source files.
4. Copy the repository URL from your browser into the submission document.

If `git` is not recognized, install Git for Windows, close/reopen PowerShell, and repeat these commands.

## Optional Streamlit Community Cloud deployment

1. Push the repository to GitHub.
2. Sign in at [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub and create an app from the repository.
3. Select branch `main` and main file path `streamlit_app.py`, then deploy.
4. Open the generated app URL and test the citizen view. Treat the cloud database as temporary unless you configure persistent storage.

## Demo video (under 5 minutes)

Suggested 3–4 minute outline:

1. (20 sec) State the problem and introduce Scheme Saathi.
2. (45 sec) Show Citizen finder and explain the optional profile and keyword search.
3. (60 sec) Expand a scheme record, show its source, criteria, documents, and explain that the match is not an approval.
4. (60 sec) In Service desk, demonstrate adding a record from an official source, filtering records, and downloading the CSV.
5. (30 sec) Mention SQLite, tests, privacy limits, and how to run it.

Use Windows Snipping Tool screen recording or another recorder, keep the video under five minutes, then upload to YouTube (Unlisted is suitable for class submission if your instructor accepts it). Copy its link into the submission document. Avoid showing personal information.

