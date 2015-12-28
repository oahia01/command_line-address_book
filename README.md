# command_line-address_book

Implementation: script for creating and maintaining a command-line-controlled address book

usage: address_book.py [-h] [-a C [C ...] | -s SEARCH_CONTACTS
                       [SEARCH_CONTACTS ...] | -m MODIFY_CONTACTS
                       [MODIFY_CONTACTS ...] | -d DEL_CONTACTS
                       [DEL_CONTACTS ...] | -sh | -cl]

optional arguments:
  -h, --help            show this help message and exit
  -a C [C ...], --add_contact C [C ...]
                        Add contacts to address book: name {space}
                        email,{space} phone
  -s SEARCH_CONTACTS [SEARCH_CONTACTS ...], --search_contacts SEARCH_CONTACTS [SEARCH_CONTACTS ...]
                        Search contacts in address book
  -m MODIFY_CONTACTS [MODIFY_CONTACTS ...], --modify_contacts MODIFY_CONTACTS [MODIFY_CONTACTS ...]
                        Modify contacts in address book
  -d DEL_CONTACTS [DEL_CONTACTS ...], --del_contacts DEL_CONTACTS [DEL_CONTACTS ...]
                        Delete contacts from address book
  -sh, --show_contacts  Show contacts in address book
  -cl, --clear_contacts
                        Clear contacts from address book