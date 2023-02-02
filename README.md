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

The last step to being able to use these formulas is to make sure you're including the `html_math.css` stylesheet in your webpage. Make sure you're can serve the user a copy of the file at the correct location, and put the following into the "head" section of your html document:

```html
<link rel="stylesheet" href="experiment.css">
```

## The Formula Language

The formula language is not a well-known standard like LaTeX, but is fairly simple and easy to learn. It treats the following characters as special: `@«⎖»`. This set of characters has the advantage that they are rarely/never used in mathematical notation. `@` denotes the start of a function call, and can be easily typed on most keyboards. The characters `«⎖»` denote the arguments of the function call, where `«»` encloses the list of arguments and `⎖` separates the individual arguments. These characters cannot be easily typed on most keyboards, so it will be helpful to know how to quickly type them on your keyboard.

In Ubuntu, this can be done by typing `CTL-SHIFT-U` then typing the hex code for the character, then pressing "enter". Here are the relevant codes:

```
Character   Hex Code
«           ab
»           bb
⎖           2396
```

The philosophy of the language is "bring you own (unicode) symbols". To type a greek lowercase sigma, instead of typing `\sigma`, just type the unicode symbol `σ` directly. This has the advantage that any symbol in unicode, even very obscure ones, can be used in equations, so long as the client has the glyph for them. The following data may be useful to get started here:

```
Greek alphabet:
ΑαΒβΓγΔδΕεΖζΗηΘθΙιΚκΛλΜμΝνΞξΟοΠπΡρΣσςΤτΥυΦφΧχΨψΩω

Useful symbols:
∑   -- sum
⅀    -- fancy sum
∏   -- product
∫   -- integral

More symbols here: https://unicode-table.com/en/sets/mathematical-signs/
```

## Testing

Run:

```
python3 test.py
```

Open the generated `test.html` file in your browser and admire the pretty formulas.


