class Item:
	def __init__(self, name, price):
		self.name = name
		self.price = price

item = Item("hello", 12)
print(item.name)