---
layout: post
title: "Migrate kubernetes embedded etcd to external etcd - easy back and forth switch"
date: 2021-07-01 01:18:00.001+00:00
tags: [kubernetes, external etcd, stacked etcd, embedded etcd]
---

**Gist:  **

**Create a multi-master kubernetes cluster from the comfort of a shell menu without tweaking a thing. Front the apiservers with load balancer of your choice - namely h****[aproxy](<http://www.haproxy.org/>)/[nginx](<https://www.nginx.com/>)/[envoy](<https://www.envoyproxy.io/>). Do hassle free back and forth switch between embedded etcd and external etcd.  
**

In this post, we discuss **[kube-etcd-switch](<https://github.com/ratulb/kube-etcd-switch>)**  \- which is not quite a tool rather a **bunch of scripts behind a shell menu that help us to do all the above in a hassle free manner.**

Curious? Read on then. But you have been **forewarned** \- it might not be your cup of tea.

**Kubernetes treats pods as cattle - they are discarded if not healthy**. No effort is wasted on reviving unhealthy pods - instead new ones are created to replace the bad ones. 

Kubernetes is conjoined with etcd by an umbilical chord. Etcd stores kubernetes schema and state. Kubernetes is useless without etcd\(as things stand currently\). At times - it can be quite a challenge to bring up a kubernetes cluster if etcd starts throwing its tantrums. For example - you want to remove an etcd node because it has gone bad - but etcd cluster would not let you do that because the node is not up yet. Quite a vexatious situation to be in.

So, what do we do in such a chicken and egg situation? Well, follow the same kubernetes philosophy - we discard the etcd cluster \( Not the cluster itself - we have compunction - mechanical sympathy. Instead we scrap etcd \) - create a new one to replace the faulty one. We treat everything as cattle - no pets. If a piece of software is not crunching data and providing information - it is not serving its cause - it's redundant.  Below we provide a glimpse of how we do that. **That is, of course, as long as we have data at our hands, a backup or a snapshot - we care for data - it's valuable - amorphous gold.**

First up, we need a kubernetes cluster -**kube-etcd-switch** can interface with any existing kubernetes cluster - but here we show how to setup a k8s cluster as well because we don't have one at hand currently and we need a cluster for the show to go on.

**Requirements:** A set of machines \(**Debian buster/ubuntu16/18/20 flavor**\) with root **SSH access**.

Here, we use four machines - one for load balancer\(lb\), two for kubernetes master nodes\(m-1,m-2\), one worker\(w-1\) node.

**We run everything from the load balancer node.**

1\) Clone the following GitHub repository - go inside and launch the 'cluster.sh' script.

git clone [https://github.com/ratulb/kube-etcd-switch](<https://github.com/ratulb/kube-etcd-switch> "https://github.com/ratulb/kube-etcd-switch")

cd kube-etcd-switch/

./cluster.sh 

We would be presented with menu which has quite a few choices as shown

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjq2nI6_l5JTQZPRRdZOd92Dxmpbpq-DMj-2Yger0ckjZV-ary1pGSrSMagO6e1T286SfmVpRqW9FaO9fa_nZwBhfEAPXyCx4OvsltjNdBoSVLvj2xjoo2O-eQ7SyT4vNYzNbi_Jm2cMP4/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjq2nI6_l5JTQZPRRdZOd92Dxmpbpq-DMj-2Yger0ckjZV-ary1pGSrSMagO6e1T286SfmVpRqW9FaO9fa_nZwBhfEAPXyCx4OvsltjNdBoSVLvj2xjoo2O-eQ7SyT4vNYzNbi_Jm2cMP4/>)

  


We need a cluster - hence we make the appropriate selection and get on with the cluster setup process driven by the menu choices.

2\) We enter the cluster details such as**load balancer, master nodes and worker node**. Following few snaps capture the steps.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhIh86hY5RQtTm5Z7LwUbA17Da7t7aJ2ha2zX6eO0CUo30xR8vSH7XJUGtfuwmEZeEMygP6bpb0oizUwMUgAkEfQxk6H30edmSsoME0AoA-ABwhJGEVwv5vG1hLn-rk18kbXdllzOb2njs/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhIh86hY5RQtTm5Z7LwUbA17Da7t7aJ2ha2zX6eO0CUo30xR8vSH7XJUGtfuwmEZeEMygP6bpb0oizUwMUgAkEfQxk6H30edmSsoME0AoA-ABwhJGEVwv5vG1hLn-rk18kbXdllzOb2njs/>)

  


