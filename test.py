import os
import sys
import re

if __name__ == "__main__":
    a = 12
    expression = 'a>45'
    eval_code = compile(expression, '', 'eval')
    ret = eval(eval_code)
    print ret