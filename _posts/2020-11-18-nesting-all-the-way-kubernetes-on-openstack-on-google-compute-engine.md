---
layout: post
title: "Nesting all the way - kubernetes on openstack on google compute engine"
date: 2020-11-18 21:32:00.029+00:00
tags: [install openstack, install openstack in google compute engine, openstack stand alone, openstack, openstack basic, openstack in single machine, install kubernetes on openstack, openstack for beginner]
---

**The gist:** Can gcp/azure/AWS can be squeezed into one machine?

**Openstack is a cloud provider framework\(read GCP/AWS/Azure - except that it is opensource\). Here we squeeze the whole storage/compute/network virtualization framework to one GCP instance - create tenant, provision VMs and create a kubernetes cluster out of those VMs and deploy PODs.**  


  


**Provisioning  the compute engine: **

**Not all compute engines support virtualization - we need to create them from disks which are tagged specifically to support virtualization** and we need to provision the compute engines on N1\(Haswell\) and later series of CPUs and these CPUs are not available in all the GCP regions. At this point - US central and some Europe regions have N1 series of CPUs. [See my earlier post on how to do this](<http://rbsomeg.blogspot.com/2020/09/nested-virtualbox-vm-inside-google.html>).

  


**Create the disks in the GCP cloud console:**

We execute the the following command in the google cloud console to create a disk that would support virtualization:

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj4NUxH8jv4pwczk-nImDdIJ3IgTavgK6V7A10xX3_HpCG2gBH0ZwdNZmkh0rPuUP0ldeJpKcPeZkVtWPHLLRNvL28BdVNgEIEZDVaQpwF107Ab3kA9jMSHojD6Oc6lZeY1XvaQd6HnHRI/s16000/tagged-disk-for-virtualization.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj4NUxH8jv4pwczk-nImDdIJ3IgTavgK6V7A10xX3_HpCG2gBH0ZwdNZmkh0rPuUP0ldeJpKcPeZkVtWPHLLRNvL28BdVNgEIEZDVaQpwF107Ab3kA9jMSHojD6Oc6lZeY1XvaQd6HnHRI/s680/tagged-disk-for-virtualization.png>)

  


  


**$****gcloud compute disks create disk-tagged-for-virtualization --image-project ubuntu-os-cloud --image-family ubuntu-1804-lts --zone us-central1-a --licenses "https://www.googleapis.com/compute/v1/projects/vm-options/global/licenses/enable-vmx"**

**  
**

****

**[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi3Mss9_Eyc31DnQErSpXJV_npLsvS4YEkx71I6whIvvee87jRfpF5hzX2IrmsDyUlzX84TdSrVGBaXclHT1DkKxXIzdMVBFiHhdHkZmLBQDiFAvGmkV1Cjiqk5tI0jU_cg-kHJOpqVlQ0/w640-h246/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi3Mss9_Eyc31DnQErSpXJV_npLsvS4YEkx71I6whIvvee87jRfpF5hzX2IrmsDyUlzX84TdSrVGBaXclHT1DkKxXIzdMVBFiHhdHkZmLBQDiFAvGmkV1Cjiqk5tI0jU_cg-kHJOpqVlQ0/>)**

**  
  
**

**  
**

  


  


  


  


  


  


This would create a 10 GB disk - which can be resized as per our requirements. In this case we resize it to 120 GB to launch our ubuntu 18.04 bionic compute engine VM. Inside this VM we would deploy Openstack using Devstack. So, whole Openstack deployment would be contained within one compute engine with 6 vCPUs, 16 GB RAM and 120 GB hard disk.  

Within the Openstack deployment, we would launch 2 ubuntu 18.04 VMs - one would be the master node and another would be worker node of the kubernetes cluster. Both nodes would be 2 vCPU and 20 GB hard disk each. We would deploy weave CNI network plugin for POD networking and would validate that POD connectivity works without any hiccups. Would check for POD port forwarding, expose a deployment as NodePort and check for NodePort service accessibility. We would also, validate kubernetes DNS by going inside POD a container and access other containers by POD DNS names.

**Disclaimer:**  

**This is not an advisable production setup and compute and storage capacities are not based on any benchmark. This could be a POC, academic exercise or a guide for someone looking to get started with Openstack and hack its internals from there.** We could have taken nesting and virtualization levels deeper just by making use of [Linux lxd](<https://linuxcontainers.org/lxd/introduction/>) containers because ubuntu has in-built   support for them. But that is a post for another day.

Following are the snaps of the provisioned GCP compute VM based off of the disk that we have created above.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiiYaJKvggks2y8YopO23ObnYoCi_ss85tKwwz65HicZEU0u9eiMkEUCeZqpyendo8hFY3_GiuDTH7DlTaSmd5bwgGqonOQhjZTDMyLa8z1hNw2Zx9NSEbZRQiBEt7xQZVUGfYEjPK4pB8/s16000/provisioned-compute-engine-1.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiiYaJKvggks2y8YopO23ObnYoCi_ss85tKwwz65HicZEU0u9eiMkEUCeZqpyendo8hFY3_GiuDTH7DlTaSmd5bwgGqonOQhjZTDMyLa8z1hNw2Zx9NSEbZRQiBEt7xQZVUGfYEjPK4pB8/s736/provisioned-compute-engine-1.png>)

  
  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


We have selected N1 series of CPU and US central region for required virtualization support. We have appropriately named the compute engine 'openstack'\(pun intended\)\!

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhLxp1hkokJZK6mn89nIQ2JiWETa9y0lX9PMW-a0HtbRA1UIccXTD39w2xjumB5aVVZWMXRfbCJm5ZYTYlJ38gqnDFocOixixzeoT6rQOo33wiIwNoxxqnEl0SSSthWD-P785eP8selOew/s16000/provisioned-compute-engine.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhLxp1hkokJZK6mn89nIQ2JiWETa9y0lX9PMW-a0HtbRA1UIccXTD39w2xjumB5aVVZWMXRfbCJm5ZYTYlJ38gqnDFocOixixzeoT6rQOo33wiIwNoxxqnEl0SSSthWD-P785eP8selOew/s759/provisioned-compute-engine.png>)

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEikmqOxcroFjFnLwwUcbI2MMgHC6LZ1z1iXnacTDYVCV0gcCp9G5Vqq1JAqssEGrERerqFC9FMEel8froh_b7RV6Pf14aN-qv0IXc5km8xyfhdVdZs5Dv5OStxc-mkuut9O79WqxI9RXvQ/s16000/Hard-disk-and-http.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEikmqOxcroFjFnLwwUcbI2MMgHC6LZ1z1iXnacTDYVCV0gcCp9G5Vqq1JAqssEGrERerqFC9FMEel8froh_b7RV6Pf14aN-qv0IXc5km8xyfhdVdZs5Dv5OStxc-mkuut9O79WqxI9RXvQ/s665/Hard-disk-and-http.png>)

  
  


  


  


  


  


  


  


  


  


  


  


  


  


