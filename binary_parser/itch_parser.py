from messages import *
from struct import unpack
import argparse
import sys

STOCK_LOCATE ={'AAPL':14, 'SQ':7088, 'MSFT':59}
def message_factory(msg):
	mtype = msg[0]

	if mtype == 'S':
		return SystemEventMessage(msg)
	elif mtype == 'A':
		return AddOrderMessage(msg)
	elif mtype == 'F':
		return AddOrderMessageAttr(msg)
	elif mtype == 'D':
		return OrderDeleteMessage(msg)
	elif mtype == 'E':
		return OrderExecutedMessage(msg)
	elif mtype == 'C':
		return OrderExecutedWithPriceMessage(msg)
	elif mtype == 'X':
		return OrderCancelMessage(msg)
	elif mtype == 'U':
		return OrderReplaceMessage(msg)
	else:
		return None


def parse_file(input_file, output_file, stock_locate):

	fi = open(input_file,'rb')
	fo = open(output_file, 'w')


	while True:
		payload = unpack('!H', fi.read(2))[0]
		msg = fi.read(payload)
		ItchMessage = message_factory(msg)

		if ItchMessage and ItchMessage.stock_locate in {stock_locate, 0}:
			fo.write(ItchMessage.output() + '\n')

			if ItchMessage.mtype == 'S' and ItchMessage.event_code == 'C':
				break


	fi.close()
	fo.close()


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input_file', help='input file path')
	parser.add_argument('-o', '--output_file', help='outut file path', default='a.csv')
	parser.add_argument('-s', '--symbol', help='stock symbol', default='AAPL')
	args = parser.parse_args()

	ok = True
	print '... loading', args.input_file
	try:
		fi = open(args.input_file, 'rb')
	except IOError:
		print '+++ input file not found'
		ok = False

	if args.symbol not in STOCK_LOCATE:
		print '+++ symbol not in stock_locate set, find it first'
		ok = False


	if ok:
		print '... parsing trade data for', args.symbol
		stock_locate_num = STOCK_LOCATE[args.symbol]
		parse_file(args.input_file, args.output_file, stock_locate_num)
		print '... done, file saved at', args.output_file