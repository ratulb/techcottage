---
layout: post
title: "NFS persistent volume and claim in kubernetes"
date: 2020-10-25 02:59:00.015+00:00
tags: [kubernetes, nfs, nfs installation on ubuntu, persistent volume claim, persistent volume]
---

This write up shows detailed steps of how to setup a nfs server as a storage backend and make use of it in POD's[ persistent volume via persistent volume claim](<https://kubernetes.io/docs/concepts/storage/persistent-volumes/>). These have been tested to work with  kubernetes v1.19.3 and nfs v4.2 version ubuntu Ubuntu 18.04.5 LTS.

**Set up nfs server:**

Following commands would set up the server for storage backend:

apt update && apt install nfs-kernel-server -y 

Create a directory called /mnt/nfs-share and provide all permission to clients. We may need to re-consider what permissions are allowed based on requirements. 

mkdir -p /mnt/nfs-share/ && chmod -R 777 /mnt/nfs-share

We also, change the ownership of the shared directory next.

chown -R nobody:nogroup /mnt/nfs\_share/

We need to edit the **/etc/exports** file to grant access to clients. Here we are specifically granting access to couple of machines.

vi /etc/exports 

/mnt/nfs-share/ 10.148.0.13/32\(rw,sync,no\_subtree\_check\)/mnt/nfs-share/ 10.148.0.12/32\(rw,sync,no\_subtree\_check\)

Execute the following commands to complete the server setup process:

exportfs -a

systemctl restart nfs-kernel-server

Note: We might need to allow firewall access depending on whether firewall is active or not:

root@master:~/deployments/nfs\# ufw statusStatus: inactive

If firewall is **active** fire the following commands:

ufw allow from 10.148.0.12 to any port nfs

ufw allow from 10.148.0.13 to any port nfs

**  
**

**Set up a client and check that shared access is working:**

Install nfs client in one of the boxes that would share kubernetes workloads :

root@worker-1:~\# apt install nfs-common

Create a directory and mount the shared nfs server directory as shown below:

mount 10.148.0.10:/mnt/nfs\_share /mnt/client\_share

Writing something in the client's **/mnt/client\_share** folder should reflect it on the server and other connected clients.

  


**Create PV and PVC \(Persistent volume & claim\):**

First we create PV definition on the kubernetes server:

root@master:~/deployments/nfs\# cat pv-nfs.yaml apiVersion: v1kind: PersistentVolumemetadata: name: pv-nfs-volspec: capacity: storage: 1Gi volumeMode: Filesystem accessModes: \- ReadWriteMany persistentVolumeReclaimPolicy: Retain storageClassName: nfs-storage-class mountOptions: \- hard \- nfsvers=4.2 nfs: path: /mnt/nfs-share server: 10.148.0.10root@master:~/deployments/nfs\# kubectl apply -f pv-nfs.yaml persistentvolume/pv-nfs-vol created

  


Next, we create the PVC definition followed by the busybox pod definition as shown below:

root@master:~/deployments/nfs\# cat pvc-nfs.yaml apiVersion: v1kind: PersistentVolumeClaimmetadata: name: pvc-nsfspec: accessModes: \- ReadWriteMany storageClassName: nfs-storage-class resources: requests: storage: 100Miroot@master:~/deployments/nfs\# kubectl apply -f pvc-nfs.yaml persistentvolumeclaim/pvc-nsf created

  


kubectl get pv,pvc 

The above command out should show the status of **PV and PVC** as BOUND at this point.

The POD definition:

root@master:~/deployments/nfs\# cat pod-busybox.yaml apiVersion: v1kind: Podmetadata: name: busyboxspec: containers: \- image: busybox name: busybox command: \- sh \- -c \- 'while true; do date >> /tmp/nfs/index.html; hostname >> /tmp/nfs/index.html; sleep 10; done' imagePullPolicy: IfNotPresent volumeMounts: \- name: nfs-claim mountPath: "/tmp/nfs" restartPolicy: OnFailure volumes: \- name: nfs-claim persistentVolumeClaim: claimName: pvc-nsf nodeName: masterroot@master:~/deployments/nfs\# kubectl apply -f pod-busybox.yaml pod/busybox createdroot@master:~/deployments/nfs\# kubectl get pod busybox NAME READY STATUS RESTARTS AGEbusybox 1/1 Running 0 10s

The changes in **index.html** can be seen in server**/mnt/nfs\_share** , client**/mnt/client\_share** and inside the busybox container's **/tmp/nfs** directories.

*Originally published on [https://rbsomeg.blogspot.com](https://rbsomeg.blogspot.com/2020/10/nfs-persistent-volume-and-claim-in-kubernetes.html)*
