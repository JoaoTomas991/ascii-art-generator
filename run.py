#!/usr/bin/env python3
"""
ASCII Generator - Start Script

This script allows starting the ASCII Generator project in multiple ways:

1. Normal mode (menu): python run.py
2. Intelligent mode: python run.py --intelligent
3. Direct command: python run.py "draw a heart"
4. With options: python run.py --command "draw a rectangle 10x5" --color blue

Examples:
    python run.py                            # Main menu
    python run.py --intelligent              # Interactive intelligent mode
    python run.py "draw a heart"             # Execute command and exit
    python run.py "make a circle with radius 8"  # Execute command and exit
    python run.py "write HELLO with font banner"  # Execute command and exit
"""

import sys
import argparse
from ascii_art_generator.console import enable_utf8_output
from ascii_art_generator.main import main as cli_main
from ascii_art_generator.cli import setup_console


def run_intelligent_mode():
    """Run in intelligent mode with pre-activated English command parsing."""
    # Simulate pressing 'i' to enter intelligent mode
    sys.argv = ['ascii_art_generator', 'i']
    try:
        cli_main()
    except SystemExit:
        pass


def run_command(command: str):
    """Execute a single command in intelligent mode."""
    from ascii_art_generator.cli import ASCIIArtCLI
    
    cli = ASCIIArtCLI()
    cli.intelligent_mode = True

    # "teach <word> as <mood>" isn't parsed like a drawing command - it's
    # handled directly here too (not just in the intelligent-mode REPL) so
    # a learned word can be taught and used across two separate one-shot
    # invocations, since it persists to disk (see learned_words.py).
    if command.lower().strip().startswith('teach '):
        cli._handle_teach_command(command.strip())
        return

    # Parse and execute the command
    parsed = cli.parser.parse_command(command)
    
    if parsed:
        cli.execute_parsed_command(parsed)
    else:
        print("Could not understand the command. Try:")
        print("  - draw a heart")
        print("  - make a rectangle 10x5")
        print("  - write HELLO with font banner")


def main():
    """Main entry point."""
    # run_command() below bypasses cli.main(), so this entry point has to set
    # the output encoding up itself (see ascii_art_generator/console.py).
    enable_utf8_output()

    parser = argparse.ArgumentParser(
        description='ASCII Generator - Command Line Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                           # Interactive menu
  python run.py --intelligent             # Intelligent mode
  python run.py "draw a heart"            # Execute command
  python run.py --command "make a circle" # With options

Supported Commands:
  Shapes: draw a rectangle, make a circle, create a triangle
  Text: write HELLO, convert TEXT to ascii
  Patterns: make a checkerboard, generate a gradient
  Colors: color red, color blue, color green
  Fonts: font small, font block, font banner
  Styles: style dotted, style empty
        """
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        default='',
        help='Command in English (e.g., "draw a heart")'
    )
    
    parser.add_argument(
        '-i', '--intelligent',
        action='store_true',
        help='Activate interactive intelligent mode'
    )
    
    parser.add_argument(
        '-c', '--command',
        dest='command_option',
        type=str,
        default='',
        help='Command to execute (alternative to positional argument)'
    )
    
    parser.add_argument(
        '--color',
        type=str,
        default=None,
        help='Color to apply (red, blue, green, etc.)'
    )
    
    parser.add_argument(
        '--font',
        type=str,
        default=None,
        help='Font to use (small, block, banner, shadow)'
    )
    
    parser.add_argument(
        '--size',
        type=int,
        default=None,
        help='Size (for simple shapes)'
    )
    
    parser.add_argument(
        '--width',
        type=int,
        default=None,
        help='Width (for rectangles)'
    )
    
    parser.add_argument(
        '--height',
        type=int,
        default=None,
        help='Height (for rectangles)'
    )
    
    parser.add_argument(
        '--radius',
        type=int,
        default=None,
        help='Radius (for circles and spirals)'
    )
    
    args = parser.parse_args()
    setup_console()
    
    # Build command from arguments
    command = args.command or args.command_option
    
    if args.intelligent:
        # Run in intelligent mode
        run_intelligent_mode()
    elif command:
        # Add additional parameters to command
        parts = [command]
        if args.color:
            parts.append(f"color {args.color}")
        if args.font:
            parts.append(f"font {args.font}")
        if args.size:
            parts.append(f"size {args.size}")
        if args.width:
            parts.append(f"width {args.width}")
        if args.height:
            parts.append(f"height {args.height}")
        if args.radius:
            parts.append(f"radius {args.radius}")
        
        full_command = ' '.join(parts)
        run_command(full_command)
    else:
        # Run normal CLI
        try:
            cli_main()
        except SystemExit:
            pass


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception:
        # A standalone executable (PyInstaller) started by double-click runs
        # in its own console window, which would close before the error
        # could be read - keep it open until the user presses Enter.
        if getattr(sys, 'frozen', False) and len(sys.argv) == 1:
            import traceback
            traceback.print_exc()
            input("\nPress Enter to close...")
        raise
