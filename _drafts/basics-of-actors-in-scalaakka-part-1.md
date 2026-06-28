---
layout: post
title: "Basics of actors in scala/Akka part 1"
date: 2012-12-21 12:11:00+00:00
tags: []
---

Starting with Scala 2.10.0 - scala actors will be replaced by akka actors.Since we are already using scala actors in production - the need arose to get familiarised with akka in general and specially actors . I had already, out of curiosity, tried to develop some knowledge about akka - but  was never quite able to do so - mainly because a\) the documentation looks so voluminous - it scared me away each time. b\) There are so many things - actors, typed actors, dataflow concurrency, software transaction memory, microkernel and what not. The lack of a step by step fast track guide - showing some basic stuff acted against me being able to give akka a shot in my previous attempts. So, if you are in the same situation, then this post is for you. I will show the basic stuff - that, I hope, will help you explore the rest. I am assuming prior familiarity with scala actors here.

  
  
I am using scala-2.10.0-RC5 - the lib already contains akka actors library.  
  
Note: akka actors library shipped with scala does not support remote actors. How to do that I will in a subsequent post.  
  


An scala actor needs to extend \`akka.actor.Actor\` trait overiding the \`receive\` message\(unlike scala there is not \`react\` method\). Importing \`akka.actor.\_\` package is enough for creating and testing actors locally. Also, actors are grouped into named \`ActorSystem\` which provide thread pool, dead letter box, message dispatcher etc etc - the infrastrucre. Also, there can be more than one actor system in the same VM. Following shows how to create an actor system, defining an instantiating an actor and sending a message to the actor:

  
  


scala> import akka.actor.\_

import akka.actor.\_

  


scala> val actorSystem = ActorSystem\("actorsystem"\)

system: akka.actor.ActorSystem = akka://actorsystem

  


scala> class MyActor extends Actor \{

     |   def receive = \{

     |     case x => println\("Received : "+ x\)

     |   \}

     | \}

defined class MyActor

  


scala> val myActor = actorSystem.actorOf\(Props\[MyActor\]\)

myActor: akka.actor.ActorRef = Actor\[akka://actorsystem/user/$a\]

  


scala> myActor \! "Hi"

Received : Hi

  
In the above \`Props\` is a factory for actor configuration.  
  
  


Actors should be named. They are automatically started when created, have pre-start and pre-shutdown hooks. Above example shows how to create an actor from the system. If actors are to be created from within an actor, then we should use 'context.actorOf' instead. Following shows an actor with non-default constructor which creates actors in response to messages.

  


scala> val system = ActorSystem\("system"\)  
system: akka.actor.ActorSystem = akka://system 

  


scala> :paste

// Entering paste mode \(ctrl-D to finish\)

  


case object Create

case object Kill

case class Msg\(s: String\)

  


class MyActor\(arg: String\) extends Actor \{

  override def preStart = println\("Some arbitrary arg : "+ arg\)

  var myChild: Option\[ActorRef\] = None 

  


  def receive = \{

    case Msg\(s\) => \(myChild getOrElse create\) \! s; println\("Passed on"\)

    case Create => myChild getOrElse create; println\("create returned"\)

    case Kill => myChild match \{

       case Some\(a\) => context.stop\(a\)

         myChild = None

         println\("killed"\)

       case \_ => //Do nothing

    \}

  \}

 

  def create: ActorRef = \{

   val child = context.actorOf\(Props\(new Actor \{

      def receive = \{

        case x => println\("Got a msg from my parent : "+ x\)

      \}

    \}\), name="childactor"\)

   

    myChild = Some\(child\)

    child

  \} 

 

  override def postStop = println\("Some code to execute after stopping..."\)

  


\}

  


  


// Exiting paste mode, now interpreting.

  


defined module Create

defined module Kill

defined class Msg

defined class MyActor

  


  


scala> val parentActor = system.actorOf\(Props\(new MyActor\("Some constructor args"\)\), name="parent"\)

parentActor: akka.actor.ActorRef = Actor\[akka://system/user/parent\]

  


scala> Some arbitrary arg : Some constructor args

  


scala> parentActor \! Create

  


scala> create returned

  


scala> parentActor \! Msg\("Testing"\)

  


scala> Passed on

Got a msg from my parent : Testing

  


  


scala> parentActor \! Kill

  


scala> killed

  


  


scala> parentActor \! Create

  


  


scala> create returned

  


  


scala> parentActor \! Msg\("Testing again"\)

  


scala> Passed on

Got a msg from my parent : Testing again

  


  


scala> parentActor \! PoisonPill

  


scala> Some code to execute after stopping...

  


  


scala> system.shutdown

  
  
_**parentActor: akka.actor.ActorRef = Actor\[akka://system/user/parent\]**_  
  
  


Actors have parent-child relationship and parental supervision. An actor is a parent of each actor it creates. In the above line \`user\` is parent of actor named \`parent\`. \`user\` is a one of the system actors that gets created when an actor system is created. User created actors and their children are created underneath \`user\` system actor. Actors can looked up using \`actorFor\` on actor system or contenxt. The difference between actorOf and actorFor is that in the later case we get a reference to an ActorRef\(If it exists otherwise reference to the dead letter system actor where all messages will passed on in case of no-existent actors\) - but actor itself is not created.

  


scala> val system = ActorSystem\("system"\)  
system: akka.actor.ActorSystem = akka://system 

  


scala> val p = system.actorFor\("/user/parent"\)

p: akka.actor.ActorRef = Actor\[akka://system/user/parent\]

  


scala> parentActor \! Msg\("Testing"\)

  


scala> Passed on

Got a msg from my parent : Testing

  


  


scala> p \! Msg\("Testing again"\)

  


scala> Passed on

Got a msg from my parent : Testing again

  


scala> val nonExistentActor = system.actorFor\("/user/xyz"\)

nonExistentActor: akka.actor.ActorRef = Actor\[akka://system/user/xyz\]

  


scala> nonExistentActor \! "This msg will be passed on to dead letter actor"

  


  


The preferred way of stopping an actor is by calling \`context.stop\(self\)\` in response to some shutdown message. Shown below are some other ways of stopping an actor. One things to notice is that in case of kill message the post shutdown hook is not getting called. 

  


scala> val a1 = system.actorOf\(Props\(new MyActor\("cons args"\)\), name="a1"\) //actor names should be unique in an actor system

Some arbitrary arg : cons args

a1: akka.actor.ActorRef = Actor\[akka://system/user/a1\]

  


scala> val a2 = system.actorOf\(Props\(new MyActor\("cons args"\)\), name="a2"\) 

Some arbitrary arg : cons args

a2: akka.actor.ActorRef = Actor\[akka://system/user/a2\]

  


scala> val a3 = system.actorOf\(Props\(new MyActor\("cons args"\)\), name="a3"\) 

Some arbitrary arg : cons args

a3: akka.actor.ActorRef = Actor\[akka://system/user/a3\]

  


scala> a1 \! Msg\("Msg to a1"\)

  


scala> Passed on

Got a msg from my parent : Msg to a1

  


  


scala> a2 \! Msg\("Msg to a2"\)

  


scala> Passed on

Got a msg from my parent : Msg to a2

  


  


scala> a3 \! Msg\("Msg to a3"\)

  


scala> Passed on

Got a msg from my parent : Msg to a3

  


  


scala> system.stop\(a1\)

  


scala> Some code to execute after stopping...

  


  


scala> a2 \! Kill

  


scala> killed

  


  


scala> a3 \! PoisonPill

  


scala> Some code to execute after stopping...

  


We talked about parental supervision above. When an actor fails, it's parent can decide what action should be taken. The parent actor can escalate it or may handle failure. It may kill all the children and restart them or kill only the failed actor and restart it. Other options are - let the failed actor continue\(resume\) handling messages or the parent may decide to stop the failed actor permanently.

  
To supervise a child, an actor needs to override the \`supervisorStrategy\` member of the actor.   
  
Following shows an actor that kills failed child and restarts it in response.  
  


import akka.actor.OneForOneStrategy

import scala.concurrent.duration.\_

import akka.actor.SupervisorStrategy.\_

  


  


scala> :paste

// Entering paste mode \(ctrl-D to finish\)

  


class MyActor extends Actor \{

  override def supervisorStrategy = OneForOneStrategy\(maxNrOfRetries = 2, withinTimeRange = 1 minute\) \{

        case e: Exception => Restart//Exception to restart directive

  \}

  var child = context.actorOf\(Props\[Child\]\)

  


  def receive = \{

    case s: String => child \! s

    case a: ActorRef => child = sender

    case e: Exception => child \! e

  \}

\}

  


class Child extends Actor \{

  def receive = \{

    case s: String => println\("Parent msg : "+ s\)

    case e: Exception => throw new Exception\("throwing up"\)

    case \_ => println\("Don't know what it is\!"\)

  \}

  


  override def postRestart\(reason: Throwable\):Unit = \{

    println\("I am being restarted :" + reason.getMessage\)

    context.parent \! self

  \}

\}

  


  


// Exiting paste mode, now interpreting.

  


defined class MyActor

defined class Child

  


scala> val parent = system.actorOf\(Props\[MyActor\]\)

parent: akka.actor.ActorRef = Actor\[akka://system/user/$a\]

  


scala> parent \! "Testing"

  


scala> Parent msg : Testing

  


  


scala> parent \! new Exception

  


scala> \[ERROR\] \[12/21/2012 16:58:27.328\] \[system-akka.actor.default-dispatcher-2\] \[akka://system/user/$a/$a\] throwing up

java.lang.Exception: throwing up

....................

  


I am being restarted :throwing up

  


  


scala> parent \! "Testing after restart"

  


scala> Parent msg : Testing after restart

  
Conclusion: I have just touched upon basics stuff. In the next post I will briefly write about hot swapping of actor behaviour, routing and remote actors.
