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
        if p and p not in seen:
            seen.add(p)
            passwords.append(p)

    current_year = str(datetime.date.today().year)
    
    identity_words = [
        "king", "queen", "boss", "legend", "official", "real", "cool",
        "rockstar", "gamer", "dev", "coder", "hacker", "warrior", "alpha",
        "beta", "india", "bharat", "jaihind", "cricket", "fitness", "gym",
        "beast", "lion", "single", "taken", "heart", "love", "money",
        "success", "startup", "ceo",
    ]
    gamer_patterns = ["OP", "Pro", "YT", "Gaming", "Live", "007", "999", "420", "69"]
    repeated_digits = [
        "111", "222", "000", "786", "108", "007", "9999", "333", "444", "555",
        "666", "777", "888", "123", "1234", "12345", "1010", "1122", "1313",
        "1414", "7777", "0000", "1984", "2000", "2001",
    ]
    suffixes = ["", "@", "!", "_", ".", "@123", "@1234", "@#", "@!", "!@", "#123"]

    all_dob_variants = []
    all_year_variants = [str(int(current_year) + offset) for offset in range(-8, 9)]

    for dob in dobs:
        try:
            dd, mm, yyyy = dob.split("-")
            yy_str = yyyy[-2:]
            dob_variants = [
                dd + mm + yyyy,  # DDMMYYYY
                dd + mm + yy_str,  # DDMMYY
                mm + dd + yyyy,  # MMDDYYYY
                yyyy + mm + dd,  # YYYYMMDD
                yy_str + mm + dd,  # YYMMDD
                dd + mm,  # DDMM
                mm + dd,  # MMDD
                yyyy + dd + mm,  # YYYYDDMM
                yy_str + dd + mm,  # YYDDMM
                yyyy,  # YYYY
                yy_str,  # YY
            ]
            all_dob_variants.extend(dob_variants)

            # Add year variants from dob
            year_int = int(yyyy)
            offsets = [-3, -2, -1, 0, 1, 2, 3]
            for offset in offsets:
                val = str(year_int + offset)
                if val not in all_year_variants:
                    all_year_variants.append(val)
        except Exception:
            continue

    all_dob_variants = list(dict.fromkeys(all_dob_variants))
    yy_list = list(dict.fromkeys([y[-2:] for y in all_year_variants]))

    # ====================== Names ======================
    name_objects = []
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

        double_name_patterns = []
        if surname_cap:
            double_name_patterns.extend(
                [
                    first_cap + surname_cap,
                    first_cap + "." + surname_cap,
                    first_cap + "_" + surname_cap,
                ]
            )

        name_objects.append({
            "first_raw": first_raw,
            "first_lower": first_lower,
            "first_cap": first_cap,
            "surname_cap": surname_cap,
            "last_initial": last_initial,
            "double_name_patterns": double_name_patterns
        })

        # Name + Year combinations
        for y in all_year_variants:
            add(f"{first_cap}{y}")
            add(f"{first_cap}@{y}")
            add(f"{first_cap}{y}@")
            add(f"{first_cap}#{y}")
            add(f"{first_cap}!{y}")
            add(f"{first_cap}_{y}")
            add(f"{first_cap}.{y}")
            
            if surname_cap:
                add(f"{surname_cap}{y}")
                add(f"{surname_cap}@{y}")
            if last_initial:
                add(f"{first_cap}{last_initial}{y}")
                add(f"{first_cap}{last_initial}@{y}")

        for y2 in yy_list:
            add(f"{first_cap}{y2}")
            add(f"{first_cap}@{y2}")
            add(f"{first_cap}{y2}!")
            if surname_cap:
                add(f"{surname_cap}{y2}")
            if last_initial:
                add(f"{first_cap}{last_initial}{y2}")

        common_numbers = ["123", "1234", "12345", "786", "999", "000", current_year, f"@{current_year}", f"{current_year}!"]
        for num in common_numbers:
            add(f"{first_cap}{num}")
            if num not in [f"@{current_year}", f"{current_year}!"]:
                add(f"{first_cap}@{num}")

        # Human Identity
        for word in identity_words:
            add(f"{first_cap}{word}")
            for y2 in yy_list:
                add(f"{first_cap}{word}{y2}")
            add(f"{first_cap}{word}123")
            add(f"{first_cap}@{word}")
            
        # Gamer Style
        for g in gamer_patterns:
            add(f"{first_cap}{g}")
            for y2 in yy_list:
                add(f"{first_cap}{g}{y2}")
            add(f"{first_cap}{g}!")
            add(f"{first_cap}{g}@")
            
        # Prefix Variants
        min_prefix_len = 4
        first_len = len(first_lower)
        if first_len >= min_prefix_len:
            max_prefix_len = 8 if first_len > 8 else first_len
            for prefix_len in range(min_prefix_len, max_prefix_len + 1):
                prefix_cap = first_lower[:prefix_len].capitalize()
                for y in all_year_variants:
                    add(f"{prefix_cap}@{y}")
                    add(f"{prefix_cap}{y}")
                    add(f"{prefix_cap}{y}@")
                    add(f"{prefix_cap}#{y}")
                    add(f"{prefix_cap}!{y}")
                    add(f"{prefix_cap}_{y}")
                    add(f"{prefix_cap}.{y}")
                for y2 in yy_list:
                    add(f"{prefix_cap}{y2}")
                    add(f"{prefix_cap}@{y2}")
                    add(f"{prefix_cap}{y2}!")
                for num in ["123", "1234", "12345", current_year]:
                    add(f"{prefix_cap}{num}")
                add(f"{prefix_cap}@{current_year}")
                add(f"{prefix_cap}{current_year}!")

        # Repeated Digits
        for rd in repeated_digits:
            add(first_cap + rd)
            add(first_lower + rd)

    # ====================== Phones ======================
    all_phone_variants = []
    for obj in name_objects:
        first_raw = obj["first_raw"]
        for phone in phones:
            phone_variants = [
                phone[-3:],
                phone[-4:],
                phone[-5:],
                phone[:4],
                phone,
                first_raw + phone,
            ]
            all_phone_variants.extend(phone_variants)
            
            # also basic additions
            first_cap = obj["first_cap"]
            phone3 = phone[-3:]
            phone4 = phone[-4:]
            add(f"{first_cap}{phone4}")
            add(f"{first_cap}{phone3}")
            add(f"{first_cap}@{phone4}")
            # The prefix ones for phone
            if len(first_raw) >= 4:
                prefix_cap = first_raw[:max(4, min(8, len(first_raw)))].capitalize()
                add(f"{prefix_cap}{phone4}")
                add(f"{prefix_cap}{phone3}")

    if not name_objects:
        for phone in phones:
            all_phone_variants.extend([
                phone[-3:],
                phone[-4:],
                phone[-5:],
                phone[:4],
                phone,
            ])
            
    all_phone_variants = list(dict.fromkeys(all_phone_variants))

    # ====================== Combinations ======================
    for obj in name_objects:
        first_cap = obj["first_cap"]
        first_lower = obj["first_lower"]
        first_raw = obj["first_raw"]
        double_name_patterns = obj["double_name_patterns"]

        for dob_v in all_dob_variants:
            for suf in suffixes:
                add(first_cap + dob_v + suf)
                add(first_lower + dob_v + suf)
                add(first_raw.capitalize() + dob_v + suf)
                
            for dn in double_name_patterns:
                add(dn + dob_v)
                add(dn + "@" + dob_v)

        for ph in all_phone_variants:
            for suf in suffixes:
                add(first_cap + ph + suf)
                add(first_lower + ph + suf)
                
            for dn in double_name_patterns:
                add(dn + ph)
                
        for dob_v, ph in product(all_dob_variants, all_phone_variants):
            add(first_cap + dob_v + ph)
            add(first_cap + ph + dob_v)

    # ====================== Keywords ======================
    for kw in keywords:
        kw_cap = kw.capitalize()
        add(kw_cap)
        add(f"{kw_cap}123")
        add(f"{kw_cap}1234")
        add(f"{kw_cap}{current_year}")
        add(f"{kw_cap}@{current_year}")
        for y in all_year_variants:
            add(f"{kw_cap}{y}")
            add(f"{kw_cap}@{y}")

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
    passwords: List[str], output_file: str = None
) -> str:
    if output_file is None:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"output/passforge_dict_{timestamp}.txt"
        
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        for pw in passwords:
            f.write(pw + "\n")
            
    return output_file


