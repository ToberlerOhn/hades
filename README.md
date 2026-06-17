# hades

Hades is a programming language created by Toby Paradise as a passion project.

# Syntax & Grammar

## Basic grammar

### Operators

#### Arithmetic

| Operator |      Meaning      |
| :------: | :---------------: |
|    +     |     Addition      |
|    ++    |  Unary Addition   |
|    -     |    Subtraction    |
|    --    | Unary Subtraction |
|    \*    |  Multiplication   |
|    /     |     Division      |
|   \*\*   |  Exponentiation   |
|   %  |  Modulo   |

#### Comparison

| Operator |         Meaning          |
| :------: | :----------------------: |
|    ==    |       is equal to        |
|    !=    |     is not equal to      |
|   ===    |     is type equal to     |
|   !==    |    is different type     |
|    >     |       greater than       |
|    <     |        less than         |
|    >=    | greater than or equal to |
|    <=    |  less than or equal to   |

|

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

- list &rarr; [element0, element1...]
  - lists are mutable and have built in methods such as .update(), .remove(), .add(), etc.. See below documentation for more detail.

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

Structures (structs) aggregate the storage of multiple data items, of potentially differing data types, into one contiguous memory block referenced by a single variable.

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

Classes have a on-creation built in method that is called, well, on creation called creators. This is to initialize any variables or perform any other tasks that you want done automatically. Creators are the always named the same name as the class itself.

Example definition:

```
Student: class {
    Student(name: str, age: int, year: int, gpa: float) => nothing {
        my.name: str = name;
        my.age: int = age;
        my.year: int = year;
        my.gpa: float = gpa;

        print('My name is %my.name%'); // see further documentation for help on printing
    };

    method AgeUp(me) => nothing {
        // by calling me within the function, all variables and methods are
        // automatically included within the scope
        my.age += 1;
        my.year += 1;
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