3\)  Load balancer details

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiFnppRJTBYp0vNWgIs_I_XyMYEAZlj-x3b6NFdg3YLmXdNPlUYrzjgwL6pMo3YbiX7Xo1fAqy1f2-adzyhdUZ8Gyqgk82DGau7KBcx6YrpaqNJ1vkiosOJ6hlOuwLKnCGgud6rzYdxKig/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiFnppRJTBYp0vNWgIs_I_XyMYEAZlj-x3b6NFdg3YLmXdNPlUYrzjgwL6pMo3YbiX7Xo1fAqy1f2-adzyhdUZ8Gyqgk82DGau7KBcx6YrpaqNJ1vkiosOJ6hlOuwLKnCGgud6rzYdxKig/>)

  


4\) Next we enter master and worker details:

  


![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhQA1jFMkX71BH384yNCvbSR2Z2HdzeuFTF1dv6SSbk7r44O8H3sJ4eje7K5jh7Z2v1b5ohy8xcHP8V-UC1MiOmj4ImiZHwzMN2bHkt_d26HyTXAPdQCHip3FbmdA1I7Aik-iF9I-lAgkQ/s16000/image.png)

  


  


  


  


  


  


  


  


  


5\) Next we select option to launch the cluster creation process. This would provide us with **running kubernetes cluster in a matter of minutes with weave CNI plugin and demo nginx pod deployed.**

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgR3yjo9B4LTLF2sQP8vYdd2IsCyMXSc9O2UHB76nBcUnQ6gkoejjklPPf60EfWRvcIZZ2wxLY-fxzzWgS_wJXEC2AJeZyYBQbiLvsNUe9ER0wnAczLaULAnQTmoUWMUM4qvKXUbuJ-gew/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgR3yjo9B4LTLF2sQP8vYdd2IsCyMXSc9O2UHB76nBcUnQ6gkoejjklPPf60EfWRvcIZZ2wxLY-fxzzWgS_wJXEC2AJeZyYBQbiLvsNUe9ER0wnAczLaULAnQTmoUWMUM4qvKXUbuJ-gew/>)

  


6\) Following snap shows the end result of cluster creation:

  


![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhp0QiZN0JThq4zzdwBDiUriHwKenoJ2RYBfziM6tZfLpn7K4I0zf-9ibv0_goiQYbndG9buZkWmVPPi0SStLiVjufhXcldGILE_AVO643exDxoa7jDoLaOb0thmkWuicC-4xU5_k9drHs/s16000/image.png)

  


7\) Next is the initialization step. For **k8s-etcd-switch** to work with any cluster it needs to be initialized first. We need to provide the master IP \(or name\) of any one of the masters for this.  **k8s-etcd-switch will query the cluster - gather information such a master members, copy ETCD CA cert and setup kubectl,****[cloudflare CFSSL](<https://github.com/cloudflare>)****and other required binaries to perform its duties**. The initialization process can be repeated - it is idempotent. **The initialization process is minimum once per servers' certificate rotation.**

Following snaps show the initialization choices.

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgqCVl4q3jt4zUTYLiyr61i2-YTSf51LiwyB90GLh0RfkUsJozYncsi4ZPBHX-VwjEBt9-YvpDpNClAUYNIcTk2kv_hTkHqPzDfqbUkHtAj08O-VeuxvVpuoz9iqdfwCdvojpE_MKvsXLs/s16000/image.png)

  


Note: Above we see that master endpoints are already detected - that is because k8s setup has already configured kube config. It will not be so for a pre-existing cluster. Initialization would be needed in either case.

8\) Post initialization k8s-etcd-switch show cluster's system pod states. Now it can talk to the kubernetes cluster.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhQ9U2Rt3R2vMKzIcGHU-AdHudjjCklvvSe0fMGgHGGOz-wt9tE1N824NEHFPyfFo9tDlN8Uf1TazcArJX1GJXC0wSIhI8LIt8EamK75vQ2jKXCYEm79QxVNzGDSMDopHpcCqgzZJq21iI/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhQ9U2Rt3R2vMKzIcGHU-AdHudjjCklvvSe0fMGgHGGOz-wt9tE1N824NEHFPyfFo9tDlN8Uf1TazcArJX1GJXC0wSIhI8LIt8EamK75vQ2jKXCYEm79QxVNzGDSMDopHpcCqgzZJq21iI/>)

  


