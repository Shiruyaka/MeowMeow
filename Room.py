

def parse_rooms_from_db(data):
    rooms = list()

    for i in data:
        tmp = i[4]

        if tmp == None:
            tmp = 0
        rooms.append(Room(i[0], i[1], i[2], i[3], tmp, i[5], i[6]))

    return rooms



class Room():
    def __init__(self, id, name, desc, master, signed, lim_in_room, kind):

        self.id = id
        self.name = name
        self.desc = desc
        self.master = master
        self.signed = signed
        self.lim_in_room = lim_in_room
        self.whitelist = list()
        self.kind = kind
        self.online = list()

    def add_usr_whitelist(self, lst):
        for i in lst:
            self.whitelist.append(i)

    def is_user_on_whitelist(self, nick):
        for i in self.whitelist:
            if i == nick:
                return True
        return False

    def tostring(self):
        return '[' +  str(self.id) + '&' + self.name + '&' + self.desc + '&' + self.master + '&' \
               + str(self.signed) + '&' + str(self.lim_in_room) + '&' + self.kind + ']'
