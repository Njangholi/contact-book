import os
import sys

from rich.console import Console
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

from sqlalchemy import inspect

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import SessionLocal, engine
from services.contact_service import (
    ContactServiceError,
    add_contact,
    delete_contact,
    get_contact,
    list_contacts,
    search_contacts,
    update_contact,
)


def check_databse_initialized():
    return inspect(engine).has_table("contacts")


console = Console()


def show_contacts(db):
    contacts = list_contacts(db)

    if not contacts:
        console.print("[yellow]No contacts found.[/yellow]")
        return

    table = Table(title="📒 Contacts")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Name", style="bold")
    table.add_column("Phone", style="green")
    table.add_column("Email")
    table.add_column("Category", style="magenta")

    for c in contacts:
        table.add_row(
            str(c.id),
            f"{c.first_name} {c.last_name}",
            c.phone or "-",
            c.email or "-",
            c.category or "-",
        )

    console.print(table)


def add_new_contact(db):
    console.print("[bold cyan]Add New Contact[/bold cyan]")

    first_name = Prompt.ask("First name")
    last_name = Prompt.ask("Last name", default="")
    phone = Prompt.ask("Phone")
    email = Prompt.ask("Email", default="")
    category = Prompt.ask(
        "Category", choices=["Family", "Friends", "Work", "Other"], default="Other"
    )

    try:
        add_contact(
            db,
            {
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "email": email,
                "category": category,
            },
        )
        console.print("[green]✅ Contact added successfully[/green]")

    except ContactServiceError as e:
        console.print("[red]❌ Failed to add contact:[/red]")
        for err in e.errors:
            console.print(f" • {err}")


def search_contact(db):
    query = Prompt.ask("Search query")
    results = search_contacts(db, query, [])

    if not results:
        console.print("[yellow]No matching contacts.[/yellow]")
        return

    for c in results:
        console.print(
            f"[cyan]{c.id}[/cyan] "
            f"[bold]{c.first_name} {c.last_name}[/bold] "
            f"[green]{c.phone}[/green]"
        )


def delete_contact_prompt(db):
    contact_id = IntPrompt.ask("Enter contact ID to delete")

    # contact = search_contacts(db, str(contact_id), [])
    contact = get_contact(db, contact_id)
    if not contact:
        console.print("[red]Contact not found.[/red]")
        return

    console.print(
        f"\n[bold]You are about to delete:[/bold]\n"
        f"[cyan]{contact.first_name} {contact.last_name}[/cyan] | "
        f"[green]{contact.phone}[/green]"
    )

    if Confirm.ask("Are you sure you want to delete this contact?"):

        try:
            delete_contact(db, contact.id)
            console.print("[green]🗑 Contact deleted successfully[/green]")
        except ContactServiceError as e:
            console.print("[red]❌ Error:[/red]")
            for err in e.errors:
                console.print(f" • {err}")
    else:
        console.print("[yellow]Deletion cancelled.[/yellow]")


def edit_contact_prompt(db):
    contact_id = IntPrompt.ask("Enter contact ID to edit")

    contact = get_contact(db, contact_id)
    if not contact:
        console.print("[red]Contact not found[/red]")
        return

    console.print(
        "[bold cyan]\nEdit Contact (press Enter to keep current value)\n[/bold cyan]"
    )
    first_name = Prompt.ask("First name", default=contact.first_name or "")
    last_name = Prompt.ask("Last name", default=contact.last_name or "")
    phone = Prompt.ask("Phone", default=contact.phone or "")
    email = Prompt.ask("Email", default=contact.email or "")
    category = Prompt.ask(
        "Category",
        choices=["Family", "Friends", "Work", "Other"],
        default=contact.category or "Other",
        case_sensitive=False,
    )

    data = {
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "email": email,
        "category": category,
    }

    try:
        update_contact(db, contact_id, data)
        console.print("[green]✅ Contact updated successfully[/green]")
    except ContactServiceError as e:
        console.print("[red]❌ Failed to update contact:[/red]")
        for err in e.errors:
            console.print(f" • {err}")


def main_menu():
    console.print("\n[bold magenta]📒 Contact Book CLI[/bold magenta]\n")

    console.print(
        "1️⃣  List all contacts\n"
        "2️⃣  Add new contact\n"
        "3️⃣  Search contacts\n"
        "4️⃣  Edit contact\n"
        "5️⃣  Delete contact\n"
        "6️⃣  Exit\n"
    )

    return IntPrompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6"])


def main():
    db = SessionLocal()

    while True:
        choice = main_menu()

        if choice == 1:
            show_contacts(db)
        elif choice == 2:
            add_new_contact(db)
        elif choice == 3:
            search_contact(db)
        elif choice == 4:
            edit_contact_prompt(db)
        elif choice == 5:
            delete_contact_prompt(db)
        elif choice == 6:
            console.print("[bold green]👋 Goodbye![/bold green]")
            break


if __name__ == "__main__":
    if not check_databse_initialized():
        print(
            """
            ❌ Database is not initialized.\n
            Please run the following command first:\n
            `python src/init_db.py`
            """
        )

    else:
        main()
