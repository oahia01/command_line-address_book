import argparse, os, pickle, re


class addrB:
    count = 0
    pattern_name = r"^(\w+)$"
    pattern_email = r"^((\w+@\w+)([.]\w+)+)$"
    pattern_phone = r"^(\d+)$"
    re_name = re.compile(pattern_name, re.IGNORECASE)
    re_email = re.compile(pattern_email, re.IGNORECASE)
    re_phone = re.compile(pattern_phone, re.IGNORECASE)

    def __init__(self, addrBName, contact_name_list=[]):
        self.addrBName = addrBName
        self.contact_name_list = contact_name_list

    def add_contact(self, contact_infoN):
        # contact_dict = []
        # if len(contact_infoN) == 3:
        self.count += 1
        if not (addrB.re_name.match(contact_infoN[0]) and addrB.re_email.match(
                contact_infoN[1])) or not addrB.re_phone.match(contact_infoN[2]):
            print 'Wrong contact information format.'
            return
        contact_dict = {'c_name': contact_infoN[0], 'c_email': contact_infoN[1], 'c_phone': contact_infoN[2]}
        contact_dict_keyv_pair = {str(self.count): contact_dict}
        self.contact_name_list.append(contact_dict_keyv_pair)

    def search(self, personN):
        """Returns a dictionary """
        for person_keyv_pair in self.contact_name_list:
            for key, val in person_keyv_pair:
                if val['c_name'] == personN:
                    return val
        return {'notFound': 'notFound'}

    def get_contact_name_list(self):
        return self.contact_name_list

    def modify(self, personN, change_type, change):
        for person_keyv_pair in self.contact_name_list:
            for person_info in person_keyv_pair.values():
                if person_info['c_name'] == personN:
                    for key in person_info.keys():

                        if change_type == key[2:].capitalize():
                            person_info[key] = change
                            return

    def delete(self, personN):
        for person_keyv_pair in self.contact_name_list:
            for person_info in person_keyv_pair.values():
                if person_info['c_name'] == personN:
                    del person_keyv_pair
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


def main_prog(fileN):
    global addressBook
    if os.path.getsize(fileN.name) > 0:
        stored_list = pickle.load(fileN)
        addressBook = addrB('My Address Book', stored_list)
        addressBook.set_count(len(stored_list))
    else:
        addressBook = addrB('My Address Book')

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
            save_contact_list(addressBook.get_contact_name_list(), fileN)
            print 'Address Book cleared'
            return
    else:
        parser.parse_args('-h'.split())
    save_contact_list(addressBook.get_contact_name_list(), fileN)


def save_contact_list(contact_list, fileN):
    # if addrBook.get_contact_name_list():
    fileN.seek(0, 2)  # now switching to writing mode so append to end of file with 0 offset
    target = os.path.join(os.getcwd(), 'Address Books', 'my_address_book.pkl')
    with open(target, 'wb+') as fileN:
        pickle.dump(contact_list, fileN)

target = os.path.join(os.getcwd(), 'Address Books', 'my_address_book.pkl')
if not os.path.exists(os.path.dirname(target)):
    os.makedirs(os.path.dirname(target))

# with open(target, 'wb+') as fileN:
#     main_prog(fileN, False)    
if not os.path.exists(target):
    with open(target, 'wb+') as fileN:
        main_prog(fileN)
else:
    with open(target, 'rb+') as fileN:
        main_prog(fileN)
