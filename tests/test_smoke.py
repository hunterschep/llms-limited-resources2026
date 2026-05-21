from pathlib import Path


def test_repo_has_makefile():
    assert Path("Makefile").exists()


def test_core_package_exists():
    assert Path("src/wmt26/data/schema.py").exists()
    assert Path("src/wmt26/eval/metrics.py").exists()
