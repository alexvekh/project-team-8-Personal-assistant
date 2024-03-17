from .classes import Record, Birthday, AddressBook, Email, Phone, Note, Note
from .check import *
from .classes import Record
from .validate import email_is_valid
from termcolor import colored
from datetime import datetime
from collections import defaultdict
from re import fullmatch




def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return "Wrong format. Use 'help' for additional imformation."
            #return f"Error: {e}"
        except KeyError:
            return "Wrong format. Use 'help' for additional imformation."
            #return "Please provide a name."
        except IndexError as e:
            return "Wrong format. Use 'help' for additional imformation."
            #return f"Error: {e}"
        except NameError as e:
            return "Wrong format. Use 'help' for additional imformation."
            #return f"Error: {e}"
        except TypeError as e:
            return "Wrong format. Use 'help' for additional imformation."
            #return f"Error: {e}"
            
    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# Phone -----------------------------------------------------------------------------
@input_error
def add_contact(args, book):
    """
    Function to add a new contact.

    Args:
        args: Command line arguments.
        book: Dictionary with contacts.

    Returns:
        String with information about the addition result.
    """
    name, phone = args
    if len(phone) != 10 or not phone.isdigit():
        return colored("Error: Invalid phone number format. Please enter a 10-digit number.", 'red', attrs=['bold'])
    
    record = Record(name)
    record.add_phone(phone)
    book[name] = record
    return colored("✅ Contact added.", 'green', attrs=['bold'])


def show_phone(args, book):
    (name,) = args
    if name in book:
        record = book[name]

        res = []
        for phone in record.phones:
            res.append(phone.value)
        return f"{name}: {','.join(res)}"
    else:
        return colored("Sorry, {name} doesn't exist. Use 'add' to append this contact.", 'red', attrs=['bold'])


@input_error
def change_contact(args, book):
    """
    Function to change an existing contact.

    Args:
        args: Command line arguments.
        book: Dictionary with contacts.

    Returns:
        String with information about the change result.
    """
    name, field, new_value = args
    if name in book:
        record = book[name]
        if field == "phone":
            record.phones = [Phone(new_value)]
        elif field == "birthday":
            record.birthday = Birthday(new_value)
        elif field == "email":
            record.emails = [Email(new_value)]
        elif field == "note":
            record.note = new_value
        return colored(f"\U0001F4DD Contact {name} updated.", 'cyan', attrs=['bold'])
    else:
        return colored(f"\U000026D4 Sorry, {name} not found.", 'red', attrs=['bold'])



def get_phones(record):  # Service for get phones from record
    res = []
    for phone in record.phones:
        res.append(phone.value)
    if res[0]:
        return ",".join(res)
    else:
       return colored("📵 No phone", 'yellow', attrs=['bold'])


# # Find ----------------------------------------------------------------
# @input_error
# def find_contacts(book, field, value):
#     """
#     Function to search for contacts by a given field and value.

#     Args:
#         book: Dictionary with contacts.
#         field: Field to search by (name, phone, birthday, email).
#         value: Value to search for.

#     Returns:
#         List of strings with information about found contacts.
#     """

#     found_contacts_info = []
#     if field == "name":
#         found_contacts = [record for record in book.values() if record.name.lower() == value.lower()]
#     elif field == "phone":
#         found_contacts = [
#             record
#             for record in book.values()
#             if value in [phone.value for phone in record.phones]
#         ]
#     elif field == "birthday":
#         found_contacts = [
#             record
#             for record in book.values()
#             if record.birthday and record.birthday.value.strftime("%d.%m.%Y") == value
#         ]
#     elif field == "email":
#         found_contacts = [
#             record
#             for record in book.values()
#             if value in [email.value for email in record.emails]
#         ]
#     else:
#         found_contacts = []

#     for record in found_contacts:
#         contact_info = f"{record.name}:"
#         contact_info += f"  Phones: {get_phones(record)}"
#         contact_info += f"  Emails: {get_emails(record)}"
#         contact_info += f"  Birthday: {record.birthday.value.strftime('%d.%m.%Y') if record.birthday else 'Not set'}"
#         contact_info += f"  Note: {record.note if record.note else 'No note'}"
#         found_contacts_info.append(contact_info)

