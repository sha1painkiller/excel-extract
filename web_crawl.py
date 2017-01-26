'''
Copyright (C) 2017 Burt Lien - All Rights Reserved
You may use, distribute and modify this code on your
own way.
This is a web crawler program, with autentication,
to get specific information (personal use)
Author: burt.lien@gmail.com
Refer to README for usages.
'''
import os.path
import sys
from datetime import datetime
import getopt
import re
import pandas as pd
from robobrowser import RoboBrowser

def fetch_web(url, name, passwd, path):

    #mute warning for data hazard
    pd.options.mode.chained_assignment = None  # default='warn'
    #create a browser
    browser = RoboBrowser() #(history=True)
    try:
        browser.open(url, timeout = 10)
    except:
        print("!!!!connection timeout!!!!")
        return

    form = browser.get_form()

    form["login"] = name
    form["password"] = passwd
    browser.session.headers['Referer'] = url
    #submit username and password
    browser.submit_form(form)

    #read_html return list of DataFrame
    #add " match='<key>'" if a specific table is what you're looking for
    dfs = pd.read_html(str(browser.select), header = 0)
    #first table is what we need in this example case
    df = dfs[0]
    #TODO: contains 2 garbage row in the end of the DataFrame?? just drop it.. investigate later..
    df = df.drop(df.index[-2:])
    #remove rows with null ID
    df = df[df['Bug ID'].notnull()]

    #trim redundant characters in the fields
    df['Bug ID'] = df['Bug ID'].str.replace('Edit \| ', '')
    #save as csv format
    df.to_csv(path)

def show_result(df, kw, complete):

    #mute warning for data hazard
    pd.options.mode.chained_assignment = None  # default='warn'

    #strip redundant space for better formatting
    desc = 'Subject'
    df[desc] = df[desc].str.strip()

    #find tuples that contain specific key words (case insensitive)
    if kw == '*':
        query_df = df
    else:
        query_df = df[df['Assigned To'].str.contains(kw, case = False)]
        if query_df.empty:
            print('No result found!!')
            return

    #drop index
    query_df = query_df.drop(query_df.columns[0], axis = 1)
    #drop some fields to make the report simpler
    if not complete:
        query_df = query_df.drop(['Date Last Modified', 'Status'], axis = 1)

    #query_df.style.set_properties(align = "center")
    #do not show the preceding index
    #left justified the Description column
    #use df['Description'].str.len().max() to compute the length of the longest string in df['Description'], and use that number, N, in a left-justified formatter '{:<Ns}'.format
    #the formatting might fail if data is not string type.. to be fixed
    print(query_df.to_string(formatters = {desc:'{{:<{}s}}'.format(df[desc].str.len().max()).format}, index = False))
    print('==> found %d tickets \033[0m<==' % len(query_df.index))

    #show the last modified datetime for a justification whether enforce fetch should be triggered or not
    mtime = os.path.getmtime(path)
    last_modified = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    print('Last update: ' + last_modified)


if __name__ == '__main__':

    usages = '''usage: python3 web_crawl.py [-h] [-k <keyword>|*] [-m 1|0] [-f 1|0]'
       -h help messages
       -k keyword; "*" for everything
       -m 1|0 1->show complete fields
              0->only selected fields
       -f 1|0 1->force retrieve tables from web
              0->read from local cache
              automatically turns to force mode upon absence of local cache file
       '''
    if len(sys.argv) < 2:
        print(usages)
        sys.exit()

    #default settings
    complete = enforce = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "k:m:f:h")
    except getopt.GetoptError:
        print(usages)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usages)
            sys.exit()
        elif opt in ('-k'):
            keyword = arg
        elif opt in ('-m'):
            complete = bool(arg == '1')
        elif opt in ('-f'):
            enforce = bool(arg == '1')

    #read config from external file
    dic = eval(open(".config").read())
    target_url = dic['website']
    name = dic['name']
    passwd = dic['password']
    csv_name = dic['csv_name']
    path = "./dat/"
    path_file = path + csv_name
    #check existing file
    if os.path.isfile(path_file) and not enforce:
        print('parsing existing bts.csv')
    else:
        print('renew %s..' % csv_name)
        if enforce and os.path.isfile(path_file):
            os.remove(path_file)
        fetch_web(target_url, name, passwd, path_file)

    #read external csv
    df = pd.read_csv(path_file)

    #show customized results
    show_result(df, keyword, complete)

