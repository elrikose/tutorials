# Elastic Block Store (EBS)

From [Amazon](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AmazonEBS.html):

>Amazon Elastic Block Store (Amazon EBS) provides block level storage volumes for use with EC2 instances. EBS volumes behave like raw, unformatted block devices. You can mount these volumes as devices on your instances. EBS volumes that are attached to an instance are exposed as storage volumes that persist independently from the life of the instance. You can create a file system on top of these volumes, or use them in any way you would use a block device (such as a hard drive). You can dynamically change the configuration of a volume attached to an instance.


## Delete on Termination

I created my web server late last year on an EC2 instance on AWS. While I built the instance with terraform, I didn't set the EBS for the EC2 instance's "Delete on Termination" flag to false. That would mean if I would terminate the instance instead of stop it, that my main EBS volume would just disappear. While that's not that big of a deal because I built the webserver with automation and could easily regenerate it quicky. I didn't necessarily want to lose things like server logs.

I started poking around the console looking for how to switch the flag and I was perplexed how to set it after the fact. I went poking around the web and found there was no way to do it! You have to use the `aws ec2 modify-instance-attribute` CLI command to change it

### Parameters for the CLI 

You need two things to be able to use the AWS CLI command

- EC2 instance ID
- Storage device name

The instance ID was easy to get either by using the console or in a roughshod way using the AWS CLI:

```shell
$ aws ec2 describe-instances --output yaml | grep Instance
  Instances:
...
    InstanceId: i-04753
    InstanceType: t2.micro
...
```

The device name is also easy to find in the console by going to the Storage tab, but can also be found via the CLI:

```shell
$ aws ec2 describe-instances --output yaml | grep -A 6 BlockDeviceMappings
    BlockDeviceMappings:
    - DeviceName: /dev/xvda
      Ebs:
        AttachTime: '2021-11-28T03:03:28+00:00'
        DeleteOnTermination: true
        Status: attached
        VolumeId: vol-0e40
```

That would mean our two parameters would be:

- EC2 instance ID: i-04753
- Storage device name: /dev/xvda

### Running the CLI

First you need to create a json file that specifies the device name and the DeleteOnTermination flag:

```json
[
  {
    "DeviceName": "/dev/xvda",
    "Ebs": {
      "DeleteOnTermination": false
      }
  }
]
```

And then you invoke the comand:

```
aws ec2 modify-instance-attribute --instance-id i-04753 --block-device-mappings file://storage.json
```

There is no output on a successful change, but you can confirm that the change was made with the same command as above:

```shell
$ aws ec2 describe-instances --output yaml | grep -A 6 BlockDeviceMappings
    BlockDeviceMappings:
    - DeviceName: /dev/xvda
      Ebs:
        AttachTime: '2021-11-28T03:03:28+00:00'
        DeleteOnTermination: false
        Status: attached
        VolumeId: vol-0e40
```

Notice **DeleteOnTermination** is now set to false.

(HT to [Pete Wilcock](https://www.petewilcock.com/how-to-modify-deletion-on-termination-flag-for-ebs-volume-on-running-ec2-instance/))

## Snapshots

- Snapshots are a good way to transfer EBS storage from one Availability Zone to another.
- It is recommended to turn off the EC2 Instance before snapshotting it based on your use case.
- Move a snapshot to an archive tier to save roughly 75% of the cost, but it takes 1-2 days to recover.
- Setup a snapshot recycle bin with a retention policy of 1 day to 1 year.
- From a snapshot you recreate a volume into a certain availability zone under the Actions menu.