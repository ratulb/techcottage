---
layout: post
title: "Algorithms and data structures in rust - mergesort"
date: 2020-08-02 18:13:00.008+00:00
tags: [rust, data structure, merge sort]
---

Bets about[**rust**](<https://www.rust-lang.org/>) are turning out to be right. Initially proposed as system programming language\(read servo - rewrite of firefox browser\) - numerous front end web frameworks are appearing and becoming ubiquitous. Rust has a steep learning curve - but that is a reasonable investment considering the low level power it gives to do system level things at the same time high level abstraction that comes without the price\(zero cost\). Borrow and ownership prevent memory issues, move semantics avoids data races, effort less C binding, avoidance of a runtime are some of the salient features of rust. Its implementation of [**Async & wait**](<https://rust-lang.github.io/async-book/>) is also novel.

  


Its has been quite some time following the developments in rust - have been utilizing rust in one of my projects currently. I am going to be publishing some posts on rust and what better way than implementing algorithms and data structures to start with?

  


Following is an implementation of merge sort algorithm in rust. 

  


Rust allows defining local functions. Which is kind of neat & compact. Below is merge sort algorithm implemented using local functions.   
  
![]({{ site.baseurl }}/assets/images/algorithms-and-data-structures-in-rust-mergesort-1.png)  
  
  
We make use of life times to return the sorted array. There does not seem to be an easy way to create arrays at runtime - the reason being arrays are allocated at the stack.  


  


**Source:  <https://github.com/ratulb/algos_in_rust>**

*Originally published on [https://rbsomeg.blogspot.com](https://rbsomeg.blogspot.com/2020/08/algorithms-and-data-structures-in-rust-mergesort.html)*
