import os

filename = 'test'
upload_dir = ''

path = os.path.basename(filename)
open(os.path.join(upload_dir, path), 'rb')