#     return found_contacts_info


# def show_found_contacts(contacts):
#     """
#     Function to display information about found contacts.

#     Args:
#         contacts: List of found contacts.

#     Returns:
#         String with information about found contacts.
#     """
#     res = []
#     for record in contacts:
#         res.append(f"{record.name}:")
#         res.append(f"  Phones: {get_phones(record)}")
#         res.append(f"  Emails: {get_emails(record)}")
#         res.append(
#             f"  Birthday: {record.birthday.value.strftime('%d.%m.%Y') if record.birthday else 'Not set'}"
#         )
#         res.append(f"  Note: {record.note if record.note else 'No note'}")
#     return "\n".join(res)


# @input_error
# def find_contact_by_field(args, book):
#     """
#     Function to find a contact by a specified field and value.

#     Args:
#         args: Command line arguments.
#         book: Dictionary with contacts.

#     Returns:
#         String with information about the found contact.
#     """
#     field, value = args
#     found_contacts = find_contacts(book, field, value)
#     if found_contacts:
#         return show_found_contacts(found_contacts)
#     else:
        # return f"No contacts found by {field} with value {value}."


# @input_error
# def change_contact_field(args, book):
#     """
#     Function to change a specified field of a contact.

#     Args:
#         args: Command line arguments.
#         book: Dictionary with contacts.

#     Returns:
#         String with information about the change result.
#     """
#     name, field, new_value = args
#     if name in book:
#         record = book[name]
#         if field == "phone":
#             record.phones = [Phone(new_value)]
#         elif field == "birthday":
#             record.birthday = Birthday(new_value)
#         elif field == "email":
#             record.emails = [Email(new_value)]
#         elif field == "note":
#             record.note = new_value
#         return f"Contact {name} updated."
#     else:
#         return "Sorry, {name} doesn't exist. Use 'add' for append this contact."


@input_error
def show_all(book):
# ============= was table format ==============================================
#     res = []
#     res.append("{:^20}".format("CONTACTS"))
#     res.append("{:^20}".format("-" * 10))
#     for name, record in book.items():
#         res.append("{:<14} {:<14}".format(name + ":", get_phones(record)))
#     res.append("{:^20}".format("=" * 20))
# =============================================================================
    res = ["{:^60}".format("CONTACTS"), "{:-^60}".format("")]
    for name, record in book.items():
        emails = ", ".join(email.value for email in record.emails) or "No Email"
        phones = ", ".join(phone.value for phone in record.phones) or "No Phone"
        birthday = record.birthday.value.strftime('%d.%m.%Y') if record.birthday else "No Birthday"
        addresses = "; ".join(f"{address.street}, {address.house_number}, {address.city}, {address.postal_code if address.postal_code else ''}, {address.country if address.country else ''}" for address in record.addresses) or "No Address"
        money = book[name].money
        
        contact_info = f"👤 Name: {name}\n📞 Phone: {phones}\n📧 Email: {emails}\n🎂 Birthday: {birthday}\n🏠 Address: {addresses}\n💰 Money: {money} dollars"
        res.append(contact_info)
        res.append("{:-^60}".format(""))  # Додав розділювач між контактами
    return "\n".join(res)

@input_error
def show_table(book):
# ============= was table format ==============================================
#     res = []
#     res.append("{:^20}".format("CONTACTS"))
#     res.append("{:^20}".format("-" * 10))
#     for name, record in book.items():
#         res.append("{:<14} {:<14}".format(name + ":", get_phones(record)))
#     res.append("{:^20}".format("=" * 20))
# =============================================================================
    res = ["{:^60}".format("CONTACTS"), "{:-^60}".format("")]
    for name, record in book.items():
        emails = ", ".join(email.value for email in record.emails) or "No Email"
        phones = ", ".join(phone.value for phone in record.phones) or "No Phone"
        birthday = record.birthday.value.strftime('%d.%m.%Y') if record.birthday else "No Birthday"
        addresses = "; ".join(f"{address.street}, {address.house_number}, {address.city}, {address.postal_code if address.postal_code else ''}, {address.country if address.country else ''}" for address in record.addresses) or "No Address"
        money = book[name].money
        
        contact_info = f"👤 Name: {name}\n📞 Phone: {phones}\n📧 Email: {emails}\n🎂 Birthday: {birthday}\n🏠 Address: {addresses}\n💰 Money: {money} dollars"
        res.append(contact_info)
        res.append("{:-^60}".format(""))  # Додав розділювач між контактами
    return "\n".join(res)

