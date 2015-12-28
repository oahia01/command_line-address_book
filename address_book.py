import os
import address_book_handler

target_file = os.path.join(os.getcwd(), 'Address Books', 'my_address_book.pkl')
if not os.path.exists(os.path.dirname(target_file)):
    os.makedirs(os.path.dirname(target_file))

if not os.path.exists(target_file):
    with open(target_file, 'wb+') as fileN:
        address_book_handler.address_book_ops(fileN)
else:
    with open(target_file, 'rb+') as fileN:
        address_book_handler.address_book_ops(fileN)