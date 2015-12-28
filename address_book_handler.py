import argparse
import os
import pickle
import re

class AddressBookInstance:
    """Address Book top-level class"""

    count = 0
    pattern_name = r"^(\w+)$"
    pattern_email = r"^((\w+@\w+)([.]\w+)+)$"
    pattern_phone = r"^(\d+)$"
    re_name = re.compile(pattern_name, re.IGNORECASE)
    re_email = re.compile(pattern_email, re.IGNORECASE)
    re_phone = re.compile(pattern_phone, re.IGNORECASE)

    def __init__(self, address_book_name, contact_name_list=[]):
        self.addrBName = address_book_name
        self.contact_name_list = contact_name_list

    def add_contact(self, contact_entry):
        self.count += 1
        if not (AddressBookInstance.re_name.match(contact_entry[0]) and AddressBookInstance.re_email.match(
                contact_entry[1])) or not AddressBookInstance.re_phone.match(contact_entry[2]):
            print 'Wrong contact information format.'
            return
        contact_dict = {'c_name': contact_entry[0], 'c_email': contact_entry[1], 'c_phone': contact_entry[2]}
        contact_dict_keyv_pair = {str(self.count): contact_dict}
        self.contact_name_list.append(contact_dict_keyv_pair)

    def search(self, entry_name):
        """Returns a dictionary containing details matching entry_name"""

        for person_keyv_pair in self.contact_name_list:
            for key, val in person_keyv_pair:
                if val['c_name'] == entry_name:
                    return val
        return {'notFound': 'notFound'}

    def get_contact_name_list(self):
        return self.contact_name_list

    def modify(self, entry_name, change_type, change):
        for entry_keyv_pair in self.contact_name_list:
            for entry_info in entry_keyv_pair.values():
                if entry_info['c_name'] == entry_name:
                    for key in entry_info.keys():

                        if change_type == key[2:].capitalize():
                            entry_info[key] = change
                            return

    def delete(self, entry_name):
        for entry_keyv_pair in self.contact_name_list:
            for entry_info in entry_keyv_pair.values():
                if entry_info['c_name'] == entry_name:
                    del entry_keyv_pair
                    self.count -= 1
                    break
        return

    def show(self):
        if self.get_contact_name_list():
            print '\nContact List ({}) :'.format(self.count)
            for person_dict in self.contact_name_list:
                for person in person_dict.values():
                    print 'Name:', person['c_name'],
                    print 'Email:', person['c_email'],
                    print 'Phone:', person['c_phone']
        else:
            print '{} is empty'.format(self.addrBName)

    def set_count(self, new_count):
        self.count = new_count

    def clear_contact_list(self):
        self.contact_name_list = []


def parse_cmd_args():
    parser = argparse.ArgumentParser(description='Parse arguments for address book program')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--add_contact', nargs='+',
                       metavar='C',
                       help='Add contacts to address book: name {space} email,'
                            '{space} phone')
    group.add_argument('-s', '--search_contacts', help='Search contacts in address book', nargs='+')
    group.add_argument('-m', '--modify_contacts', help='Modify contacts in address book', nargs='+')
    group.add_argument('-d', '--del_contacts', help='Delete contacts from address book', nargs='+')
    group.add_argument('-sh', '--show_contacts', help='Show contacts in address book', action='store_true')
    group.add_argument('-cl', '--clear_contacts', help='Clear contacts from address book', action='store_true')
    return parser, parser.parse_args()


def address_book_ops(entry_file):
    global addressBook
    if os.path.getsize(entry_file.name) > 0:
        stored_list = pickle.load(entry_file)
        addressBook = AddressBookInstance('My Address Book', stored_list)
        addressBook.set_count(len(stored_list))
    else:
        addressBook = AddressBookInstance('My Address Book')

    (parser, args) = parse_cmd_args()

    if args.add_contact:
        contact_info = []
        for arg in args.add_contact:
            contact_info.append(arg)
        if len(contact_info) == 3:
            addressBook.add_contact(contact_info)
        else:
            print 'Insufficient or surplus information. Only 3 items needed.'
    elif args.search_contacts:
        if 'notFound' in addressBook.search(args.search_contacts):
            print 'Not Found'
    elif args.modify_contacts:
        if len(args.modify_contacts) == 3:
            addressBook.modify(args.modify_contacts[0],
                               args.modify_contacts[1], args.modify_contacts[2])
    elif args.del_contacts:
        addressBook.delete(args.del_contacts)
    elif args.show_contacts:
        addressBook.show()
    elif args.clear_contacts:
        resp = raw_input('Are you sure you want to clear address book? Enter \'Y\' to confirm: ')
        if resp == 'Y' or resp == 'y':
            addressBook.clear_contact_list()
            save_contact_list(addressBook.get_contact_name_list(), entry_file)
            print 'Address Book cleared'
            return
    else:
        parser.parse_args('-h'.split())
    save_contact_list(addressBook.get_contact_name_list(), entry_file)


def save_contact_list(contact_list, entry_file):
    entry_file.seek(0, 2)  # now switching to writing mode so append to end of file with 0 offset
    target = os.path.join(os.getcwd(), 'Address Books', 'my_address_book.pkl')
    with open(target, 'wb+') as entry_file:
        pickle.dump(contact_list, entry_file)
