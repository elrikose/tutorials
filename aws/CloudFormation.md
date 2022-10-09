# CloudFormation

CloudFormation - declarative Infrastucture as Code Automation. Create, update, delete infrastructure

Manual Work is hard to reproduce
- in another region
- in another AWS account
- Same region but different params

Create all of this in one stack:

- ELB
- Two EC2 instances with 2 elastic IPs
- Security Group
- S3 bucket

CloudFormation will create all of it in the right order.

# Benefits

Code:
- Don't manually create anything
- Version control
- Code reviews

Cost:
- Free except the cost of the stack.
- Templates can be cost estimated for the spend
- Automate the deletion and creation of templates

Productivity
- Destroy and re-create whenever you want
- UI creates a diagram

Separation of usage
- VPC stack
- App Stack

# How Does It Work?

- Templates are uploaded to S3
- Templates are read-only have have to be replaced with a new version
- Stacks have a name
- Deleting a stack deletes everything

# Templates

- Use the GUI Designer
- Build YAML files and execute with `aws` CLI.

Resources Section
- Mandatory
- All your cloud resource are declared here
- Parameters - inputs to the CF
- Mappings - static variables
- Outputs - what has been created
- Conditionals - control what is created
- Metadata

Helpers
- Reference other templates
- Functions

# Creating in Console

- There is an option to switch between JSON and YAML
- When creating a new stack, you can import New Resources or Existing Resources
- Either upload or specify an S3 URL for a template if you have an existing template.

# Change Set Preview

If you replace an existing template, the UI gives you a "Change set preview". It lists things that are Added, modified, or deleted.

# Resources

Cloud resources which is the only **mandatory** section in a Cloud Formation template. 

- Resources can reference each other
- There are over 224 types of resources
- Resource names are defined by `AWS::<product name>::<data type name>`
- Look at the Amazon docs to get all of the resource properties: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html

- You can't create a dynamic set of resources since it is a declarative syntax
- Not all AWS Services are supported, but most are.
- If a service isn't supported you can use a Lambda Custom Resource

# Parameters

A way to provide inputs to the template.

- For reusability
- Some parameters can't be known beforehand
- Use if a value is likely to change in the future

## Parameter Settings

- Types
  - String
  - Number
  - CommaDelimitedList
  - List
  - AWS Parameter
- Description
- Constraints
- Constraint Description
- Min/Max Length
- Min/Max Value (Number)
- Defaults
- AllowedValues (array)
- AllowedPattern (regex)
- NoEcho (secrets)

## Parameter References

You reference a parameter using the `Fn::Ref` function with the shorthand being `!Ref`.

`!Ref` can also be used to reference other items in the template (parameters, resources)

## Pseudo Parameters

AWS offers pseudo params that can be use anywhere

- AWS::AccountId
- AWS::NotificationARNs
- AWS::Region
- AWS::NoValue
- AWS::StackId
- AWS::StackName

# Mappings

Fixed variables in your template. All values are hardcoded in the template. Use case dev/prod, regions your targeting, ami types.

Use mappings when you know all of the values based on an environment:

- Region
- AZ
- Account
- Environment

Use params when you need user control at template run.

## Fn::FindInMap

Function that gets a value from a map

```
!FindInMap [ MapName, TopLevelKey, SecondLevelKey ]
```

# Outputs

Optionally output values that can be used in other stacks. A way to link templates. Use case: Template that creates a VPC and subnets and you export those as outputs.

Notes:
- You have to export the output for it to be used somewhere else
- Best way to collaborate on a team
- You can't delete a stack until the referencing stacks are deleted.
- Exporting. Use `Export: Name:` in the output
- Importing. Use `Fn::ImportValue` or `!ImportValue`

# Conditions

Used to control the creation of resources. 

- Use case: In a certain environment (dev, test, prod) do or don't create resource.

```yaml
Conditions:
  CreateProdResources: !Equals [ !Ref EnvType, prod ]
```

Conditional functions
- `Fn::And`
- `Fn::Equals`
- `Fn::If`
- `Fn::Not`
- `Fn::Or`

How to conditionalize a resource?

```yaml
Resources:
  MountPoint:
     Type: "AWS::EC2::VolumeAttachment"
     Condition: CreateProdResources
```

# Intrinsic Functions

Functions you can use in any template

- `Fn::Ref` - reference parameters and resources
- `Fn::GetAtt` - Get other attributes out of the resources from `!Ref`
- `Fn::FindInMap` - Get values out of Mappings. Requires 3 params.
- `Fn::ImportValue` - Get items exported from other templates
- `Fn::Join` - Joins values with a delimeter
- `Fn::Sub` - Substitute values
- Conditions: `Fn::And`, `Fn::Equals`, `Fn::If`

## GetAtt

```yaml
AvailabilityZone:
  !GetAtt EC2Instance.AvailabilityZone
```

## Join

```yaml
Item: !Join [ delimeter, [ comma-delimeted list ]]
```

If delimeter is `:`, and list is `a, b, c` it would create `a:b:c`

```yaml
Item: !Join [ ":", [ a, b, c ]]
```

## Sub

Very handy way to subsitute values. String must have `${VariableName}`.

# Rollbacks

If a stack creation fails:

- Everything rollsback and is deleted
- Look at the logs
- Optionally you can ask not to rollback for troubleshooting purposes

If stack update fails

- Rollsback to previous known state
- Logs

# ChangeSets

When you update a stack is shows you what will be changed

# Nested Stacks

Stacks part of other stacks. Isolate the same patterns. Considered best practices. You have to update the parent stack before the child

# Cross Stacks

Stacks with different lifecycles

- Uses stack exports and `!ImportValue`
- Pass exports to multiple stacks

Nested stacks are different from cross stacks. They are not shared.

# Stack Sets

Create, update, or delete stacks among different accounts or regions.

- There is an Administrator needed for StackSet
- Trusted accounts can update their own part of the stacks
- Updating a stack set updata all stack instances.

# CloudFormation Drift

What happens if someone manually changes the configuration? That is a drift.

CloudFormation can use CloudFormation Drift feature to detect drift. It shows you the difference. You can update the templates, or revert the stack.

Use CloudTrail to see who made the change.