There are various ways we can deploy Openstack. But here we are going to use 'devstack' - which facilitate single or multi-node deployment of Openstack. Devstack is collection of scripts used to bring up a complete Openstack setup quickly. The whole setup is triggered by a script  'stack.sh'. It pulls down various  components of Openstack from GitHub source code repository mirrors, configures the system and makes it ready. Hence, Devstack is a natural choice to get started with Openstack. Below is quick rundown of various openstack core infrastructure components:

**Dashboard:**

Web-based management interface of openstack. Also, interchangeably referred to as horizon, it is an intuitive UI to create, configure and manage various components and services that a cloud framework must provide - such as control, compute, network and storage. More specifically, horizon is a core UI infrastructure based on which component specific management UIs are built and the dashboard stiches them together.

Note: API and CLI exploits are there underneath to execute the tasks that are performed on the dashboard. The dashboard piggy back on the APIs.

**Keystone:**

The identity management component that handles user, roles, tenants. Also, manages catalog of services and service endpoints. One thing to notice is that - in Openstack parlance - tenants and projects mean the same thing. Operations are executed in a project or tenant context. Once openstack setup is complete, two users 'admin' and 'demo' will be present in the system. Admin is the super user over the whole cloud setup.

**Glance:**

Glance is the OS image registry. The Glance is the VM image management component. Before we launch a VM we need to make M boot images will get their authorized host key\(to access them via SSH\) and network device MAC address populated during the cloud initialization phase of VM launch.

**Neutron:**

Neutron is responsible for virtual networking in Openstack. It exposes APIs to manage the software defined tenant networks\(**SDN**\) to which VMs are launched. Neutron provides inter-network connectivity via virtual routers. External connectivity to internal VMs can be provided if a router is has a gateway that is connected to an external network. VMs can be accessed via **floating** IPs which have direct one-to-one with VMs' internal IPs.

**Nova:**

Nova manages the VM instances. Once a VM image is available in Glance and a virtual network is defined, with the addition of SSH key pair \(which can either be generated or imported\) and security group \(which controls VM's ingress and egress traffic\), Nova looks at the hypervisor resources and schedules a VM on a compute node. Once the VM is launched, the public key of the SSH key pair is injected into the authorized\_keys file of launched VM during the cloud initialization phase.

**Cinder:**

Cinder is the component for block storage management. It manages the volumes that get attached to and detached from VMs. Cinder works with glusterFS, ceph and many more solutions.

**Swift:**

Swift is the object storage in Openstack. It is analogous to AWS S3. 

**Ceilometer:**

Originally designed for tenant resource consumption billing purposes, it is the telemetry component of openstack. Its provides resource usage statistics and can be configured for alert and monitoring.

Now that we know what core components of openstack are, let get started with the first up.

**Setting things up:**

We SSH into our provisioned GCP instance called 'openstack'. First thing, we do is create an user called 'stack' with home directory set to /opt/stack. This is done because devstack scripts are required to be executed by the 'stack' user.

We update the system, create the 'stack' user, login as stack and checkout the latest stable release 'victoria' of Devstack repo.

$ sudo su -

root@openstack:~\# apt update

root@openstack:~\# apt upgrade -y

root@openstack:~\# useradd -s /bin/bash -d /opt/stack -m stack

root@openstack:~\# echo "stack ALL=\(ALL\) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack  
root@openstack:~\# su - stack

stack@openstack:~\# git clone https://github.com/openstack-dev/devstack.git -b stable/victoria devstack/

stack@openstack:~$ cd devstack/

stack@openstack:~/devstack$ ip addrinet 10.128.0.48/48 scope global dynamic ens4  
Extra output ommitted...  


Replace the HOST\_IP below as necessary.

At this point, we create local configuration file as follows:

stack@openstack:~/devstack$ cat > local.conf <<EOF\[\[local|localrc\]\] ADMIN\_PASSWORD=secret DATABASE\_PASSWORD=\$ADMIN\_PASSWORD RABBIT\_PASSWORD=\$ADMIN\_PASSWORD SERVICE\_PASSWORD=\$ADMIN\_PASSWORD HOST\_IP=10.128.0.48 RECLONE=yes LOGFILE=/opt/stack/logs/stack.sh.log VERBOSE=True LOG\_COLOR=False SCREEN\_LOGDIR=/opt/stack/logs EOF

stack@openstack:~/devstack$ ./stack.sh

The above script will install Openstack and related dependencies, configure the components with each other and setup a single node running Openstack cloud framework for us. Successful deployment will have output similar to the following  at the command prompt:

Total runtime 1159This is your host IP address: 10.128.0.48This is your host IPv6 address: ::1Horizon is now available at <http://10.128.0.48/dashboard>Keystone is serving at <http://10.128.0.48/identity/>The default users are: admin and demoThe password: secretServices are running under systemd unit files.

At this point, we can access the horizon dashboard using the external IP address of compute engine from our local machine.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh5ujv27MDC3maoe_5ZkIqQXUNJ9wnjbUXncMMugyq32SiYjO6of7uvpuLNL1pFAC3vLCKvFd1IbjmS4BK7-Jv82GpdNlVtFArHGdlqdvgXRr5ozA_ZNZsUJ3fUlfINcs669i4R17ipix8/s16000/external-ip.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh5ujv27MDC3maoe_5ZkIqQXUNJ9wnjbUXncMMugyq32SiYjO6of7uvpuLNL1pFAC3vLCKvFd1IbjmS4BK7-Jv82GpdNlVtFArHGdlqdvgXRr5ozA_ZNZsUJ3fUlfINcs669i4R17ipix8/s638/external-ip.png>)

  
  


  


  


**  
**

**1.** We access the the horizon dashboard using the external IP.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjU9f10eMTMuHVWMANYbnUsNalALNn5pOSI_HnMDmRc6iezWROFyjmfY2P89JRIuWNjeqty20K-cobyBuMtS0LDnesrRyUy1dL0-2DJ-x5BP8lcxOUfejJgnQ6rOOBksRr0ToDQiEUFr6w/s16000/admin-login.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjU9f10eMTMuHVWMANYbnUsNalALNn5pOSI_HnMDmRc6iezWROFyjmfY2P89JRIuWNjeqty20K-cobyBuMtS0LDnesrRyUy1dL0-2DJ-x5BP8lcxOUfejJgnQ6rOOBksRr0ToDQiEUFr6w/s638/admin-login.png>)

  
  


  


  


  


  


  


  


  


  


  


  


  


