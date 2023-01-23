 # Kubernetes Cluster Upgrade with Kubeadm

 Upgrade nodes one at a time. You must drain the worker node `kubectl drain --ignore-daemonsets` and make them unscheduleable. After an upgrade call `kubectl uncordon <node>` to make it schedulable again. 

 ## Upgrading a Control Node

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

 ## Upgrade a Worker Node

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