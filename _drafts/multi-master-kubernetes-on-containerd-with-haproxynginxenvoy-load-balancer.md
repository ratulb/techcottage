---
layout: post
title: "Multi master kubernetes on containerd with haproxy/nginx/envoy load balancer"
date: 2021-01-18 20:56:00.009+00:00
tags: []
---

[Kubernetes has declared that it is going to remove support for docker as runtime](<https://kubernetes.io/blog/2020/12/02/dont-panic-kubernetes-and-docker/>).  Its has deprecated docker as runtime post v1.20.  Complete removal of docker as runtime is planned for the 1.22 release in late 2021.

Kubernetes had been using docker to get to [containerd](<https://github.com/containerd/containerd>)\(which is what it actually needs\) via dockershim. 

This post shows how to create a kubernetes cluster on containerd via a simple menu driven script. The script has been verified to work with debian 10, ubuntu 16.04, 18.04 and 20.04.

For the multi-master case, it also provides the choice of [haproxy](<https://www.haproxy.com/>)/[nginx](<https://www.nginx.com/>)/[envoy ](<https://www.envoyproxy.io/>)as load balancer to front the kube api servers.

**Requirements:** A bunch of machines with **root ssh** access from where the provisioning script is run.

For demo purpose, it uses 4 compute engine instances - 1 for load balancer, 2 master nodes and 1 worker node.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjlAVGcO-EuHjqXG2vPYUPJ9CcUoWKyLI2iYVsaY6NHSRNjULiwgXmYh0ie6af6MSjhfFuSNh9hdMpb7ynuxIicw7kMTCaFDCThlQ4EcyoRHvlMhed3kiyMp7tVYumXahCZcqRkNqt6mSM/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjlAVGcO-EuHjqXG2vPYUPJ9CcUoWKyLI2iYVsaY6NHSRNjULiwgXmYh0ie6af6MSjhfFuSNh9hdMpb7ynuxIicw7kMTCaFDCThlQ4EcyoRHvlMhed3kiyMp7tVYumXahCZcqRkNqt6mSM/>)

  


  


  


  


  


  


Checkout the following git repository:

git clone https://github.com/ratulb/k8s-easy-install -b containerd

And launch the script cluster.sh

cd k8s-easy-install && ./cluster.sh

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiRH8BnV0D9MwZRA1jwek_cLuvdn_pt7QmuLQlIgZyzbgqibeVfwjiO3nseYqdH0zXuxt6cLp49GTahhauPcTyFIct6KfFBZ6LpKB2WGNCJ6qGnfM4_XJfjG8oD5AJkpaVveVFskgj0Ls4/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiRH8BnV0D9MwZRA1jwek_cLuvdn_pt7QmuLQlIgZyzbgqibeVfwjiO3nseYqdH0zXuxt6cLp49GTahhauPcTyFIct6KfFBZ6LpKB2WGNCJ6qGnfM4_XJfjG8oD5AJkpaVveVFskgj0Ls4/>)

  


  


 

User would be presented with a menu as shown below:

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjkbB4KKnV_UmbJv6bRGth5DEQJct4yvks55MFEsF9RBwKsVMIjmC0ZXJ_nRo21yhuyF71Vvpqudw0iQ8beNkVCLvoyLN9TxbcyL8gs342Y15yFjDM4yv-MTeUmwfJ3h1vEvF6lwjqq8EY/w655-h177/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjkbB4KKnV_UmbJv6bRGth5DEQJct4yvks55MFEsF9RBwKsVMIjmC0ZXJ_nRo21yhuyF71Vvpqudw0iQ8beNkVCLvoyLN9TxbcyL8gs342Y15yFjDM4yv-MTeUmwfJ3h1vEvF6lwjqq8EY/>)

  
  


  


  


  


  


  


  


Next, select option 5 and enter the load balancer details:

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEimn8jiUJsnELGnbM39uB2GDUCSPTIzkAocONBNl2FQPw1Y2y2w586BNdtv6uvz_bCCoSRZqS16C96DXIEIK00zQmJpMWDxUpqr8YsnJZWz4XhaOktkuRcLsMUbtIZtOI19F5V73t_eyZE/w657-h416/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEimn8jiUJsnELGnbM39uB2GDUCSPTIzkAocONBNl2FQPw1Y2y2w586BNdtv6uvz_bCCoSRZqS16C96DXIEIK00zQmJpMWDxUpqr8YsnJZWz4XhaOktkuRcLsMUbtIZtOI19F5V73t_eyZE/>)

  
  


  


  


  


  


  


  


  


  


  


  


  


  


  


Next,  provide the master nodes'  and worker node's addresses and trigger launch.

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgzFsH6XPijJ5utyWvpAo2hKcXDg_JmywOJq6TVem7LOLoppog9LzmRfowh9H9wg2wPcSIkNcVn5nqaOvs2tl-cqGltJBja45NZ2apoPUZnRBjHyVGJ6sV4Z7MkNCML8gB8iSXAZnmzPFE/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgzFsH6XPijJ5utyWvpAo2hKcXDg_JmywOJq6TVem7LOLoppog9LzmRfowh9H9wg2wPcSIkNcVn5nqaOvs2tl-cqGltJBja45NZ2apoPUZnRBjHyVGJ6sV4Z7MkNCML8gB8iSXAZnmzPFE/>)

  
  


  
  


  


  


  


Next, in a couple of minutes - we see cluster setup in progress - followed by completion of setup.

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi7UVmjMJspNu45fK9F0j4grQR2fU7IEZ3IdN8bK4Fn-UozadzSTE6aPp5ywU6CVV2TAAvNFjlzivdkCkG2uhGX33kBYhknJwpBCRRKiyQSOQyybq1xUdI5L5QIlxQlcENgmwJr1MOnCv8/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi7UVmjMJspNu45fK9F0j4grQR2fU7IEZ3IdN8bK4Fn-UozadzSTE6aPp5ywU6CVV2TAAvNFjlzivdkCkG2uhGX33kBYhknJwpBCRRKiyQSOQyybq1xUdI5L5QIlxQlcENgmwJr1MOnCv8/>)

  
  
  


  


  


  


  


  


  


  


  


  


  


  


  


  


**  
**

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhUhZ1dguDT4Z3WGJP94ruTq99tVoi6BXhwvhfZ8sDYjR70i3qQkPEUbncPPHcWLNCI00uaY47r0hMggjFQWIBlB7oWLoCaY2YB-f96lYlSTasbzaextNMrd9S_nswnENZDSgP7JUtH6lU/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhUhZ1dguDT4Z3WGJP94ruTq99tVoi6BXhwvhfZ8sDYjR70i3qQkPEUbncPPHcWLNCI00uaY47r0hMggjFQWIBlB7oWLoCaY2YB-f96lYlSTasbzaextNMrd9S_nswnENZDSgP7JUtH6lU/>)

  


**Disclaimer:**

At it's core this script is very dumb  \- it does what it is told to do - it has no recollection at all. If told these are the masters - it will act so. Next time, if the masters are given as workers - it will carry out the steps to make them behave as workers. It will not check that it is destroying a running cluster.  Obeys the kubernetes philosophy - **everything is cattle - no pets**. That said, the whole thing is evolving - its only part of a project that is on foot currently . That's for another post on another day.

At present, it does some checks though - input mistakes like machine appearing both as worker as well as master or load balancer collocated\(no valid reason for this scenario\) - with master or a worker - and load balancer port still being 6443. 

  


Note: This branch has been moved to containerd. Following is the git clone command:

git clone https://github.com/ratulb/k8s-easy-install -b containerd
