[日本語記事はこちら](https://qiita.com/kovin/items/b24fa91f89449cb6f3c6)
# What this application brings to you
* You can check your code faster than manual check
  * No need to copy and paste test cases
  * No need to compare your output and the correct output
  * PARALELLY check your code with each of the test cases
* You will never submit your code by mistake
* Only one command `act` is needed to submit your code! You are even free from specifying file name!

[You can see specific examples in this article.](https://qiita.com/kovin/items/b24fa91f89449cb6f3c6) (Japanese)

# Usage
* clone this repository (anywhere you like)
* fill ./sample/config.json
* install python libraries if you need: `bs4, pickle, json, abc, argparse`
* add alias of this app to bashrc: `alias act='python3 [path of where you cloned this repository]/AtcoderContestTool/sample/main.py'`

* git clone this repository
```
git clone https://github.com/hiranoo/AtcoderContestTool
```
* move to sample directory
```
cd AtcoderContestTool/sample
```
* create act_config.json
```
cp act_config.json.sample act_config.json
```
* change 4 'hogehoge's depending on your environment
```
vi act_config.json
```
* change main.py at line 15 to the full path of your cloned repository
* set alias of this application. 'hogehoge' means the path.
```
vi ~/.bashrc

alias act='/hogehoge/AtcoderContestTool/sample/main.py'
```
* install python libraries: 
abc
os
sys
glob
shutil
time
subprocess
bs4
multiprocessing
argparse
json
requests
pickle

* update template file (optional)
```
AtcoderContestTool/sample/template.cpp
```
modify code if you like

if you change file name, update "env"."template_filename" in act_config.json.

# Functions
* to fetch test cases
* to check your code with test cases (you can specify test case number or all cas
* to submit your code (your code could be submitted if passed the all test cases as default, or if ordered with your commandline input)

## Fetching test cases
* test cases could be scraped from the contest page

## Checking your code with test cases

### Flow
* Fetch test cases if no cases are found
* Check your code with all cases as default or the ordered case
  * as default:
    * your code would be the lastly modified one
    * your code would be compiled beforehand if needed
  * another choice:
    * you can specify the file name to check
* Check result would be AC, WA, RE or TLE
  * as default:
    * display all outputs and error messages if the result is WA, RE, or TLE.
    
## Submitting your code
* `C++ and Python are supported`
* as default:
  * your code would be submitted only when passed all test cases
  * your code would be lastly modified code regardless of language
* another choice:
  * your code would be submitted even if it wouldn't pass all test cases
  * your code would be specified with its file name
