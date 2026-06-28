---
layout: post
title: "VPC native kubernetes cluster in GCP"
date: 2021-06-15 20:11:00+00:00
tags: []
---

**  VPC native k8s clusters have quite a few advantages:**

  * POD IPs are directly routable. This eliminates the need for a load balancer to hop from node to pod. Instead traffic can reach PODs directly minimizing latency.
  * POD IPs are reserved before PODs are created. This helps avoid POD IP collision with existing resource IPs.
  * Firewall rules can be configured for POD IP ranges instead of node IP ranges.
  * POD IPs can be accessed from on-premise connected networks via VPN or cloud inter-connect.



VPC native cluster requires a subnet for cluster nodes, 2 secondary subnets inside the subnet for nodes - one for POD IPs and another for service IPs.

**Commands to launch a VPC native k8s cluster quickly:**

**Create VPC network:**  


gcloud compute networks create gke --project=\[project\_id\] --subnet-mode=custom --mtu=1460 --bgp-routing-mode=regional 

**Create subnet and secondary ranges for POD and services:**  


gcloud compute networks subnets create primary-subnet --project=\[project\_id\] --range=10.0.0.0/8   
\--network=gke --region=asia-south1 --secondary-range=pod-subnet=172.16.0.0/12 --secondary-range=service-subnet=192.168.0.0/16

**Launch the cluster:**

gcloud container clusters create gke-cluster \  
    \--network gke \  
    \--enable-ip-alias \  
    \--subnetwork=primary-subnet \  
    \--cluster-secondary-range-name=pod-subnet \  
    \--services-secondary-range-name=service-subnet \  
    \--num-nodes 3 \  
  \--zone asia-south1-b

**Initialize kubeconfig:**

gcloud container clusters get-credentials gke-cluster --zone asia-south1-b

**Deploy a nginx POD:**

kubectl run nginx --image nginx

**Expose POD via cloud load balancer:**

kubectl expose pod nginx -l run=nginx --port 80 --type LoadBalancer

**Access exposed POD via load balancer IP:**

curl \[load balancer IP\]

*Originally published on [https://rbsomeg.blogspot.com](https://rbsomeg.blogspot.com/2021/06/vpc-native-kubernetes-cluster-in-gcp.html)*
