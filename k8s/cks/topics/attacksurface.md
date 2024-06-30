# Reduce Attack Surface

- Keep Applications and Kernel up to date
- Remove not needed packages
- Network in a firewall or NSG
- Close ports
- IAM: Restrict user permissions, run as user not root

# Worker Nodes

- Only keep Kubernetes components
- Nodes should be ephemeral and can be recreated

# Some Helpful Commands

For open ports: `netstat -plnt` or `lsof -i 22`
Stop and start service: `sudo systemctl status <service>`
Processes: `ps`

# Exercise: Disable Service snapd via systemctl

List units of service:

```sh
$ sudo systemctl list-units --type=service --state=running
  UNIT                             LOAD   ACTIVE SUB     DESCRIPTION                                                 
  accounts-daemon.service          loaded active running Accounts Service                                            
  atd.service                      loaded active running Deferred execution scheduler                                
  containerd.service               loaded active running containerd container runtime                                
  cron.service                     loaded active running Regular background program processing daemon                
  dbus.service                     loaded active running D-Bus System Message Bus                                    
  docker.service                   loaded active running Docker Application Container Engine                         
  falco-kmod.service               loaded active running Falco: Container Native Runtime Security with kmod          
  falcoctl-artifact-follow.service loaded active running Falcoctl Artifact Follow: automatic artifacts update service
  getty@tty1.service               loaded active running Getty on tty1                                               
  irqbalance.service               loaded active running irqbalance daemon                                           
  kubelet.service                  loaded active running kubelet: The Kubernetes Node Agent                          
  ModemManager.service             loaded active running Modem Manager                                               
  multipathd.service               loaded active running Device-Mapper Multipath Device Controller                   
  networkd-dispatcher.service      loaded active running Dispatcher daemon for systemd-networkd                      
  packagekit.service               loaded active running PackageKit Daemon                                           
  polkit.service                   loaded active running Authorization Manager                                       
  rsyslog.service                  loaded active running System Logging Service                                      
  serial-getty@ttyS0.service       loaded active running Serial Getty on ttyS0
  snapd.service                    loaded active running Snap Daemon                                       
  ssh.service                      loaded active running OpenBSD Secure Shell server                                 
  systemd-journald.service         loaded active running Journal Service                                             
  systemd-logind.service           loaded active running Login Service                                               
  systemd-networkd.service         loaded active running Network Service                                             
  systemd-resolved.service         loaded active running Network Name Resolution                                     
  systemd-timesyncd.service        loaded active running Network Time Synchronization                                
  systemd-udevd.service            loaded active running udev Kernel Device Manager                                  
  udisks2.service                  loaded active running Disk Manager                                                
  unattended-upgrades.service      loaded active running Unattended Upgrades Shutdown                                
  user@1000.service                loaded active running User Manager for UID 1000     
```

Then you stop snapd and disable it

```sh
sudo systemctl stop snapd
sudo systemctl disable snapd
```


