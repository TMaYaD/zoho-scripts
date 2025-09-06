"""
Interactive configuration setup command
"""

import click
import os
from ...settings import Settings
from ...client import client
from .org import org


@click.command()
@click.pass_context
def setup(ctx):
    """Interactively set up configuration and create .env file."""

    click.echo("🔧 Zoho Books Configuration Setup")
    click.echo("=" * 40)
    click.echo()

    # Check if .env already exists
    if os.path.exists(".env"):
        if not click.confirm("⚠️  .env file already exists. Do you want to overwrite it?"):
            click.echo("Setup cancelled.")
            return

    click.echo("Please provide your Zoho Books API credentials:")
    click.echo("(You can get these from https://api-console.zoho.com/)")
    click.echo()

    # Collect configuration values interactively
    client_id = click.prompt("Client ID", type=str)
    client_secret = click.prompt("Client Secret", type=str)

    click.echo()
    click.echo("🔐 Testing Self Client credentials...")
    click.echo("This will validate your credentials and test API access.")
    click.echo()

    try:
        # Test Self Client credentials by getting an access token
        click.echo("🔄 Testing credentials with Zoho API...")
        token_data = client.get_self_client_access_token(client_id, client_secret)

        click.echo("✅ Successfully authenticated with Zoho API!")
        click.echo(f"  Access token obtained (expires in {token_data['expires_in']} seconds)")
        click.echo(f"  API Domain: {token_data['api_domain']}")
        click.echo()

        # Show summary before saving
        click.echo("Configuration Summary:")
        click.echo(f"  Client ID: {client_id[:8]}...")
        click.echo(f"  Client Secret: {client_secret[:8]}...")
        click.echo("  Authentication: Self Client (no refresh token needed)")
        click.echo()

    except ValueError as e:
        click.echo(f"❌ Authentication failed: {str(e)}")
        click.echo("Please check your Client ID and Client Secret, then try again.")
        click.echo("Make sure you have created a Self Client in the Zoho Developer Console.")
        return

    if click.confirm("Save this configuration to .env file?"):
        # Create Settings instance and save
        settings = Settings(client_id, client_secret)
        settings.save()

        click.echo("✅ Configuration saved successfully!")
        click.echo()

        # Call config org to select organization
        click.echo("Now let's select your organization:")
        ctx.invoke(org)

        click.echo("✅ Setup complete! You can now use the Zoho Books CLI commands.")
    else:
        click.echo("Setup cancelled.")