**  
**

**2.** Next, create an user call 'dev' with role 'member'. 

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEihGidNBoJ-rBPtrXTEM5W4RYk8-_T4WPIZa7zJRCIZurAODPYDTBKCl-31I5XDFHAMp2229dLDQOZE_XsOsQoDNct9w_13uALBbZoYMeqyS1UGFqV0OzyGeER9ZOVVr_kiPHIB1knmtMQ/w640-h458/create-dev-user1.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEihGidNBoJ-rBPtrXTEM5W4RYk8-_T4WPIZa7zJRCIZurAODPYDTBKCl-31I5XDFHAMp2229dLDQOZE_XsOsQoDNct9w_13uALBbZoYMeqyS1UGFqV0OzyGeER9ZOVVr_kiPHIB1knmtMQ/s743/create-dev-user1.png>)

  


**3.** We create a project called 'dev-project' for the user.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjIL0ZNAk7PFkHJw9SwIpedYjHYKlGoG4BtyQtOmeVt3a3yBesSy4aYPQ1ZKMerw6aebrcYlePgpWLgvsPpqbbo-QhEUt1i2WifEed1qzN7PcmiN_4aa9vO8g4RZtTsyi30mEWE_YeV0RM/s16000/create%253Dproject.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjIL0ZNAk7PFkHJw9SwIpedYjHYKlGoG4BtyQtOmeVt3a3yBesSy4aYPQ1ZKMerw6aebrcYlePgpWLgvsPpqbbo-QhEUt1i2WifEed1qzN7PcmiN_4aa9vO8g4RZtTsyi30mEWE_YeV0RM/s638/create%253Dproject.png>)

  
  


  


  


  


  


  


  


  


  


**  
**

**  
**

**4.** We complete the user creation along with project creation and logout and login as dev.

At this point we have provisioned a tenant.  We should able to upload a VM image \(ubuntu 18.04 cloud image\), define virtual network, generate SSH key pair, create a security group. These are the requirement for launching a VM.

  


  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiFbLkCYVcwHbXvuLAhjQjl9H6PjHmxteh2Fp0oJtFR9RAIp22cTQRvvmMROpF-97_brJPTm-gCBpo0LBm6OBO0esxJ2VYZgXq0n3s_A7h1ImnyCqA528iGfW8vV_rg_OkmmGWUXhW7gQU/s16000/login-dev.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiFbLkCYVcwHbXvuLAhjQjl9H6PjHmxteh2Fp0oJtFR9RAIp22cTQRvvmMROpF-97_brJPTm-gCBpo0LBm6OBO0esxJ2VYZgXq0n3s_A7h1ImnyCqA528iGfW8vV_rg_OkmmGWUXhW7gQU/s607/login-dev.png>)

  
  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


**5.** First we download ubuntu 18.04 bionic image to our local machine from [this link.](<https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg-amd64.img .>) See [this page](<https://docs.openstack.org/image-guide/obtain-images.html>) for details.

In case download or upload taking long time - we can download the image on the 

compute engine itself and upload the image to the system by using the CLI. Fire the following commands from /opt/stack/devstack directory:

  


stack@openstack:~/devstack$ wget [https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg](<https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg-amd64.img> "https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg-amd64.img")[-amd64.img](<https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg-amd64.img> "https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg-amd64.img")

stack@openstack:~/devstack$ source openrc dev dev-project

  


stack@openstack:~/devstack$ openstack image create --disk-format qcow2 --container-format bare \ \--public --file bionic-server-cloudimg-amd64.img ubuntu-18.04-image

If we use the CLI to upload the image, we ignore step 6.

**6**. Next we upload the image:

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi-WgfgdaWO327-I4ZRRZvSHlb6cb6BCg-0jHHhs5kyljqEE_l_EJI0c7sfE_gGvm4-4r9hVqBijEMBIboygUIgMBYiT_B_Cwb15G9G6TOzMww-pGdeqdZs4c9Khi1xynAlk8kWnS6vrrM/s16000/image.png)

  
  


  


  


  


  


  


  


  


  


  


  


  


**7**. Now image listing should show our image.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhYQb67TAUeZH4L3yVzFAU7F_pZLPOhX1Kh9Ql354SDFFwcBp7K8vrQSuAQm26TEjc4OwEuW1lXKF_vM6o3kDE-MKLDzKG4P5Wmr_Mr989aKv5lOXvqqc1HHZioDe0nwZsBh40aJ8el5jA/w640-h342/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhYQb67TAUeZH4L3yVzFAU7F_pZLPOhX1Kh9Ql354SDFFwcBp7K8vrQSuAQm26TEjc4OwEuW1lXKF_vM6o3kDE-MKLDzKG4P5Wmr_Mr989aKv5lOXvqqc1HHZioDe0nwZsBh40aJ8el5jA/>)

  
  


  
  


  


  


  


  


  


  


  


  


**8**. Next we, create the security group called 'dev-security-group'.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgME7VBEU7Y7LY8SsdUl-x0y4UsemSTtMPKBugabarZQOQpWWTO2bnF7es4Xkq_2wUMhfstdRMNCf0VO_s-9lV1y9ji9YmqSxhHJr_YPt_4TmMRBMr8U_1OxAn0Vzmf0bqjLDZNPfiq1CE/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgME7VBEU7Y7LY8SsdUl-x0y4UsemSTtMPKBugabarZQOQpWWTO2bnF7es4Xkq_2wUMhfstdRMNCf0VO_s-9lV1y9ji9YmqSxhHJr_YPt_4TmMRBMr8U_1OxAn0Vzmf0bqjLDZNPfiq1CE/>)

  
  


  


  


  


  


  


  


  


  


  


  


We add 3 rules -

  1. All ICMP
  2. All TCP
  3. SSH



[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgleFwWAGNL_r6OilMKRd676px5zZqbEzbP8zeyz-oDqeG7hQnAeVZH9adMo87saB_TZECr10IESeK5eMOU5TPdp3U3qLWaUOnxYXxYbODmLvonttUen2E8cGa4SSewX8FjarP9J9qEO0I/w640-h499/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgleFwWAGNL_r6OilMKRd676px5zZqbEzbP8zeyz-oDqeG7hQnAeVZH9adMo87saB_TZECr10IESeK5eMOU5TPdp3U3qLWaUOnxYXxYbODmLvonttUen2E8cGa4SSewX8FjarP9J9qEO0I/>)

  
  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


**9**. Next, we create the SSH key pair called 'dev-key-pair'. 

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhRSr6E_kOeihL7XDjvWCiA1Rr7K2D6UEd-ZwcU6E6SpfusYdkK9_VtM2j9oq3BttgkbrRCy7gEZAlfen1yGMic2JkKY5SFwd69eShhVBhXYqgzs6_4E3zQmjp2zR1JPLR5Eanam2G9jHA/s16000/image.png)

  


  


  


  


  


  


  


  


  


  


  


  


  


