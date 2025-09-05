#!/usr/bin/env python3
"""
Zoho Books CLI - Management tools for Zoho Books operations
"""
from dotenv import load_dotenv

from .commands import cli


load_dotenv()
if __name__ == "__main__":
    cli()
