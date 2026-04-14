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
        return {
            "best_case_seconds": 0.0,
            "average_case_seconds": 0.0,
            "worst_case_seconds": 0.0,
        }

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


from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()

def print_simulation_report(result: Dict, charset_label: str, speed_label: str):
    """Clean and beautiful CLI report using rich."""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Property", style="bold red")
    table.add_column("Value", style="none")
    
    table.add_row("Password Length", f"{result['length']} characters")
    table.add_row("Character Set", charset_label)
    table.add_row("Character Pool Size", f"{result['charset_size']:,}")
    table.add_row("Cracking Speed", f"{speed_label} ({format_large_number(result['guesses_per_second'])} guesses/sec)")
    table.add_row("", "")
    table.add_row("Total Search Space", format_large_number(result["search_space"]))
    
    time_table = Table(show_header=False, box=None, padding=(0, 2))
    time_table.add_column("Case", style="yellow")
    time_table.add_column("Time", style="bold")
    time_table.add_row("Best Case", seconds_to_readable(result['best_case_seconds']))
    time_table.add_row("Average Case", seconds_to_readable(result['average_case_seconds']))
    time_table.add_row("Worst Case", seconds_to_readable(result['worst_case_seconds']))

    # Determine risk color
    risk_color = "red"
    if result['risk_level'] in ["MODERATE", "LOW", "VERY LOW"]:
        risk_color = "green" if result['risk_level'] != "MODERATE" else "yellow"

    content = Group(
        table,
        "\n[bold yellow]⏱️  Estimated Crack Time:[/bold yellow]",
        time_table,
        f"\n[bold {risk_color}]🚨 Risk Level         : {result['risk_level']}[/bold {risk_color}]",
        f"[dim]   → {result['risk_description']}[/dim]"
    )

    panel = Panel(
        content,
        title="[bold red]🔥 BRUTE-FORCE SIMULATION REPORT[/bold red]",
        border_style="red",
        expand=False
    )
    console.print()
    console.print(panel)


def save_simulation_report(
    result: Dict,
    charset_label: str,
    speed_label: str,
    output_file=None,
) -> str:
    """Save professional report to file."""
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"output/brutecheck_report_{timestamp}.txt"
        
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
        
    return output_file


from rich.prompt import Prompt, IntPrompt
from modules.nav import ask_choice, ask_string

def run_brutecheck():
    """User-friendly CLI entry point."""
    from rich.panel import Panel
    console.print()
    console.print(Panel("[bold red]🔥 BruteCheck - Brute Force Simulator[/bold red]", expand=False, border_style="red", padding=(0, 2)))

    # Character set selection
    console.print("\n[bold red]Choose character set:[/bold red]")
    for key, (label, _) in CHARSET_OPTIONS.items():
        console.print(f"  [yellow]{key}[/yellow]. {label}")

    charset_choice = ask_choice("\nEnter choice", choices=list(CHARSET_OPTIONS.keys()))
    if charset_choice in ['b', 'q']:
        return
    charset_label, charset_size = CHARSET_OPTIONS[charset_choice]

    # Password length
    console.print("\n[bold red]Common password lengths:[/bold red] 8, 10, 12, 16")
    length_str = ask_string("Enter password length (or choose from above)")
    if length_str == "__BACK__": return
    try:
        length = int(length_str)
    except ValueError:
        console.print("[yellow]Invalid length, defaulting to 12.[/yellow]")
        length = 12

    # Guesses per second
    console.print("\n[bold red]Choose cracking speed (realistic presets):[/bold red]")
    for key, (label, _) in GUESS_SPEED_PRESETS.items():
        console.print(f"  [yellow]{key}[/yellow]. {label}")

    speed_choice = ask_choice("\nEnter choice", choices=list(GUESS_SPEED_PRESETS.keys()))
    if speed_choice in ['b', 'q']: return

    speed_label, guesses_per_second = GUESS_SPEED_PRESETS[speed_choice]

    # Run simulation
    console.print(f"\n[bold green]🔄 Simulating brute-force attack on {length}-character password...[/bold green]")
    result = analyze_brute_force(length, charset_size, guesses_per_second)

    # Display and save
    print_simulation_report(result, charset_label, speed_label)
    saved_file = save_simulation_report(result, charset_label, speed_label)

    console.print(f"\n[bold green]✅ Report saved to: [/bold green]{saved_file}\n")
