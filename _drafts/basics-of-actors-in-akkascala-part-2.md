---
layout: post
title: "Basics of Actors in akka/scala part 2"
date: 2012-12-24 09:34:00+00:00
tags: []
---

**Hot swap of akka's actors behaviour**  
  
Akka actors' receive method accepts a partial function from Any to Unit\(i.e. PartialFunction\[Any, Unit\]\) and this function can be dynamically changed at runtime. Shown below is a simple example of that:  
  


scala> class MyActor extends Actor \{

     |   def receive = \{

     |     case s: String => println\("Current behaviour : "+ s\)

     |     case pf: PartialFunction\[Any, Unit\] => context.become\(pf\)

     |   \}

     | \}

  


  


scala> val pf:PartialFunction\[Any, Unit\] = \{

     |   case s => println\("Behaving differently : "+ s\)

     | \} 

pf: PartialFunction\[Any,Unit\] = <function1>

  


  


  


scala> val system =ActorSystem\("system"\)

system: akka.actor.ActorSystem = akka://system

  


scala> val ma = system.actorOf\(Props\[MyActor\]\)

ma: akka.actor.ActorRef = Actor\[akka://system/user/$a\]

  


scala> ma \! "Testing"

Current behaviour : Testing

  


scala> ma \! pf

  


scala> ma \! "Testing again"

Behaving differently : Testing again

  


Complementing \`become\`, the context also provides an \`unbecome\` which reverts the actor's behavior to the previous one in the hotswap stack.

  
**Router Actor**  
  


A router is just an actor that routes incoming messages to other actors. Akka has a default set of routers for various use cases. Shown below is a router which routes messages to routees in a round robin fashion.

  


scala> class Routee extends Actor \{

     |   def receive = \{

     |     case x => println\(self.path + " : received : "+ x\)

     |   \}

     | \} 

defined class Routee

  


scala> val routee1 = system.actorOf\(Props\[Routee\],name="routee1"\)

routee1: akka.actor.ActorRef = Actor\[akka://system/user/routee1\]

  


scala> val routee3 = system.actorOf\(Props\[Routee\],name="route3"\)

routee3: akka.actor.ActorRef = Actor\[akka://system/user/route3\]

  


scala> val routee2 = system.actorOf\(Props\[Routee\],name="route2"\)

routee2: akka.actor.ActorRef = Actor\[akka://system/user/route2\]

  


scala> import akka.routing.RoundRobinRouter

import akka.routing.RoundRobinRouter

  


scala> val routees = Vector\[ActorRef\]\(routee1, routee2, routee3\)

routees: scala.collection.immutable.Vector\[akka.actor.ActorRef\] = Vector\(Actor\[akka://system/user/routee1\], Actor\[akka://system/user/route2\], Actor\[akka://system/user/route3\]\)

  


scala> val router = system.actorOf\(Props\(\).withRouter\(RoundRobinRouter\(routees = routees\)\)\)

router: akka.actor.ActorRef = Actor\[akka://system/user/$b\]

  


scala> router \! "testing"

  


scala> akka://system/user/routee1 : received : testing

  


  


scala> router \! "testing"

akka://system/user/route2 : received : testing

  


scala> router \! "testing"

akka://system/user/route3 : received : testing

  
  
**Remote actors:**  
  


As mentioned in the previous post, akka actors shipped with scala does not support remoting by default. We need to add addtional jars from the akka distribution. Following are the jars that need to be in the class path:

  


  * akka-remote\_2.10.0-RC5-2.1.0-RC6.jar
  * netty-3.5.8.Final.jar
  * protobuf-java-2.4.1.jar

  


The first step is to create a conf file called \`application.conf\` with following content:

  


 akka \{

   actor \{

     provider = "akka.remote.RemoteActorRefProvider"

   \}

   remote \{

     transport = "akka.remote.netty.NettyRemoteTransport"

     netty \{

       hostname = "127.0.0.1"

       port = 2552

     \}

   \}

 \}

  


This file should be available in the classpath. We launch  two scala consoles, from two terminals, making a copy of the \`application.conf\` and changing port number to 2553 in one of them. 

  
  


class RemoteActor extends Actor \{

 def receive = \{

   case msg => println\("Received : "+ msg\)

               sender \! "Got : "+ msg

 \}

\}

  


usr@ubuntu:~/akka/remoting$ scala -cp ./:$AKKA\_LIB/akka-remote\_2.10.0-RC5-2.1.0-RC6.jar:$AKKA\_LIB/netty-3.5.8.Final.jar:$AKKA\_LIB/protobuf-java-2.4.1.jar

Welcome to Scala version 2.10.0-RC5 \(Java HotSpot\(TM\) Server VM, Java 1.7.0\).

Type in expressions to have them evaluated.

Type :help for more information.

  


scala> import akka.actor.\_

import akka.actor.\_

  


scala> class RemoteActor extends Actor \{

     |  def receive = \{

     |    case msg => println\("Received : "+ msg\)

     |                sender \! "Got : "+ msg

     |  \}

     | \}

defined class RemoteActor

  


scala> val remoteSystem = ActorSystem\("remotesystem"\)

remoteSystem: akka.actor.ActorSystem = akka://remotesystem

  


  


scala> val remoteActor = remoteSystem.actorOf\(Props\[RemoteActor\],name="remoteactor"\)

remoteActor: akka.actor.ActorRef = Actor\[akka://remotesystem/user/remoteactor\]

  


scala> remoteActor \! "local msg"

Received : local msg

  


We send a message the actor locally - it receives the message and prints it but reply does not get printed because the sender\(i.e. REPL\) is not an actor - so the reply goes to the dead letter actor.

  


Now we go to the second scala console create an actor and look up the actor created before and send a message to it.

  


scala> class MyActor extends Actor \{

     |    def receive = \{

     |      case x: String => println\("Received : "+ x\)

     |      case \(a: ActorRef, x: String\) => a \! x

     |    \}

     | \}

defined class MyActor

  


scala> val system = ActorSystem\("system"\)

system: akka.actor.ActorSystem = akka://system

  


val ma = system.actorOf\(Props\[MyActor\],name="myactor"\)  
ma: akka.actor.ActorRef = Actor\[akka://system/user/myactor\]  
  


  


scala> val remoteActor = system.actorFor\("akka://remotesystem@127.0.0.1:2553/user/remoteactor"\)

remoteActor: akka.actor.ActorRef = Actor\[akka://remotesystem@127.0.0.1:2553/user/remoteactor\]

  


scala> ma \! \(remoteActor, "testing"\)

  


scala> \[INFO\] \[12/24/2012 14:31:21.155\] \[system-akka.actor.default-dispatcher-5\] \[NettyRemoteTransport\(akka://system@127.0.0.1:2552\)\] RemoteClientStarted@akka://remotesystem@127.0.0.1:2553

Received : Got : testing

  
  
**On the remote actor side we see:**  
  


scala> \[INFO\] \[12/24/2012 14:29:43.906\] \[remotesystem-15\] \[NettyRemoteTransport\(akka://remotesystem@127.0.0.1:2553\)\] RemoteClientStarted@akka://system@127.0.0.1:2552

Received : testing

  


**Conclusion:** In these two parts posts we explored basics of scala/akka actors. Hopefully, anyone looking for where to begin about akka actors may have got some footing to explore the rest of akka.