# Find contact info by name ------------------------------------------------
@input_error
def find(args, book):
    name = args[0]
    if name in book:
        emails = ", ".join(email.value for email in book[name].emails) or "No Email"
        phones = ", ".join(phone.value for phone in book[name].phones) or "No Phone"
        birthday = book[name].birthday.value.strftime('%d.%m.%Y') if book[name].birthday else "No Birthday"
        addresses = "; ".join(f"{address.street}, {address.house_number}, {address.city}, {address.postal_code if address.postal_code else ''}, {address.country if address.country else ''}" for address in book[name].addresses) or "No Address"
        money = book[name].money
        
        contact_info = f"Name: {name}\nPhone: {phones}\nEmail: {emails}\nBirthday: {birthday}\nAddress: {addresses}\nMoney: {money} dollars"
        return contact_info
    else:
        return colored(f"\U000026D4 Contact {name}  not found.", 'red', attrs=['bold'])

# Birthday ----------------------------------------------------------------
@input_error
def add_birthday(args, book):
    name, birthday = args
    if name in book:
        record = book[name]
        record.add_birthday(birthday)
        return colored(f"🎉 {name}'s birthday added", 'green', attrs=['bold'])
    else:
        return colored(f"❌ Sorry, {name} doesn't exist. Use 'add' to add this contact.", 'red', attrs=['bold'])


@input_error
def show_birthday(args, book):
    (name,) = args
    if name in book:
        record = book[name]
        if record.birthday != None:
            birthday = record.birthday.value.strftime("%d.%m.%Y")
            return colored(f"🎂 {name}'s birthday is {birthday}", 'cyan', attrs=['bold'])
        else:
            return colored(f"❓ {name}'s birthday isn't recorded", 'yellow', attrs=['bold'])
    else:
        return colored(f"❌ Sorry, {name} doesn't exist. \nUse 'add' to add this contact to the book.", 'red', attrs=['bold'])

@input_error
def change_birthday(args, book):
    name, birthday = args
    if name in book:
        record = book[name]
        record.add_birthday(birthday)
        return colored(f"🔄 {name}'s birthday changed", 'green', attrs=['bold'])
    else:
        return colored(f"❌ Sorry, {name} doesn't exist.", 'red', attrs=['bold'])

@input_error
def delete_birthday(args, book):
    (name,) = args
    if name in book:
        record = book[name]
        if record.birthday != None:
            res = record.remove_birthday()
            return res
        else:
            return colored(f"🚫 No birthday for {name}", 'yellow', attrs=['bold'])
    else:
        return colored(f"❌ Sorry, {name} doesn't exist. \nUse 'add' to add this contact to book.", 'red', attrs=['bold'])

@input_error
def birthdays(args, book):
    if args:
        days = args[0]
        book.get_birthdays_by_days(days)
    else:
        book.get_birthdays_per_week()


# Email  ----------------------------------------------------------------------
@input_error        
def get_emails(record):
    """
    Function to retrieve emails from a record.

    Args:
        record: Record object.

    Returns:
        String with email addresses.
    """
    res = [email.value for email in record.emails]
    if res:
        return ",".join(res)
    else:
        return "Sorry, {name} doesn't exist. Use 'add' to append this contact." 


# "add-email name email": "adding email to existing contact"
@input_error
def add_email(args, book):
    """
    Function to add an email to a contact record.

    Args:
        args (tuple): A tuple containing the name (str) and email (str) to add.
        book (dict): A dictionary representing the address book.

    Returns:
        str: A confirmation message of adding the email.

    Raises:
        ValueError: If the input arguments are not in the correct format.
    """
    name, email = args
    if name in book:
        record = book[name]
        record.emails.append(Email(email))
        return colored(f"✅ {name}'s email added successfully", 'green', attrs=['bold'])
    else:
        return colored(f"❌ Sorry, {name} doesn't exist. \nUse 'add' to add this contact to the book.", 'red', attrs=['bold'])

