# web-crawler
A personal utility to facilitate information retrieval

How to use:
1. Install Python 3
   go to https://www.python.org/downloads/ and choose the latest version
2. Install pandas
   http://pandas.pydata.org/pandas-docs/stable/install.html
   (note: "pip install pandas" if you have pip installed)
3. Install robobrowser
   http://robobrowser.readthedocs.io/en/latest/installation.html
   (note: "pip install robobrowser" if you have pip installed)
4. config ".config" file in this directory
   fill in "website", "name", and "passwd" (mandatory, or it will not work for sure.)
5. run "python web_crawler.py <keyword>"

Note:
There might be a annoying warning message for the lack of default xml parser.
You can patch the following file to mute the warning:
    in "/usr/local/lib/python3.5/dist-packages/robobrowser/browser.py" (find it in your own platform)
    - def __init__(self, session=None, parser=None, user_agent=None,
    + def __init__(self, session=None, parser="lxml", user_agent=None,


It is verified under Python 3.5.2 for the moment.

