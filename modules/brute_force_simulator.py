import os
from datetime import datetime
from typing import Dict, Tuple

# Realistic character sets
CHARSET_OPTIONS = {
    "1": ("Lowercase only (a-z)", 26),
    "2": ("Lowercase + Uppercase (a-z A-Z)", 52),
    "3": ("Lowercase + Uppercase + Digits (a-z A-Z 0-9)", 62),
    "4": ("Full charset (a-z A-Z 0-9 + symbols)", 94),
}

# Realistic cracking speeds (guesses per second)
GUESS_SPEED_PRESETS = {
    "1": ("Basic CPU", 1_000_000),  # 1 million
    "2": ("High-end GPU", 500_000_000),  # 500 million
    "3": ("GPU Cluster / Cloud Rig", 10_000_000_000),  # 10 billion
    "4": ("Custom (advanced user)", None),
}


def format_large_number(value: int) -> str:
    """Format large numbers with commas (e.g., 1,000,000,000)."""
    return f"{int(value):,}"


def seconds_to_readable(seconds: float) -> str:
    """Convert seconds into human-readable time with better granularity."""
    if seconds < 1:
        return "less than 1 second"

    units = [
        ("year", 31_557_600),
        ("month", 2_628_000),
        ("day", 86_400),
        ("hour", 3_600),
        ("minute", 60),
        ("second", 1),
    ]

    parts = []
    remaining = int(seconds)

    for name, count in units:
        value = remaining // count
        if value > 0:
            parts.append(f"{value} {name}{'s' if value != 1 else ''}")
            remaining %= count
        if len(parts) == 2 and name != "second":
            break

    if not parts:
        return "less than 1 second"

    return ", ".join(parts)


def calculate_search_space(length: int, charset_size: int) -> int:
    """Calculate total possible passwords: charset_size^length"""
    return charset_size**length


def estimate_crack_time(search_space: int, guesses_per_second: int) -> Dict[str, float]:
    """Estimate best, average, and worst-case crack time."""
    if guesses_per_second <= 0:
        return {"best": 0, "average": 0, "worst": 0}

    best_case = 1 / guesses_per_second
    average_case = search_space / (2 * guesses_per_second)
    worst_case = search_space / guesses_per_second

    return {
        "best_case_seconds": best_case,
        "average_case_seconds": average_case,
        "worst_case_seconds": worst_case,
    }


def classify_risk(worst_case_seconds: float) -> Tuple[str, str]:
    """Return risk level + short explanation."""
    if worst_case_seconds < 60:
        return "CRITICAL", "Can be cracked instantly"
    if worst_case_seconds < 3600:
        return "VERY HIGH", "Cracked in under an hour"
    if worst_case_seconds < 86_400:
        return "HIGH", "Cracked in less than a day"
    if worst_case_seconds < 2_592_000:  # 30 days
        return "MODERATE", "Cracked within a month"
    if worst_case_seconds < 31_557_600:  # 1 year
        return "LOW", "Takes months to a year"
    return "VERY LOW", "Extremely hard to crack"


def analyze_brute_force(
    length: int, charset_size: int, guesses_per_second: int
) -> Dict:
    """Main brute-force analysis function."""
    search_space = calculate_search_space(length, charset_size)
    times = estimate_crack_time(search_space, guesses_per_second)
    risk_level, risk_desc = classify_risk(times["worst_case_seconds"])

    return {
        "length": length,
        "charset_size": charset_size,
        "guesses_per_second": guesses_per_second,
        "search_space": search_space,
        "best_case_seconds": times["best_case_seconds"],
        "average_case_seconds": times["average_case_seconds"],
        "worst_case_seconds": times["worst_case_seconds"],
        "risk_level": risk_level,
        "risk_description": risk_desc,
    }


