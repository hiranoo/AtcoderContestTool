# This tool can give you many merits below
* You can check your code faster than manual check
  * No need to copy and paste test cases
  * No need to compare your output and the correct output
  * PARALELLY check your code with each of the test cases
* You will never submit your code by mistake
* Only one command "act" is needed to submit your code! You are even free from specifying file name!

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
    * your output would be displayed only if WA
    * desired output would not be displayed
    * error messages would be displayed if 
  * another choice:
    * display all outputs and error messages regardless of the result
    
## Submitting your code
* C++, Java and Python are supported
* as default:
  * your code would be submitted only when passed all test cases
  * your code would be lastly modified code regardless of language
* another choice:
  * your code would be submitted if not passed all test cases
  * your code would be specified with its file name
