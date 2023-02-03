# HTML Math

This python code generates html equations that can be placed inline with the rest of your html document. (Or you can place them on their own lines if you want, it's your choice.) [This page](https://jkorpela.fi/math/) inspired a lot of the code here.

## How to use:

To call the functionality from your own python code:

```python
from html_math import html_math
print(html_math('@na«∫⎖0⎖∞» @exp« »@p«(⎖@fr«-x@^«2»⎖2»⎖)» dx'))
print(html_math('@na«⅀⎖s∈S» @fr«@sign« »(s)⎖|s|!»'))
```

This creates the html code for the inline equation. You can run the function from a repl and then copy/paste the resulting html into your document, or call the function automatically, if your document is programmatically generated.

A note about getting these equations to show up inline: Getting them to appear on their own lines is no problem, just put them in a `<div>`. If you want them inline with text, then that entire paragraph of text should be inside of a `<div class="math-p">`, not inside a `<p>`. The reason for this is that paragraphs cannot contain block tags, but divs can. `html_math.css` already has the code for the `math-p` class.

The last step to being able to use these formulas is include the `html_math.css` stylesheet in your webpage. Make sure to serve the user a copy of the file at the correct location, and put the following into the "head" section of your html document:

```html
<link rel="stylesheet" href="experiment.css">
```

The CSS code can also be customized, with the `math-formula-root` class providing global control of all formulas. For example, this can be useful if you'd like to remove the background color of the formulas, or to specify a particular font to use. You may also wish to change around the styling of the `math-p` class some.

## Testing

Run:

```
python3 test.py
```

Open the generated `test.html` file in your browser and admire the pretty formulas.

## The Formula Language

### Introduction

The formula language is quite different from LaTeX, but is fairly simple and easy to learn. It treats the following characters as special: `@«⎖»`. This set of characters has the advantage that they are rarely/never used in mathematical notation. `@` denotes the start of a function call, and can be easily typed on most keyboards. The characters `«⎖»` denote the arguments of the function call, where `«»` encloses the list of arguments and `⎖` separates the individual arguments. These characters cannot be easily typed on most keyboards, so it will be helpful to know how to quickly type them on your keyboard.

In Ubuntu, this can be done by typing `CTL-SHIFT-U` then typing the hex code for the character, then pressing "enter". Here are the relevant codes:

```
Character   Hex Code
«           ab
»           bb
⎖           2396
```

### Philosophy

The philosophy of the language is "bring you own (unicode) symbols". To type a greek lowercase sigma, instead of typing `\sigma`, just type the unicode symbol `σ` directly. This has the advantage that any symbol in unicode, even very obscure ones, can be used in equations, so long as the client has the glyph for them. The following data may be useful to get started here:

```
Greek alphabet:
ΑαΒβΓγΔδΕεΖζΗηΘθΙιΚκΛλΜμΝνΞξΟοΠπΡρΣσςΤτΥυΦφΧχΨψΩω

Useful symbols:
∑   -- sum
⅀   -- fancy sum
∏   -- product
∫   -- integral

More symbols here: https://unicode-table.com/en/sets/mathematical-signs/
```

### Formula language tutorial

Launch:

```
python3 interactive.py
```

Follow the instructions for starting the server and navigating to the correct page. Refresh the page whenever you want to view a formula you entered.

#### Bolded vectors and operators

Variables are normally italic. Variables representing a vector are bold and italic, and those representing an operator are bold. The command to write a vector variable is `@v`, so you might write a vector like `@v«v»`. The command to write an operator variable is `@M` (think "Matrix"), so you might write an operator like `@M«M»`. Here's a simple linear equation:

```
@M«A»@v«x» = @v«b»
```

This command should only be applied to single greek or latin letters, the interpreter will get confused if you try to apply it to multiple letters, or to other symbols.

#### Fractions

The command to write fractions is `@fr`. It takes 2 arguments, the numerator and denominator of the fraction. Remember to separate the arguments with `⎖`, which has hex code `0x2396`. Here's a simple fraction:

```
@fr«3⎖4»
```

Here's a more complicated nested fraction containing variables and symbols. (Note the use of the unicode minus sign `−` (hex code `0x2212`) for subtraction, which is slightly longer than the usual dash `-`.)

```
@fr«@v«x»∙@M«A»@v«y» + @fr«12⎖7»⎖1 − z»
```

#### Superscripts and subscripts

Superscripts and subscripts are written separately from the variable being super/subscripted. The variable could go before, or after, or doesn't even need to be there at all! Superscript: `x@^«2»`. Subscript: `x@_«0»`. Both: `x@ss«2⎖0»`. The command `@ss` is a double acronym: it stands for both SuperScript and SubScript. Try the fomula `@ss«2⎖0»`: sub/super-scripts can stand alone.

#### Special functions

There are lots of functions that look like words. They are representated as a sequence of non-italic letters. For example, "sin", "cos", "exp", "mod", "det", "Tr", "sign", and so on. The formula language takes a permissive attitude to typesetting these special functions: Any function call that doesn't correspond to a built-in function will be interpreted as a special function. Example formulas:

```
@sin«»(θ)
@det« »@M«X»
@ss«@hello«»⎖@world«»»
```

Note that we put a space `« »` as the argument if we want a gap between the function and the thing it's being applied to.

#### Arrays

You can also use the delimiters `«⎖»` without an associated function call, this will produce an array. For example, `«1⎖2⎖3»` produces the array `[1, 2, 3]`. You might think that arrays are not too useful, since you could just write the brackets and commas yourself. The real utility of arrays will be seen in the next section.

#### Tables, matrices, and boxes

Tables, matrices, and boxes are for when we need to represent a grid of numbers (or other data). The most basic kind of grid is a table. In a matrix the numbers are spaced out from each other, so that neighbouring numbers are not confused as belonging to the same entry of the matrix. Boxes are like a matrix, but have a border around them. The arguments for all of these functions are arrays, with each array representing a row of the matrix. Examples:

```
@tab««a⎖b»⎖«c⎖d»»
@mat««a⎖b»⎖«c⎖d»»
@box««a⎖b»⎖«c⎖d»»
```

The recommended option for represeting matrices, column vectors, and row vectors is `@box`. This notation is clear, reduces the overloading of parentheses and brackets, and is a good fit for representing formulas on a computer.

#### Parentheses that grow

What if you really don't want to use the newfangled box notation? You might think of trying something like this:

```
(@mat««a⎖b»⎖«c⎖d»»)
```

That just results in tiny parentheses around a big matrix. To get them to grow with the matrix, you'll have to use the `@p` command, which is size its outer arguments to match the height of its inner argument. This will give a conventional matrix, represented with parentheses:

```
@p«(⎖@mat««a⎖b»⎖«c⎖d»»⎖)»
```

Using some creativity and leaving the last argument blank, you can also do multi-case functions this way:

```
f(n) = @p«{⎖@tab««@fr«n⎖2»⎖  @if«» n @even«»»⎖«3n + 1⎖  @if«» n @odd«»»»⎖»
```

#### N-ary sums and products, integrals, etc.

The last function is a fairly easy one: `@nr`, which stands for "n-ary". This lets us represent sums, products, and integrals. It takes 1 to 3 arguments, depending on whether we want no limits, a lower limit only, or both lower and upper limits. Examples:

```
@na«∫» x dx
@na«∑⎖s∈S» |s|
@na«∏⎖i=1⎖∞» @fr«2@^«i» − 1⎖2@^«i»»
```

#### End of tutorial

You can exit the interactive formula tester by triggering a keyboard interrupt (`CTL-C`).




