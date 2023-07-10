# Terraform Expressions

Language features that are used to refer or comput values within a configuration

- Strings and Templates
- References to values
- Operators
- Function Calls
- Conditional expressions
- For expressions
- Splat expressions
- Dynamic blocks
- Type constraints
- Version constraints

# Types and Values 

Primitive
- string
- number
- bool

No Type
- null - used to specify the default of resource configuration

Collections
- list
- map

# Strings

You can only use double quotes. 

Special characters:

- `\n` - newline
- `\t` - tab
- `\uNNNN` - Unicode charaters
- `$${` - literal `${`
- `%%{` - literal `%{`

Multiline uses **heredoc** style:

```sh
<<EOF
This is 
multiline
EOF
```

# String Template

String interpolation converts variables into strings using the `${ ... }`. For example:

```sh
"Instance type: ${var.instance_type}"
```

String directives use `%{ ... }` to evaluate conditional logic. For example:

```sh
"Instance type: %{ if var.instance_type != "" }${var.instance_type}%{ else }none%{endif }"
```

Or as part of a multiline:

```sh
<<EOF
%{ for ip in aws_instance.example.*.private_ip }
server ${ ip }
%{ endfor}
EOF
```

# Operators

Mathematical operations to perform on numeric expressions:

- addition: `a + b`
- subtraction: `a - b`
- multiplication: `a * b`
- division: `a / b`
- modulus: `a % b`
- equality: `a == b`
- not-equal: `a != b`
- less than: `a < b`
- less than or equal: `a <= b`
- greater than: `a > b`
- greater than: `a >= b`
- or: `a || b`
- and: `a && b`
- negate: `!boolean`

# Conditionals

Only way to do if/else statements in expressions:

`boolean condition ? true_value : false_value`

Typical pattern to set a default if a variable is not set

`var.a != "" ? var.a : "default"`

# For

For allows for iteraton over a list, set, map, or object

list example:

`[for item in var.list: length(item)]`

list example with index:

`[for index, item in var.list: "${index}: ${item}"]`

map example is key and value:

`[for key, value in var.map: "${key}: ${value}"]`

All examples above return a tuple (immutable list). If you put them in `{}` it will return an object.

`{ for item in var.list : item => "item is ${item}" }` creates an object `{ item1 = "item is item1", item2 = "item is item2"}`

You can also conditionalize the for loop results:

`[ for item in var.list: item if item != "" ]`

# Splats

Shorter syntax for **for expressions**. It originated from Ruby. It is used to simplify `for_each` addressing of the inner part of the object

# Dynamic Blocks

Dynamic blocks allow you to construct repeatable nested blocks in a repeatable way.

# Version Constraints

Terraform uses semantic versioning `major.minor.patch`. So you can constrain the version:

- version must equal `"1.0.0"` or `"=1.0.0"`
- version must not equal `"!=1.0.0"`
- version is greater than, or less than `>=1.0.0`
- accept versions that only increment patch `~> 1.0.0`

# Progressive Versioning

Progressive versioning is the practice of always using the latest version of something for security, tech debt, agility.

- Run test builds with latest changes
- Stay compatible to fix small things instead of big things