# "email name": "get email of specific contact"
@input_error
def show_email(args, book):
    """
    Function to get the email of a specific contact.

    Args:
        args (tuple): A tuple containing the name (str) of the contact.
        book (dict): A dictionary representing the address book.

    Returns:
        str: A string containing the contact's name and their email(s).

    Raises:
        ValueError: If the input arguments are not in the correct format.
    """

    name = args[0]

    if name in book:
        record = book[name]
        res = []
        for email in record.emails:
            res.append(email.value)
        return f"{name}: {','.join(res)}"
    else:

        return colored(f"❌ Sorry, {name} doesn't exist. \nUse 'add' to add this contact to the book.", 'red', attrs=['bold'])
    
@input_error
def change_email(args, book):
    name = args[0]
    if name in book:
        if book[name].emails:
            for number, email in enumerate(book[name].emails, 1):
                print(f"{number}: {email}")
            while True:
                answer = input("Type the number of email you want to change ===>  ")
                if answer.isdigit() and 1 <= int(answer) <= len(book[name].emails):
                    while True:
                        new_email = input("Enter new email ==>  ")
                        if email_is_valid(new_email):
                            book[name].emails[int(answer)-1] = Email(new_email)
                            return colored("Email has been changed.", 'green', attrs=['bold'])
                        else:
                            print(colored("Seems like this email is incorrect. Try again.", 'red'))
                else:
                    print(colored(f"Must be the number between 1 and {len(book[name].emails)}", 'red'))
        else:
            return colored("Contact has no emails.", 'red')
    else:
        return colored("No such contact.", 'red')

# "change-email name email": "changing email of existing contact"
@input_error
def delete_email(args, book):
    """
    Function to delete an email from an existing contact.

    Args:
        args (tuple): A tuple containing the name (str) of the contact and the email (str) to delete.
        book (dict): A dictionary representing the address book.

    Returns:
        str: A confirmation message of deleting the email.

    Raises:
        ValueError: If the input arguments are not in the correct format.
    """
    name, email_to_delete = args
    if name in book:
        record = book[name]
        for email in record.emails:
            if email.value == email_to_delete:
                record.emails.remove(email)
                return colored(f"🗑️ Email {email_to_delete} deleted from {name}'s contacts.", 'green', attrs=['bold'])
        return colored(f"🔍 Email {email_to_delete} not found in {name}'s contacts.", 'yellow', attrs=['bold'])
    else:
         print(colored(f"🚫 Sorry, {name} doesn't exist. Use 'add' to append this contact.", 'red', attrs=['bold']))


# Address -----------------------------------------------------------------
@input_error
def add_address(args, book):
    name, street, house_number, city, postal_code, country = args
    if name in book.data:
        record = book.data[name]
        record.add_address(street, house_number, city, postal_code, country)
        return colored("🏠 Address added.", 'green', attrs=['bold'])
    else:
        return colored("🚫 Contact does not exist.", 'red', attrs=['bold'])


@input_error
def show_address(args, book):
    name = args[0]
    if name in book.data:
        record = book.data[name]
        addresses = record.addresses
        if addresses:
            address_str = "\n".join([f"{address}" for address in addresses])
            return colored(f"🏠 Addresses for {name}:\n{address_str}", 'blue', attrs=['bold'])
        else:
            return colored(f"❌ No addresses found for {name}.", 'red')

    else:
        return colored("❌ Contact does not exist.", 'red')


def edit_address(args, book):
    name, street, house_number, city, postal_code, country = args
    if name in book.data:
        record = book.data[name]
        record.edit_address(street, house_number, city, postal_code, country)
        return colored("Address edited.", 'green', attrs=['bold'])
    else:
        return colored("❌ Contact does not exist.", 'red')


def remove_address(args, book):
    (name,) = args
    if name in book.data:
        record = book.data[name]
        record.remove_address()
        return colored("🗑️ Address removed.", 'yellow', attrs=['bold'])
    else:
        return colored("❌ Contact does not exist.", 'red')


