from apple_script import *

"""
Sends messages
messages -- list of messages to send
contacts -- list of contacts to send them to
repeat_count -- number of times to send messages.
"""
def send_messages(messages, contacts, repeat_count):
    open_status = open_application("Messages")

    if len(messages) * repeat_count > 5:
        print("No more than 5 messages while in testing phase")
        exit(1)

    for contact in contacts:
        for message in messages:
            for _ in range(repeat_count):
                if contact.startswith("."):
                    send_group_message(contact[1:], message)
                else:
                    send_user_message(contact, message)

    if open_status:
        close_application("Messages")

    return