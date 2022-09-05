# Amazon Machine Image (AMI)

AMIs are a customization of an EC2 instance by adding your own software, configuration, operating system, monitoring, etc. It boots faster because everything is pre-packaged.

- AMIs are built for a specific region but can be copied.
- Amazon provides a number of public AMIs.
- Amazon Marketplace has a number of AMIs that vendors have created with their own software.

## AMI Build Workflow

- Start an EC2 Instance and customize it.
- Stop the instance
- Build the AMI - creating EBS Snapshots
- Launch other instances from the AMI.

For example you could create an AMI where it has nginx or Apache already installed, then all you would have to do is configure the webserver.