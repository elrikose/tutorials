# ConfigMaps

ConfigMaps are a way to store non-secret information using a key-value mechanism. ConfigMaps can be used in a pod as:

- Volume mounted files
- Environment variables
- Command-line arguments

ConfigMaps store key value pairs in the `data:` section of the manifest.

ConfigMaps can also be marked in the manifest as `immutable: false` which would require the configmap to be destroyed and re-created.

### Create with --from-literal

A Literal you just pass on the command-line as a string literal and it will be visible in the shell history:

```sh
kubectl create configmap nginx-configmap --from-literal=KEY1=1234
```

Multiple literals can also be specified:

```sh
kubectl create configmap nginx-configmap --from-literal KEY1=1234 --from-literal KEY2=1234 --from-literal multi-line.txt="multi-line\ntext\nis\nin\nthis\nfile\n"
```

Notice the Following:

- Like most of `kubectl` usage, `--from-literals` does not require a `=` before the key value pairs for the secrets.
- If a ConfigMap needs a space, wrap it in double quotes

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-configmap
apiVersion: v1
data:
  KEY1: "1234"
  KEY2: "1234"
  multi-line.txt: multi-line\ntext\nis\nin\nthis\nfile\n
```

### Create with --from-file

Creating a secret from a file encodes the entire file using the filename as the key. First create the secret files:

```sh
echo -n "1234" > KEY1
echo -n "1234" > KEY2
echo "multi-line\ntext\nis\nin\nthis\nfile" > mutlti-line.txt
```

Then create the ConfigMap:

```sh
kubectl create configmap nginx-configmap-file --from-file ./KEY1 --from-file ./KEY2 --from-file ./multi-line.txt
```

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-configmap-file
data:
  KEY1: "1234"
  KEY2: "1234"
  multi-line.txt: |
    multi-line
    text
    is
    in
    this
    file
```

Notice `--from-literal` and `--from-file` are very similar except the file invocation uses a yaml `|` to embed multi-line text in the file.

## Attaching ConfigMap to a Pod

There are three common ways of attaching a ConfigMap to a pod for usage:

- Volume Mounting
- Loading all ConfigMap keys into environment
- Loading a single ConfigMap key into the environment

### Volume Mounting

The config is already created from above and it simply is mounted into a folder path `/config` in the pod.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-configmap-volume-mount
spec:
  containers:
  - name: nginx
    image: nginx
    volumeMounts:
    - name: nginx-configmap-volume
      mountPath: "/config"
      readOnly: true
  volumes:
  - name: nginx-configmap-volume
    configMap:
      name: nginx-configmap-file
```

Each of the keys will be files on the file system:

```sh
$ kubectl exec nginx-configmap-volume-mount -it -- ls -l /config 
total 0
lrwxrwxrwx 1 root root 11 Jan  8 19:49 KEY1 -> ..data/KEY1
lrwxrwxrwx 1 root root 11 Jan  8 19:49 KEY2 -> ..data/KEY2
lrwxrwxrwx 1 root root 11 Jan  8 19:49 KEY3 -> ..data/multi-file.txt
```

And the contents of the file will be the unencoded values:

```sh
$ kubectl exec nginx-configmap-volume-mount -it -- sh -c "cat /config/KEY1"
1234

$ kubectl exec nginx-configmap-volume-mount -it -- sh -c "cat /config/multi-line.txt"
multi-line
text
is
in
this
file
```

### Loading All Secret Keys into Environment

This is probably the easiest to load, directly into the environment:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-configmap-env-from
spec:
  containers:
    - name: nginx
      image: nginx
      envFrom:
      - configMapRef:
          name: nginx-configmap-file
```

And then you can get all of the keys from the environment

```sh
$ kubectl exec nginx-configmap-env-from -it -- sh -c "env | grep KEY"
KEY1=1234
KEY2=1234
```

Notice that the `multi-line.txt` key is not in the environment because of the naming:

```sh
$ kubectl exec nginx-configmap-env-from -it -- sh -c "env | grep multi"
command terminated with exit code 1
```

### Loading a Single Secret Key into Environment

This is the most tedious way to load an item as it requires 5 lines to only pull a single key from a secret:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-configmap-single-env
spec:
  containers:
    - name: nginx
      image: nginx
      env:
        - name: KEY1
          valueFrom:
            configMapKeyRef:
              name: nginx-configmap-file
              key: KEY1
```

And then you can get the key from the environment:

```sh
$ kubectl exec nginx-configmap-single-env -it -- sh -c "env | grep KEY"
KEY1=1234
```