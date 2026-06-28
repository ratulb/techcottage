---
layout: post
title: "Nested virtualbox VM inside google compute engine"
date: 2020-09-23 22:51:00.008+00:00
tags: [compute engine, virtualbox, GCP, nested VM, guest VM inside compute engine]
---

Though guest VM inside google compute engine raises concerns about performance, there are situations where they prove useful. In this post I am going to discuss how we can install a ubuntu guest VM on google compute engine instance.

There are few caveats though - we can install a KVM compatible hypervisor only on Linux VM instances running only on**  Haswell or newer processors**. Also, Haswell based processors **are not available in all GCP regions** \- they are available in certain regions in US\(US central\) and Europe.

Windows compute engines do not support nested virtualization.

We need to create compute engines supporting nested virtualization off of disk images tagged with a specific license, namely:

**"--licenses https://compute.googleapis.com/compute/v1/projects/vm-options/global/licenses/enable-vmx";**

With these restrictions in mind, lets proceed with the following steps to launch a compute engine which will host a ubuntu guest VM on top of oracle virtualbox.

**1\) Log into GCP console and launch the cloud shell:**

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiISX3flYS58LZp9uFS0ldGbB-qH83KIY3mMvs7VMjPqVF7a2bD5RZQqq7Eu8YaI3PY1qrxNyerGkriMhkeU43WeSCueGfVbFxjNLkH-QqWKzgH88igs4CG0XPwEd4b1h9L9OqK1QCVG04/w631-h219/cloud-shell1.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiISX3flYS58LZp9uFS0ldGbB-qH83KIY3mMvs7VMjPqVF7a2bD5RZQqq7Eu8YaI3PY1qrxNyerGkriMhkeU43WeSCueGfVbFxjNLkH-QqWKzgH88igs4CG0XPwEd4b1h9L9OqK1QCVG04/s726/cloud-shell1.png>)

**  2\) set project:**

**   gcloud config set project \[PROJECT\]**

  


**3\)  We would create disk image from ubuntu family tagging it with above license as shown:**

**$ gcloud compute disks create virtualization-tagged-disk --image-project ubuntu-os-cloud --image-family ubuntu-1804-lts --zone us-central1-a --licenses "https://www.googleapis.com/compute/v1/projects/vm-options/global/licenses/enable-vmx"**

It might ask for authorization - click on **"Authorize".**

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjuhyphenhyphenKoja_ccDnFE0kMfXrKDW9KSDR8dNufmt9leGI_9M2qt0b7NZ22yL9SC6l_vvjkILYQ3dmqAl2Unf0EwS6eFXSX34U5TSwPfDd_NnheC-lP8lPit6hIyYggwIENx8yFis1iAcgrucU/w613-h138/cloud-shell-disk-iamge.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjuhyphenhyphenKoja_ccDnFE0kMfXrKDW9KSDR8dNufmt9leGI_9M2qt0b7NZ22yL9SC6l_vvjkILYQ3dmqAl2Unf0EwS6eFXSX34U5TSwPfDd_NnheC-lP8lPit6hIyYggwIENx8yFis1iAcgrucU/s844/cloud-shell-disk-iamge.png>)

  


This will create a disk image called "virtualization-tagged-disk". We can launch a ubuntu VM based off of this image and install oracle virtualbox on that compute engine instance and then launch a guest VM inside virtualbox.

  


Note: We would have to launch the instance in a **GCP region where  Haswell processors \(N1 family\) **are available.

  


**4\) Select the disk image as shown:**

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgdm4eMd1fv4vkmxj_tIheQaVbqhcp83ggxEZVhxryc10cQoZrrHFb39gQYBl2-7jOsgQ4dZagXTQGzC-ntUwVUbUbz33lLnhXGdRTl2h3qQawwnHPxBjzpngRbfZHHLQNGPFL1MEHCU5Q/w657-h220/select-disk.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgdm4eMd1fv4vkmxj_tIheQaVbqhcp83ggxEZVhxryc10cQoZrrHFb39gQYBl2-7jOsgQ4dZagXTQGzC-ntUwVUbUbz33lLnhXGdRTl2h3qQawwnHPxBjzpngRbfZHHLQNGPFL1MEHCU5Q/s905/select-disk.png>)

  


  


**5\) Launch an instance selecting the disk and appropriate region and processor:**

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj4L2ynOfQ39mlNjDhOqNfXZwkVjVxh1tHAZojcokL1Twz2dlocIdvWk8WBMg1LbT7YhL_jt0iOCGhlTpVguceBdxPtyXIqJ9gk-Yf6zKWyrQUmAU5eK15jIOBg60vlnWgx9BRNuQ0TEtg/w584-h305/n1-central-us.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj4L2ynOfQ39mlNjDhOqNfXZwkVjVxh1tHAZojcokL1Twz2dlocIdvWk8WBMg1LbT7YhL_jt0iOCGhlTpVguceBdxPtyXIqJ9gk-Yf6zKWyrQUmAU5eK15jIOBg60vlnWgx9BRNuQ0TEtg/s831/n1-central-us.png>)

  


Once the compute engine instance is started - we can ssh into it and setup a desktop environment so that we can access it via RDP.

**Setting up RDP and install oracle virtualbox:**

**Setup RDP on the compute engine:**

**1\) Once inside the compute engine instance - we can uncomment following series of command to setup the RDP server environment and change the password for root user and then exit and connect back to the box via a remove RDP client:**

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjgmVQ0K7LaP9WzlOe5FTFGwZvgJ5oJ1nw_J5cYPLjb5CiR5F9TvH9mqim3Rf6iGvEa6LEFUFK6uWhEdNk4yj8K_16rsOYdfFJcWu-dQnKQSzrenVjGX5_HUJD8kGMPzAb5TmF4fZEkBsk/w544-h165/rdp.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjgmVQ0K7LaP9WzlOe5FTFGwZvgJ5oJ1nw_J5cYPLjb5CiR5F9TvH9mqim3Rf6iGvEa6LEFUFK6uWhEdNk4yj8K_16rsOYdfFJcWu-dQnKQSzrenVjGX5_HUJD8kGMPzAb5TmF4fZEkBsk/s464/rdp.png>)

  


**2\) Connect to the box via a remote desktop client client install virtualbox.**

  


**curl -O https://download.virtualbox.org/virtualbox/6.1.14/virtualbox-6.1\_6.1.14-140239~Ubuntu~bionic\_amd64.deb**

**apt install ./virtualbox-6.1\_6.1.14-140239~Ubuntu~bionic\_amd64.deb**

  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg9tWapQxE16QJ4AMKanbv9NZHgjaXzK3cMQJwUoNarluy4piBFJUlEalGvVvRQ-HeNcLPK-jmYdp1ovn_vDzJnsP78UIZNKSG31H7k_R1codhme2cNjOJbiX0kVuaCsAfoB7YRwRFUWdQ/w716-h192/virtualbox.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg9tWapQxE16QJ4AMKanbv9NZHgjaXzK3cMQJwUoNarluy4piBFJUlEalGvVvRQ-HeNcLPK-jmYdp1ovn_vDzJnsP78UIZNKSG31H7k_R1codhme2cNjOJbiX0kVuaCsAfoB7YRwRFUWdQ/s899/virtualbox.png>)

  


  


  


**Note:** For better view install xfce4 goodies:

apt-get install xfce4 xfce4-goodies

*Originally published on [https://rbsomeg.blogspot.com](https://rbsomeg.blogspot.com/2020/09/nested-virtualbox-vm-inside-google-compute-engine.html)*