9\) **At this point - our cluster is pristine**\( it would not be so for an existing cluster \). Lets go ahead and **deploy a demo nginx pod in the default namespace**. We select console and deploy the pod.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjvqKaP1Sbdq37dimq30ii28JxI6mob7Kp0TRU8A8AzMOv4R655qpJGOh01oEunFkEg9a1iLdukTQRLPnFTS_gQtX4z0N0KWMcuuIEyJxMWY6iGRNeNx0CGIDnT8YhUrKDgoro6Bgv8vPk/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjvqKaP1Sbdq37dimq30ii28JxI6mob7Kp0TRU8A8AzMOv4R655qpJGOh01oEunFkEg9a1iLdukTQRLPnFTS_gQtX4z0N0KWMcuuIEyJxMWY6iGRNeNx0CGIDnT8YhUrKDgoro6Bgv8vPk/>)

  


10\) We see that our **nginx pod is running along with demo pods** that were deployed during the cluster creation process. 

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgVYD91gBSbyC49LdojFs5VyoyOoKb_NyGY8KlsAPv-UkIHLKMhw-pZncdeLAGd0YEj1BGQoix-JAmdopSZYzys1qBKp2rnYbWmIjtlnsoh6SLcdz7RLu2Kw7clroEtr9GpOpWPodLfobg/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgVYD91gBSbyC49LdojFs5VyoyOoKb_NyGY8KlsAPv-UkIHLKMhw-pZncdeLAGd0YEj1BGQoix-JAmdopSZYzys1qBKp2rnYbWmIjtlnsoh6SLcdz7RLu2Kw7clroEtr9GpOpWPodLfobg/>)

  
  


  
  


  


  


  


11\) We want to survive cluster failure whether kubernetes or etcd. Kubernetes is done deal - we have shown it above. Etcd would be without it's salt - if it did not have data. But now it has data - whole kubernetes cluster's schema and state - that also contains our freshly deployed nginx pod's information. We need that data - **we want to preserve it to survive cluster failure - computation calamity.  **

We exit out of the console - that would take us back to where we were before. We select snapshot view from the menu - we would be presented with an option to choose between embedded and external etcd cluster. Presently, we do not have an external cluster. We choose embedded and take a snapshot. 

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg8-mE2U0t7_bexdeZzaWZxBOVcfAE2opr1fRo8nDIVOF-ODIpusEghO9DwqEuw_49YBGwXYKBYmWZZghm7ADUpF3GRC7Yj4anjKXJN3_uRtCkVT5AsTEuMoJM9Zge5O3GjpnAds0D_Dh4/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg8-mE2U0t7_bexdeZzaWZxBOVcfAE2opr1fRo8nDIVOF-ODIpusEghO9DwqEuw_49YBGwXYKBYmWZZghm7ADUpF3GRC7Yj4anjKXJN3_uRtCkVT5AsTEuMoJM9Zge5O3GjpnAds0D_Dh4/>)

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjq6vruG22wvZMFsxLLmXOUClH6imeeGKo0L5K2NJtN9fcBLjU78FCpjGqRiq9Y9mR2wIySSJk7ruGVCnzHr6wl8WKyVQaqHfCjIX3I9tYRJJRSvbRzFhoo9C_BVWeqq3s8hJ6-W6Ju1jI/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjq6vruG22wvZMFsxLLmXOUClH6imeeGKo0L5K2NJtN9fcBLjU78FCpjGqRiq9Y9mR2wIySSJk7ruGVCnzHr6wl8WKyVQaqHfCjIX3I9tYRJJRSvbRzFhoo9C_BVWeqq3s8hJ6-W6Ju1jI/>)

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiCaSCFbRdfIE8fkgUJa0AnH7-zf8610Uv_thW4F7tw4-omwWMx9LRue1Jlj72nDKxLWgI9EUccrS5OgfRmgEmF_ikqM9yAR7hetkwZeOuIwLwthPvgw3BIUHNzoh4GQsFg9libTsRE3is/s16000/image.png)

12\)**With a snapshot in hand - we are safe. We heave a sigh of relief. We are ready to combat disaster. We want put our conviction to test - we want to simulate a catastrophe and survive through it - making ourselves doubly reassured that we can infuse life back into etcd in the event of a cluster failure.**

