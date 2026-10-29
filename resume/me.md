---
layout: page
title: Resume
permalink: /resume/
---

[Download PDF](/assets/me.pdf)


## RATUL BURAGOHAIN

**System Architect · Distributed Systems · ML Systems**

Bengaluru, India · [ratul75@hotmail.com] 
[GitHub](https://github.com/ratulb) · [LinkedIn](https://www.linkedin.com/in/ratul-b-5747563/) · [Tech Cottage](https://ratulb.github.io/techcottage/)


## Summary

System architect with 24 years of software experience building high-performance, secure distributed systems across payments, healthcare, travel and enterprise software. Led monolith-to-microservices migrations at Visa and for independent clients; consulting on Kubernetes and service-mesh work since 2019. Currently building ML systems from first principles in Mojo: a tensor library and autograd engine, a tokenizer, and a GPT-2 training pipeline.

---

### Experience

#### Independent Consultant & Open-Source Engineer
*09/2019 – Present*

**Consulting: Kubernetes and service mesh**

- Migrated clients' monolithic systems to Kubernetes-based architectures with Istio-based microservices.
- Built CI/CD pipelines, infrastructure automation and monitoring — cutting deployment from days of manual work to a push-button, hours-long process.
- Published the supporting tooling as open source: [k8s-easy-install](https://github.com/ratulb/k8s-easy-install) (one-script multi-master cluster setup), [kube-etcd-switch](https://github.com/ratulb/kube-etcd-switch) (stacked/external etcd switching, backup, restore and disaster recovery), [k8s-cluster-from-source](https://github.com/ratulb/k8s-cluster-from-source) (cluster build without kubeadm).

**Open source: ML systems in Mojo (2024 – present)**

- [Tenmo](https://github.com/ratulb/tenmo): tensor library and neural-network framework with autograd, SIMD-vectorized kernels, GPU support and extensive test suites.
- [mbpe](https://github.com/ratulb/mbpe): trainable BPE tokenizer with Python bindings, byte-for-byte compatible with tiktoken and benchmarked against tiktoken and tiktoken-rs.
- [chargpt](https://github.com/ratulb/chargpt) and GPT-2 pipeline: character-level GPT with KV-cached decoding verified against an uncached reference, and a GPT-2 training pipeline, both built on Tenmo and mbpe.
- Writing [*Tokens to Transformers in Mojo*](https://ratulb.github.io/tokens-to-transformers/), a code-first book building GPT-2 from bytes to training loop (chapters 1–6 complete).

### Principal Member of Technical Staff, athenahealth
*06/2018 – 04/2019*

- Rolled out the API gateway: routing, protocol and payload translation, authentication, rate limiting, logging and monitoring.
- Built AWS infrastructure (CloudFront, Route 53, Global Accelerator, ECS, S3, ElastiCache, ELB) with CloudFormation and CloudWatch-driven auto-scaling via SNS and Lambda.
- Owned disaster recovery and high-availability design and implementation.

### Senior Staff Software Engineer, Visa
*08/2015 – 06/2018*

- Re-engineered the monolithic payment processing system into Docker-based microservices.
- Introduced Consul for service discovery and Vault for credentials and key rotation.
- Secured data at rest, in transit and in memory. Deployed a Redis cluster as the online store for in-flight transactions.

### Development Lead, Cheapesto
*10/2014 – 08/2015*

- Built a travel platform integrating Amadeus, Mystifly, Carsolize and Priceline for flights, hotels, cars, packages, cruises and tours.

### Senior Member of Technical Staff, Actiance
*04/2013 – 07/2014*

- Built a multi-tenant big-data ingestion and archival system with near real-time search on Kafka, Storm, ZooKeeper, Elasticsearch, Cassandra and MongoDB, with authentication and authorization.

### Development Lead, Sabre
*03/2010 – 12/2012*

- Re-engineered the legacy back end for performance using memcached and Akka actors.
- Integrated Travelocity's international shopping path: flights, hotels, cars, cruises and rewards.

### Architect, i2 Technologies
*07/2002 – 10/2008*

- Built an enterprise inventory management system and a middleware integration stack (RMI, JMS/MQSeries, webMethods, web services, SSO).
- Led development of the Attribute-Based Order Capture engine, a rules-based order capture system, and an agile business process platform. Contributed to a transportation management system.


## Skills

- **Languages:** Mojo, Rust, Java, Scala, Python, JavaScript, Shell
- **ML systems:** tensor and autograd design, SIMD and GPU kernels, BPE tokenization, transformer training
- **Distributed systems:** Kubernetes, Istio, Envoy, gRPC, etcd, Kafka, Storm, Akka, Consul, Vault
- **Cloud:** AWS, GCP, Azure, OpenStack, Docker, CI/CD, observability
- **Data:** PostgreSQL, MySQL, Oracle, SQL Server, Cassandra, MongoDB, CockroachDB, Redis, Memcached, Hazelcast, Aerospike, Elasticsearch
- **Blockchain:** Solana (Rust), Ethereum (Solidity)


## Writing & Open Source

- [Tech Cottage](https://ratulb.github.io/techcottage/) - technical writing on Mojo, Rust, Kubernetes, gRPC and Scala.
- [Arrows](https://crates.io/crates/arrows) - a distributed actor framework for Rust, providing location-transparent actors across a cluster.
- [Solana](https://ratulb.github.io/solana_program_and_rust_client/index.html) - an on-chain program paired with a Rust off-chain client.
- [Rust Programming](https://ratulb.github.io/rust_programming) — Programming problems in rust


## Education & Certifications

**BE, Electrical & Electronics Engineering**, National Institute of Technology, Tiruchirappalli, 1997

Coursera/IBM: Advanced Machine Learning and Signal Processing; Fundamentals of Scalable Data Science (2020). Coursera: Machine Learning; Functional Programming Principles in Scala (2012).


## Earlier Career

**Field Engineer**, Halliburton (oilfield operations), 1997 – 2002