from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

def run_passforge() -> None:
    """
    CLI entry point
    """
    console.print()
    console.print(Panel("[bold green]📖 PassForge - Dictionary Generator[/bold green]", border_style="green", expand=False, padding=(0, 2)))
    console.print("Enter keywords separated by commas.")
    console.print("[cyan]Supported formats:[/cyan]")
    console.print("  • Full names with spaces → Rahul Sharma")
    console.print("  • Phone numbers        → 9876543210")
    console.print("  • Dates                → 15-08-2002")
    console.print(
        "\n[dim]Example: Rahul Sharma, Priya Singh, 9876543210, 15-08-2002, admin, secure[/dim]\n"
    )

    from modules.nav import ask_string
    user_input = ask_string("Enter keywords")

    if user_input == "__BACK__": return

    if not user_input:
        console.print("[red]No input provided.[/red]")
        return

    names, phones, dobs, keywords = normalize_input(user_input)

    console.print(
        f"\n[bold blue]Detected[/bold blue] → Names: {len(names)} | Phones: {len(phones)} | DOBs: {len(dobs)} | Keywords: {len(keywords)}"
    )

    with console.status("[bold green]Generating passwords...[/bold green]", spinner="dots"):
        passwords = generate_passwords_from_tokens(names, phones, dobs, keywords)
        saved_file = save_dictionary(passwords)

    console.print(f"\n[bold green]✅ Dictionary generated successfully![/bold green]")
    console.print(f"Total unique passwords: [bold white]{len(passwords)}[/bold white]")
    console.print(f"File saved: [dim]{saved_file}[/dim]")
