---
layout: post
title: "Setting up a kubernetes cluster - quick and easy"
date: 2020-11-23 00:45:00.045+00:00
tags: [kubernetes cluster setup]
---

**Take home: Install a kubernetes cluster across machines by running a simple script. No manual intervention whatsoever.   All setup for consumption.**

  


Often times, we need a kubernetes cluster to try out something new real quick or  to use it on a daily basis for our development work. It's like back old days when every so often we needed a tomcat, WebLogic, WebSphere server at your disposal. 

Setting up kubernetes cluster is not difficult at all - but you still need to pass through few hoops like installing a runtime/k8s artifacts, configuring a CNI plugin etc. It becomes  a hassle if we have to carry out the same steps on multiple worker machines every now and then.

Here is a simple script that can spin off a kubernetes cluster in a matter of minutes, a CNI plugin installed and a demo POD deployed - all up and running. No manual intervention. All we need is SSH  root or sudo access. Below are sneak pics: 

1\. We provision three compute VMs across 3 geo-graphic locations \(Just for the fun of it\!\)

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjULIScVkin0pGlbWia-T-dAd73Y5h1ChcrdF7N37HQAqClY_ckbJsvfAli65qE_8RGTA1AwVKPE4zBvPo67i_QoXviL77OgXuplBTJ5hZfMldY1rzjV7EkWyJmhkdXQax2rzpw-mcU3UQ/w400-h296/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjULIScVkin0pGlbWia-T-dAd73Y5h1ChcrdF7N37HQAqClY_ckbJsvfAli65qE_8RGTA1AwVKPE4zBvPo67i_QoXviL77OgXuplBTJ5hZfMldY1rzjV7EkWyJmhkdXQax2rzpw-mcU3UQ/>)

  
  


  


  


  


  


  


  


  


  


  


2\. We SSH to one of boxes that we named 'mgnt-server'. This we would use as one of the two worker nodes. Generate a SSH key pair.

Note: It is not necessary that 'mgnt-server' be part of the k8s cluster.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiWw6_FH1jjDublm9NwnQEMtUhvHSL5bS-sv8weR_aoG1RW1dUhKB7tLCC6Icic6OVCfU_aKxYWZpJLcTHIoKaAEgIM_7TO9HjlxkTFZsHodYn-d9JAkd8QGqB8R7SPUKHxoqFGLgEa5_A/w400-h352/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiWw6_FH1jjDublm9NwnQEMtUhvHSL5bS-sv8weR_aoG1RW1dUhKB7tLCC6Icic6OVCfU_aKxYWZpJLcTHIoKaAEgIM_7TO9HjlxkTFZsHodYn-d9JAkd8QGqB8R7SPUKHxoqFGLgEa5_A/>)

  
  


  
  


  


  


  


  


  


  


  


  


  


  


3\. Apply the public key to master and worker nodes' authorized\_keys. 

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhAiseIpwhVcQULATXyQA_CjMsiCkupTZrqSf88XXYK68ZK4S_raJ7hI04QaJAuRSozbaMPdEp9hVUnmw17OH0pQNRGIOiGogjDw9ZR1iK0xuUQJQg36NiAUcgl64lrmmZXnRDMyV-4PHk/w400-h279/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhAiseIpwhVcQULATXyQA_CjMsiCkupTZrqSf88XXYK68ZK4S_raJ7hI04QaJAuRSozbaMPdEp9hVUnmw17OH0pQNRGIOiGogjDw9ZR1iK0xuUQJQg36NiAUcgl64lrmmZXnRDMyV-4PHk/>)

  
  


  


  


  


  


  


  


  


  


4\. We check out the git repository containing the cluster launch script and proceed to edit the setup.conf file.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEibJSsKt1MOAL_XfvCqSu-fV_Y1Bzz0gPRxPJrftdVJYenBQo49ErzsNK0A5Cp7-TXqjCWSD3e4TAPRVO4nryZk7FROCvCXS-U7dhRGowWddjygujNvFfhP-4jadNDCh6UbQh_q97pBqn8/w640-h430/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEibJSsKt1MOAL_XfvCqSu-fV_Y1Bzz0gPRxPJrftdVJYenBQo49ErzsNK0A5Cp7-TXqjCWSD3e4TAPRVO4nryZk7FROCvCXS-U7dhRGowWddjygujNvFfhP-4jadNDCh6UbQh_q97pBqn8/>)

  


  


  


  


  


  


  


  


  


  


  


  


  


  


