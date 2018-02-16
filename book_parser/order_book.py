from bintrees import RBTree

class Order(object):
	def __init__(self, time_stamp, order_ref_num, buy_sell_indicator, shares, price):
		self.time_stamp = time_stamp
		self.order_ref_num = order_ref_num
		self.buy_sell_indicator = buy_sell_indicator
		self.shares = shares
		self.price = price


class OrderList(object):
	def __init__(self):
		self.order_list = []
		self.order_head = 0
		self.num_of_orders = 0
		self.volume = 0

	def __len__(self):
		return len(self.order_list)

	def get_head_order(self):
		return self.order_list[self.order_head]

	def add_order(self, order):
		self.order_list.append(order)
		self.num_of_orders += 1
		self.volume += order.shares

	def remove_order(self, order):
		assert(self.num_of_orders > 0)
		self.volume -= order.shares
		self.num_of_orders -= 1
		order.shares = 0
		
	def cancel_order(self, order, shares_to_cancel):
		assert(self.num_of_orders > 0)
		if order.shares == shares_to_cancel:
			self.remove_order(order)
		else:
			order.shares -= shares_to_cancel
			self.volume -= shares_to_cancel


class OrderTree(object):
	def __init__(self):
		self.price_tree = RBTree()
		self.price_map  = {} #price to order_list
		self.order_map  = {} #order_ref_num to order

	def create_price(self, price):
		assert(price not in self.price_map)
		new_list = OrderList()
		self.price_tree.insert(price, new_list)
		self.price_map[price] = new_list

	def remove_price(self, price):
		assert(price in self.price_map)
		self.price_tree.remove(price)
		del self.price_map[price]

	def add_order(self, order):
		if order.price not in self.price_map:
			self.create_price(order.price)
		self.order_map[order.order_ref_num] = order
		self.price_map[order.price].add_order(order)	

	def remove_order(self, order_ref_num):
		assert(order_ref_num in self.order_map)
		
		order = self.order_map[order_ref_num]
		self.price_map[order.price].remove_order(order)
		del self.order_map[order_ref_num]

	def cancel_order(self, order_ref_num, shares_to_cancel):
		assert(order_ref_num in self.order_map)
		order = self.order_map[order_ref_num]
		self.price_map[order.price].cancel_order(order, shares_to_cancel)

	def excute_order(self, order_ref_num, shares_to_excute):
		self.cancel_order(order_ref_num, shares_to_excute)

	def update_order(self, time_stamp, order_ref_num, new_order_ref_num, shares, price):
		assert(order_ref_num in self.order_map)
		buy_sell_indicator = self.order_map[order_ref_num].buy_sell_indicator
		self.remove_order(order_ref_num)

		new_order = Order(time_stamp, new_order_ref_num, buy_sell_indicator, shares, price)
		self.add_order(new_order)


class OrderBook(object):
	def __init__(self):
		self.bidTree = OrderTree()
		self.askTree = OrderTree()

	@staticmethod
	def process_order_list(order, orderList):
		# process an order, try to cross orderList
		while orderList.order_head < len(orderList) and order.shares > 0:
			curr_order = orderList.get_head_order()
			if order.shares >= curr_order.shares :
				order.shares -= curr_order.shares

				orderList.remove_order(curr_order)
				orderList.order_head += 1
			else:
				orderList.cancel_order(curr_order, order.shares)
				order.shares = 0

	def add_bid(self, bidOrder):
		askTree = self.askTree
		while askTree.price_tree:
			lowest_ask = askTree.price_tree.min_key()

			if bidOrder.price < lowest_ask:
				break

			orderList = askTree.price_map[lowest_ask]
			self.process_order_list(bidOrder, orderList)
			if bidOrder.shares == 0:
				break

			if orderList.volume == 0:
				askTree.remove_price(lowest_ask)

		if bidOrder.shares > 0:
			self.bidTree.add_order(bidOrder)

	def add_ask(self, askOrder):
		bidTree = self.bidTree
		while bidTree.price_tree:
			highest_bid = bidTree.price_tree.max_key()
			if askOrder > highest_bid:
				break

			orderList = bidTree.price_map[highest_bid]
			self.process_order_list(askOrder, orderList)
			if askOrder.sahres == 0:
				break

			if orderList.volume == 0:
				bidTree.remove_price(highest_bid)

		if askOrder.shares > 0:
			self.askTree.add_order(askOrder)

	def get_top_bid(self):
		# return best price and shares
		orderTree = self.bidTree
		while orderTree.price_tree and orderTree.price_tree.max_item()[1].volume == 0:
			orderTree.remove_price( orderTree.price_tree.max_key() )

		if not orderTree.price_tree:
			return '',''
		else:
			best_price, orderList = orderTree.price_tree.max_item()
			return best_price, orderList.volume


	def get_top_ask(self):
		# return best price and shares
		orderTree = self.askTree
		while orderTree.price_tree and orderTree.price_tree.min_item()[1].volume == 0:
			orderTree.remove_price( orderTree.price_tree.min_key() )

		if not orderTree.price_tree:
			return '',''
		else:
			best_price, orderList = orderTree.price_tree.min_item()
			return best_price, orderList.volume

	def remove_order(self, order_ref_num):
		if order_ref_num in self.bidTree.order_map:
			orderTree = self.bidTree
		elif order_ref_num in self.askTree.order_map:
			orderTree = self.askTree
		else:
			print '+++ remove failed, reference number not found'
			return None

		orderTree.remove_order(order_ref_num)

	def cancel_order(self, order_ref_num, shares_to_cancel):
		if order_ref_num in self.bidTree.order_map:
			orderTree = self.bidTree
		elif order_ref_num in self.askTree.order_map:
			orderTree = self.askTree
		else:
			print '+++ cancel failed, reference number not found'
			return None

		orderTree.cancel_order(order_ref_num, shares_to_cancel)

	def excute_order(self, order_ref_num, shares_to_excute):
		self.cancel_order( order_ref_num, shares_to_excute)


	def update_order(self, time_stamp, order_ref_num, new_order_ref_num, shares, price):
		if order_ref_num in self.bidTree.order_map:
			orderTree = self.bidTree
		elif order_ref_num in self.askTree.order_map:
			orderTree = self.askTree
		else:
			print '+++ cancel failed, reference number not found'
			return None
		orderTree.update_order(time_stamp, order_ref_num, new_order_ref_num, shares, price)