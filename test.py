from html_math import html_math

PROLOGUE = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="html_math.css">
</head>
<body>
    <p>Formulas:</p>
'''

EPILOGUE = '''</body>
</html>
'''


if __name__ == '__main__':
    test_cases = [
        html_math('@box««@v«x»@^«T»@M«A»@v«y»⎖b»⎖«c⎖d»» + 17 + @fr«3+x@ss«2⎖0»⎖4» - @sin« (5θ)»'),
        html_math('@p«{⎖@tab««n»⎖«k»»⎖}»'),
        html_math('x < y > z'),
        html_math('a@at«»&b'),
        html_math('@p«{⎖@p«(⎖1+@fr«12⎖7»⎖)»+@p«{⎖@tab««n»⎖«k»»⎖}»⎖}»'),
        html_math('@na«∫⎖0⎖∞» @exp« »@p«(⎖@fr«-x@^«2»⎖2»⎖)» dx'),
        html_math('@na«⅀⎖s∈S» @fr«@sign« »(s)⎖|s|!»'),
        html_math('f(n) = @p«{⎖@tab««@fr«n⎖2»⎖  @if«» n @even«»»⎖«3n + 1⎖  @if«» n @odd«»»»⎖»')
    ]

    with open('test.html', 'w') as f:
        f.write(PROLOGUE)
        for i, case in enumerate(test_cases):
            print(case, '\n')
            f.write('   <div class="math-p">Test case %d: %s ...</div>\n' % (i, case))
        f.write(EPILOGUE)


