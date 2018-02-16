class Message(object):
	def to_int(self):
		stay_as_str = ['mtype', 'description', 'buy_sell_indicator', 'stock', 'event_code']
		for key in self.__dict__:
			if key not in stay_as_str:
				self.__dict__[key] = int(self.__dict__[key])


class SystemEventMessage(Message):
	def __init__(self, message):
		self.mtype = 'S'
		self.description = 'System Event Message'
		(self.stock_locate, self.tracking_num,
		 self.time_stamp, self.event_code)= message[2:].split(',')



class AddOrderMessage(Message):
	def __init__(self, message):
		self.mtype = 'A'
		self.description = 'Add Order Message'
		(self.stock_locate, self.tracking_num, 
			self.time_stamp,
			self.order_ref_num, self.buy_sell_indicator, 
			self.shares, self.stock, self.price) = message[2:].split(',')


class OrderDeleteMessage(Message):
	def __init__(self, message):
		self.mtype = 'D'
		self.description = 'Order Delete Message'

		(self.stock_locate, self.tracking_num, 
			self.time_stamp,
			self.order_ref_num ) = message[2:].split(',')


class OrderExecutedMessage(Message):
	def __init__(self, message):
		self.mtype = 'E'
		self.description = 'Order Executed Message'

		(self.stock_locate, self.tracking_num, 
			self.time_stamp,
			self.order_ref_num, self.executed_shares,
			self.match_num) = message[2:].split(',')


class OrderCancelMessage(Message):
	def __init__(self, message):
		self.mtype = 'X'
		self.description = 'Order Cancel Message'

		(self.stock_locate, self.tracking_num, 
			self.time_stamp,
			self.order_ref_num, self.cancalled_shares) = message[2:].split(',')


class OrderReplaceMessage(Message):
	def __init__(self, message):
		self.mtype = 'U'
		self.description = 'Order Replace Message'
		(self.stock_locate, self.tracking_num, 
			self.time_stamp,
			self.order_ref_num, self.new_order_ref_num,
			self.shares, self.price) = message[2:].split(',')


def message_factory(msg):
	mtype = msg[:2]

	if mtype == 'S,':
		Msg = SystemEventMessage(msg)
	elif mtype == 'A,':
		Msg = AddOrderMessage(msg)
	elif mtype == 'D,':
		Msg = OrderDeleteMessage(msg)
	elif mtype == 'E,':
		Msg =  OrderExecutedMessage(msg)
	elif mtype == 'X,':
		Msg =  OrderCancelMessage(msg)
	elif mtype == 'U,':
		Msg =  OrderReplaceMessage(msg)
	else:
		return None

	Msg.to_int()
	return Msg