We head back to the main menu - choose console \(this can be done from a usual terminal - there is no difference  \- but we want to be in the context of the menu - hence choose console anyway\)  and the run the script shown in the following snap. This script will wreak havoc on our cluster - it will wipe out our cluster and render it useless. All data would be  expunged. **Only the static pods would be running meekly with utter indifference.** **Had it been a production cluster - business would have come to a grinding halt. Some may be updating their resumes - freshening up on the tricks of the trade. Yet some others may be philosophizing what life is all about - consequences may be far and beyond one's imagination - all due to a failed etcd cluster\(pun intended 😜\).  **

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjyjEjjO085Nt9ET6TBa81TchRd11IpR44JyF5CMCsh2e-LnbOsR9-LBcB1kv4kbbBdB2fof4oIye8jGsnJJDHp-vpvRxyqTXFcZgTMavikvf3_ZBAHSdYW9T4GLluxX5Z0jN5ViIrO70M/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjyjEjjO085Nt9ET6TBa81TchRd11IpR44JyF5CMCsh2e-LnbOsR9-LBcB1kv4kbbBdB2fof4oIye8jGsnJJDHp-vpvRxyqTXFcZgTMavikvf3_ZBAHSdYW9T4GLluxX5Z0jN5ViIrO70M/>)

  
  


  


  


  


  


  


  


  


  


  


  


  


  


  


**Cluster demolition in progress:**

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh-1FO731on5LGT-Aj7-0mXi7Xc5W5b1CTylaOreDBE4dg9XGRpzmWXN-vWGeMkUHdbYT6z9aAm93hDa46K43T2W2tDRjxr-a_3bDBU_iazWnEfUstvm0VcctJU9QhkfIYx38esiCtMLJQ/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh-1FO731on5LGT-Aj7-0mXi7Xc5W5b1CTylaOreDBE4dg9XGRpzmWXN-vWGeMkUHdbYT6z9aAm93hDa46K43T2W2tDRjxr-a_3bDBU_iazWnEfUstvm0VcctJU9QhkfIYx38esiCtMLJQ/>)

  
  


**Total annihilation:**

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhSfsR7Aixj6Gs5X0Ryk5f4EJ5vj2EjmyyRxULsIdhNY3xESfYiZ1pWicUEF6hYn2IxSE_3SNUTIK3uZCUXos8tkpYIKwZsQHMt_0OTpL90G99sjf0gdvx8KnXn_w2OTAYshrfsM22Bop8/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhSfsR7Aixj6Gs5X0Ryk5f4EJ5vj2EjmyyRxULsIdhNY3xESfYiZ1pWicUEF6hYn2IxSE_3SNUTIK3uZCUXos8tkpYIKwZsQHMt_0OTpL90G99sjf0gdvx8KnXn_w2OTAYshrfsM22Bop8/>)

  
  


13\) **Now that our cluster is decimated, we want to bring it back to life using the snapshot that we had taken. We can - and we would restore the snapshot on top of embedded etcd cluster - but first we would launch an external etcd cluster and restore the snapshot on top of it and verify that api servers are responding as expected.  **

  


We exit from the console and go back to main menu and choose 'Manage external etcd'

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhAjnmqafajIQzA33t8uCQTErTFnyqgNCgViMRJ5bYAgcmxk6K_d-c9xyG5g3unKVJPIFBWVOYfpHRSAbyUWC_zwQdF338-Zt_8decsavW8A4opy6oYJnlwuV9sCAOVzKKIzAmPZMWFTYQ/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhAjnmqafajIQzA33t8uCQTErTFnyqgNCgViMRJ5bYAgcmxk6K_d-c9xyG5g3unKVJPIFBWVOYfpHRSAbyUWC_zwQdF338-Zt_8decsavW8A4opy6oYJnlwuV9sCAOVzKKIzAmPZMWFTYQ/>)

  


14\) **We proceed with external etcd cluster setup process.** For this post, we choose to host the cluster on the load balancer and the worker node \( Digression: we can also imagine kubernetes master nodes being part of external etcd cluster. For that to happen - the stacked/embedded etcd would need to bottom out one by one giving external etcd space to be hosted as separate processes  on the master nodes\).

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh0356WuYWkwR4B8HMp01Jb88V_0Nmpjvz8NiASqpVKt8NCfvAbFiWDAvHDbHBxTNAttO3aVqjjjoKQLvmhM4DGHnTh88PNCBSpoNBiLJG5LYss35gUzhoAw3I-HQoAScCUKpBg60UPYR4/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh0356WuYWkwR4B8HMp01Jb88V_0Nmpjvz8NiASqpVKt8NCfvAbFiWDAvHDbHBxTNAttO3aVqjjjoKQLvmhM4DGHnTh88PNCBSpoNBiLJG5LYss35gUzhoAw3I-HQoAScCUKpBg60UPYR4/>)

  