We save the downloaded private key in a file called 'dev-key-pair.pem' in the compute engine.

We change the permission on the dev-key-pair.pem by executing the following command:

stack@openstack:~/devstack$ ls -la | grep pem-rw-rw-r-- 1 stack stack dev-key-pair.pemstack@openstack:~/devstack$ chmod 0600 dev-key-pair.pem stack@openstack:~/devstack$

**10.** Next we are going to create network called 'dev-network'. 

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgE_nuTDDOyo4J5IFyoTDUxcE1gSMdHX2WUCpUze2eeBgpaw2ASxfLNfBPKsCQxH9vohyphenhyphenHZlhjpQpJLDkEMUAK8o7wLo7sM080s26wZyK4hyphenhyphenrcon7vvIt0dWaR1XFiWiHq_2ulWCadVP_Y/w640-h521/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgE_nuTDDOyo4J5IFyoTDUxcE1gSMdHX2WUCpUze2eeBgpaw2ASxfLNfBPKsCQxH9vohyphenhyphenHZlhjpQpJLDkEMUAK8o7wLo7sM080s26wZyK4hyphenhyphenrcon7vvIt0dWaR1XFiWiHq_2ulWCadVP_Y/>)

  
  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


**11**. We create a subnet called dev-subnet.

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgoiP_e0Jz-M5JLCFo93y2-aU1_F6AlSY1Cde8r32Tn82AKGA7e97w_CAie59DrSu3DCk9nxVPTQhipeqGDUJdbpP_y6sXNnma7oRyZzRYdOqFci3A90RM1RQWGC_KSfS6cDgxxtcjDF8M/w640-h394/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgoiP_e0Jz-M5JLCFo93y2-aU1_F6AlSY1Cde8r32Tn82AKGA7e97w_CAie59DrSu3DCk9nxVPTQhipeqGDUJdbpP_y6sXNnma7oRyZzRYdOqFci3A90RM1RQWGC_KSfS6cDgxxtcjDF8M/>)

  
  


  
  


  


  


  


  


  


  


  


  


  


  


  


  


  


**12**. Enter the subnet allocation details and DNS address 8.8.8.8

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEichXetT8w8nP120yBN79X1cR2MUUpGJ0bNYlzUpsNgHiJ2crIxt-gmB3qTxO5L4uUAyqmXnv08aKUDqjIzQOBynoqpI-BKzYfr-gKgLU6BTNoYyvml4LVaChmjY1CleDZW0PUSxGhIOyk/w640-h424/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEichXetT8w8nP120yBN79X1cR2MUUpGJ0bNYlzUpsNgHiJ2crIxt-gmB3qTxO5L4uUAyqmXnv08aKUDqjIzQOBynoqpI-BKzYfr-gKgLU6BTNoYyvml4LVaChmjY1CleDZW0PUSxGhIOyk/>)

  
  


  


  


  


  


  


  


  


  


  


  


  


  


**13**. At this point we have an internal network without any external connectivity. We would connect this internal network to the public network which was provisioned as part of openstack deployment. To do this we would create a router called 'dev-router' which would stitch together public and dev-network. This would provide external connectivity from the internal network.

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjHFo1vreeoFn_mEMGSCnrwsY1Q6dMaJXtpYxlwJF8WE_9Lk0h35LeNp22WPp8GW6FKuojWVhc0JXRnY4zN2NmHA1g3rmvR469LDFaFkt6tycu4DeyHfjZvVJsr8EHVgotQx9J0yRvigag/w640-h454/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjHFo1vreeoFn_mEMGSCnrwsY1Q6dMaJXtpYxlwJF8WE_9Lk0h35LeNp22WPp8GW6FKuojWVhc0JXRnY4zN2NmHA1g3rmvR469LDFaFkt6tycu4DeyHfjZvVJsr8EHVgotQx9J0yRvigag/>)

  
  


  
  


  


  


  


  


  


  


  


  


  


  


  


**14**. We add the internal 'dev-network' as an interface to the router.

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh1sLBo97RG3EndueQTszTj6MgKUh8E1VK0M-jURFPkCy_rv7hyjFreriv4aZ1KnAI7HrP84JMvAzJZJki2IJCbUJNbCqER1sYHjRtUNvK_3_NaHmA-yWeTfnaxCC0XvrZrvxWCL3hyjbQ/w640-h412/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh1sLBo97RG3EndueQTszTj6MgKUh8E1VK0M-jURFPkCy_rv7hyjFreriv4aZ1KnAI7HrP84JMvAzJZJki2IJCbUJNbCqER1sYHjRtUNvK_3_NaHmA-yWeTfnaxCC0XvrZrvxWCL3hyjbQ/>)

  
  


  


  


  


  


  


  


  


  


  


  


  


**15**. Current network topology.

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgoS78G5dwUqqsNS7U8zqTIhGFCvMcM-fR1ZKwQWnItUOI99Ig3xbc-jAHa6l3ztyUJcLunAO2k-h1XlztO6JDpEVutSlEK_8rp9vLE1qRkM-o8xPjeSh7oYC6Gl836CFwpXYOnuK0uOoY/w640-h312/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgoS78G5dwUqqsNS7U8zqTIhGFCvMcM-fR1ZKwQWnItUOI99Ig3xbc-jAHa6l3ztyUJcLunAO2k-h1XlztO6JDpEVutSlEK_8rp9vLE1qRkM-o8xPjeSh7oYC6Gl836CFwpXYOnuK0uOoY/>)

  
  


  


  


  


  


  


  


  


  


  


At this stage we are ready to get on with the VM launch process. We would first create a VM named master - select the uploaded ubuntu image, associate the dev-network, dev-key-pair, dev-security-group and finally launch the VM.

**16**. VM named 'master'.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjfnZXuyOGxMH6HU8WeFtwJ-PriR8Nk7tyYD4lW5cwgsXB5WKdqOkM22alReBZI6Cw7Ani0ZShfgn7wDJXDL4o2QAkYWO5NsWRmHM4S-JDr9CX98PKtvwgJmYi8-lhIrlBH_-ECT-aOzlA/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjfnZXuyOGxMH6HU8WeFtwJ-PriR8Nk7tyYD4lW5cwgsXB5WKdqOkM22alReBZI6Cw7Ani0ZShfgn7wDJXDL4o2QAkYWO5NsWRmHM4S-JDr9CX98PKtvwgJmYi8-lhIrlBH_-ECT-aOzlA/>)

  


  


  


  


  


  


  


  


  


  


  


  


  


  