# Note --------------------------------------------------------------------


def new_note(notes):
    while True:
        title = input("Type the title here ===>  ")
        if title:
            break
        else:
            print("Title cannot be empty.")
            continue
    text = input("Type the text here ===>  ")
    while True:
        tags = input(
            "Type tags here (for example: <#tag1> <#multiple_word_tag_2> <#tag3>)  ===>  "
        ).split()
        if all(fullmatch(r"\#\w+", tag) for tag in tags):
            notes.append(Note(title, text, tags))
            return "Note has been added"
        else:
            print("Wrong format.")


def edit_note(notes):
    if notes:
        note = find_note(notes)
        answer = input(
            "Type <y> if you want to change the title or any else key to continue ===>  "
        )
        if answer == "y":
            note.data["title"] = input("Type the new title here ===>  ")
        answer = input(
            "Type <y> if you want to change the text or any else key to continue ===>  "
        )
        if answer == "y":
            note.data["text"] = input("Type the new text here ===>  ")
        answer = input(
            "Type <y> if you want to change tags or any else key to continue ===>  "
        )
        if answer == "y":
            while True:
                tags = input(
                    "Type tags here (for example: <#tag1> <#multiple_word_tag_2> <#tag3>)  ===>  "
                ).split()
                if all(fullmatch(r"\#\w+", tag) for tag in tags):
                    note.data["tags"] = tags
                    break
                else:
                    print("Wrong format.")
        return "Note has been edited."
    return "No notes added."


def delete_note(notes):
    if notes:
        note = find_note(notes)
        del notes[notes.index(note)]
        return "Note has been deleted."
    return "No notes added."


def find_note(notes):
    note_dict = dict(zip(range(1, len(notes) + 1), notes))
    for number, note in note_dict.items():
        print(str(number) + ": " + note.data["title"])
    while True:
        answer = input("Type the number of note ===>  ")
        if answer.isdigit() and 1 <= int(answer) <= len(notes):
            return notes[int(answer) - 1]
        else:
            print(f"Must be the number between 1 and {len(notes)}")
            continue


def show_notes(notes):
    if notes:
        while True:
            answer = input(
                "What are we looking for? (a for all notes and s for specific) a/s ===>  "
            )
            if answer == "a":
                notes_to_print = notes
                return "\n".join(str(note) for note in notes_to_print)
            elif answer == "s":
                while True:
                    key = input(
                        "What element do you want to search by? (title/text/tags) ===>  "
                    )
                    if key in ("title", "text"):
                        element = input(f"Type the {key} you want to look for ===>  ")
                        notes_to_print = tuple(
                            filter(lambda note: element in note.data[key], notes)
                        )
                        return (
                            "\n".join(str(note) for note in notes_to_print)
                            if notes_to_print
                            else "No such notes."
                        )
                    elif key == "tags":
                        while True:
                            tags = input(
                                "Type the tag(s) you want to look for (for example: <#tag1> <#multiple_word_tag_2> <#tag3>)  ===>  "
                            ).split()
                            if all(fullmatch(r"\#\w+", tag) for tag in tags):
                                break
                            else:
                                print("Wrong format.")
                                continue
                        notes_to_print = tuple(
                            filter(
                                lambda note: all(
                                    tag in note.data["tags"] for tag in tags
                                ),
                                notes,
                            )
                        )
                        return (
                            "\n".join(str(note) for note in notes_to_print)
                            if notes_to_print
                            else "No such notes."
                        )
                    else:
                        print("Wrong format.")
                        continue
            else:
                print("Wrong format.")
                continue
    else:
        return "No notes added."

# Money -----------------------------------------------------------------------------
@input_error
def deposit(args, book):
    name, amount = args
    if name in book:
        if amount.isdigit() and int(amount) > 0:
            amount = int(amount)
            record = book[name]
            record.deposit(amount)
            return "Deposit successful."
        else:
            return "Invalid amount."
    else:
        return "No such contact."
    
