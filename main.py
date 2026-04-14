import sys
from rich.console import Console
from rich.panel import Panel

from modules.config import load_config, PROJECT_NAME, VERSION
from modules.about import show_startup_banner, show_about_screen, show_help_screen
from modules.nav import ask_choice

from modules.passforge import run_passforge
from modules.strengthmeter import run_strengthmeter
from modules.brutecheck import run_brutecheck
from modules.hashscan import run_hashscan
from modules.auditor import run_auditor

console = Console()

def print_menu():
    menu_text = (
        "[cyan]1.[/cyan] Generate Dictionary\n"
        "[cyan]2.[/cyan] Analyze Password Strength\n"
        "[cyan]3.[/cyan] Simulate Brute Force\n"
        "[cyan]4.[/cyan] Parse Sample Hashes\n"
        "[cyan]5.[/cyan] Generate Audit Report\n"
        "[cyan]6.[/cyan] About AuthLens\n"
        "[cyan]7.[/cyan] Help"
    )
    panel = Panel(
        menu_text,
        title=f"[bold cyan]🔐 {PROJECT_NAME.upper()} v{VERSION}[/bold cyan]",
        border_style="cyan",
        width=50,
        expand=False,
    )
    console.print()
    console.print(panel)


def main():
    config = load_config()
    if config.get("show_banner", True):
        console.print()
        show_startup_banner()

    try:
        while True:
            print_menu()
            console.print()
            choice = ask_choice("Enter your choice", choices=["1", "2", "3", "4", "5", "6", "7"])

            if choice == "q":
                console.print(f"\n[bold green]Exiting {PROJECT_NAME}. Goodbye![/bold green]\n")
                break
                
            if choice == "b":
                # At main menu, back acts as quit
                console.print(f"\n[bold green]Exiting {PROJECT_NAME}. Goodbye![/bold green]\n")
                break

            if choice == "1":
                run_passforge()
            elif choice == "2":
                run_strengthmeter()
            elif choice == "3":
                run_brutecheck()
            elif choice == "4":
                run_hashscan()
            elif choice == "5":
                run_auditor()
            elif choice == "6":
                show_about_screen()
            elif choice == "7":
                show_help_screen()
    except KeyboardInterrupt:
        console.print(f"\n\n[bold green]Exiting {PROJECT_NAME}. Goodbye![/bold green]\n")
        sys.exit(0)

if __name__ == "__main__":
    main()