# i want to encode everything that is needed for the input of the employee into a barcode.
# brainstorm here:
# current input requires Y/N input, this would need to be improved upon
# preferred name, first, last, job title, perm_lvl, DOB
# contact info would need to be in a different (scannable) code
#
# todo: this data should be hashed before it is inputted into the QR code.
# todo: this should include their pkey or some identifiable foreign key
#
import qrcode

first_name = 'Jacob'
last_name = 'Pinard'
job_title = 'Coordinator'
perm_lvl = '2'
DOB = '12-21-2001'
img = qrcode.make(f'{first_name}, {last_name}, {job_title}, {perm_lvl}, {DOB}')
# type(img) #qrcode.image.pil.PilImage
img.save(f'{first_name}-{last_name}.png')