@input_error
def withdraw(args, book):
    name, amount = args
    if name in book:
        if amount.isdigit() and int(amount) > 0:
            amount = int(amount)
            record = book[name]
            if record.money >= amount:
                record.withdraw(amount)
                return "Withdraw successful."
            else:
                return "You cannot withdraw more than you have."
        else:
            return "Invalid amount."
    else:
        return "No such contact."
@input_error
def get_money(args, book):
    name = args[0]
    if name in book:
        return f"{name} has {book[name].money} dollars."
    else:
        return "No such contact."
    
def bank(book):
    return sum(book[name].money for name in book)
        

def show_commands():
   
    groups = {
        "General Commands": {
            "help": "Display all available commands.",
            "exit": "Exit the program."
        },
        "Contact Management": {
            "add [name] [phone]": "Add a new contact.",
            "delete [name]": "Delete an existing contact.",
            "change [name] [existing phone][new phone]": "Change the phone number of an existing contact.",
            "all": "Display all contacts."
        },
        "Phone Management": {
            "phone [name]": "Display the phone number of a specific contact."
        },
        "Birthday Management": {
            "add-birthday [name] [birthday]": "Add a birthday for a contact.",
            "show-birthday [name]": "Show the birthday of a specific contact.",
            "change-birthday [name] [new birthday]": "Change birthday for your contact",
            "delete-birthday [name]": "Delete a contact's birthday."
        },
        "Email Management": {
            "add-email [name] [email]": "Add an email to a contact.",
            "email [name]": "Show the email of a specific contact.",
            "change-email [name]": "Update your contact's email.",
            "delete-email [name]": "Remove an email from a contact."
        },
        "Address Management": {
            "add-address [name] [street] [house_number] [city] [postal_code] [country]": "Add an address to a contact.",
            "change-address [name] [new details]": "Edit an existing address.",
            "show-address [name]": "Display the address of a specific contact.",
            "delete-address [name]": "Delete an address from a contact."
        },
        "Note Management": {
            "add-note": "Add a note to a contact.",
            "show-notes": "Display notes all or specific note.",
            "edit-note": "Edit an already existing note.",
            "delete-note": "Remove a note."
        },
        "Money Management": {
        "deposit [name] [amount]": "deposit to person`s wallet",
        "withdraw [name] [amount]": "withdraw from person`s wallet",
        "money [name]": "show current person`s wallet balance",
        "bank": "show sum of all wallets"
        }
        }

    for group_name, commands in groups.items():
        print(f"\n{group_name}:")
        for command, description in commands.items():
            print(f"  {command:40} - {description}")
    return ''

@input_error
def delete(args, book):
    if len(args) == 1:  # if in args 1 arg
        arg = args[0]  # get arg from []
        res = book.delete(arg)
        return res
    elif len(args) == 2:
        name, field = args
        record = book.find(name)
        if field == "phones":
            res = record.remove_phones()
            return res
        elif field == "birthday":
            res = record.remove_birthday()
            return res
        elif field == "email":
            res = record.remove_email()
            return res
        elif field == "address":
            res = record.remove_address()
            return res
        elif field == "notes":
            res = record.remove_notes()
            return res


## --------- Не стирать, колись продовжу --------------------------------
# @input_error
# def find(args, book):
#     print(f"шукати {args}")
#     arg = args[0]
#     if is_looks_date(arg):    # якщо arg схожий на дату
#         print(f"Функція буде шукати date {arg}")
#         for record in book.values():
#             print("record", record)
#     #   record виводить
#             if record.birthday:
#                 print(record.birthday, record.birthday.value, arg, Birthday(arg))
#                 print(type(record.birthday), type(record.birthday.value), type(arg), type(Birthday(arg)))
#                 if Birthday(arg) == record.birthday:
#                     print(True)
# # Треба порівняти birthday з arg і вивести records де це співпада
#     elif is_looks_phone(arg):
#         print(f"Функція буде шукати phone {arg}")
#         #book.find_in_field("phone", arg)
#     elif is_looks_email(arg):
#         print(f"Функція буде шукати email {arg}")
#         #book.find_in_field("email", arg)
#     # Address not aveilable to check:
#     # name
#     else:
#         return "Contact does not exist."

###----------------------------------------------------------------------------

