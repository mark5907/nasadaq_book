import order_book
import sys
import argparse
from csv_messages import message_factory


def build_book(input_file, output_file):
	book = order_book.OrderBook()


	fi = open(input_file, 'r')
	fo = open(output_file, 'w')
	for row in fi.xreadlines():
		msg = message_factory(row.strip())

		if msg is None:
			continue

		if msg.mtype == 'A':
		    order = order_book.Order(msg.time_stamp, msg.order_ref_num, msg.buy_sell_indicator, msg.shares, msg.price)
		    if order.buy_sell_indicator == 'S':
		        book.add_ask(order)
		    if order.buy_sell_indicator == 'B':
		        book.add_bid(order)
		elif msg.mtype == 'D':
		    book.remove_order( msg.order_ref_num)
		    
		elif msg.mtype == 'X':
		    book.cancel_order(msg.order_ref_num, msg.cancalled_shares)
		elif msg.mtype == 'U':
		    book.update_order(msg.time_stamp, msg.order_ref_num, msg.new_order_ref_num, msg.shares, msg.price)
		elif msg.mtype == 'E':
		    book.excute_order(msg.order_ref_num, msg.executed_shares)

		best_bid, best_bid_shares = book.get_top_bid()
		best_ask, best_ask_shares = book.get_top_ask()
		to_write = "{},{},{},{},{}\n".format(msg.time_stamp, best_bid, best_bid_shares, best_ask, best_ask_shares)
		fo.write(to_write)
	fo.close()
	fi.close()


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input_file', help='input file path')
	parser.add_argument('-o', '--output_file', help='outut file path', default='a.csv')
	args = parser.parse_args()
	build_book(args.input_file, args.output_file)