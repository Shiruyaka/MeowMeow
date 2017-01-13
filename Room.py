

def parse_rooms_from_db(data):
    rooms = list()

    for i in data:
        rooms.append(Room(i[0], i[1], i[2], i[4], i[3], i[5]))

    return rooms



class Room():
    def __init__(self, id, name, desc, lim_in_room, master, kind):

        self.id = id
        self.name = name
        self.desc = desc
        self.lim_in_room = lim_in_room
        self.master = master
        self.kind = kind

