from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VendorRule:
    slug: str
    directory_name: str
    match_terms: tuple[str, ...] = ()
    pdf_prefix: str = ""


VENDOR_RULES: dict[str, VendorRule] = {
    "aws": VendorRule(
        slug="aws",
        directory_name="AWS",
        match_terms=("amazon web services", "aws emea"),
    ),
    "hosting": VendorRule(
        slug="hosting",
        directory_name="hosting.de",
        match_terms=("hosting.de gmbh",),
    ),
    "moritz": VendorRule(
        slug="moritz",
        directory_name="Moritz",
        match_terms=("moritz hoeppner",),
    ),
    "google": VendorRule(
        slug="google",
        directory_name="Google",
        match_terms=("google cloud emea limited", "apps commerce"),
    ),
    "github": VendorRule(
        slug="github",
        directory_name="GitHub",
        match_terms=("github, inc.",),
        pdf_prefix="github-",
    ),
}


def get_vendor_rule(vendor_slug: str) -> VendorRule:
    normalized_slug = vendor_slug.strip().lower()

    try:
        return VENDOR_RULES[normalized_slug]
    except KeyError as exc:
        supported = ", ".join(sorted(VENDOR_RULES))
        raise ValueError(
            f"Unbekannter Rechnungssteller: {vendor_slug}. Unterstützt: {supported}"
        ) from exc

