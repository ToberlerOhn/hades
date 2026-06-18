# hades

Hades is a programming language created by Toby Paradise as a passion project.

# Syntax & Grammar

## Basic grammar

### Operators

#### Arithmetic Operators

|   Operation    |  Syntax  |
| :------------: | :------: |
|   Unary Plus   |   `+a`   |
|  Unary Minus   |   `-a`   |
| Incrementation |  `a++`   |
| Decrementation |  `a--`   |
|    Addition    | `a + b`  |
|  Subtraction   | `a - b`  |
| Multiplication | `a \* b` |
|    Division    | `a / b`  |
|     Modulo     | `a % b`  |

Note that exponentiation is not defined as an operator, but as a function `pow(a,b)`

#### Comparison Operators

|        Operation         |     Syntax     |
| :----------------------: | :------------: |
|         equal to         |    `a == b`    |
|       not equal to       |    `a != b`    |
|      type equal to       |   `a === b`    |
|    type not equal to     |   `a !== b`    |
|       greater than       |    `a > b`     |
|        less than         |    `a < b`     |
| greater than or equal to |    `a >= b`    |
|  less than or equal to   |    `a <= b`    |
|         contains         | `a contains b` |

#### Logical Operators

| Operation |   Syntax   |
| :-------: | :--------: |
|    NOT    |    `!a`    |
|    AND    |  `a && b`  |
|    OR     | `a \|\| b` |
|    XOR    |  `a ^^ b`  |

#### Bitwise Operations

|  Operation  |  Syntax  |
| :---------: | :------: |
|     NOT     |   `~a`   |
|     AND     | `a & b`  |
|     OR      | `a \| b` |
|     XOR     | `a ^ b`  |
| Shift left  | `a << b` |
| Shift right | `a >> b` |

#### Assignment Operators

Assignment: `a = b`
| Syntax | Equivalence |
| :-----: | :------: |
| `a += b` | `a = a + b` |
| `a -= b` | `a = a - b` |
| `a *= b` | `a = a * b` |
| `a /= b` | `a = a / b` |
| `a %= b` | `a = a % b` |
| `a &&= b` | `a = a && b` |
| `a \|\|= b` | `a = a \|\| b` |
| `a ^^= b` | `a = a ^^ b` |
| `a &= b` | `a = a & b` |
| `a \|= b` | `a = a \| b` |
| `a ^= b` | `a = a ^ b` |

### Datatypes:

#### Simple datatypes:

- nothing &rarr; `nothing`
- boolean &rarr; `TRUE`, `FALSE`
- integer &rarr; `1234`
- floating point number &rarr; `1234.5678`
- string &rarr; `'foo'`

#### Complex datatypes:

- function &rarr; see below section
- structure &rarr; ...
- class &rarr; ...

##### Arrays:

- record &rarr; "element0, element1"
  - records are immutable sequences of items of arbitrary type.
  - attempting to mutate (i.e. update, remove, or add elements) throws a TypeError
  - accessed using record"element_index"

- list &rarr; [element0, element1...]
  - lists are mutable and have built in methods such as .update(), .remove(), .add(), etc.. See below documentation for more detail.
  - accessed using list[element_index]

#### Defining variables using datatypes:

|       Full name       | Definition name |
| :-------------------: | :-------------: |
|        nothing        |    `nothing`    |
|        boolean        |      `_b`       |
|        integer        |      `int`      |
| floating point number |     `float`     |
|        string         |      `str`      |
|        record         |      `rec`      |
|         list          |     `list`      |
|       structure       |    `struct`     |

Variables above must be decalred and initialized in the same statement, with the exeption of nothing. For example,

```
foo: nothing;
bar: _b = FALSE;
```

Lists must note the type within the list, with the possiblity of multiple types, but records do not:

```
baz: list<int, float> = [1, 1.5, 2, 2.33];
qux: record = "1, 1.5, 2, 2.33";
```

#### Other declarations of complex datatypes

##### Functions:

```
func my_function(parameter1: type, paramter2: type...) => ReturnType {
    // function body goes here
};
```

##### Structures:

Structures (structs) aggregate the storage of multiple data items, of potentially differing data types, into one contiguous memory block referenced by a single variable. An item is referred to as a 'struct value'.

Example definition:

```
Student: struct = {
    age: int;
    id: int;
    university: str;
    gpa: float
};
```

There are two ways to create a struct from a template:

```
Alice: struct<Student> = {21, 82911, 'UMass Amherst', 3.712};
Bob: struct<Student> = {
    age = 20,
    id = 278925,
    university = Williams,
    gpa = 3.980
}
```

The second can be used for more clarity, especially in cases with large structs with many items to keep track of.

##### Classes:

A class acts as a constructor or template for objects created using the class. They are like structures, but they can also include methods that act like a function within the class.

Classes use `my.` to refer to in-class methods and variables, like `this` or `self`.

Classes have an on-creation built in method that is called on creation (duh), called creators. This is to initialize any variables or perform any other tasks that you want done automatically. Creators are the always named the same name as the class itself.

Example definition:

```
Student: class {
    creator Student(name: str, age: int, year: int, gpa: float) => nothing {
        my.name: str = name;
        my.age: int = age;
        my.year: int = year;
        my.gpa: float = gpa;

        print('My name is %my.name%'); // see further documentation for help on printing
    };

    method AgeUp(me) => nothing {
        // by calling me within the function, all variables and methods are
        // automatically included within the scope
        my.age++;
        my.year++;
    };
}
```

Example creation:

```
Alice: Student = Student{
    'Alice',
    20,
    3,
    3.712};
Alice.AgeUp();
print(Alice.age); // prints 21
```

### If statements

If statements are handled like most languages:

```
foo = 5;
if (foo == 3) {
    print('foo is 3');
} else if (foo == 5) {
    print('foo is 5');
} else {
    print('foo isn\'t 3 or 5')
}
// outputs 'foo is 5'
```

### Loops

There are four types of loops.

#### While loops

A while loop checks a condition, then if the condition is truthy, executes the statement within the brackets. It continues doing this until the condition is false.

```
while (condition) {
    // code goes here
};
```

Do-while loops first do the statement within brackets, then check the condition after. This means that a do-while loop is executed at least once, buta a while loop may not be executed at all.
```
do {
    // code goes here
} while (condition);
```

Here is code using both types of while loops that both output
```
0
1
2
```
using a while loop:
```
i = 0;
while (i < 3) {
    print(i);
    i++;
};
```
using a do-while loop:
```
i = 0;
do {
    print(i);
    i++
} while i < 2;
```

## Truthiness

Truthiness is used to determien whether a non-boolean value evaluates to a TRUE or FALSE, especially when dealing with if statements (see above)

| Data type |    Truthy set     | Falsy set |
| :-------: | :---------------: | :-------: |
|  nothing  |        N/A        |    all    |
|  boolean  |       TRUE        |   FALSE   |
|  integer  |        ≠ 0        |     0     |
|   float   |       ≠ 0.0       |    0.0    |
|  string   |     non-empty     |    ''     |
|  record   |     non-empty     |    ""     |
|   list    |     non-empty     |    []     |
| structure | containing values |   empty   |