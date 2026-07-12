from __future__ import annotations

from pathlib import Path

TRANSACTIONS_DIRNAME = "Transactions"
BUSINESS_ACCOUNT_NAME = "DKB-Business"
PERSONAL_ACCOUNT_NAME = "Girokonto"
VISA_BUSINESS_ACCOUNT_NAME = "DKB-VISA-Business-Card"
PAYPAL_ACCOUNT_NAME = "paypal@monkkee.com"
CSV_SUFFIX = ".csv"


def month_dir(repo_root: Path, year: int, month: int) -> Path:
    return repo_root / "tmp" / "staging" / f"{year:04d}" / f"{month:02d}"


def transactions_dir(repo_root: Path, year: int, month: int) -> Path:
    return month_dir(repo_root, year, month) / TRANSACTIONS_DIRNAME


def account_csv_path(repo_root: Path, year: int, month: int, account_name: str) -> Path:
    return transactions_dir(repo_root, year, month) / f"{account_name}{CSV_SUFFIX}"

