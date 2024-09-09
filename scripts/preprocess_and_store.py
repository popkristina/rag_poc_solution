import pandas as pd
import argparse


###################### ARGUMENT PARSER #######################

parser = argparse.ArgumentParser(description='Inputs for script.')
parser.add_argument('--new_data', dest='new_docs_path',
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))


######## READ NEW DATA TO UPDATE VECTOR DATABASE WITH ########




########## CONNECTION TO EXISTING VECTOR DATABASE ############




###### UPDATE VECTOR DATABASE WITH NEW KNOLEDGE VECTORS ######



