# Welcome to the BulletScript Documentation!
## Introduction
BulletScript is a scripting language developed by "ademyro" in August 2022.
It is not supposed to be fast or efficient because it was made for fun.
Its syntax is C-styled, but it has some Python syntax.
Here is a BulletScript code example:
```python
# this is a comment.
# bubble sort
fn bubblesort(list) {
  for i in range(list.len()) {
    for j in range(list.len()) {
      if list[j] > list[i] {
        # swap them
        temp = list[j]
        list[j] = list[i]
        list[i] = temp
      }
    }
  }
  return list
}

println(bubblesort([4, 2, 9, 6, 1, 8, 3, 5, 0, 7]))
```

See? Not that different, eh? Anyways, let's get started.
## Getting started
Bulletscript is currently in an early stage of development. Here's what it can do for now:
* If statements
* Loops (While and For)
* Variable support (imagine no variables)
* User-Defined functions
* Print, Println, Readln, Range
* List, Number, String, Boolean support  
<a/>  
To get started, you must install BulletScript. In this repository, there is a file called BulletScript Installer. Run it from your terminal. The installer will
guide you through the installation.

Once the installer prints "Done!" you should **almost** be good to go. Now we only need to add BulletScript to the PATH.
Press **Win + R**.  
Then, type in **sysdm.cpl**. It should take you to your system's properties. Go to the 'advanced' tab.  
Click 'environment-variables'  
Double click 'Path'  
Click 'new'  
Type in 'C:\bscript-cmds'  
And then, close everything by clicking 'OK'.
Perfect! Everything should be set up now.
Next, open your **Terminal** and type in the following: 'fire'.
It should give you a Python error saying **'list index out of range'**. It is because you did not provide any arguments. However, if you do not get a Python error, you probably didn't do the installation correctly.  
Anyways, let's write a Hello World program in BulletScript!
## Hello World
Open your favorite Editor and create a file that ends with '.bs'.
Here are some functions that could help you print Hello World:
```py
print("Something") # prints something without jumping to the next line.
println("Something") # prints something and jumps to the next line.
```

Execute your code by running 'fire [file].bs' in your terminal.

# Snippets
Here are some BulletScript snippets if you are interested in viewing some simple programs written in BulletScript.
**Keep in mind that the snippets look not very efficient, as BulletScript is not that developed for now.**
### Palindrome String
```py
fn reverse(string) {
    reversed = strnull
    for c in string.chararray(), reversed = c + reversed
    return reversed
}

print(reverse("foof") == "foof")
```
### Max of two numbers (there are no ternary operators for now)
```py
fn max(x, y) {
    if x > y, return x
    return y
}
```
### Digitize Number
```py
fn digitize(num) {
    digits = []
    for n in num.string().chararray(), digits.append(n)
    return digits
}

print(digitize(123)) # [1, 2, 3]
```
### List Head
```py
random_list = range(5)
println(random_list[0]) # 0

```
# Some useful functions
## String
**string.num()**  
Returns the string as a number. If it can't be parsed as a number, he throws an error.
Example use:
```py
age = '20'
num = age.num()
println(num)
```

**string.len()**  
Returns the string's length **as a number**.  
Example use:
```py
text = 'foo'
println("Foo contains " + text.len().string() + " characters.")
```

**string.chararray()**  
Returns the string as a list.  
**Note:** In future versions this method will no longer exist, and will be replaced with **string.char_list()**  
Example use:
```py
text = 'foo'
text_chars = text.chararray()
text_chars[0] = 'b' # ['b', 'o', 'o']
```

## List
**list.string()**  
Returns the list as a string, so it can be **concatenated** among other strings.  
Example use:
```py
random_list = [1, 2, 3]
# println("List: " + random_list) # does not work
println("List: " + random_list.string()) # List: [1, 2, 3]
```

**list.append(element)**  
Appends an element to the list.  
Example use:
```py
list = [1, 2, 3]
list.append(4)
println(list) # [1, 2, 3, 4]
```

**list.len()**  
Returns the list's length **as a number**.  
Example use:
```py
list = [1, 2, 3]
println(list.len()) # 3
```

## Number
BulletScript does not do any distinction between floats and integers, he just assumes it is a number and continues.
**number.string()**  
Returns the number as a string, so you can **concatenate** it among other strings.  
Example use:
```py
age = 20
println("Age: " + age.string())
```
