---
layout: post
title: "Linux oft-required commands(for self reference)"
date: 2019-11-25 19:33:00+00:00
tags: []
---

**_Install and export JAVA\_HOME:_**  
  
apt-get update  
sudo apt install default-jdk  
  
 which java  
  
Output: /usr/bin/java  
  
readlink -f /usr/bin/java  
  
Output: /usr/lib/jvm/java-11-openjdk-amd64/bin/java  
  
export JAVA\_HOME=/usr/lib/jvm/java-11-openjdk-amd64  
  
**_Find files containing text:_**  
  
find . -type f -exec grep -H '8080' \{\} \;  
  
**_Remove all stopped docker containers_**  
  

    
    
    docker rm $(docker ps -a -q)
