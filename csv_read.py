# Excel (xlsx) information retrieval
# (c) 2016, Burt Lien <burt.lien@gmail.com>
#
# used to generate a report for specific topic

import sys
import pandas as pd
#import numpy as np

def excel_find_relevant(ef, kw, complete):
    df = pd.read_csv(ef)
    #df is a type of DataFrame now.

    #strip redundant space
    desc = 'Subject'
    df[desc] = df[desc].str.strip()

    #find tuples that contain specific key words
    query_df = df[df['Assigned To'].str.contains(kw, case=False)]
    if query_df.empty:
        print('No result found!!')
        return

    #drop some fields to make the report simpler
    if not complete:
        query_df = query_df.drop(['Assigned To', 'Date Last Modified', 'Status'], axis=1)

    #do not show the preceding index
    #left justified the Description column
    #use df['Description'].str.len().max() to compute the length of the longest string in df['Description'], and use that number, N, in a left-justified formatter '{:<Ns}'.format
    #the formatting might fail if data is not string type.. to be fixed
    print(query_df.to_string(formatters={desc:'{{:<{}s}}'.format(df[desc].str.len().max()).format}, index=False))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage: python <this script> <excel file name> <keyword to be searched>')
        print('ex: python csv_read.py weekly_repot.csv Burt')
        sys.exit()
    excel_f = sys.argv[1]
    keyword = sys.argv[2]
    complete = False
    #do not care the value of the 3rd argument.. not defined for the moment
    if len(sys.argv) == 4:
        complete = True
    print('---------- looking for \"' + keyword + '\" in \"' + excel_f + '\" ----------')
    excel_find_relevant(excel_f, keyword, complete)
    print('---------- end of query ----------')


