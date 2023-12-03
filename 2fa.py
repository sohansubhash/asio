import json
import click

# Load the 2fa.directory JSON file
with open("tfa.json", "r") as file:
    directory_data = json.load(file)

# Define the accounts list
accounts = []


@click.group()
def cli():
    pass


@cli.command()
def add_account():
    # Prompt user for domain or site name
    input_value = click.prompt("Enter domain or site name")

    # Find matching entries in the JSON file
    matches = [
        entry
        for entry in directory_data
        if input_value in [entry[0], entry[1]["domain"]]
    ]

    if not matches:
        click.echo("No matching entries found.")
        return

    # Display matched entries to the user
    click.echo("Matching entries:")
    for i, match in enumerate(matches, start=1):
        click.echo(f"{i}. {match[0]} ({match[1]['domain']})")

    # Prompt user to select an entry
    selected_index = click.prompt(
        "Select an entry (enter the corresponding number)", type=int, show_default=False
    )

    if selected_index < 1 or selected_index > len(matches):
        click.echo("Invalid selection.")
        return

    selected_entry = matches[selected_index - 1]

    # Transform the selected entry into the account format
    account = {
        "id": f"account_{len(accounts) + 1}",
        "name": selected_entry[0],
        "metadata": {
            "url": selected_entry[1].get(
                "url", f"https://{selected_entry[1]['domain']}"
            ),
            "documentation": selected_entry[1].get("documentation", ""),
            "recovery-documentation": selected_entry[1].get("recovery", ""),
        },
        "supports": {
            "recovery": ["email", "phone", "passphrase", "file", "codes"],
            "tfa": selected_entry[1]["tfa"],
            "notes": "",
        },
        "enabled": {tfa: [] for tfa in selected_entry[1]["tfa"]},
    }

    # Add the account to the accounts list
    accounts.append(account)

    click.echo("Account added successfully.")


@cli.command()
def pretty_print_accounts():
    # Pretty print the accounts list
    click.echo(json.dumps({"accounts": accounts}, indent=2))


if __name__ == "__main__":
    cli()
