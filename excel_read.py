# Excel (xlsx) information retrieval
# (c) 2016, Burt Lien <burt.lien@gmail.com>
# 
# used to generate a report for specific topic

import sys
import pandas as pd
#import numpy as np

def excel_find_relevant(ef, kw):
    df = pd.read_excel(ef, header=None, parse_cols="B:G", names=['ID','Desc','Project','Owner','Status','Severity'])
    #df is a type of DataFrame now.

    #strip redundant space 
    desc = 'Desc'
    df[desc] = df[desc].str.strip()
    
    #find tuples that contain specific key words
    query_df = df[df['Project'].str.contains(kw, case=False)]
    if query_df.empty:
        query_df = df[df['Owner'].str.contains(kw, case=False)]
        if query_df.empty:
            print('No result found!!')
            return

    #do not show the preceding index
    #left justified the Description column
    #use df['Description'].str.len().max() to compute the length of the longest string in df['Description'], and use that number, N, in a left-justified formatter '{:<Ns}'.format
    #the formatting might fail if data is not string type.. to be fixed
    print(query_df.to_string(formatters={desc:'{{:<{}s}}'.format(df[desc].str.len().max()).format}, index=False))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage: python <this script> <excel file name> <keyword to be searched>')
        print('ex: python excel_read.py weekly_repot.xlsx Burt')
        sys.exit()
    excel_f = sys.argv[1]
    keyword = sys.argv[2]
    print('---------- looking for \"' + keyword + '\" in \"' + excel_f + '\" ----------')
    excel_find_relevant(excel_f, keyword) 
    print('---------- end of query ----------')

