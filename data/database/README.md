# Airport operations database

This folder contains **fictional training data** for the Sharjah "Data & AI with Gemini" workshop.

## How to restore the SQLite file

The original `airport_ops.db` database is about **29 MB**. To make the complete database available through this repository, its compressed archive has been stored in eight parts under `airport_ops.db.zip.parts/`.

After cloning or downloading the repository, run:

```bash
python data/database/restore_database.py
```

This creates `data/database/airport_ops.db`. The script verifies SHA-256 checksums before saving the database and is safe to run more than once.

For Google Colab, after cloning the repository, run:

```python
!python sharjah/data/database/restore_database.py
```

The generated SQLite file is intentionally not tracked in Git, since the source parts are already included. It is **synthetic educational data**, not real airport records.

## Other available data

- [Data dictionary](Data_Dictionary.md)
- [Excel workbook](../Airport_Copilot_Workbook.xlsx) — all 11 worksheets
- [Fictional documents and policies](../documents/)