15\) The external etcd cluster is ready with required configurations and binaries but not yet started.**It would be up once we restore the snapshot.**

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgQwtI9gpVOyvpJpGEQU9EDXYxKrxFFIkuWF81DiWvaLS3UTF4kGi0BABBGkioqrsQEn2CzCSR6udY4yNJlnHSYvKq_yTy_tNfnJAVs3BUgZxFLsIZTN1WPf3oStf6PdmQEuPluQXqkzaI/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgQwtI9gpVOyvpJpGEQU9EDXYxKrxFFIkuWF81DiWvaLS3UTF4kGi0BABBGkioqrsQEn2CzCSR6udY4yNJlnHSYvKq_yTy_tNfnJAVs3BUgZxFLsIZTN1WPf3oStf6PdmQEuPluQXqkzaI/>)

  


16\) Lets go ahead and restore the snapshot. Following snaps capture the steps. We go back to snapshot view and select restore option.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjNsF5SJd0jz6rY-7TRCaCzlv9uLhQJoGkKuahao5tqDLPyBxdc_r4qUboIBPD5cfoUeiAoKzrSQgMYi7UnxsuHG5TkW7XaYF4o6EJjKaZSLGYHkJy_zym1_6WEdaeJUAae7ZQ0lRUHqFA/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjNsF5SJd0jz6rY-7TRCaCzlv9uLhQJoGkKuahao5tqDLPyBxdc_r4qUboIBPD5cfoUeiAoKzrSQgMYi7UnxsuHG5TkW7XaYF4o6EJjKaZSLGYHkJy_zym1_6WEdaeJUAae7ZQ0lRUHqFA/>)

  


17\) We choose external etcd as target cluster and select the snapshot that we had saved earlier.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj0Qf6yAIc9474RVUXKinCtdrhGXAwkTNjF1QZ6CP4CjAST7ofJlitf7xS99fMZDbZn2RiF-nheyQh_LZp6oIJspPe_hAJmZSffB7BiSpuZEIDhhCBiKt42uLMoLOM_Gdu9eNebdtErorA/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj0Qf6yAIc9474RVUXKinCtdrhGXAwkTNjF1QZ6CP4CjAST7ofJlitf7xS99fMZDbZn2RiF-nheyQh_LZp6oIJspPe_hAJmZSffB7BiSpuZEIDhhCBiKt42uLMoLOM_Gdu9eNebdtErorA/>)

  


18\) **We see snapshot restoration on external etcd cluster in progress.**

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjy8bp0vsx-xRMwgX7ytJAuOMO6e39AYT1IYl8q328OYSBqhfNdz6MYe6KaimLCV_g5f-IlVLu1lszvFVBRgj2HqHib6utdP1D0eBFbFGKuXXc-6EEsGmNBus1qEAmjeV9Ttt-heKrJod0/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjy8bp0vsx-xRMwgX7ytJAuOMO6e39AYT1IYl8q328OYSBqhfNdz6MYe6KaimLCV_g5f-IlVLu1lszvFVBRgj2HqHib6utdP1D0eBFbFGKuXXc-6EEsGmNBus1qEAmjeV9Ttt-heKrJod0/>)

  


19\) Snapshot restoration on **external etcd cluster is complete** and system pods are up and running in a couple of minutes. 

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjN7-c5_opBA0rzXIXdEB-VGDTjlDCUL8jEZk2Ro88GZeK4b2ZNmL3Alh-XHGwnY8CqPVlZbvmbJo3HVac820BM-37ZCEwlBNzA8qR7D97iY3d8jnPgUw6Ew2T_JMqL-7YgFRYPmXcf67Q/s16000/image.png)

  
  


  


  


  


  


  


  


  


  


  


  


  


