# Intro

   Stringify makes you easy to stringify complex data structure,
 especially useful for debugging purpose. Since object may implement its own toJSON function,
 JSON.stringify may ignore some attributes. Using Stringify, you don't need to worrty that something is hidden
 from custom toJSON implementation. Also, Stringify will print functions if there's any one,
 and you may choose to print the content of the functions.

# Installation

```bash
npm install git+https://git@github.com/roackb2/stringify.git
```

# Feature

* Circular detection: No need to worry about circular references
* Function attributes printed: You could see all functions inside an object
* Print function content: If specified, Stringify would print function content and is beatifully indented. (as long as the closing curly bracket of the function is correctly indented)

# Usage

```javascript
var obj = [{
    hello: "world1",
    test: true,
}, {
    hello: "world2",
    test: {
        inner: 1, object: "two"
    },
    test2: {
        inner: 2, object: "three"
    }
}, {
    hello: "world3",
    test: [{
        inner: 1
    }, {
        inner: {
            supperInner: "hi",
            func: function() {
                var test;
            },
            func2:
                function()
                    {
                        var test2
                    },
            err: new Error("test error object"),
            date: new Date(),
            reg: /ab+c/
        }
    }],
}];
obj[2].weird_arr = [];
obj[2].weird_arr.test = 'yo';
obj[2].weird_arr['\0x2c'] = 'hey';
obj[3] = obj;
obj[4] = obj[1];
var args;
function test(one, two, three) {
    obj[5] = arguments;
    console.log(stringify(obj, false, true));
}
test(1, 2, 3)
```
The result would be:

```javascript
[
    0: {
        hello: world1,
        test: true
    },
    1: {
        hello: world2,
        test: {
            inner: 1,
            object: two
        },
        test2: {
            inner: 2,
            object: three
        }
    },
    2: {
        hello: world3,
        test: [
            0: {
                inner: 1
            },
            1: {
                inner: {
                    supperInner: hi,
                    func: function () {
                        var test;
                    },
                    func2: function ()
                    {
                        var test2
                    },
                    err: Error: test error object,
                    date: Tue Jan 05 2016 14:53:44 GMT+0800 (CST),
                    reg: /ab+c/
                }
            }
        ],
        weird_arr: {
            test: yo,
            x2c: hey
        }
    },
    3: [Circular],
    4: {
        hello: world2,
        test: {
            inner: 1,
            object: two
        },
        test2: {
            inner: 2,
            object: three
        }
    },
    5: [
        0: 1,
        1: 2,
        2: 3
    ]
]
```

# Parameters

stringify(obj, ignoreFunc, printFuncContent)

* obj [Any]: the object to stringify
* ignoreFunc [boolean]: whether to ignore function attributes
* printFuncContent [boolean]: whether to print funciton content, the ignoreFunc must be set to false.

> NOTICE: function stringify takes more than three arguments, except for the first three ones, the other ones are for internal recursive call usage, so don't pass more than three arguments to the funciton when calling it.

# Supported Data Types

* Object
* Array
* Arguments
* Date
* Boolean
* Number
* String
* Error

# Unsupported Data Types

* Map
* Set
* WeakMap






