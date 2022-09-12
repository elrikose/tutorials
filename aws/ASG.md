# Auto Scaling Groups (ASG)

- If load changes, create or get rid of servers quickly. Scale out/Scale in.
- Ensure minimum and maximus
- Automatically register to LBs
- You dont pay for the ASGs, just the underlying instances

- Min Capacity
- Desired Capacity
- Max Capacity

The LB checks the health of instances and can terminate.

You can scale out/in based on CloudWatch Metrics, like average CPUs

## ASG Launch Templates

Used to determine how you scale out the ASG

- AMI + instance type
- EC2 User Data
- EBS Volumes
- Security Groups
- SSH Key Pairs
- IAM Roles
- Network and subnet info

## Scaling Policies - Dynamic

Target Tracking Scaling
-  Easy setup. I want ASG CPU to stay around 40%

Simple / Step Scaling
- CloudWatch alarm, high CPU, increase by 2
- CloudWatch alarm, very low CPU, decrease by 1

Schedule Actions
- Big events. Increase capacity

## Scaling Policies - Predictive

Forecast load and adjust based on history

## Good scaling metrics

- CPUUtilization - Average CPU across instances
- RequestCountPerTarget
- Average Network In / Out - network bound

## Scaling Cooldown

- Default 5 minutes to not launch or terminate to let things stabilize.
- Use a ready made AMI instead of EC2 User data to reduce the cooldown period