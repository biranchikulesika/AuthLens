from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.table import Table

from modules.config import PROJECT_NAME, VERSION, TAGLINE, MODULE_NAMES
from modules.nav import getch

console = Console()

def show_startup_banner():
    ASCII_LOGO = r"""[bold cyan]    █████╗ ██╗   ██╗████████╗██╗  ██╗██╗     ███████╗███╗   ██╗███████╗
   ██╔══██╗██║   ██║╚══██╔══╝██║  ██║██║     ██╔════╝████╗  ██║██╔════╝
   ███████║██║   ██║   ██║   ███████║██║     █████╗  ██╔██╗ ██║███████╗
   ██╔══██║██║   ██║   ██║   ██╔══██║██║     ██╔══╝  ██║╚██╗██║╚════██║
   ██║  ██║╚██████╔╝   ██║   ██║  ██║███████╗███████╗██║ ╚████║███████║[/bold cyan]"""

    banner_text = f"{ASCII_LOGO}\n\n[italic]{TAGLINE}[/italic]\n[dim]v{VERSION}[/dim]\n"
    banner_text += f"\n[green]Modules:[/green] " + ", ".join(MODULE_NAMES)
    
    panel = Panel(
        Align.center(banner_text),
        border_style="cyan",
        expand=False
    )
    console.print(panel)

def wait_for_back():
    console.print()
    console.print("[dim]Press 'b' to go back...[/dim]")
    while True:
        ch = getch()
        ch_lower = ch.lower() if len(ch) == 1 else ch
        if ch_lower == 'b' or ch == '\x1b' or ch_lower == 'q' or ch_lower == '\x03' or ch == '\r' or ch == '\n':
            console.print()
            return

def show_about_screen():
    content = f"""[bold cyan]{PROJECT_NAME} (v{VERSION})[/bold cyan]
{TAGLINE}

[bold green]Purpose:[/bold green]
AuthLens is a polished, professional-grade CLI security audit suite designed for educational and defensive purposes.

[bold green]Modules:[/bold green]
"""
    for mod in MODULE_NAMES:
        content += f" - [cyan]{mod}[/cyan]\n"

    content += """
[bold green]Intended Use:[/bold green]
Educational, defensive analysis, and audit/demo context. Use responsibly on systems you own or have explicit permission to test.
"""

    panel = Panel(
        content,
        title="[bold cyan]About AuthLens[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    )
    console.print()
    console.print(panel)
    wait_for_back()

def show_help_screen():
    table = Table(title="AuthLens Help & Navigation", border_style="cyan", show_header=True, header_style="bold green")
    table.add_column("Key / Action")
    table.add_column("Description")
    
    table.add_row("1-7", "Select an option from the main menu.")
    table.add_row("b", "Go back to the previous menu.")
    table.add_row("q", "Quit the application.")
    table.add_row("CTRL+C / ESC", "Force quit safely or abort current input.")
    
    content = """[bold cyan]Workflow:[/bold cyan]
1. Generate wordlists using [cyan]PassForge[/cyan].
2. Analyze password strength with [cyan]StrengthMeter[/cyan].
3. Test authentication mechanisms using [cyan]BruteCheck[/cyan].
4. Scan and identify hashes using [cyan]HashScan[/cyan].
5. Compile findings into an [cyan]Auditor[/cyan] report.

[bold cyan]Outputs:[/bold cyan]
Results are saved to the console and to the defined output directory (`output/` by default) for easy review.

[bold cyan]Configuration:[/bold cyan]
Modify `config.json` to adjust options such as output directory or startup banner toggle.
"""
    
    console.print()
    console.print(table)
    console.print(Panel(content, border_style="cyan", padding=(1, 2)))
    wait_for_back()
