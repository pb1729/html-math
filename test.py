from html_math import html_math

PROLOGUE = '''<html>
<head>
<link rel="stylesheet" href="html_math.css">
</head>
<body>
'''

EPILOGUE = '''</body>
</html>
'''

test_cases = [
    html_math('@box««@v«x»@^«T»@M«A»@v«y»⎖b»⎖«c⎖d»» + 17 + @fr«3+x@ss«2⎖0»⎖4» - @sin« (5θ)»'),
    html_math('@p«{⎖@tab««n»⎖«k»»⎖}»'),
    html_math('x < y > z'),
    html_math('a@at«»&b'),
    html_math('@p«{⎖@p«(⎖1+@fr«12⎖7»⎖)»+@p«{⎖@tab««n»⎖«k»»⎖}»⎖}»'),
    html_math('@na«∫⎖0⎖∞» @exp« »@p«(⎖@fr«-x@^«2»⎖2»⎖)» dx'),
    html_math('@na«⅀⎖s∈S» @fr«@sign« »(s)⎖|s|!»'),
]


with open('test.html', 'w') as f:
    f.write(PROLOGUE)
    for i, case in enumerate(test_cases):
        print(case, '\n')
        f.write('   <p>Test case %d: %s</p>\n' % (i, case))
    f.write(EPILOGUE)


