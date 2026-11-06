import tempfile
import unittest
from pathlib import Path

from app.database import initialize, list_schemes, match_profile, save_scheme, set_active


class SchemeDatabaseTests(unittest.TestCase):
    def setUp(self):
        # Keep test files inside the project workspace, where Windows sandbox
        # permissions allow creating and cleaning up temporary databases.
        self.temp = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent)
        self.db = Path(self.temp.name) / "test.sqlite"
        initialize(self.db)

    def tearDown(self):
        self.temp.cleanup()

    def record(self):
        return {"name": "Example", "department": "Department", "jurisdiction": "Central", "category": "Education", "summary": "A sourced record", "eligibility": "See source", "documents": "See source", "application_steps": "See source", "official_url": "https://example.gov.in", "verified_on": "2026-11-06", "min_age": 18, "max_age": 30, "max_income": 500000, "state": None, "occupation": "Student", "active": 1}

    def test_save_list_and_archive_without_deleting(self):
        scheme_id = save_scheme(self.record(), self.db)
        self.assertEqual(len(list_schemes(self.db)), 1)
        set_active(scheme_id, False, self.db)
        self.assertEqual(list_schemes(self.db), [])
        self.assertEqual(len(list_schemes(self.db, include_inactive=True)), 1)

    def test_profile_match_and_mismatch(self):
        record = self.record()
        self.assertEqual(match_profile(record, {"age": 22, "occupation": "Student"}), (True, []))
        matched, reasons = match_profile(record, {"age": 35, "occupation": "Farmer"})
        self.assertFalse(matched)
        self.assertEqual(len(reasons), 2)


if __name__ == "__main__":
    unittest.main()