**17**. Next we select the ubuntu image.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjabDJnAQsOivDroVdsp2O6MkR06Xc_Csccb9nnxzuR3QAA1cXTQodCQFU4tGmen49XckN2zk8DrvAD8rTc4iec5vncAApm8VcVjiP74s_Xj7lJkdGggwBEBqWIHfYC9gdC6OJIN_TNqqY/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjabDJnAQsOivDroVdsp2O6MkR06Xc_Csccb9nnxzuR3QAA1cXTQodCQFU4tGmen49XckN2zk8DrvAD8rTc4iec5vncAApm8VcVjiP74s_Xj7lJkdGggwBEBqWIHfYC9gdC6OJIN_TNqqY/>)

  
  


  


  


  


  


  


  


  


  


  


**18**. Next we select m1.small flavor with 2 GB RAM and 20 GB hard disk.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjrDWB6InZrN9T1ujRktPu3I3fWSq_mtb7OYSwGvp7bfATwG6VCCIETBegarORQ363lMLdxIY8QQcBLyNbYCdj3qVrt1AxJb304p2HsiDDnmsdCMGZwRf8XHgqB0khMiaXjO6qB2mm2GWs/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjrDWB6InZrN9T1ujRktPu3I3fWSq_mtb7OYSwGvp7bfATwG6VCCIETBegarORQ363lMLdxIY8QQcBLyNbYCdj3qVrt1AxJb304p2HsiDDnmsdCMGZwRf8XHgqB0khMiaXjO6qB2mm2GWs/>)

  
  


  


  


  


  


  


  


  


**19**. We select the dev-network.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgxv0fcbvhBcJdIULV60tGgearSeb3WhO6h6OcLbcJ1TNZneIdx_bN7tHl7Zx6p94kQgZriRbppuZzhyNNcFlnJwLfdJwAk_j62-7HL9pOEp_M9xBHWaYVQ4SmitkodWRZcvazvl2V61Wo/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgxv0fcbvhBcJdIULV60tGgearSeb3WhO6h6OcLbcJ1TNZneIdx_bN7tHl7Zx6p94kQgZriRbppuZzhyNNcFlnJwLfdJwAk_j62-7HL9pOEp_M9xBHWaYVQ4SmitkodWRZcvazvl2V61Wo/>)

  
  


  


  


  


  


  


  


  


**20**. We select the dev-security-group.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEihf64dNfWx28Rpr_VapRvcxXYLlY3LPgshgNA5DVs_CpuzQhj0UxD21RUUCWnSwT0565uICe952zAUr-1tpA41Fz6iju7MeADyEMNMBAiyHphrPktZGlm3OFU9-qJw8NPBs_7uksJ_9sM/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEihf64dNfWx28Rpr_VapRvcxXYLlY3LPgshgNA5DVs_CpuzQhj0UxD21RUUCWnSwT0565uICe952zAUr-1tpA41Fz6iju7MeADyEMNMBAiyHphrPktZGlm3OFU9-qJw8NPBs_7uksJ_9sM/>)

  
  


  


  


  


  


  


  


  


  


  


**21**.  Select the dev-key-pair.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjZnJvnZhPu9NgpO7_M4-44Eu8SerWWUy9FkteR-c2mwad68NHCOfzmnB28gtRoJo8qMYYe50Wn1TiwSvV5wCN0DbSkICQsRK_Jlrh0DnlbuyKJtPk97rkky6BCg7xDkZk0erHkKbA2FXY/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjZnJvnZhPu9NgpO7_M4-44Eu8SerWWUy9FkteR-c2mwad68NHCOfzmnB28gtRoJo8qMYYe50Wn1TiwSvV5wCN0DbSkICQsRK_Jlrh0DnlbuyKJtPk97rkky6BCg7xDkZk0erHkKbA2FXY/>)

  
**22**. We follow the same procedure to another VM called 'worker'. We see both instances are running.

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhjOwbdzeWvdnaP09aQJ8l75w0G-7ooPgN1KrMpKWEwuostAgRshssUaz7ng-9-JVTNBNZr2Mq7q5VjO334hh7uhgprIeFCzLrxSAAsU-MAka1hjztnhNGNOPTjClcLI984V5zW_sY4LX0/w640-h272/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhjOwbdzeWvdnaP09aQJ8l75w0G-7ooPgN1KrMpKWEwuostAgRshssUaz7ng-9-JVTNBNZr2Mq7q5VjO334hh7uhgprIeFCzLrxSAAsU-MAka1hjztnhNGNOPTjClcLI984V5zW_sY4LX0/>)

  
  


  
  


  


  


  


  


  


  


**23**. Lets try to open the console of the master. 

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhed9gMp1r-y5xLq0uNbobT3YJDOMo_pn0rcA4vkU44zD31xxH_moIQxa4L6yhyOPDgcFWWU_4_wDI_B-M9-sHtKQz1Ol-qHRJZpe4IYbUpJRtMKHtsg4aW5GIwPXISd33YBynIWVnpo-o/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhed9gMp1r-y5xLq0uNbobT3YJDOMo_pn0rcA4vkU44zD31xxH_moIQxa4L6yhyOPDgcFWWU_4_wDI_B-M9-sHtKQz1Ol-qHRJZpe4IYbUpJRtMKHtsg4aW5GIwPXISd33YBynIWVnpo-o/>)

  
  


  


  


  


  


  


  


  


We don't get to see the console. Hovering over the 'Click here to see only the console' - we find that the link is pointing to the internal IP of the compute engine at port 6080. 

We would need to open firewall port 6080 on the compute engine and also we replace the internal IP with the external IP of the compute engine to open that link.

**24**. Open the firewall port 6080 of the compute engine.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj4zhBpIhGfnnR46e8EKjCiWGIjDdhCRXWfEg8iAUb9N_HUnbwJvyK4PvkUZCDn5gs1BuLfX6NEiLQhUXuCaw-8E9oaQbxWrttNGMsilcE32EnMlC6G0sQ9-3OlBVzRC9IU_CvEfF8M8RA/w640-h314/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj4zhBpIhGfnnR46e8EKjCiWGIjDdhCRXWfEg8iAUb9N_HUnbwJvyK4PvkUZCDn5gs1BuLfX6NEiLQhUXuCaw-8E9oaQbxWrttNGMsilcE32EnMlC6G0sQ9-3OlBVzRC9IU_CvEfF8M8RA/>)

  
  


  
  


  


  


  


  


  


  


  


  


