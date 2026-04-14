import os
import re
from itertools import product
import datetime
from typing import List, Tuple


def normalize_input(
    user_input: str,
) -> Tuple[List[str], List[str], List[str], List[str]]:
    """
    Parse comma-separated input and classify tokens:
    - Names (with or without space)
    - Phone numbers (exactly 10 digits)
    - Dates (dd-mm-yyyy)
    - Regular keywords
    """
    if not user_input or not user_input.strip():
        return [], [], [], []

    raw_tokens = [token.strip() for token in user_input.split(",") if token.strip()]

    names: List[str] = []
    phones: List[str] = []
    dobs: List[str] = []
    keywords: List[str] = []

    date_pattern = re.compile(r"^\d{2}-\d{2}-\d{4}$")

    for token in raw_tokens:
        if " " in token:  # Full name
            cleaned = token.replace(" ", "")
            names.append(token)  # Original with space
            names.append(cleaned)  # Without space
            names.append(token.replace(" ", "."))  # With dot
            names.append(token.replace(" ", "_"))  # With underscore

        elif token.isdigit() and len(token) == 10:  # Phone number
            phones.append(token)

        elif date_pattern.match(token):  # DOB: dd-mm-yyyy
            dobs.append(token)

        else:  # Regular keyword
            keywords.append(token)

    # Remove duplicates while preserving order
    names = list(dict.fromkeys(names))
    phones = list(dict.fromkeys(phones))
    dobs = list(dict.fromkeys(dobs))
    keywords = list(dict.fromkeys(keywords))

    return names, phones, dobs, keywords


def generate_passwords_from_tokens(
    names: List[str], phones: List[str], dobs: List[str], keywords: List[str]
) -> List[str]:
    """
    Generate passwords using names, phones, dates and keywords.
    """
    passwords: List[str] = []
    seen = set()

    def add(p: str) -> None:
        if p and len(p) >= 6 and p not in seen:
            seen.add(p)
            passwords.append(p)

    current_year = str(datetime.date.today().year)

    # ====================== Names ======================
    for name in names:
        if not name:
            continue

        parts = name.split() if " " in name else [name]
        first_raw = parts[0]
        first_lower = first_raw.lower()
        first_cap = first_lower.capitalize()

        surname_cap = ""
        last_initial = ""
        if len(parts) > 1:
            surname = parts[-1]
            surname_cap = surname.lower().capitalize()
            last_initial = surname[0].lower()

        year_variants = [str(int(current_year) + offset) for offset in range(-8, 9)]
        yy = [y[-2:] for y in year_variants]

        # Name + Year combinations
        for y in year_variants:
            add(f"{first_cap}{y}")
            add(f"{first_cap}@{y}")
            add(f"{first_cap}{y}@")
            add(f"{first_cap}#{y}")
            add(f"{first_cap}!{y}")
            add(f"{first_cap}_{y}")
            add(f"{first_cap}.{y}")

        for y2 in yy:
            add(f"{first_cap}{y2}")
            add(f"{first_cap}@{y2}")
            add(f"{first_cap}{y2}!")

        # Common number endings
        common_numbers = ["123", "1234", "12345", "786", "999", "000", current_year]
        for num in common_numbers:
            add(f"{first_cap}{num}")
            add(f"{first_cap}@{num}")

        # Surname variants
        if surname_cap:
            for y in year_variants[:6]:
                add(f"{surname_cap}{y}")
                add(f"{surname_cap}@{y}")

        # First + Last initial
        if last_initial:
            for y in year_variants[:5]:
                add(f"{first_cap}{last_initial}{y}")
                add(f"{first_cap}{last_initial}@{y}")

    # ====================== DOBs ======================
    for dob in dobs:
        try:
            dd, mm, yyyy = dob.split("-")
            yy = yyyy[-2:]
            dob_variants = [
                dd + mm + yyyy,  # DDMMYYYY
                dd + mm + yy,  # DDMMYY
                mm + dd + yyyy,  # MMDDYYYY
                yyyy + mm + dd,  # YYYYMMDD
                yy + mm + dd,  # YYMMDD
                dd + mm,  # DDMM
                mm + dd,  # MMDD
            ]

            for name_part in names:
                first_cap = (
                    name_part.split()[0].capitalize()
                    if " " in name_part
                    else name_part.capitalize()
                )
                for dob_v in dob_variants:
                    add(f"{first_cap}{dob_v}")
                    add(f"{first_cap}@{dob_v}")
                    add(f"{first_cap}!{dob_v}")
        except Exception:
            continue

    # ====================== Phones ======================
    for phone in phones:
        phone3 = phone[-3:]
        phone4 = phone[-4:]

        for name_part in names:
            first_cap = (
                name_part.split()[0].capitalize()
                if " " in name_part
                else name_part.capitalize()
            )
            add(f"{first_cap}{phone4}")
            add(f"{first_cap}{phone3}")
            add(f"{first_cap}@{phone4}")

    # ====================== Keywords ======================
    for kw in keywords:
        kw_cap = kw.capitalize()
        add(kw_cap)
        add(f"{kw_cap}123")
        add(f"{kw_cap}1234")
        add(f"{kw_cap}{current_year}")
        add(f"{kw_cap}@{current_year}")

    # ====================== Final Variations ======================
    final_passwords: List[str] = []
    seen_final = set()
    for p in passwords:
        variants = [p, p.lower(), p.upper()]
        if len(p) > 1:
            variants.append(p[0].lower() + p[1:])
        for var in variants:
            if var and var not in seen_final:
                seen_final.add(var)
                final_passwords.append(var)

    return sorted(final_passwords)


def save_dictionary(
    passwords: List[str], output_file: str = "output/generated_dictionary.txt"
) -> None:
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        for pw in passwords:
            f.write(pw + "\n")


def run_dictionary_generator() -> None:
    """
    CLI entry point
    """
    print("\n=== Auth Lens - Dictionary Generator ===")
    print("Enter keywords separated by commas.")
    print("Supported formats:")
    print("  • Full names with spaces → Rahul Sharma")
    print("  • Phone numbers        → 9876543210")
    print("  • Dates                → 15-08-2002")
    print(
        "\nExample: Rahul Sharma, Priya Singh, 9876543210, 15-08-2002, admin, secure\n"
    )

    user_input = input("Enter keywords: ").strip()

    if not user_input:
        print("No input provided.")
        return

    names, phones, dobs, keywords = normalize_input(user_input)

    print(
        f"\nDetected → Names: {len(names)} | Phones: {len(phones)} | DOBs: {len(dobs)} | Keywords: {len(keywords)}"
    )

    passwords = generate_passwords_from_tokens(names, phones, dobs, keywords)

    save_dictionary(passwords)

    print(f"\n✅ Dictionary generated successfully!")
    print(f"Total unique passwords: {len(passwords)}")
    print(f"File saved: output/generated_dictionary.txt")
