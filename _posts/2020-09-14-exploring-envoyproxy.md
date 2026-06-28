---
layout: post
title: "Exploring envoyproxy"
date: 2020-09-14 22:32:00.006+00:00
tags: [kubernetes, envoy, k8s, istio, envoyproxy]
---

With the adoption of micro-services, we need to tackle hosts of issues associated with remote calls and networking - because what used to be an in-process function call now becomes a RPC call that need to be handled by a service **which needs to be discovered**. Service discovery has its own issues - among others, the most important being able to **discover services that are active**. Once services are discovered - we need to handle **uniform spread of requests** among discovered service instances. **Traffic encryption** becomes another issue that we need to handle once a call goes out over the wire from one micro-service to another.  

Another very obvious requirement in a cluster of micro-services is the need to monitor and trace requests. Without this requirement being taken care, it is difficult to figure out how services are executing on distributed network.

While there still many more issues that we need to take care of in a micro-services' setup - what should be our approach on a high-level to tackle them?

Among others - one approach could be to develop client side libraries - which handle issues of service discovery, load balancing\(retry, timeout, circuit breaking etc\) and others. This was the approach Netflix Eureka/ribbon/zuul stack had proposed. Eureka client acted as a service proxy - eureka server acting as a service registry and ribbon providing client side load balancing and zuul handling request routing.

While the library approach works - there are few things to consider while we embark on the library journey:

\- Business code now get entangled with infrastructure code.

\- We are sticking are head out either as an one language shop or we are undertaking quite a complicated job of developing/maintaining client libraries in multiple programming languages.

Is there an easy way to tackle the issues associated with micro-services? Yes\! That is what out-of-process proxies like **[envoy](<https://www.envoyproxy.io/>)** and **[linkerd](<https://linkerd.io/>)** provide. All ready existing proxies like Nginx and HA-PROXY etc are adding support for capabilities similar to those provided by envoy proxy. We will discuss linkerd in a later post - here we will talk about envoy proxy.

Envoy's website talks of envoy being a edge and service service proxy - this means we can use envoy for north-south as well as east-west traffic. Envoy is written in modern C++ and most of requests handling run concurrently in lock free code. This make envoy very fast. 

Envoy has lot of goodies to offer - it's **out of process architecture** straight away boosts developer productivity. The network and myriad of associated issues go away instantly - letting the developer focus on his business problem. Envoy being out of process - provides a huge advantage - we can develop our services in any language of our choice and necessity. 

As mentioned earlier - envoy provides many load balancing features - automatic request retries, circuit breaking, request timeouts, request shadowing, rate limit etc.

With envoy's traffic routing features, we can easily do **rolling upgrade of services, blue/green and canary deployment** etc.

Envoy provides **wire level  observability of request traffic and native support for distributed tracing.**

Envoy supports **HTTP/1.1, HTTP/2 & gRPC** \- it **transparently switches between HTTP/1.1 and HTTP/2**.

One very important aspect of envoy proxy is that - while envoy can be configured statically - yet it provides**robust APIs for dynamic configuration**. What is more - **envoy can patched and upgraded** without shutting it down via what is called "**Hot-Restart** ". We would configure some of envoy's features in upcoming posts - but before that following concepts about envoy would help.

**Envoy proxy concepts:**

**Downstream:** A downstream host connects to Envoy, sends requests, and receives responses.

**Upstream:** An upstream host receives connections and requests from Envoy and returns responses.

**Listeners:** They are the addresses where envoy process listens for incoming connections. For example,

0.0.0.0:9090. There can multiple listeners in an envoy process.

**Filter chains:** Each listener in an envoy process can be configured with filter chains - where each chain consists of one or more filters. Filter chains are selected based on incoming request and some matching criteria.

**Routes:** Based on matching criteria - requests are delegated to be handled by back-end clusters.

**Clusters:** Named collection of back-ends called endpoints. Requests are load balanced among the cluster endpoints.

**Endpoints:** Endpoints are the delegates which handles requests. They are part of cluster definition.

In the next post - we would install envoy and look at traffic routing. Stay tuned.

*Originally published on [https://rbsomeg.blogspot.com](https://rbsomeg.blogspot.com/2020/09/exploring-envoyproxy.html)*
