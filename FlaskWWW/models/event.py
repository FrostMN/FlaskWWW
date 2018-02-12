class Event:
    def __init__(self, name=None, date=None, event_id=None, items=[], db=None):
        if db is not None:
            self.name = db["name"]

            date = db["date"]

            self.date = date
            self.id = db["id"]
            self.items = items
        else:
            self.name = name
            self.date = date
            self.id = event_id
            self.items = items

    def date(self):
        print("self.dat: ")
        print(self.date)
        return self.date
