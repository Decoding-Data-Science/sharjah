#!/usr/bin/env python3
"""Restore the fictional airport SQLite database from repository-safe archive parts."""
from pathlib import Path
import hashlib
import io
import zipfile

HERE = Path(__file__).resolve().parent
ZIP_SHA256 = "38fd28ac7fcf66a2f49303841388100b2192f4cf9457b5565e9959d61c16f234"
DB_SHA256 = "c63e715c056c7e85b3642762aaa7bc875d661c807c49111880fdc18c4fc77920"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def restore_database() -> Path:
    destination = HERE / "airport_ops.db"
    if destination.is_file() and sha256(destination.read_bytes()) == DB_SHA256:
        print(f"Database already restored: {destination}")
        return destination

    parts = sorted((HERE / "airport_ops.db.zip.parts").glob("part_*"))
    if len(parts) != 8:
        raise FileNotFoundError(f"Expected 8 database archive parts, found {len(parts)}")

    archive = b"".join(part.read_bytes() for part in parts)
    if sha256(archive) != ZIP_SHA256:
        raise ValueError("Database archive checksum mismatch. Re-download all 8 parts.")

    with zipfile.ZipFile(io.BytesIO(archive)) as archive_file:
        database = archive_file.read("airport_ops.db")
    if sha256(database) != DB_SHA256:
        raise ValueError("Database checksum mismatch after decompression.")

    destination.write_bytes(database)
    print(f"Restored {destination} ({len(database):,} bytes)")
    return destination


if __name__ == "__main__":
    restore_database()
