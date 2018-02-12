class Item:
    def __init__(self, item_id=None, name=None, price=None, description=None, sold=0, db=None):
        if db is not None:
            self.id = db["item_id"]
            self.name = db["name"]
            self.price = db["price"]
            self.description = db["description"]
            if "number_sold" in db.keys():
                self.sold = db["number_sold"]
            else:
                self.sold = sold
        else:
            self.id = item_id
            self.name = name
            self.price = price
            self.description = description
            self.sold = sold