20\) **We have survived a disaster without a scratch. That was easy\! Lets go ahead take out an etcd node for repair. Kubernetes cluster should suffer no hiccups.  **

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjL5X7hmFmo4BJxu1g3aRWvYBUpLFXw6nKOhHk9ReIEvUtIW1NdfDsB58M6bW3IcAkhhd2h9ZUjLm6gTHUOQHV_-Rq0ZrHz7_NH_vvglMpFib-6Zrwy-IFYHpHtjdwgMf8Gli75e7gvJAg/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjL5X7hmFmo4BJxu1g3aRWvYBUpLFXw6nKOhHk9ReIEvUtIW1NdfDsB58M6bW3IcAkhhd2h9ZUjLm6gTHUOQHV_-Rq0ZrHz7_NH_vvglMpFib-6Zrwy-IFYHpHtjdwgMf8Gli75e7gvJAg/>)

  
  


  


21\) **There has been no hiccups** for the cluster as we can see from the kube system pods. Embedded etcd cluster is still running but api servers are not pointing at them. They will have nothing in them - because when the disaster struck - they were hollowed out.

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEguznlnGCghAIVirSB6VnXGhFE_hHTuOIS_xYBO2TiG6_TXLR8GCIs-vwW30nlX5XC02CQ_z8TF7Ao-GuFUFAWapAwBHV9VVd-pAYgnLk6Z8zetNkpzcqn7CGhtoaCvhNT1YC8OMcOxkBg/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEguznlnGCghAIVirSB6VnXGhFE_hHTuOIS_xYBO2TiG6_TXLR8GCIs-vwW30nlX5XC02CQ_z8TF7Ao-GuFUFAWapAwBHV9VVd-pAYgnLk6Z8zetNkpzcqn7CGhtoaCvhNT1YC8OMcOxkBg/>)

  
  


22\) **Node repaired. Lets add it back to the cluster again.**

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjt581Yx6KybjC5UhZalficoNth82iwt20gS-zeMozU1EwxuqkZJqx5aSpBGJRfcshY9M-KXeiCnntuk6T1Xf9SBqi0XLAwfLpcMIh-sMy7eOz-bmrSXOgEuauXd7_Pqw9KfaLx4YZ6K_w/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjt581Yx6KybjC5UhZalficoNth82iwt20gS-zeMozU1EwxuqkZJqx5aSpBGJRfcshY9M-KXeiCnntuk6T1Xf9SBqi0XLAwfLpcMIh-sMy7eOz-bmrSXOgEuauXd7_Pqw9KfaLx4YZ6K_w/>)

  
  


  
  


  


  


  


  


  


  


  


  


  


23\) **Repaired node has become a member of the cluster again.**

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh8wgRIU_9OeHPzkUQKxe0Ta8EE-Jzypsv3QXY7DXFA82SH0YIV_hrQfGMAmblVaDUGahdFoZYE7seNTxWqrJ1pLo5ecSPwmYKc5WmYmqSO4c8OXPetpID3-tlKeumnUhgL2Nhh_ZfbmB4/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh8wgRIU_9OeHPzkUQKxe0Ta8EE-Jzypsv3QXY7DXFA82SH0YIV_hrQfGMAmblVaDUGahdFoZYE7seNTxWqrJ1pLo5ecSPwmYKc5WmYmqSO4c8OXPetpID3-tlKeumnUhgL2Nhh_ZfbmB4/>)

  
  


  
  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


24\) Lets bring the embedded etcd cluster back to live. We go back to snapshots view, select embedded cluster as restore target.

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjAs9zmNLn0kV4sL1yTfInLT7bS4u3phsgwtdRaF2oBYJ_-XXFYaGWOA90HbT4yBNkXSERVKmSxufGT048KpWF7TLkRPlyv2flJQT2X1eZ0xVYhCNa2PlHlx_32Ech5q-bDDlHqIjVn-H0/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjAs9zmNLn0kV4sL1yTfInLT7bS4u3phsgwtdRaF2oBYJ_-XXFYaGWOA90HbT4yBNkXSERVKmSxufGT048KpWF7TLkRPlyv2flJQT2X1eZ0xVYhCNa2PlHlx_32Ech5q-bDDlHqIjVn-H0/>)

  
  


  
  


  


  


  


  


  


  


  


  


  


  


  


