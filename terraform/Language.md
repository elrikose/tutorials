# Terraform Language Features

Terraform language is based off of HCL. There is extensions to it to support Dynamic Blocks and For Each.

HCL is used for:
- Terraform
- Packer Templates
- Vault Polices
- Consul Config
- Nomad Jobs

# Input Variables

Input Variables are also known as parameters to modules. They require a type, but can also define a default value, description, validation, and whether it is sensitive:

```js
variable "string_var" {
    type = string
}

variable "list_var" {
    type = list(string)
    default = [ "item1", "item2" ]
}
```

## Variable Definition Files

Define variable in a file named `terraform.tfvars`, which is autoloaded as key-value pairs

```ini
instance_type = "t2.micro"
list_var = [ "item3", "item4" ]
```

## Loading Variables

Ways in which files are loaded

- `terraform.tfvars` - loaded automatically during `terraform apply`
- `dev.tfvars` - not autoloaded
- `dev.auto.tfvars` - autoloaded, good for environments
- `-var-file dev.tfvars` - CLI option to load the variables explicitly
- `-var instance_type="t2.micro"` - Load a single variable

## Environment Variables

If you preface an environment variable with `TF_VAR_` it will automatically be read and loaded.

```sh
export TF_VAR_instance_type="t2.micro"
```

## Variable Precedence

- Environment
- terraform.tfvars
- terraform.tfvars.json
- `.auto.tfvars` or `.auto.tfvars.json`
- `-var`` or `-var-file`

# Output Values

Output values are computed value after `terraform apply` is done. 

- You can also give the outputs a description and mark them sensitive. 
- Sensitive won't be displayed to the terminal but it will be in the state file.
- `terraform output` to get the output values in a key value way.
- `terraform output -json` will dump it as JSON
- `terraform output ip_address` will output the IP Address without key
- `terraform output -raw ip_address` will not put it in quotes

# Local Values

Locals are like consts. You can define them once and use them in multiple locations in the module

```js
locals {
    instance_type = "t2.micro"
    env = "dev"
}
```

You can define multiple locals blocks in a module. Once declared, you can reference it via `local.variable_name` (eg. `local.instance_type`)

# Data Sources

Information defined outisde of Terraform. Defined in a `data` block

There is a way to use the filter block to retrieve data based on state or tags.

```js
data "data_type" "variable_name" {
  filter {
    name = "tag:owner"
    values = [ "devops" ]
  }

  filter {
    name = "tag:environment"
    values = [ "dev" ]
  }
}
```

# Resource Arguments

A way to change the behavior of a Terraform resource:

- depends_on - define dependencies explicitly
- count - create multiple instances of a resource
- for_each - create multiple instances based on a map of strings
- provider - non-default provider configurations
- lifecycle - customize the lifecycle of the resource
- provisioner - launch actions after resource creation

# Collection Types

Three types of collections

- list
- map
- set

List referencing

```js
variable "friends" {
  type list
  default = ["tom", "fred", "larry"]
}
friend = var.friends[0]
```

Map referencing

```js
variable "friends" {
  type map
  default = {
    "best friend" = "tom",
    "next best friend" = "fred",
    "least best friend" = "ned"]
}
friend = var.friends["best friend"]
```

Set is similar to a list, but must be the same type

# Structural Type

You can define a structured variable with an `object()` function that is set to type:

```js
variable "my_object" {
  type = object({
    instance_name = string
    instance_tag = optional(list)
  })
```

Tuples are used for returning multiple return values.

# Built-in Functions

Terraform includes functions to help transform and combine data into expressions

- Numeric - `abs()`, `floor()`, `ceil()`, `min()`, `max()`
- String - `chomp()`, `format()`, `indent()`, `join()`, `split()`, `lower()`, `regex()`, `replace()`, `substr()`, `trim()`
- Collection - `compact()`, `concat()`, `contains()`, `keys()/values()`, `length()`, `lookup()`, `merge()`, `sort()`
- Encoding - `base64encode()`, `base64decode()`, `urlencode()`
- Filesystem - `abspath()`, `dirname()\basename()`, `pathexpand()`, `file()`, `fileexists()`
- Date/Time - `formatdate()`, `timestamp()`
- Networking - `cidrhost()`, `cidrnetmask()`, `cidrsubnet()`
- Type Conversions - `can()`, `defaults()`, `tobool()`, `tomap()`, `tolist()`

Numeric Standouts:
- `parseint("FF", 16)` - converts a hex number string to int - 255
- `parseint("1010", 2)` - converts binary number string to int - 10

String Standouts
- `chomp("Yo Dawg\n\n")` - eats newline characters at end
- `format("Yo %s", "Dawg")` - formats a string
- `join(" ", [ "string1", "string2" ])` - joins a list of strings with first parameter - `"string1 string2"`
- `lower("UPPER")` - Lowercase a string - `upper`
- `upper("lower")` - Uppercase a string - `LOWER`
- `trimspace("  Yo!!\n")` - removes all whitespace at beginning and end

Collection Standouts
- `compact(["p","","o","t","t","e","r"])` - Removes empty strings
- `concat(["p","o","t"], ["t","e","r"])` - Concats two strings
- `contains(["p","o","t","t","e","r"], "t")` - returns if a string is in a list
- `keys()` - returns keys from a map as a list
- `values()` - returns values from a map as a list
- `zipmap()` - create a map from 2 lists. The first is the keys, the second is the values

File Standouts
- `file("path.txt")` - Reads contents of files into a string
- `fileexists("path.txt")` - Returns boolean if it exists

Network Standouts
- `cidrhost()` - Calculates a host IP based on a CIDR range and index
- `cidrnetmask()` - Calculates a netmask based on a CIDR range
- `cidrsubnet()` - Gets a subnet CIDR if you want to split a cidr range