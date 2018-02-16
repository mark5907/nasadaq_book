import struct


class Message(object):
	def add_tstamp(self):
		self.time_stamp  = (self.time_stamp_a << 16) + (self.time_stamp_b)


class SystemEventMessage(Message):
	def __init__(self, message):
		self.mtype = 'S'
		self.description = 'System Event Message'
		(self.stock_locate, self.tracking_num,
		 self.time_stamp_a, self.time_stamp_b, self.event_code)= struct.unpack('!HHIHs', message[1:])

		self.add_tstamp()

	def output(self):
		out = "{},{},{},{},{}".format(self.mtype, self.stock_locate, 
									self.tracking_num, self.time_stamp, 
									self.event_code)
		return out


class AddOrderMessage(Message):
	def __init__(self, message):
		self.mtype = 'A'
		self.description = 'Add Order Message'

		(self.stock_locate, self.tracking_num, 
			self.time_stamp_a, self.time_stamp_b,
			self.order_ref_num, self.buy_sell_indicator, 
			self.shares, self.stock, self.price) = struct.unpack('!HHIHQsI8sI', message[1:])
		
		self.stock = self.stock.strip()
		self.add_tstamp()

	def output(self):
		out = "{},{},{},{},{},{},{},{},{}".format(self.mtype, self.stock_locate, 
									self.tracking_num, self.time_stamp, 
									self.order_ref_num, self.buy_sell_indicator,
									self.shares,self.stock,self.price)
		return out

class AddOrderMessageAttr(Message):
	def __init__(self, message):
		self.mtype = 'F'
		self.description = 'Add Order Message MPID'

		(self.stock_locate, self.tracking_num, 
			self.time_stamp_a, self.time_stamp_b,
			self.order_ref_num, self.buy_sell_indicator, 
			self.shares, self.stock, self.price, self.attr) = struct.unpack('!HHIHQsI8sI4s', message[1:])
		
		self.stock = self.stock.strip()
		self.add_tstamp()

	def output(self):
		out = "{},{},{},{},{},{},{},{},{}".format('A', self.stock_locate, 
									self.tracking_num, self.time_stamp, 
									self.order_ref_num, self.buy_sell_indicator,
									self.shares,self.stock,self.price)
		return out

class OrderDeleteMessage(Message):
	def __init__(self, message):
		self.mtype = 'D'
		self.description = 'Order Delete Message'

		(self.stock_locate, self.tracking_num, 
			self.time_stamp_a, self.time_stamp_b,
			self.order_ref_num ) = struct.unpack('!HHIHQ', message[1:])
		self.add_tstamp()

	def output(self):
		out = "{},{},{},{},{}".format(self.mtype, self.stock_locate, 
									self.tracking_num, self.time_stamp, 
									self.order_ref_num)	
		return out

class OrderExecutedMessage(Message):
	def __init__(self, message):
		self.mtype = 'E'
		self.description = 'Order Executed Message'

		(self.stock_locate, self.tracking_num, 
			self.time_stamp_a, self.time_stamp_b,
			self.order_ref_num, self.executed_shares,
			self.match_num) = struct.unpack('!HHIHQIQ', message[1:])
		self.add_tstamp()

	def output(self):
		out = "{},{},{},{},{},{},{}".format(self.mtype, self.stock_locate, 
									self.tracking_num, self.time_stamp, 
									self.order_ref_num, self.executed_shares, self.match_num)	
		return out


class OrderExecutedWithPriceMessage(Message):
	def __init__(self, message):
		self.mtype = 'C'
		self.description = 'Order Executed Message with Price'

		(self.stock_locate, self.tracking_num, 
			self.time_stamp_a, self.time_stamp_b,
			self.order_ref_num, self.executed_shares,
			self.match_num, self.printable, self.execution_price) = struct.unpack('!HHIHQIQsI', message[1:])
		self.add_tstamp()

	def output(self):
		out = "{},{},{},{},{},{},{}".format('E', self.stock_locate, 
									self.tracking_num, self.time_stamp, 
									self.order_ref_num, self.executed_shares, self.match_num)	
		return out


class OrderCancelMessage(Message):
	def __init__(self, message):
		self.mtype = 'X'
		self.description = 'Order Cancel Message'

		(self.stock_locate, self.tracking_num, 
			self.time_stamp_a, self.time_stamp_b,
			self.order_ref_num, self.cancalled_shares) = struct.unpack('!HHIHQI', message[1:])
		self.add_tstamp()
	def output(self):
		out = "{},{},{},{},{},{}".format(self.mtype, self.stock_locate, 
									self.tracking_num, self.time_stamp, 
									self.order_ref_num, self.cancalled_shares)	
		return out


class OrderReplaceMessage(Message):
	def __init__(self, message):
		self.mtype = 'U'
		self.description = 'Order Replace Message'
		(self.stock_locate, self.tracking_num, 
			self.time_stamp_a, self.time_stamp_b,
			self.order_ref_num, self.new_order_ref_num,
			self.shares, self.price) = struct.unpack('!HHIHQQII', message[1:])
		self.add_tstamp()
	def output(self):
		out = "{},{},{},{},{},{},{},{}".format(self.mtype, self.stock_locate, 
									self.tracking_num, self.time_stamp, 
									self.order_ref_num, self.new_order_ref_num, 
									self.shares, self.price)	
		return out