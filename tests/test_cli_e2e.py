import subprocess
import sys
from pathlib import Path
import re


def test_prune_versions_e2e(tmp_path):
    workdir = tmp_path / "work"
    workdir.mkdir()

    (workdir / "report.txt").write_text("final")
    (workdir / "report_v1.txt").write_text("v1")
    (workdir / "report_v2.txt").write_text("v2")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "fileshear",
            "prune-versions",
            "--dir",
            str(workdir),
            "--confirm",
            "report"
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr

    archive_dir = workdir / next(p.name for p in workdir.iterdir() if re.match(r"ShearArchive_\d{4}-\d{2}-\d{2}", p.name))
    assert archive_dir.exists()

    archived_files = {p.name for p in archive_dir.iterdir()}
    assert "report.txt" in archived_files
    assert "report_v1.txt" in archived_files

    assert (workdir / "report_v2.txt").exists()
    assert not (workdir / "report.txt").exists()
    assert not (workdir / "report_v1.txt").exists()
