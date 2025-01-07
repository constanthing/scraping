import sys
import argparse


parser = argparse.ArgumentParser(description="0")
parser.add_argument( "-sd", "--separate-data", action="store_true", help="Separate data into dictionary of {Page X: [ticks]}")
# if only -x is provided then it is stored as -x
# if --x-x is provided then -x is ignored and instead stored as --x-x
parser.add_argument("-ss", "--something-something", action="store_true")

args = parser.parse_args()

separate_data = args.separate_data
print(args.something_something)

print(separate_data)

# sd = False 

# if len(sys.argv) > 1:
# 	for arg in sys.argv[1:]:
# 		if arg == "--separate-data" or arg == "-sd":
# 			sd = True
# 			break

# print(sd)
		
