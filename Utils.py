import RegisterWindow


COLOR_OF_WINDOW = '#99CCFF'
TYPE_OF_ROOM = ['Your rooms', 'Rooms', 'Friends']

def login():
    pass

def get_key_id(key_file):
    key = key_file.exportkey()
    pub_key_id = key.split('-----')[2].lstrip().rstrip()
    pub_key_id = pub_key_id[-8:].replace('\n', '')

    return pub_key_id


