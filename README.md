Part1. binary_parser
	input is the binary file download from Nasdaq website, using 10302017.NASDAQ_ITCH50 for now
	output is the csv for each message
	**Note: this script only works for AAPL, SQ, MSTF for now. We can add in more tickers with a little change to the code

	python binary_parser/itch_parser.py -i <path_to_input_file> -o <path_to_output_file> -s <ticker>

Part2. book_parser
	input is the csv file with each message (output from part 1. )
	output is the csv file with the top of the book

	python book_parser/book_builder.py -i <path_to_input_file> -o <path_to_output_file>