5\. Edit the setup.conf for worker and master nodes.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj0zfOjtyFSy-eEtQljOwBE6nSN_RlLQ3QazOqRZxbe4Qp_Z_4ewGs7xPZ7u3YQkSvGtJc1ihiiYuBNFPA7o-CTE_5NfbkaL53lrLeUVKCfmr5MXIroZRoHEMInXdyCXF2he91_5dFlk0A/w400-h49/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj0zfOjtyFSy-eEtQljOwBE6nSN_RlLQ3QazOqRZxbe4Qp_Z_4ewGs7xPZ7u3YQkSvGtJc1ihiiYuBNFPA7o-CTE_5NfbkaL53lrLeUVKCfmr5MXIroZRoHEMInXdyCXF2he91_5dFlk0A/>)

  
  


  


6\. And launch the cluster creation.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhA4cMXSHzLhGDz6YbKi4v6lCXr6BG_Kt6W0-ILUgqCnIvvalZ0z3lSnxm2vExUnLaLgt5MchGvJ106zs_g-c8d9bm1iJ_MhNkVj895kCMaKrTCAXvPZdjC1YHoln9OYlogJzuZx4R8_KE/w640-h70/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhA4cMXSHzLhGDz6YbKi4v6lCXr6BG_Kt6W0-ILUgqCnIvvalZ0z3lSnxm2vExUnLaLgt5MchGvJ106zs_g-c8d9bm1iJ_MhNkVj895kCMaKrTCAXvPZdjC1YHoln9OYlogJzuZx4R8_KE/>)

  
  


  
  


  


7\. Cluster creation progress - worker joining the cluster.

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiVIpgMIVvakqd4vKrv_Z7D4FOY_JLAh3NlLCtmznR66cTUutxiAXdOTagpUP_g8OUXa9cdcJjZ8_jZenN3ZnyPKateKAxAlKEXiiSMlaImtKV6Z1EEwGox9FttUKUKCSOcp3-faAeS13c/w400-h130/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiVIpgMIVvakqd4vKrv_Z7D4FOY_JLAh3NlLCtmznR66cTUutxiAXdOTagpUP_g8OUXa9cdcJjZ8_jZenN3ZnyPKateKAxAlKEXiiSMlaImtKV6Z1EEwGox9FttUKUKCSOcp3-faAeS13c/>)

  
  


  


  


  


  


8\. CNI plugin getting deployed.

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjFCOFHkuV62REyQuHHFX9-7C2svRtDCMqsuTJAU3mijsAh56NL0dBNcT-EpS1__dG6-dkomtu64VE2r4VD0XpIy6oJvXM-refodJpyghBPzwSS9tVZxf4u3a7lmPZ29_y1o6GW8zL07qU/w373-h400/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjFCOFHkuV62REyQuHHFX9-7C2svRtDCMqsuTJAU3mijsAh56NL0dBNcT-EpS1__dG6-dkomtu64VE2r4VD0XpIy6oJvXM-refodJpyghBPzwSS9tVZxf4u3a7lmPZ29_y1o6GW8zL07qU/>)

  
  


  


  


  


  


  


  


  


  


  


  


  


  


9\. Cluster should be ready in matter of minutes.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjJ7qd6_bapO2TXxKzxNRpGzdga-dur-nG2_zI4LTD6GuHjOqTNX2bMHyEweWGdnOe7rnMwGt01X2dSl3qQA90GBbDVEdy1ceUFvdu-r89FMeuCML5HIRTtqOMg2KXR0L4tpkQwNglSVtU/w400-h397/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjJ7qd6_bapO2TXxKzxNRpGzdga-dur-nG2_zI4LTD6GuHjOqTNX2bMHyEweWGdnOe7rnMwGt01X2dSl3qQA90GBbDVEdy1ceUFvdu-r89FMeuCML5HIRTtqOMg2KXR0L4tpkQwNglSVtU/>)

  


**Clone the following repository branch:**  


git clone  https://github.com/ratulb/k8s-easy-install.git -b docker
