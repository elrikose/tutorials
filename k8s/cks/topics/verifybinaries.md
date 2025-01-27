# Verify Platform Binaries

Sometime you need to verify what you downloaded is the same as what is local. On GitHub they have the binary hashes of the tarballs for 1.31.3 in the Changelog:

https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.31.md#v1313

You can download the server binary and expand it:

```sh
$ tar -xvf kubernetes-server-linux-amd64.tar.gz
$ cd kubernetes/server/bin
$ sha512sum kube-apiserver
da62a165c9243470af47e981c3c929af477cda2d40f8b00227456b71f32d08549578d28630917d7c60e5b80744862e006cb4de3ea8fc92211bcfefb30036ea3c  kube-apiserver
```

For example if this is the binary of the tarball has a SHA 512 hash of:

```sh
da62a165c9243470af47e981c3c929af477cda2d40f8b00227456b71f32d08549578d28630917d7c60e5b80744862e006cb4de3ea8fc92211bcfefb30036ea3c
```

And the you run the `sha512sum` of the binary and dump it into a file:

```sh
$ sha512sum kube-apiserver > kube-apiserver.txt
$ cat kube-apiserver.txt
da62a165c9243470af47e981c3c929af477cda2d40f8b00227456b71f32d08549578d28630917d7c60e5b80744862e006cb4de3ea8fc92211bcfefb30036ea3c  kube-apiserver
```

Then you can put the SHA into the same file, remove the kube-apiserver and then do a compare with `| uniq`, then you should be able to see if they are really the same.

```sh
$ cat kube-apiserver.txt
da62a165c9243470af47e981c3c929af477cda2d40f8b00227456b71f32d08549578d28630917d7c60e5b80744862e006cb4de3ea8fc92211bcfefb30036ea3c
da62a165c9243470af47e981c3c929af477cda2d40f8b00227456b71f32d08549578d28630917d7c60e5b80744862e006cb4de3ea8fc92211bcfefb30036ea3c

$ cat kube-apiserver.txt | uniq
da62a165c9243470af47e981c3c929af477cda2d40f8b00227456b71f32d08549578d28630917d7c60e5b80744862e006cb4de3ea8fc92211bcfefb30036ea3c
```

# Binaries in the container

This is very similar to above accept the binary is inside the container. The `kube-apiserver` is hardened. You can't exec into them.

```sh
$ sudo crictl ps | grep api
70dde8b7b5e21       f48c085d70203       5 days ago          Running             kube-apiserver            0                   fb721288699fa
```

And you can see that the server is running in the Linux process space:

```sh
$ ps -ef | grep kube-api
root       12127   11888  9 Jan19 ?        12:52:38 kube-apiserver --advertise-address=10.154.161.198 --allow-privileged=true --authorization-mode=Node,RBAC --client-ca-file=/etc/kubernetes/pki/ca.crt --enable-admission-plugins=NodeRestriction --enable-bootstrap-token-auth=true --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key --etcd-servers=https://127.0.0.1:2379 --kubelet-client-certificate=...
```

You can go into the `/proc` area for the PID and find the file system as well as the binary:

```sh
$ cd /proc/12127/root
$ find . -name "kube-api*"
./usr/local/bin/kube-apiserver

$ cd ./usr/local/bin
```

And then get the `sha512sum`:

```sh
$ sha512sum kube-apiserver
da62a165c9243470af47e981c3c929af477cda2d40f8b00227456b71f32d08549578d28630917d7c60e5b80744862e006cb4de3ea8fc92211bcfefb30036ea3c  kube-apiserver
```