**25**. We access the master VM console.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhUrZldFZ7iuNvQeB0Kv-grrMWipo0nL4ey6pEqa4Ie5ngDibv2dzT5ztqCLtPiJTrbHguzfdIbuSuihkIkp5kx-TSTkaw9fJM3LC9oOvUSI1mZ3r_In0jJedvkTrw3EMMVCcRPAT7iiD8/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhUrZldFZ7iuNvQeB0Kv-grrMWipo0nL4ey6pEqa4Ie5ngDibv2dzT5ztqCLtPiJTrbHguzfdIbuSuihkIkp5kx-TSTkaw9fJM3LC9oOvUSI1mZ3r_In0jJedvkTrw3EMMVCcRPAT7iiD8/>)

  
  


  


  


  


  


  


  


  


  


  


  


  


**26**. Master has got an internal IP of 192.168.0.61. Let's ping that from the compute engine. Ping does not go through.

stack@openstack:~$ ping 192.168.0.61PING 192.168.0.61\(192.168.0.61\) 56\(84\) bytes of data.

That's because we cant not ping the internal IP. 

**27**. For accessing the VMs we would need to assign floating IPs to the VMs. Floating IP provides an one to one external mapping to a VM. Lets assign floating IPs to them.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjFpSymptBAX8jvkYxuK8VxAn_SsEuoGDp0_kt4TbscBEuHi65Gc01GNucXvuvfqajAOyDaV6rSmI3vl_jv6NCJMz9SORzFGxPTVEqWDpJm5_pZV7PsZuPesLrLsTEs5OWJUsNPLpYV3RA/w640-h288/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjFpSymptBAX8jvkYxuK8VxAn_SsEuoGDp0_kt4TbscBEuHi65Gc01GNucXvuvfqajAOyDaV6rSmI3vl_jv6NCJMz9SORzFGxPTVEqWDpJm5_pZV7PsZuPesLrLsTEs5OWJUsNPLpYV3RA/>)

  
  


  


  


  


  


  


  


  


  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEixwwcfWEMH6b84Lg_f7ZZ28N7htPApyu-9d69SyzGyX1dVgoKzugfaUpljjWBnfgenRV7PfZH4GFrOSc04Hhy26xNB9qkR_KONLN627eT9OYTRPypc3meaRGsreZUs9ZSBoP4GFq-9VMU/w640-h340/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEixwwcfWEMH6b84Lg_f7ZZ28N7htPApyu-9d69SyzGyX1dVgoKzugfaUpljjWBnfgenRV7PfZH4GFrOSc04Hhy26xNB9qkR_KONLN627eT9OYTRPypc3meaRGsreZUs9ZSBoP4GFq-9VMU/>)

  
  


  


  


  


  


  


  


  


  


  


  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgLRjcl5KXtHnHuI0BJxtw_nG4aFHlbpG03pHaAbzgpFh3Rb_oImYu_P3IwF79RGs0R6fzNrPdv8QcxinqAjSFoUxcF_lTwkqm4_g2JM3NfYP9rFB0VpnSHqaYMBxffgbUozZ_RefPM1zA/w640-h276/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgLRjcl5KXtHnHuI0BJxtw_nG4aFHlbpG03pHaAbzgpFh3Rb_oImYu_P3IwF79RGs0R6fzNrPdv8QcxinqAjSFoUxcF_lTwkqm4_g2JM3NfYP9rFB0VpnSHqaYMBxffgbUozZ_RefPM1zA/>)

  
  


  


  


  


  


  


  


  


  


**28**. VMs with floating IPs assigned.

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh5EEHj96Wnx6niAQ_br9p7f-en9BJ-Fhytg38oAcgTBg0ggI8vUfOtlvgBP2QFkgDrJWx5-CscDtsN-jKtGJjQ4vkIHToiUyTF8tZ5s0eCCy94r4mCe4uzCodNOstwcHCW8OFqOc3_3ig/w640-h316/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh5EEHj96Wnx6niAQ_br9p7f-en9BJ-Fhytg38oAcgTBg0ggI8vUfOtlvgBP2QFkgDrJWx5-CscDtsN-jKtGJjQ4vkIHToiUyTF8tZ5s0eCCy94r4mCe4uzCodNOstwcHCW8OFqOc3_3ig/>)

  
  


  


  


  


  


  


  


  


  


  


**29**. At this point we should be able to ping the VMs and SSH into them using the floating IPs.

stack@openstack:~$ ping 172.24.4.252PING 172.24.4.252 \(172.24.4.252\) 56\(84\) bytes of data.64 bytes from 172.24.4.252: icmp\_seq=1 ttl=63 time=1.65 ms64 bytes from 172.24.4.252: icmp\_seq=2 ttl=63 time=0.976 ms

  


stack@openstack:~$ ping 172.24.4.25PING 172.24.4.25 \(172.24.4.25\) 56\(84\) bytes of data.64 bytes from 172.24.4.25: icmp\_seq=1 ttl=63 time=1.66 ms64 bytes from 172.24.4.25: icmp\_seq=2 ttl=63 time=0.734 ms

  


**30**. We are able to ping them. Lets SSH now.

stack@openstack:~/devstack$ ssh -i dev-key-pair.pem ubuntu@172.24.4.25Are you sure you want to continue connecting \(yes/no\)? yesWarning: Permanently added '172.24.4.25' \(ECDSA\) to the list of known hosts.Welcome to Ubuntu 18.04.5 LTS \(GNU/Linux 4.15.0-123-generic x86\_64\)

  


**31**. We are now inside both the VMs. We would update them and get on with process of setting up the kubernetes cluster. We run the following commands in both the  VMs.

  


root@master:~\# apt update

  


root@master:~\# apt install -y apt-transport-https ca-certificates \ curl software-properties-common gnupg2

  


root@master:~\# \#Prepare for docker installroot@master:~\# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key \ \--keyring /etc/apt/trusted.gpg.d/docker.gpg add -

  


root@master:~\# \#Add docker repositoryroot@master:~\# add-apt-repository "deb \[arch=amd64\] \ <https://download.docker.com/linux/ubuntu> $\(lsb\_release -cs\) stable"

  


root@master:~\# \#Install containerd and dockerroot@master:~\# sudo apt update && sudo apt install -y \ containerd.io=1.2.13-2 \ docker-ce=5:19.03.11~3-0~ubuntu-$\(lsb\_release -cs\) \ docker-ce-cli=5:19.03.11~3-0~ubuntu-$\(lsb\_release -cs\)

  


\#Specify cgroup driver to be systemdroot@master:~\# cat <<EOF | sudo tee /etc/docker/daemon.json \{ "exec-opts": \["native.cgroupdriver=systemd"\], "log-driver": "json-file", "log-opts": \{ "max-size": "100m" \}, "storage-driver": "overlay2" \} EOF

  


root@master:~\#Done with docker - reload daemon and restart dockerroot@master:~\# sudo systemctl daemon-reloadroot@master:~\# sudo systemctl restart dockerroot@master:~\# sudo systemctl enable docker

  


