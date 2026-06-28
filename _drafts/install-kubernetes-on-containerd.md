---
layout: post
title: "Install kubernetes on containerd"
date: 2020-12-17 18:35:00.009+00:00
tags: []
---

Kubernetes is [deprecating Docker](<https://kubernetes.io/blog/2020/12/02/dont-panic-kubernetes-and-docker/>) as a container runtime after v1.20. This post shows how to install kubernetes on ubuntu 18.04 using [containerd ](<https://containerd.io/>)as a container runtime. For brevity, we do this just only on one node.

Below is a clean machine snap where we don't have docker installed.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj9__yUlpQtF-XvFoFq7xCeofbiyJ-BNOyxEeQaWpCaVcNRFt-0jO4l-8G6Bjq9Tu2gAxjZE6NLgNpIpwIiCG90l4pRtIjeB-X0IJ2Ut-JbMsUUoZ-QFes8Q4wvOVZyBvO9_xjmrydaQWI/w400-h144/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj9__yUlpQtF-XvFoFq7xCeofbiyJ-BNOyxEeQaWpCaVcNRFt-0jO4l-8G6Bjq9Tu2gAxjZE6NLgNpIpwIiCG90l4pRtIjeB-X0IJ2Ut-JbMsUUoZ-QFes8Q4wvOVZyBvO9_xjmrydaQWI/>)

  
  


  
  


  


  


  


We grab the '[cri-containerd-cni'](<https://storage.googleapis.com/cri-containerd-release/cri-containerd-cni-1.3.4.linux-amd64.tar.gz>) package from <https://storage.googleapis.com/cri-containerd-release> and unpack it to the root directory:

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgE-pY4NXnHUcxrR0YnRaogdKR-b-BEYokMsfCL2z2GQDNoAELz3JhLEW57uhUjoWQX3jxzbuM5IkBoDdcFXNIyTcTA5ReAxB_8B2n7dkMRdupxKz7Dz6XmZ5tQcVjvitbo-vemuxQ-2PM/w640-h32/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgE-pY4NXnHUcxrR0YnRaogdKR-b-BEYokMsfCL2z2GQDNoAELz3JhLEW57uhUjoWQX3jxzbuM5IkBoDdcFXNIyTcTA5ReAxB_8B2n7dkMRdupxKz7Dz6XmZ5tQcVjvitbo-vemuxQ-2PM/>)

  
  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgHYoSSIrZbwjh6DyE6LCeBW5DpmLSBmENESg0sOUw7ISFAs91oZS4mAYh576RH7cVrAyP9JYdYuVE_rjRw1uKDSpskteA-nN3gi1FyITXJPSa2RMKDBCm82tDf4P0ngqT0ytY6utBhCTw/w640-h15/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgHYoSSIrZbwjh6DyE6LCeBW5DpmLSBmENESg0sOUw7ISFAs91oZS4mAYh576RH7cVrAyP9JYdYuVE_rjRw1uKDSpskteA-nN3gi1FyITXJPSa2RMKDBCm82tDf4P0ngqT0ytY6utBhCTw/>)

  


  


  


Start containerd:

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjPppApvGn1NQBIZsArDaMwcux6y-UwxyHcjq7zSoSPAoajb7fGLjRvSKX5iSBRLwUbIanIj4h6mjyklN6j_poZbR4jD8HlUuBblLflh6SQaPvLOd-hCis17RPpLL5W0K308FcYam6IYIA/w400-h79/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjPppApvGn1NQBIZsArDaMwcux6y-UwxyHcjq7zSoSPAoajb7fGLjRvSKX5iSBRLwUbIanIj4h6mjyklN6j_poZbR4jD8HlUuBblLflh6SQaPvLOd-hCis17RPpLL5W0K308FcYam6IYIA/>)

  
  


  


  


  


  


Next we follow the usual steps for installing kubernetes components from [kubernetes documentation page](<https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/>):

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhS-Uqlsp45sxPj6v5G_8e5XoRo191f3P27mhBth-1OGTrOIGl14Bctyof70H-cBf1sz1sombJOxLG2MXovAiGZS1gEjDGssXX8JL9n9ijzZkHT_AsALj7nQDbUvhw7kpq6WDZmctixImc/w400-h55/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhS-Uqlsp45sxPj6v5G_8e5XoRo191f3P27mhBth-1OGTrOIGl14Bctyof70H-cBf1sz1sombJOxLG2MXovAiGZS1gEjDGssXX8JL9n9ijzZkHT_AsALj7nQDbUvhw7kpq6WDZmctixImc/>)

  
  


  


  


  


lsmod | grep br\_netfilter

  


modprobe br\_netfilter

  