25\) We see that **our embedded cluster is back - and system pods are back too.**

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgUjmMAg1zvNQqhbxs42oknBKVX2WvTe2nxa2ZASo51V6LiXa-O2T02i4FtVEYh6P0s2Nc514Cn13AXsu3IGEeuXgbaqbO18gzdHht29is8-A_MJRHOXNB_IwDHN6i8QP2zCuV9HUyBMBk/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgUjmMAg1zvNQqhbxs42oknBKVX2WvTe2nxa2ZASo51V6LiXa-O2T02i4FtVEYh6P0s2Nc514Cn13AXsu3IGEeuXgbaqbO18gzdHht29is8-A_MJRHOXNB_IwDHN6i8QP2zCuV9HUyBMBk/>)

  
  


  
  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


  


26\) Our nginx pod should be back on the default namespace. Lets check that.

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjG9-LIj8Wx0oLMjRTvDj9EPyErMrD3fpMCMpgbk0yUQYW93SAgxWeTv9QlysP8mxVLZ8glmFOVIzWAMJFCSHUYSN2IeqFDJ2S1nkB7Lal-etkGOjeOE0d2KE9h9L91yQkCGmwB14thKx4/s16000/image.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjG9-LIj8Wx0oLMjRTvDj9EPyErMrD3fpMCMpgbk0yUQYW93SAgxWeTv9QlysP8mxVLZ8glmFOVIzWAMJFCSHUYSN2IeqFDJ2S1nkB7Lal-etkGOjeOE0d2KE9h9L91yQkCGmwB14thKx4/>)

  
  


  


This **effortless switch** between two environments using snapshots opens the door for lot of use cases - disaster recovery, cluster replication, fail over, rapid development and testing, preview releases to just name a few.

  


What about the situation - where we have just restored a snapshot but would like to **go back to the previous state we were in**? Well, we would definitely take a backup snapshot before migration - and use that as fallback option. But in reality - snapshot always takes us to a new state - it creates new data directories, new configurations - its not exactly the same setup as before.

  


**But we want to go back to the exact setup - we were in. Can we do that**? Of course we can. We would need o manually alter settings and configurations. That would involve rounds of testing and verification. That is going to be error prone and not hassle free. Well, **freedom from hassle is what k8s-kube-switch strives for.**

  


**As it turns out, these scripts can help us to go back to not only the previous state, but any previous state.** As said, when we are restoring a snapshot, we are creating new restore paths and configurations and moving on to them - whether it is embedded or external etcd. **We are leaving behind a trail of data directories and configurations. What it does is - any time we restore a snapshot, it looks at current settings and data directories across nodes and backs them all up in a single archive and saves it**\(Where? Currently underneath a directory called **kube\_vault** \- in the node where k8s-kube-switch runs. These archives can be easily be pushed to a safe storage and duplicated to prevent data loss\).

  


We have not talked about states so far. **States is the the mechanism that helps us to go back to any last good state. But it has challenges of its own. We are good if cluster topology remains same**. We can just spread out the archived state across the nodes and resume etcd and kubernetes api servers. But what if nodes leave or new nodes are added to the etcd cluster? **As we know - etcd does not like it if a node does not leave the cluster in good terms - it will not bury that hatchet otherwise. And talk of adding a node  surreptitiously to the cluster - you have to dance a new dance to calm etcds' tantrums. States is a topic for another post, another day.**

  


![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhkeUV_oJlLLl6m-NYkps51jSTJxA-Q0An7ZCJlCVuLpWvMPp17Na0DazPinZCeBkSeU9niktIDwrrGudO5C1RC518mHLh07M5H5ajLLqBq3rfkfx_avly5BaA8QPAZl66TE1Pz8T6Z1Wg/s16000/image.png)

  


**Conclusion:  **

  


**We have covered a lot. We started with a fresh cluster setup, taken a snapshot, brought it to its knees, created an external etcd cluster, restored a snapshot on it - brought it to life, taken a node out of the cluster, added it back - and   finally switched back the kubernetes cluster to embedded etcd**. We have also touched upon states.

  


Behind all this are a bunch of shell scripts. We can see what they are doing because we are close to the metal. They enable experimentation - We can choose the console option - tweak/improve/cookie cut the scripts to suit our needs - exit the console - refresh the view and see the effects. 

  


Happy experimentation - if you wish.

  


Source: <https://github.com/ratulb/kube-etcd-switch/blob/main/cluster.sh>

*Originally published on [https://rbsomeg.blogspot.com](https://rbsomeg.blogspot.com/2021/07/migrate-kubernetes-embedded-etcd-to-external-etcd-easy-back-and-forth-switch.html)*
