'''
A web crawler, with autentication, to get specific information (personal use)
Copyright 2017. burt.lien@gmail.com

the program require an external .config to feed necessary information
'''

import sys
import re
from robobrowser import RoboBrowser
import pandas as pd

def find_relevant(url, name, passwd, kw, complete):

    #mute warning for data hazard
    pd.options.mode.chained_assignment = None  # default='warn'
    #create a browser
    browser = RoboBrowser() #(history=True)
    browser.open(url)
    form = browser.get_form()
    
    form["login"] = name
    form["password"] = passwd
    browser.session.headers['Referer'] = url
    #submit username and password
    browser.submit_form(form)
    
    #read_html return list of DataFrame
    #add " match='<key>'" if a specific table is what you're looking for
    dfs = pd.read_html(str(browser.select), header=0) 
    #first table is what we need in this example case
    df = dfs[0]
    #TODO: contains 2 garbage row in the end of the DataFrame?? just drop it.. investigate later..
    df = df.drop(df.index[-2:])
    #remove rows with null ID
    df = df[df['Bug ID'].notnull()]
    #strip redundant space for better formatting
    desc = 'Subject'
    df[desc] = df[desc].str.strip()
    
    #find tuples that contain specific key words (case insensitive)
    if kw == '*':
        query_df = df
    else:
        query_df = df[df['Assigned To'].str.contains(kw, case=False)]
        if query_df.empty:
            print('No result found!!')
            return
    
    #drop some fields to make the report simpler
    if not complete:
        query_df = query_df.drop(['Date Last Modified', 'Status'], axis=1)

    #trim redundant characters in the fields
    query_df['Bug ID'] = query_df['Bug ID'].str.replace('Edit \| ', '')
    #query_df.style.set_properties(align="center")
    #do not show the preceding index
    #left justified the Description column
    #use df['Description'].str.len().max() to compute the length of the longest string in df['Description'], and use that number, N, in a left-justified formatter '{:<Ns}'.format
    #the formatting might fail if data is not string type.. to be fixed
    print(query_df.to_string(formatters={desc:'{{:<{}s}}'.format(df[desc].str.len().max()).format}, index=False))
    print('==> found %d tickets \033[0m<==' %len(query_df.index))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: python <script name> <keyword to be searched>')
        print('-- ex: python web_crawler.py Burt')
        sys.exit()
    keyword = sys.argv[1]
    complete = False
    #do not care the value of the 3rd argument.. not defined for the moment
    if len(sys.argv) == 3:
        complete = True

    #read config from external file
    dic = eval(open(".config").read())
    target_url = dic['website']
    name = dic['name']
    passwd = dic['password']
    print('---------- looking for \"' + keyword + '\" in \"' + target_url + '\" ----------')
    find_relevant(target_url, name, passwd, keyword, complete)
    print('---------- end of query ----------')