sysctl -w net.ipv4.ip\_forward=1

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiGuHP0Nhmqlg7ZiUQEsax2iW7mbq6LNLrMLYHiMn9UfWzUqJ1sagloStx0mb_ABX3zmfK1CwjNqIOZiyRApJ0rBZnvD2lLaLbIL-IS6rJeo0v-n1K-aMUF_fJ2dUM232BJFc6gBqgLLMw/)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiGuHP0Nhmqlg7ZiUQEsax2iW7mbq6LNLrMLYHiMn9UfWzUqJ1sagloStx0mb_ABX3zmfK1CwjNqIOZiyRApJ0rBZnvD2lLaLbIL-IS6rJeo0v-n1K-aMUF_fJ2dUM232BJFc6gBqgLLMw/>)

  
  


  


  


  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjOHiczifl9C5Ikca77RDavztlvKxZcYIeHrICI91hTPm81ypKS4RkYoGELcQ5CA2joyvVjZf55ifNC1okRM3er1imPJ8DB1f1z56Zmw071eb3AtyX_Fq6UUSt_xeAtaIXta4qzTMoV8jA/w640-h146/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjOHiczifl9C5Ikca77RDavztlvKxZcYIeHrICI91hTPm81ypKS4RkYoGELcQ5CA2joyvVjZf55ifNC1okRM3er1imPJ8DB1f1z56Zmw071eb3AtyX_Fq6UUSt_xeAtaIXta4qzTMoV8jA/>)

  
  


  


  


  


  


  


  


  


[Create Systemd Drop-In for Containerd](<https://github.com/containerd/cri/blob/release/1.4/docs/installation.md>): `/etc/systemd/system/kubelet.service.d/0-containerd.conf`:
    
    
    [Service]                                                 
    Environment="KUBELET_EXTRA_ARGS=--container-runtime=remote --runtime-request-timeout=15m --container-runtime-endpoint=unix:///run/containerd/containerd.sock"

  


After  this we run[ kubeadm init ](<https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init/>)

  


  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjcGrxP4njA1d-c7fevwJzAgw-1YNjr2GiD62HRXCzCqGpPXr9qtl58RB00R0lCTEgYDM9SooYl89rbogq8ImysWGMISYa-xGb8_Grsz6-kQlcY_ycdbojrWGcYpOXtnPUdZlfxU5S6AeE/w640-h101/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjcGrxP4njA1d-c7fevwJzAgw-1YNjr2GiD62HRXCzCqGpPXr9qtl58RB00R0lCTEgYDM9SooYl89rbogq8ImysWGMISYa-xGb8_Grsz6-kQlcY_ycdbojrWGcYpOXtnPUdZlfxU5S6AeE/>)

  
  


  


  


  


  


  


We see that our control plane is up:

  


  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgVO2tKWJRjQ-kzJpo04VUQLu261ecmEWNSvZaLZ0CVFk9CVRdgjr22b2RIJEMk72wHmsOC0EfsPPAAUp5m8TAxy6fw7Y9zmr98MWuJW8gc3i6hSdyI_Fqm52dcEVph15raILiLijn2v6c/w640-h262/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgVO2tKWJRjQ-kzJpo04VUQLu261ecmEWNSvZaLZ0CVFk9CVRdgjr22b2RIJEMk72wHmsOC0EfsPPAAUp5m8TAxy6fw7Y9zmr98MWuJW8gc3i6hSdyI_Fqm52dcEVph15raILiLijn2v6c/>)

  
  


  


  


  


  


  


  


  


  


  


  


  


  


Deploy[ weave cni plugin](<https://www.weave.works/docs/net/latest/kubernetes/kube-addon/>):
    
    
    kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhr6Ffk4xoTWYTID6nhHvXlIjAdFDH14n-fFo39GPmaiQgI8-FYanvVXxpibyRL5vmECyU5kHYmShXIIxBgHDdlMHtt6cJtRSIkrdZXDvMUKA4RIwM7sqcRJuVEKOFToeb9UJKhEgnh4eg/w640-h140/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhr6Ffk4xoTWYTID6nhHvXlIjAdFDH14n-fFo39GPmaiQgI8-FYanvVXxpibyRL5vmECyU5kHYmShXIIxBgHDdlMHtt6cJtRSIkrdZXDvMUKA4RIwM7sqcRJuVEKOFToeb9UJKhEgnh4eg/>)

  
  


  


  


  


  


  


  


  


[Untaint](<https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/>) the master node so that we can deploy a pod on it since we have only one node:

  


kubectl taint node k8s-containerd node-role.kubernetes.io/master:NoSchedule-

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh7LOsitEiMLMtSG1JYem3vW1vurUYZ2Ggp3VBP8E6wrTOnIFaFBbh1zfsjsUPPfedLQ0qqNbEtnwXUtxWQmoyEoSCDKNGsb5ueVe3gjLlyI2QY1lZz5eUdwSktttR5_aOcUzIVZgntHzY/w640-h148/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh7LOsitEiMLMtSG1JYem3vW1vurUYZ2Ggp3VBP8E6wrTOnIFaFBbh1zfsjsUPPfedLQ0qqNbEtnwXUtxWQmoyEoSCDKNGsb5ueVe3gjLlyI2QY1lZz5eUdwSktttR5_aOcUzIVZgntHzY/>)

  
  


  


  


  


  


  


  


  


There you go - migrate to containerd from docker for kubernetes.
