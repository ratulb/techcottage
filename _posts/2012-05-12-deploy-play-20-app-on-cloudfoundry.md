---
layout: post
title: "Deploy play 2.0 app on cloudfoundry"
date: 2012-05-12 11:47:00.001+00:00
tags: []
excerpt: "How to deploy a Play 2.0 application on CloudFoundry using the vmc command-line tool."
---

For last few days I was trying to find a to deploy my play 2.0 application. I have already deployed my app at heroku\(http://ooki.herokuapp.com/\). But heroku offers very limited resources for free account \(max slug size can not exceed 100MB and only 5MB of shared database space. So you have to work within these constraints and it becomes difficult to play around. In fact, to reduce my slug size I had to use a custom build pack from github. Also, if your application is not accessed for a long - heroku idles out your app - next time you access your app - it takes a long time for the response to come back. So you need to setup some kind ping program to keep hitting your app at regular interval say, every 10 minutes.  
  
With cloundfoundry these problems are not there - cloudfoundry free resources are quite good enough\(2GB RAM, 2GB disk space\) so that you can concentrate on what you are doing instead of thinking about resource constraint.  
  
Prerequisite:  
  
Before you can deploy your app in cloudfoundry.com - you need to open an account with cloudfoundry.com. After registering it takes a day or two to get your account activated. You also have to have either the vmc command line tool or sts\(eclipse plugin\) installed on your system - visit the http://docs.cloudfoundry.com/getting-started.html link and follow the instructions there.  
r new application is ready.App  
Once you have setup the pre-requisites and got your user name and password from cloudfoundry.com - you are all set to deploy your app on cloudfoundry.com Paas.  
  
I am going to use the vmc command line tool to deploy a newly created play 2.0 application on cloudfoundry.  
  
Follow the steps below to deploy your app.  
  
1\. Launch command prompt.  
  
2\. Type in -> play new myPlayApp  
  
ratul@ubuntu:~$ play new myPlayApp  
       \_            \_   
 \_ \_\_ | | \_\_ \_ \_  \_| |  
| '\_ \| |/ \_' | || |\_|  
|  \_\_/|\_|\\\_\_\_\_|\\\_\_ \(\_\)  
|\_|            |\_\_/   
               
play\! 2.0.1, http://www.playframework.org  
  
The new application will be created in /home/ratul/myPlayApp  
  
What is the application name?   
> myPlayApp  
  
Which template do you want to use for this new application?   
  
  1 - Create a simple Scala application  
  2 - Create a simple Java application  
  3 - Create an empty project  
  
> 1  
  
OK, application myPlayApp is created.  
  
Have fun\!  
  
3\. Opne the newly created myPlayApp/app/controllers/Application.scala file in a text editor.  
  
Change defintion of the index method like so:  
  
 def index = Action \{  
    val port = System.getenv\("VCAP\_APP\_PORT"\)  
    val host = System.getenv\("VCAP\_APP\_HOST"\)  
    println\("App port : "+ port+" and host: "+ host\)  
    Ok\(views.html.index\("Your new application is ready."+ "App port : "+ port+" and host: "+ host\)\)  
  \}  
  
  Note: VCAP\_APP\_PORT & VCAP\_APP\_HOST are port name host names cloudfoundry assigns when it runs your app.  
  
4\. Save the Application.scala.  
  
5\. Open the myPlayApp/app/views/index.scala.html in a text editor and change the line that reads @play20.welcome\(message\) to @message and save it.  
  
6\. On the command, cd myPlayApp -> ratul@ubuntu:~$ cd myPlayApp/  
  
7\. launch the play promt by tying 'play'.  
  
ratul@ubuntu:~/myPlayApp$ play  
\[info\] Loading project definition from /home/ratul/myPlayApp/project  
\[info\] Set current project to myPlayApp \(in build file:/home/ratul/myPlayApp/\)  
       \_            \_   
 \_ \_\_ | | \_\_ \_ \_  \_| |  
| '\_ \| |/ \_' | || |\_|  
|  \_\_/|\_|\\\_\_\_\_|\\\_\_ \(\_\)  
|\_|            |\_\_/   
               
play\! 2.0.1, http://www.playframework.org  
  
> Type "help play" or "license" for more information.  
> Type "exit" or use Ctrl+D to leave this console.  
  
8\. Next we will bundle the application. So type 'dist' on the play prompt.  
  
\[myPlayApp\] $ dist  
\[info\] Updating \{file:/home/ratul/myPlayApp/\}myPlayApp...  
\[info\] Done updating.                                                                    
\[info\] Compiling 5 Scala sources and 1 Java source to /home/ratul/myPlayApp/target/scala-2.9.1/classes...  
\[info\] Packaging /home/ratul/myPlayApp/target/scala-2.9.1/myPlayApp\_2.9.1-1.0-SNAPSHOT.jar ...  
\[info\] Done packaging.  
  
Your application is ready in /home/ratul/myPlayApp/dist/myPlayApp-1.0-SNAPSHOT.zip  
  
\[success\] Total time: 12 s, completed 12 May, 2012 2:56:34 PM  
  
9\. We want to push the application contents as folder structure and not as zip so that we want to be able to push deltas later on. Hence open the folder myPlayApp/dist in your explorer and extract the contents inside 'myPlayApp-1.0-SNAPSHOT.zip' in the same folder.  
  
10\. Delete the myPlayApp-1.0-SNAPSHOT.zip. Go inside the myPlayApp-1.0-SNAPSHOT folder and delete the README and start files as well - we do not need them.  
  
11\. Now we are ready to push our content to cloudfoundry. Let's logr new application is ready.Appin first.  
  
12\. On the command prompt come out from the play promt by typing 'exit'.  
  
13\. cd dist/myPlayApp-1.0-SNAPSHOT/  
  
14\. Type 'vmc login' on the command prompt.  
  
ratul@ubuntu:~/myPlayApp/dist/myPlayApp-1.0-SNAPSHOT$ vmc login  
Attempting login to \[http://api.cloudfoundry.com\]  
  
Email: ratul75@hotmail.com  
Password: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  
Successfully logged into \[http://api.cloudfoundry.com\]  
  
15\. On the prompt type : vmc target api.cloudfoundry.com  
  
ratul@ubuntu:~/myPlayApp/dist/myPlayApp-1.0-SNAPSHOT$ vmc target api.cloudfoundry.com  
Successfully targeted to \[http://api.cloudfoundry.com\]  
  
16\. When prompted by vmc, answer with y or n as shown below.  
  
ratul@ubuntu:~/myPlayApp/dist/myPlayApp-1.0-SNAPSHOT$ vmc push  
Would you like to deploy from the current directory? \[Yn\]: y  
Application Name: myPlayApp  
Detected a Standalone Application, is this correct? \[Yn\]: y  
1: java  
2: node  
3: node06  
4: ruby18  
5: ruby19  
Select Runtime \[java\]: 1  
Selected java  
Start Command: java $JAVA\_OPTS -Dhttp.port=$VCAP\_APP\_PORT -cp "\`dirname $0\`/lib/\*" play.core.server.NettyServer \`dirname $0\`  
Application Deployed URL \[None\]: myPlayApp.$\{target-base\}      
Memory reservation \(128M, 256M, 512M, 1G, 2G\) \[512M\]: 256M  
How many instances? \[1\]: 1  
Create services to bind to 'myPlayApp'? \[yN\]: n  
Would you like to save this configuration? \[yN\]: y  
Manifest written to manifest.yml.  
Creating Application: OK  
Uploading Application:  
  Checking for available resources: OK  
  Processing resources: OK  
  Packing application: OK  
  Uploading \(80K\): OK     
Push Status: OK  
Staging Application 'myPlayApp': OK                                                    
Starting Application 'myPlayApp': OK        
  
ratul@ubuntu:~/myPlayApp/dist/myPlayApp-1.0-SNAPSHOT$  
  
17\. In your browser you can now open your application - type in myPlayApp.cloudfoundry.com - and we are done\!  
  
18\. The broswer will show something like :  
  
Your new application is ready.App port : 61897 and host: 172.30.50.24

*Originally published on [https://rbsomeg.blogspot.com](https://rbsomeg.blogspot.com/2012/05/deploy-play-20-app-on-cloudfoundry.html)*
