---
layout: post
title: "Create google cloud VM inside custom VPC remotely with gcloud command"
date: 2020-02-14 16:43:00.002+00:00
tags: [create VM, GCP, google VPC, gcloud]
---

These are the steps for creating VM instances inside a google cloud VPC custom network remotely. It assumes that google cloud account has been created and[ cloud sdk](<https://cloud.google.com/sdk/docs/downloads-versioned-archives>) has been installed and working correctly.  
  
1\) Set google cloud project:  
  


  * **gcloud config set project \[xxxxxxxxxxxxxxx\]**

  


2\) Create custom VPC network

  * **gcloud compute networks create _vpc-net_ \--subnet-mode custom**



3\) Create two subnets within the VPC network

  * **gcloud compute networks subnets create _vpc-net-subnet-us-central_ \--network _vpc-net_ \--region us-central1 --range 10.0.1.0/24**
  * **gcloud compute networks subnets create _vpc-net-subnet-eu-west_ \--network _vpc-net_ \--region europe-west1 --range 10.0.2.0/24**



4\) Listing the created subnets

  * **gcloud compute networks subnets list --network _vpc-net_**



vpc-net-subnet-eu-west     europe-west1  vpc-net  10.0.2.0/24

vpc-net-subnet-us-central  us-central1   vpc-net  10.0.1.0/24

  


5\) Create the VMs inside the subnets

  * **gcloud compute instances create _vpc-net-vm-us_ \--subnet _vpc-net-subnet-us-central_ \--zone us-central1-a**
  * **gcloud compute instances create _vpc-net-vm-eu_ \--subnet _vpc-net-subnet-eu-west_ \--zone europe-west1-b**



[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhoyvrULJgPM2wnwmxuXg6KQwOMVzjQaSUK1V6fmAabqTLDQF_16O7wXcpXJ2DpZiF7y7GOVHa8JOPvGjUBgoO2q6H_CKutmIzs45qlXwhadbmIf1B5dhQD2CeJvlT0-G2etwlMmnXAzjg/s640/Capture.PNG)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhoyvrULJgPM2wnwmxuXg6KQwOMVzjQaSUK1V6fmAabqTLDQF_16O7wXcpXJ2DpZiF7y7GOVHa8JOPvGjUBgoO2q6H_CKutmIzs45qlXwhadbmIf1B5dhQD2CeJvlT0-G2etwlMmnXAzjg/s1600/Capture.PNG>)

**  
**

**  
**

6\) Try to ping \(From local machine\) or ssh \(From gcloud web console\) - it would fail.

  


  


7\) Create the filewall rules for allowing ping & ssh to the newly created VMs.

  * **gcloud compute firewall-rules create _vpc-net-allow-ssh_ \--allow tcp:22,icmp --network _vpc-net_**



Now, we should be able to ping and ssh into the VMs.  
  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhuM2tmVHSH2HX1UKqZ-UzTnglR-r0gMDO_4bJInaMawRBy7gJ1Bxhnv-Vuoo-xK9Yhsl7_tuULpZJSfPuLm0QoYidW_aEv_CADGzII8Qhz4YmfU0YaUba2fBzIzw0LqH60g_-BOiQ9hqI/s1600/Capture2.PNG)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhuM2tmVHSH2HX1UKqZ-UzTnglR-r0gMDO_4bJInaMawRBy7gJ1Bxhnv-Vuoo-xK9Yhsl7_tuULpZJSfPuLm0QoYidW_aEv_CADGzII8Qhz4YmfU0YaUba2fBzIzw0LqH60g_-BOiQ9hqI/s1600/Capture2.PNG>)
