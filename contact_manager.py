from subprocess import Popen, PIPE
import re
import os

CONTACTS_FILE = os.path.join(os.path.dirname(__file__), "files/contacts.txt")

script = '''
tell application "Contacts"
    set contactList to {}
    set allPeople to people
    repeat with aPerson in allPeople
        set q to name of aPerson as string
        if (count of phones of aPerson) is greater than 0 then
            set p to value of phone 1 of aPerson as string
        else
            set p to "No phone number"
        end if
        set contactInfo to q & ":" & p
        set end of contactList to contactInfo
    end repeat
    set AppleScript's text item delimiters to return
    set contactText to contactList as text
    contactText
end tell

'''

# Generates contacts.txt file by scraping user's contacts
def generate_contacts(fresh):
    # Run applescript
    p = Popen(['osascript'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    info, _ = p.communicate(script)

    if fresh:
        os.remove(CONTACTS_FILE)

    # Parse contact list, remove the final empty contact, remove duplicates, and sort
    contacts = info.split("\n")
    contacts = contacts[:len(contacts)-1]
    contacts = list(set(contacts))
    contacts.sort()

    # Write contacts to file
    with open(CONTACTS_FILE, 'w+') as af:

        # For each contact, parse into format "name : number" with no emojis
        for contact in contacts:
            name, number = contact.split(":")

            if not number: continue
            if number[0:2] == "+1": number = number[2:]
            number = re.sub("[^0-9]","", number)

            name = name.strip()

            af.write(f"{name} : {number}\n")

# Returns all contacts that match a certain regex
def search_contacts(search):

    matching_contacts = []
    with open(CONTACTS_FILE, 'r+') as af:
        for contact in af.readlines():
            contact = contact.lower().strip()
            search = search.lower().strip()

            # If search term not found in this contact, continue
            if not bool(re.search(search, contact)): continue

            name, number = contact.split(":")
            name = name.strip()
            number = number.strip()
            matching_contacts.append((name, number))

    return matching_contacts
