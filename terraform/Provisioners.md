# Terraform Provisioners

Provisioning -  install software, edit files, etc

- cloud-init - cross-platform initialization when you launch a VM in the cloud
- Packer - Hashicorp tool to build cloud images via config files

Provisioners are not reflected in terraform state

## Cloud-init

Yaml file that can define:

- users
- packages to upgrade/install
- Run a command

You define the init file with a template file:

```js
data "template_file" "cloud_init" {
    template = file("init.yaml")
}
```

And then in the definition for the VM you specify the `user_data`:

```js
  user_data = data.template_file.cloud_init.rendered
```

## Local-Exec / Remote-exec Provisioner

Execute activity at the end of 

### local-exec

Local-Exec - Where terraform exec will apply the command:

- Your local machine
- Automation server (Jenkins, Azure DevOps)
- Terraform Cloud

You could use it to invoke `Ansible`, `script`, etc

Ad-hoc 

```js
resource "null_resource" "completion" {
    provisioner "local-exec" {
        command = "date > log_completion.txt"
    }
}
```

After creating a VM

```js
resource "azurerm_linux_virtual_machine" "linux_vm" {
    provisioner "local-exec" {
        command = "date > vm_completion.txt"
    }
}
```

### remote-exec

remote-exec - Execute commands on the target resource after it is created

`inline` example:

```js
resource "azurerm_linux_virtual_machine" "linux_vm" {
    provisioner "remote-exec" {
        inline = [
            "sudo apt update -y",
            "sudo apt install wget"
        ]
    }
}
```

`scripts` example:

```js
resource "azurerm_linux_virtual_machine" "linux_vm" {
    provisioner "remote-exec" {
        scripts = [
            "./set-me-up.sh",
            "/home/user/bootstrapper"
        ]
    }
}
```

## File Provisioner

File provisioner will copy local files or directories to remote destination.

File: 
```js
resource "azurerm_linux_virtual_machine" "linux_vm" {
    provisioner "file" {
        source = "local/file.yml"
        destination = "/etc/file.yaml"
    }
} 
```

Directory:

```js
resource "azurerm_linux_virtual_machine" "linux_vm" {
    provisioner "file" {
        source = "source/ansible/"
        destination = "/home/user/"
    }
} 
```

Dump a string into a file:

```js
resource "azurerm_linux_virtual_machine" "linux_vm" {
    provisioner "file" {
        content = "Some random info..."
        destination = "/tmp/file.log"
    }
} 
```

## Connection

You need a mechanism to get the file up so you can specify `ssh` or `winrm` in a connection block

```js
provisioner "file" {
    ...
    connection {
      type = "ssh"
      user = "user"
      password = "pass123"
      host = "hostname"
    }
}
```

## Null Resources

An empty placeholder resource for running provisioners. They can be triggered.
