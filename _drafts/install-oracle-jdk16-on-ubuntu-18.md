---
layout: post
title: "Install oracle jdk16 on ubuntu 18"
date: 2021-04-11 06:42:00.003+00:00
tags: [ubuntu 18, java 16]
---

add-apt-repository ppa:linuxuprising/java  
``` `
    
    
    apt install oracle-java16-installer --install-recommends

The above command would set java 16 as default. To avoid that - use the following command:
    
    
    apt install oracle-java16-installer --no-install-recommends

  
``

![]({{ site.baseurl }}/assets/images/install-oracle-jdk16-on-ubuntu-18-1.png)  
``

``