def print_simulation_report(result: Dict, charset_label: str, speed_label: str):
    """Clean and beautiful CLI report."""
    print("\n" + "=" * 75)
    print("🔥 BRUTE-FORCE SIMULATION REPORT")
    print("=" * 75)
    print(f"Password Length       : {result['length']} characters")
    print(f"Character Set         : {charset_label}")
    print(f"Character Pool Size   : {result['charset_size']:,}")
    print(
        f"Cracking Speed        : {speed_label} ({format_large_number(result['guesses_per_second'])} guesses/sec)"
    )

    print("\n📊 Total Search Space : " + format_large_number(result["search_space"]))

    print("\n⏱️  Estimated Crack Time:")
    print(f"   Best Case     : {seconds_to_readable(result['best_case_seconds'])}")
    print(f"   Average Case  : {seconds_to_readable(result['average_case_seconds'])}")
    print(f"   Worst Case    : {seconds_to_readable(result['worst_case_seconds'])}")

    print(f"\n🚨 Risk Level         : {result['risk_level']}")
    print(f"   → {result['risk_description']}")
    print("=" * 75)


def save_simulation_report(
    result: Dict,
    charset_label: str,
    speed_label: str,
    output_file="output/brute_force_report.txt",
):
    """Save professional report to file."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("BRUTE-FORCE SIMULATION REPORT\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")

        f.write(f"Password Length       : {result['length']} characters\n")
        f.write(f"Character Set         : {charset_label}\n")
        f.write(f"Character Pool Size   : {result['charset_size']:,}\n")
        f.write(
            f"Cracking Speed        : {speed_label} ({format_large_number(result['guesses_per_second'])} guesses/sec)\n\n"
        )

        f.write(
            f"Total Search Space    : {format_large_number(result['search_space'])}\n\n"
        )

        f.write("Estimated Crack Times:\n")
        f.write(
            f"   Best Case      : {seconds_to_readable(result['best_case_seconds'])}\n"
        )
        f.write(
            f"   Average Case   : {seconds_to_readable(result['average_case_seconds'])}\n"
        )
        f.write(
            f"   Worst Case     : {seconds_to_readable(result['worst_case_seconds'])}\n\n"
        )

        f.write(f"Risk Level            : {result['risk_level']}\n")
        f.write(f"Explanation           : {result['risk_description']}\n")


def run_brute_force_simulator():
    """User-friendly CLI entry point."""
    print("\n🔥 Auth Lens - Brute Force Simulator")
    print("=" * 60)

    # Character set selection
    print("\nChoose character set:")
    for key, (label, _) in CHARSET_OPTIONS.items():
        print(f"  {key}. {label}")

    charset_choice = input("\nEnter choice (1-4): ").strip()
    if charset_choice not in CHARSET_OPTIONS:
        print("❌ Invalid choice.")
        return

    charset_label, charset_size = CHARSET_OPTIONS[charset_choice]

    # Password length
    print("\nCommon password lengths:")
    print("  8   10   12   16")
    length_input = input("Enter password length (or choose from above): ").strip()
    try:
        length = int(length_input)
        if length < 1:
            raise ValueError
    except ValueError:
        print("❌ Invalid length.")
        return

    # Guesses per second
    print("\nChoose cracking speed (realistic presets):")
    for key, (label, _) in GUESS_SPEED_PRESETS.items():
        print(f"  {key}. {label}")

    speed_choice = input("\nEnter choice (1-4): ").strip()

    if speed_choice == "4":  # Custom
        try:
            guesses_per_second = int(input("Enter custom guesses per second: ").strip())
        except ValueError:
            print("❌ Invalid input.")
            return
        speed_label = "Custom Speed"
    else:
        if speed_choice not in GUESS_SPEED_PRESETS:
            print("❌ Invalid choice.")
            return
        speed_label, guesses_per_second = GUESS_SPEED_PRESETS[speed_choice]

    # Run simulation
    print(f"\n🔄 Simulating brute-force attack on {length}-character password...")
    result = analyze_brute_force(length, charset_size, guesses_per_second)

    # Display and save
    print_simulation_report(result, charset_label, speed_label)
    save_simulation_report(result, charset_label, speed_label)

    print(f"\n✅ Report saved to: output/brute_force_report.txt")
