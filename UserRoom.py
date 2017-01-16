

class UserRoom():
    def __init__(self, id, name, desc, master, signed, lim_in_room, kind):
        self.id = id
        self.name = name
        self.desc = desc
        self.master = master
        self.signed = signed
        self.lim_in_room = lim_in_room
        self.kind = kind
        self.online = list()

    @staticmethod
    def parse_room(args):
        content = args.split('&')

        return UserRoom(content[0], content[1], content[2], content[3], content[4], content[5], content[6])