**32**. Next we would install kubernetes - we do not install kubectl on the worker node.

root@master:~\# sudo apt update

root@master:~\# curl -s <https://packages.cloud.google.com/apt/doc/apt-key.gpg> \ | sudo apt-key add -

root@master:~\# cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list deb <https://apt.kubernetes.io/> kubernetes-xenial main EOF

root@master:~\# apt update

On the master only:

root@master:~\# apt install -y kubelet kubeadm kubectl

On the worker

root@worker:~\# apt install -y kubelet kubeadm

Again on both VMs.

root@master:~\# systemctl daemon-reloadroot@master:~\# systemctl restart kubelet

  


**33**. We are now done with kubernetes installation. Lets initialize the master and then join the worker to the cluster. We avoid the pre-flight check errors because the settings we have chosen are not optimum for the cluster and kubernetes is not very happy about that.

root@master:~\# kubeadm init --ignore-preflight-errors=all

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgs5ksWgOPDB-IOPAP9msx99ZCJy6-jJkF3VBZn-1fqbnWGpBxDImwREQvhqvgQtH-q7jMg7ZgCcybqNBAATdcGjN1ol-OZL0qZkE3CJcBzDrSMP-YnAIhKBz4QOtkIpu4BsrFLIaCnf00/w640-h338/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgs5ksWgOPDB-IOPAP9msx99ZCJy6-jJkF3VBZn-1fqbnWGpBxDImwREQvhqvgQtH-q7jMg7ZgCcybqNBAATdcGjN1ol-OZL0qZkE3CJcBzDrSMP-YnAIhKBz4QOtkIpu4BsrFLIaCnf00/>)

  
  


  


  


  


  


  


  


  


  


  


root@master:~\# \{ mkdir -p $HOME/.kube sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config sudo chown $\(id -u\):$\(id -g\) $HOME/.kube/config \}

  


We copy the kube config to the home directory as instructed and proceed to the worker node and execute the join command.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiqN8tKQaWkFkCdKBX-BMIGzR-1M10AcO2m4rwonrdKJ2hQsXagunVKxKSi3tb1PMf9U4yWbNlqsOy1D750GT1a5GumGIc7qGPvivAiL2E1wIZAcfGi1k7d6io3pVI95jBJ2VSrZ5nOrJI/w640-h66/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiqN8tKQaWkFkCdKBX-BMIGzR-1M10AcO2m4rwonrdKJ2hQsXagunVKxKSi3tb1PMf9U4yWbNlqsOy1D750GT1a5GumGIc7qGPvivAiL2E1wIZAcfGi1k7d6io3pVI95jBJ2VSrZ5nOrJI/>)

  
  


  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjtFevN7hLgS2fLOfaf6F65KLU0OqxFkMuWO90C2ccuzWGIm-8ocPFwYchkqK0TDGVoRgU1Tg_SG3DGqO8sQZDICgcvkdXSeZ3hpIvqjNpZBhv_5b91eYJtm4NerijVnr57gKYzC8rL73Q/w640-h118/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjtFevN7hLgS2fLOfaf6F65KLU0OqxFkMuWO90C2ccuzWGIm-8ocPFwYchkqK0TDGVoRgU1Tg_SG3DGqO8sQZDICgcvkdXSeZ3hpIvqjNpZBhv_5b91eYJtm4NerijVnr57gKYzC8rL73Q/>)

  
  


  


  


  


**34.**   Lets fire the following command.

root@master:~\# kubectl get nodesNAME STATUS ROLES AGE VERSIONmaster NotReady master 16m v1.19.4worker NotReady <none> 2m54s v1.19.4

  


The nodes are not ready - that's expected - because we have not deployed CNI plugin yet. Lets do that next.

**35.** Install weave POD network plugin.

root@master:~\# kubectl apply -f \ "https://cloud.weave.works/k8s/net?k8s-version=$\(kubectl \ version | base64 | tr -d '\n'\)"serviceaccount/weave-net createdclusterrole.rbac.authorization.k8s.io/weave-net createdclusterrolebinding.rbac.authorization.k8s.io/weave-net createdrole.rbac.authorization.k8s.io/weave-net createdrolebinding.rbac.authorization.k8s.io/weave-net createddaemonset.apps/weave-net created

  


**36.** Let's check the nodes again.

root@master:~\# kubectl get nodesNAME STATUS ROLES AGE VERSIONmaster Ready master 25m v1.19.4worker Ready <none> 12m v1.19.4

  


Cluster is finally ready\! Next we deploy a nginx pod.

**37**. Deploy nginx pod.

root@master:~\# kubectl run nginx-pod --image nginxpod/nginx-pod createdroot@master:~\# kubectl get pod -wNAME READY STATUS RESTARTS AGEnginx-pod 1/1 Running 0 21s

We see that pod is running.

**38**. Let's port-forward to the pod in another terminal and curl it from current terminal.

root@master:~\# kubectl port-forward nginx-pod 9999:80Forwarding from 127.0.0.1:9999 -> 80Forwarding from \[::1\]:9999 -> 80

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg7qmOQich8LukkBo2yyoP91lUunXl6EOkF6C4CO7yNXnbjiXF_GDOLjXCckNSvm5pCPs19PjpGhBV7Xhp-heAxS9k4K7nUR9WYAalrcH6E0RyZtUUTY2plbDbNDkPQ5ZwC_Jn7-pzefg0/w640-h408/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg7qmOQich8LukkBo2yyoP91lUunXl6EOkF6C4CO7yNXnbjiXF_GDOLjXCckNSvm5pCPs19PjpGhBV7Xhp-heAxS9k4K7nUR9WYAalrcH6E0RyZtUUTY2plbDbNDkPQ5ZwC_Jn7-pzefg0/>)

  
  


  


  


  


  


  


  


  


  


  


  


  


Port forward is working fine. 

**39.** Lets create create a NodePort service and access it from the cluster nodes.

First we create the deployment:

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhL25e1Fr3TDo2x_2EfTFwmQkQ5mANvOe1ZuG1vP9RpeRvukg5gfNMnHlu6Vax9biRbwpufbtEgy_JuCUATeCPaXmVRCorW4JRcvEZgj2jEm2zINqb9sKZ5ql8qoxxRk-VElrVgQ24VcCE/w640-h537/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhL25e1Fr3TDo2x_2EfTFwmQkQ5mANvOe1ZuG1vP9RpeRvukg5gfNMnHlu6Vax9biRbwpufbtEgy_JuCUATeCPaXmVRCorW4JRcvEZgj2jEm2zINqb9sKZ5ql8qoxxRk-VElrVgQ24VcCE/>)

  
  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


