# Introduction

This page contains all of my preparation for taking the Certified Kubernetes Administrator (CKA) exam. A good bit of the following comes from LinuxFoundation.org. It has a good page that outlines the test details:
https://docs.linuxfoundation.org/tc-docs/certification/tips-cka-and-ckad
The Candidate Handbook is also handy for understanding more about the test itself:
https://docs.linuxfoundation.org/tc-docs/certification/lf-handbook2
Including the testing UI called **ExamUI**:
https://docs.linuxfoundation.org/tc-docs/certification/lf-handbook2/exam-user-interface/examui-performance-based-exams
The rest comes from the web or the [kubernetes.io](https://kubernetes.io/docs/home/) documentation. I am trying to rely primarily on the Kubernetes documentation for technical help because that is the only reference that you can have during the exam.

# CKA Exam Details and Rules

General details about the Exam:

- The exams are delivered online and consist of performance-based tasks (problems) to be solved on the command line running Linux.
- The exams consist of **15-20** performance-based tasks.
- Candidates have **2 hours** to complete the CKA and CKAD exam.
- The exams are proctored remotely via streaming audio, video, and screen sharing feeds.
- Results will be emailed 24 hours from the time that the exam is completed.

Workspace Rules:
- Clutter-free work area
  - No objects such as paper, writing implements, electronic devices, or other objects on top of surface
  - No objects such as paper, trash bins, or other objects below the testing surface
- Clear walls
  - No paper/print outs hanging on walls
  - Paintings and other wall décor is acceptable
  - Candidates will be asked to remove non-décor items prior to the exam being released
- Lighting
  - Space must be well lit so that proctor is able to see candidate’s face, hands, and surrounding work area
  - No bright lights or windows behind the examinee
- Other
  - Candidate must remain within the camera frame during the examination
  - Space must be private where there is no excessive noise. Public spaces such as coffee shops, stores, open office environments, etc. are not allowed.

# System Requirements and Pre-requisites

OSs that are supported for the exam ([link](https://helpdesk.psionline.com/hc/en-gb/articles/4409608794260-PSI-Bridge-Platform-System-Requirements)):
- Windows 8.1, 10, 11
- macOS 10.15(Catalina), 11(Big Sur), 12(Monterey), 13 (Ventura)
- Ubuntu 18.04, 20.04
Video Limitations
- One active monitor (either built in or external)  (NOTE: Dual Monitors are NOT supported)
- The Linux Foundation recommends  a screen size of 15” or higher to support the ExamUI.
- The Linux Foundation recommends a screen resolution of 1080p.
You must use one of these browsers:
- Mozilla Firefox version 52 or greater
- Google Chrome 72 or greater
- Microsoft Edge 79 or greater
- **NOTE: Safari is NOT allowed**

Test your system for the proctoring system at this website:
https://syscheck.bridge.psiexams.com/

# Exam Environment

Kubernetes versions:
- The CKA environment is currently running Kubernetes v1.25.
- The CKA & CKAD environments are currently running etcd v3.5.

Tools and aliases that are already configured on the exam system:
- `kubectl` with k alias and Bash autocompletion
- `jq` for YAML/JSON processing
- `tmux` for terminal multiplexing
- `curl` and `wget` for testing web services
- `man` and man pages for further documentation

Here are some other interesting tidbits:
- Root privileges can be obtained by running `sudo −i`.
- You must return to the base node (hostname node-1) after completing each task.
- Nested ssh is not supported.
- You can use `kubectl` and the appropriate context to work on any cluster from the base node.
- When connected to a cluster member via `ssh`, you will only be able to work on that particular cluster via `kubectl`.
- Where no explicit namespace is specified, the default namespace should be acted upon.
- If you need to destroy/recreate a resource to perform a certain task, it is your responsibility to back up the resource definition appropriately prior to destroying the resource.

There are six clusters that comprise the exam environment:
| Cluster | Members               | CNI      | Description |
|---------|-----------------------|----------|-------------|
| k8s     | 1 master, 2 worker    | flannel  | k8s cluster |
| hk8s    | 1 master, 2 worker    | calico   | k8s cluster |
| bk8s    | 1 master, 1 worker    | flannel  | k8s cluster |
| wk8s    | 1 master, 2 worker    | flannel  | k8s cluster |
| ek8s    | 1 master, 2 worker    | flannel  | k8s cluster |
| ik8s    | 1 master, 1 base node | loopback | k8s cluster − missing worker node |

# Documentation

During the test you can only use the Kubernetes documentation at [kubernetes.io](https://kubernetes.io/docs/home/). In the upper right you can set the **Versions** depending on if the test is using an older version of Kubernetes.
- Documentation Home: https://kubernetes.io/docs/home/
- kubectl reference: https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands
- Cheat Sheet: https://kubernetes.io/docs/reference/kubectl/cheatsheet/

# Shortcuts
There are a number of helpful commands in the [Kubectl cheat sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/):
https://kubernetes.io/docs/reference/kubectl/cheatsheet/
As stated above, `kubectl` alias and bash completion should be enabled by default. However, commands can often be tedious to type and slow down an already time-constrained exam. I plan to add the following to my `.bashrc`:

```sh
alias kn="kubectl get nodes -o wide"
alias kp="kubectl get pods -o wide"
alias kd="kubectl get deployment -o wide"
alias ks="kubectl get svc -o wide"
alias kdp="kubectl describe pod"
alias kdd="kubectl describe deployment"
alias kds="kubectl describe svc"
alias kdn="kubectl describe node"
```

For switching contexts and namespaces, these aliases from the cheat sheet are very handy:

```sh
alias kx='f() { [ "$1" ] && kubectl config use-context $1 || kubectl config current-context ; } ; f'
alias kn='f() { [ "$1" ] && kubectl config set-context --current --namespace $1 || kubectl config view --minify | grep namespace | cut -d" " -f6 ; } ; f'
```

Dry running is a tedious, so create an environment variable:

```sh
export DR="--dry-run=client -o yaml"
```

And then it can be added to a command:

```sh
kubectl run --image=nginx --name my-nginx $DR
```

# Exam Focus Areas

Storage - 10%
- Understand storage classes, persistent volumes
- Understand volume mode, access modes and reclaim policies for volumes
- Understand persistent volume claims primitive
- Know how to configure applications with persistent storage
Troubleshooting - 30%
- Evaluate cluster and node logging
- Understand how to monitor applications
- Manage container stdout & stderr logs
- Troubleshoot application failure
- Troubleshoot cluster component failure
- Troubleshoot networking
Workloads & Scheduling - 15%
- Understand deployments and how to perform rolling update and rollbacks
- Use ConfigMaps and Secrets to configure applications
- Know how to scale applications
- Understand the primitives used to create robust, self-healing, application deployments
- Understand how resource limits can affect Pod scheduling
- Awareness of manifest management and common templating tools
Cluster Architecture, Installation & Configuration - 25%
- Manage role based access control (RBAC)
- Use Kubeadm to install a basic cluster
- Manage a highly-available Kubernetes cluster
- Provision underlying infrastructure to deploy a Kubernetes cluster
- Perform a version upgrade on a Kubernetes cluster using Kubeadm
- Implement etcd backup and restore
Services & Networking - 20%
- Understand host networking configuration on the cluster nodes
- Understand connectivity between Pods
 - Understand ClusterIP, NodePort, LoadBalancer service types and endpoints
 - Know how to use Ingress controllers and Ingress resources
 - Know how to configure and use CoreDNS
 - Choose an appropriate container network interface plugin

 # Kubeadm upgrade

 Upgrade nodes one at a time. You must drain the worker node `kubectl drain --ignore-daemonsets` and make them unscheduleable. After an upgrade call `kubectl uncordon <node>` to make it schedulable again. 

 ## Control Node

 Update the package lists from the software repository.

 ```sh
 sudo apt-get update
 ```

 To get the list of kubeadm's to upgrade to (Debian):

 ```sh
 sudo apt list -a kubeadm
 ```

 This will install the kubeadm version 1.26.0.

 ```sh
 sudo apt install kubeadm=1.26.0-00
 ```

 First plan the upgrade to get the list of versions the took can upgrade to as well as the remote versions:

 ```
 kubeadm upgrade plan
 ```

 Then you upgrade the control plane

 ```sh
 kubeadm upgrade apply v1.26.0
 ```

 And then you upgrade the kubelet:

 ```
 sudo apt install kubelet=1.26.0-00
 ```

 ## Worker Node

 You can't just update the kubelet and be done on a worker node. `kubeadm upgrade node` must be called for the cluster to recognize the version in the API server.

 Update the package lists from the software repository.

 ```sh
 sudo apt-get update
 ```

 Install the kubeadm version 1.26.0.

 ```sh
 sudo apt install kubeadm=1.26.0-00
 ```

 Upgrade the node:

 ```sh
 kubeadm upgrade node
 ```

 Now that the node is upgrade, it is time to update the kubelet with the version 1.26.0. This should restart the service, but I have seen it drop warnings to the console:

 ```sh
 sudo apt install kubelet=1.26.0-00 
 ```

 You may need to reload the daemon and restart kubelet service after it has been upgraded.

 ```sh
 systemctl daemon-reload
 systemctl restart kubelet
 ```