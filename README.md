# Zoho Books CLI

A command-line interface for managing Zoho Books data, including item management and invoice renumbering operations.

## Project Structure

```
zoho-scripts/
├── pyproject.toml                    # Poetry configuration
├── zoho/                     # Main package
│   ├── __init__.py                   # Package initialization
│   ├── __main__.py                  # CLI entry point
│   ├── config.py                    # Configuration settings
│   ├── client.py                    # Base Zoho Books API client
│   └── managers.py                  # Specialized managers
└── README.md                        # This file
```

## Installation

### Using Poetry (Recommended)

1. Install Poetry if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install dependencies and set up the project:
   ```bash
   poetry install
   ```

3. Configure the CLI:
   ```bash
   poetry run zoho config setup
   ```

## Usage

The CLI provides a unified interface for all Zoho Books operations:

```bash
# Show help
zoho --help

# Show version
zoho --version
```

### Configuration Management

```bash
# Interactive setup (first time)
zoho config setup

# Force reconfiguration
zoho config setup --force

# Validate current configuration
zoho config validate

# Validate API credentials specifically
zoho config validate-credentials

# Validate specific credentials
zoho config validate-credentials --client-id "your_id" --client-secret "your_secret"

# Show current configuration
zoho config show

# Show configuration with secrets
zoho config show --show-secrets

# Reset configuration
zoho config reset
```

### Item Management

```bash
# List all items
zoho items list

# List items with specific name
zoho items list --name "Plywood"

# List items containing text
zoho items list --contains "Wood"

# Limit results
zoho items list --limit 10

# Process items with OLD suffix (default)
zoho items process-old

# Process items with custom suffix
zoho items process-old "ARCHIVED"
```

### Invoice Management

```bash
# List all invoices
zoho invoices list

# List invoices by status
zoho invoices list --status sent

# Limit results
zoho invoices list --limit 5

# Analyze invoice numbering (dry run by default)
zoho invoices renumber

# Renumber invoices with custom settings
zoho invoices renumber --start-number 1000 --prefix "INV" --suffix "-2024"

# Apply renumbering (remove dry run)
zoho invoices renumber --no-dry-run

# Filter by status and apply
zoho invoices renumber --status-filter sent --no-dry-run
```

## Features

### Item Operations
- ✅ List and filter items
- ✅ Process items with OLD suffix
- ✅ Update related bills and invoices
- ✅ Create new items with proper settings
- ✅ Comprehensive error handling

### Invoice Operations
- ✅ List and filter invoices
- ✅ Analyze current numbering patterns
- ✅ Identify gaps in invoice numbering
- ✅ Sequential renumbering with custom formatting
- ✅ Dry-run mode for safety
- ✅ Status-based filtering

## Configuration

The CLI uses a comprehensive configuration system with multiple sources:

### Configuration Sources (in order of precedence):
1. **Environment Variables** - Highest priority
2. **Configuration File** - `~/.zoho/config.ini`
3. **Default Values** - Built-in defaults

### Environment Variables:
```bash
export ZOHO_CLIENT_ID="your_client_id"
export ZOHO_CLIENT_SECRET="your_client_secret"
export ZOHO_REFRESH_TOKEN="your_refresh_token"
export ZOHO_ORG_ID="your_org_id"
export ZOHO_TARGET_ACCOUNT_ID="your_target_account_id"
```

### Configuration File Format:
```ini
[zoho]
client_id = your_client_id
client_secret = your_client_secret
refresh_token = your_refresh_token
org_id = your_org_id
target_account_id = your_target_account_id
accounts_base_url = https://accounts.zoho.com
books_base_url = https://books.zoho.com
inventory_account_name = Inventory Asset
```

### Interactive Setup Process:
1. **API Credentials** - Enter your Zoho API Client ID and Secret (with validation)
2. **OAuth Authorization** - Complete the OAuth flow to get refresh token (or reuse existing valid token)
3. **Organization Selection** - Choose your Zoho Books organization (with existing selection as default)
4. **Account Selection** - Select the target inventory account (with existing selection as default)
5. **Validation** - Test the configuration and API connection

### Credential Validation:
The CLI includes comprehensive credential validation:
- **Format validation** - Checks credential length and format
- **API validation** - Tests credentials against Zoho's API
- **Token validation** - Verifies refresh tokens are still valid
- **Standalone validation** - Use `validate-credentials` command to test credentials independently

## Development

### Code Organization

The project follows a modular architecture with clear separation of concerns:

- **`zoho/__main__.py`**: CLI entry point and command group registration
- **`zoho/commands/`**: Modular command organization
  - **`items/`**: Item management commands (`list`, `process-old`)
  - **`invoices/`**: Invoice management commands (`list`, `renumber`)
  - **`config/`**: Configuration management commands (`setup`, `validate`, `show`, `reset`)
- **`zoho/settings.py`**: Type-safe configuration with Pydantic
- **`zoho/client.py`**: Base API client with authentication
- **`zoho/managers.py`**: Business logic for specific entities

### Adding New Commands

To add a new command:

1. Create a new command file in the appropriate directory:
   ```python
   # zoho/commands/items/new_command.py
   import click
   from ...managers import ItemManager

   @click.command()
   def new_command():
       """Description of the new command."""
       # Command implementation
   ```

2. Register the command in the group's `__init__.py`:
   ```python
   # zoho/commands/items/__init__.py
   from .new_command import new_command
   items.add_command(new_command)
   ```

### Testing

```bash
# Test the CLI
poetry run zoho --help

# Test specific command groups
poetry run zoho items --help
poetry run zoho invoices --help
poetry run zoho config --help

# Test individual commands
poetry run zoho config show
poetry run zoho items list --limit 5
```

## Architecture

```
CLI (Click) → Commands → Settings (Pydantic) → Managers → Client → Zoho Books API
```

- **CLI Layer**: User interface with Click commands
- **Commands Layer**: Modular command organization by functionality
- **Settings Layer**: Type-safe configuration with Pydantic
- **Manager Layer**: Business logic for specific entities
- **Client Layer**: Base API client with authentication
- **Configuration Layer**: Multi-source config management

### Project Structure

```
zoho-scripts/
├── pyproject.toml              # Poetry + dependencies
├── zoho/
│   ├── __init__.py            # Package initialization
│   ├── __main__.py            # CLI entry point
│   ├── settings.py             # Configuration management
│   ├── client.py               # API client
│   ├── managers.py             # Business logic
│   └── commands/               # Command modules
│       ├── __init__.py         # Command groups
│       ├── items/              # Item management commands
│       │   └── __init__.py     # list, process-old
│       ├── invoices/           # Invoice management commands
│       │   └── __init__.py     # list, renumber
│       └── config/              # Configuration commands
│           └── __init__.py     # setup, validate, show, reset
├── env.example                 # Environment template
└── README.md                   # Documentation
```

## Error Handling

The CLI includes comprehensive error handling:

- API errors are captured and categorized
- Detailed error reporting with context
- Graceful handling of network issues
- Transaction safety with dry-run modes

## Security Notes

- API credentials are stored in `~/.zoho/config.ini` - consider using environment variables for production
- All destructive operations include dry-run modes
- Always test with a small dataset before running on production data
- Refresh tokens are automatically managed and refreshed

## Contributing

When adding new functionality:

1. Follow the existing architecture pattern
2. Add comprehensive error handling
3. Include dry-run capabilities for destructive operations
4. Update documentation and help text
5. Add tests for new functionality
