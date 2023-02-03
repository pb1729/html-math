from html_math import html_math
from test import PROLOGUE, EPILOGUE
import readline


print('In another tab run:')
print('python3 -m http.server')
print('Then go to that page, and navigate to test.html.')
print('Refresh the page whenever you want to view a new formula.')
while True:
    try:
        math = html_math(input('> '))
        print(math, '\n')
    except Exception as e:
        print(e)
        continue
    with open('test.html', 'w') as f:
        f.write(PROLOGUE)
        f.write('    <div class="math-p">Your formula: %s</div>' % math)
        f.write(EPILOGUE)