We deploy the above deployment yaml.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiI2dUqPw8q_77zJjTT1mMb5P9f9tnnR3XXuAkazeXCAfWY4OV5Sa7cGs4EXuuvRi482JLfamy-SgHF6OhZE05jMKQw-DrT-6hq3NIrWRs9OOLbMdfaAt8mt7L55chHCwqbFp2O6bViSJM/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiI2dUqPw8q_77zJjTT1mMb5P9f9tnnR3XXuAkazeXCAfWY4OV5Sa7cGs4EXuuvRi482JLfamy-SgHF6OhZE05jMKQw-DrT-6hq3NIrWRs9OOLbMdfaAt8mt7L55chHCwqbFp2O6bViSJM/>)

  
  


  


  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEikFhL_AIkMgumJGNnVncZGNGLEBTyKQeOu5SoeyOq1obkQeK7sHILXNxfelegry1oxE2QOPGuwkRFznwrCorsE-j5GhBjwR0zucDpTUEwFLiUIbnowHDUXziZhcAJ1dMdDcLy2zjgmXmc/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEikFhL_AIkMgumJGNnVncZGNGLEBTyKQeOu5SoeyOq1obkQeK7sHILXNxfelegry1oxE2QOPGuwkRFznwrCorsE-j5GhBjwR0zucDpTUEwFLiUIbnowHDUXziZhcAJ1dMdDcLy2zjgmXmc/>)

  
  


  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgZxrdAfTO17iA8CukZArr9LlBuFuur8wKBSWtZtzVx28l2yHye99uI718BVUApghU6FwrgVVcborwcn9PhbxqCdZsvT0iM5YxpVEGsY83KZ25-pI1kKRrIIBvMEfIhwqD1WJFQNvjKQBs/w640-h90/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgZxrdAfTO17iA8CukZArr9LlBuFuur8wKBSWtZtzVx28l2yHye99uI718BVUApghU6FwrgVVcborwcn9PhbxqCdZsvT0iM5YxpVEGsY83KZ25-pI1kKRrIIBvMEfIhwqD1WJFQNvjKQBs/>)

  
  


  


  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhcW5AxgDejy__WSQKYrZnKCLaOEacfLmBVCwOK8KL44iY_7ZuFmLbHT69JPX4PybdXWEboXrdsMTEFB4aSC32lYUTvI5s7qiREJ-7eHHxKMrHNacizM8Htc3LHqVEDVWNfwuF8QvNXitM/w640-h64/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhcW5AxgDejy__WSQKYrZnKCLaOEacfLmBVCwOK8KL44iY_7ZuFmLbHT69JPX4PybdXWEboXrdsMTEFB4aSC32lYUTvI5s7qiREJ-7eHHxKMrHNacizM8Htc3LHqVEDVWNfwuF8QvNXitM/>)

  
  


  


  


**40.  **Now, lets access it from the worker node.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEizLpgPWVNLoPegf_EBd1UTf0hgu5IFV_2luBCYaYcmdB0C5ukqBuQEtU1FaqOXFAku3su5GWzUmCyIUO23Ts_hUuaObxoraj22Nx2MfNLyLBAZE5gpVt8GGRdOyR7KbFxbR4O_NNwHbMI/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEizLpgPWVNLoPegf_EBd1UTf0hgu5IFV_2luBCYaYcmdB0C5ukqBuQEtU1FaqOXFAku3su5GWzUmCyIUO23Ts_hUuaObxoraj22Nx2MfNLyLBAZE5gpVt8GGRdOyR7KbFxbR4O_NNwHbMI/>)

  


  


  


  


  


  


  


We can access the NodePort service from the host machine. 

**41.  **Let's access it via the floating IP.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi76ljfyd-gRnBPb179mhGzlf2MSaHN2uDXhnPq3mwNn1p0Q_3UMn0Buf9BHEVJfli__22FOvcz_SjnEOVXDfibdS7673uPTfdaJa19B41CzWy3FM-003YDRwa6G10hLksw5xoSu_kta6w/w640-h206/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi76ljfyd-gRnBPb179mhGzlf2MSaHN2uDXhnPq3mwNn1p0Q_3UMn0Buf9BHEVJfli__22FOvcz_SjnEOVXDfibdS7673uPTfdaJa19B41CzWy3FM-003YDRwa6G10hLksw5xoSu_kta6w/>)

  
  


  


  


  


We can access the NodePort via floating IP too.

**42.  **Next, let go inside a POD container and check if other PODs are available via kube DNS.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgORHMwGK_sMsPjcjEEU4J1NptxkE4_yWY2378v1TmE3u2kNreMQZbwzWo3nH6bLPZjpek9DjYVm-VK4RIE-kpvFcKPUACk8Zf4kjFBbVYnF-myUOeOYV6R_DYwCTfkTPI1FN2FGvPIiDc/w640-h178/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgORHMwGK_sMsPjcjEEU4J1NptxkE4_yWY2378v1TmE3u2kNreMQZbwzWo3nH6bLPZjpek9DjYVm-VK4RIE-kpvFcKPUACk8Zf4kjFBbVYnF-myUOeOYV6R_DYwCTfkTPI1FN2FGvPIiDc/>)

  
  


  


  


  
  


  


As expected, kube DNS access is working fine.

  


**Conclusion:**

**At the heart of cloud computing is virtualization. It combines storage, compute and network virtualization. Here, in this exercise, we used a google compute engine, which itself is virtual machine and we deployed whole openstack network, storage and compute virtualization framework, provisioned two ubuntu VMs, launched a kubernetes cluster, deployed PODs and everything works\!** As mentioned in the beginning, we could have taken this nesting and virtualization much further  but this has been already long post. We stop here for today.

  


Lastly: The CLI version of this can be found at [github](<https://github.com/ratulb/k8s-openstack-gcp>) \- which is a hassle free way of achieving the whole thing by running couple of scripts. Following is a snap of the same.

 

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiBTUBm6NYz3g4zO3EXjSnqajtixUwcvYhLKtUo8-SlgZKJCQzcHV3yoQe85FywXbNQEnjAyrbYwKDaTGgjS2i9TXq-mNdOKYrqxn71z1tacvL00raQwvvqtspFFzTBg5V9r4UceD1YHms/w640-h336/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiBTUBm6NYz3g4zO3EXjSnqajtixUwcvYhLKtUo8-SlgZKJCQzcHV3yoQe85FywXbNQEnjAyrbYwKDaTGgjS2i9TXq-mNdOKYrqxn71z1tacvL00raQwvvqtspFFzTBg5V9r4UceD1YHms/>)

*Originally published on [https://rbsomeg.blogspot.com](https://rbsomeg.blogspot.com/2020/11/nesting-all-the-way-kubernetes-on-openstack-on-google-compute-engine.html)*
