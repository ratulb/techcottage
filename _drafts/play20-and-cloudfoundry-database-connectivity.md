---
layout: post
title: "Play2.0 and cloudfoundry database connectivity"
date: 2012-05-18 06:31:00.001+00:00
tags: []
---

Right at the outset, an honest confession - I am no good at shell script. When I tried to deploy my play2.0 - scala application in cloudfoundry - and connect to the provisioned database service - I faced the difficult task of parsing a JSON string\(cloudfoundry provides details of the services in JSON format\) - extract the database credentials - and set them as environment variables so that when I start my play2.0 netty server - the server can read those environment variables and connect to the database. Following snippet shows a sample database related info that cloudfoundry provides as environment variable:  
  
**\{"postgresql-9.0":\[\{"name":"database","label":"postgresql-9.0","plan":"free","tags":\["postgresql","postgresql-9.0","relational"\],"credentials":\{"name":"d59efd73d7a0d458da6b156ea0ae67b6b","host":"172.30.48.124","hostname":"172.30.48.124","port":5432,"user":"u6dacee22b17d4c9d8e4aa832b7cc2947","username":"u6dacee22b17d4c9d8e4aa832b7cc2947","password":"p9cfd7252af8d4af4beb3815b38cf184e"\}\}\]\}  
 **  
  
So, I had basically two options before me:  
  
a\) I write a shell script to parse the JSON script and extract  the relevant data  
b\) Or I change the netty server start-up code itself - so that when launched - it reads the VCAP\_SERVICES JSON string - takes out the relevant database credentials and connects to the provisioned database instance.  
  
So, I started on my venture to find a nice little shell script parses a JSON string and dishes out the database settings when asked for. Googling gave me some scripts - but they were not very helpful - either they were too lousy or too specific to some other tasks - and I dared not to modify them for the obvious reason as I have mentioned at the outset - I am not good at shell script.  
  
  
So, I decided to follow my second option. I got the play2.0 source code from github repository - modified the netty server scala code - so that it calls some other piece of scala code\(which does the JSON parsing - and sets the database specific details nice and cool\) - and does what it normally does. Following snippet shows the piece of code that does JSON parsing and environment variable setting.  
  
package play.core.server  
  
import play.api.libs.json.\_  
import play.api.libs.json.Json.\_  
import play.api.libs.json.Json  
import java.util.\{Map=>JMap\}  
import java.util.\_  
import java.lang.reflect.Field  
  
object VCAPJsonParser \{  
  def init\_env\(\): Unit  = \{  
    val vcap\_services = System.getenv\("VCAP\_SERVICES"\)  
    if\(vcap\_services == null || "" == vcap\_services\)\{  
      println\("vcap\_services env value is not set\!"\)  
      \(\)  
    \}else \{  
    println\("The VCAP\_SERVICES json  : "+ vcap\_services\)  
    val services: JsValue = Json.parse\(vcap\_services\)  
    val postgresql = services \ "postgresql-9.0"  
    val credentials = postgresql\(0\) \ "credentials"  
    println\("The credentials json : "+ credentials\)  
    val dbname = \(credentials \ "name"\).as\[String\]  
    val hostname = \(credentials \ "hostname"\).as\[String\]  
    val user = \(credentials \ "user"\).as\[String\]  
    val password = \(credentials \ "password"\).as\[String\]  
    val port = \(credentials \ "port"\).as\[Int\]  
    val database = "jdbc:postgresql://" +hostname+":"+port+"/" +dbname  
    println\("database url : "+ database + ", user : "+ user+ ", password : "+ password\)  
    val envObj = System.getenv\(\)  
    val env = envObj.asInstanceOf\[JMap\[String,String\]\]  
    var newEnv: JMap\[String,String\] = new java.util.HashMap\(\)  
    newEnv.putAll\(env\)  
    newEnv.put\("postgres\_database",database\)  
    newEnv.put\("postgres\_dbuser",user\)  
    newEnv.put\("postgres\_password",password\)  
    setEnv\(newEnv\)  
    println\("Env set: "+ System.getenv\(\)\)  
    println\("\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*"\)  
    println\("Database url : "+ System.getenv\("postgres\_database"\)+", user : "+ System.getenv\("postgres\_dbuser"\)+", password : "+ System.getenv\("postgres\_password"\)\)  
    \(\)  
   \}  
  \}  
    
  def main\(args: Array\[String\]\): Unit = \{  
    init\_env  
  \}  
  
  
  def setEnv\(newenv: JMap\[String,String\]\): Unit = \{  
    try \{  
    val processEnvironmentClass : Class\[\_\] = Class.forName\("java.lang.ProcessEnvironment"\)  
        val theEnvironmentField : Field  = processEnvironmentClass.getDeclaredField\("theEnvironment"\)  
        theEnvironmentField.setAccessible\(true\)      
    val env: JMap\[String,String\] = \(theEnvironmentField.get\(null\)\).asInstanceOf\[JMap\[String,String\]\]  
        env.putAll\(newenv\)  
        val theCaseInsensitiveEnvironmentField: Field = processEnvironmentClass.getDeclaredField\("theCaseInsensitiveEnvironment"\)  
        theCaseInsensitiveEnvironmentField.setAccessible\(true\)  
        val cienv: JMap\[String,String\] =\(theCaseInsensitiveEnvironmentField.get\(null\)\).asInstanceOf\[JMap\[String,String\]\]  
    cienv.putAll\(newenv\)  
    \}catch \{  
     case e1: NoSuchFieldException => try \{  
      
       val classes: Array\[Class\[\_\]\] = \(classOf\[Collections\]\).getDeclaredClasses\(\)      
       val env: JMap\[String,String\] = System.getenv\(\)  
       for\(cl <\- classes\)\{  
     if\("java.util.Collections$UnmodifiableMap".equals\(cl.getName\(\)\)\) \{  
       val field: Field = cl.getDeclaredField\("m"\)  
       field.setAccessible\(true\)  
           val obj = field.get\(env\)  
           val map = obj.asInstanceOf\[JMap\[String,String\]\]  
       map.clear\(\)  
           map.putAll\(newenv\)  
     \}  
       \}   
     \}catch \{  
       case e11: Exception => e11.printStackTrace\(System.err\)  
     \}  
     case e2: Exception => e2.printStackTrace\(System.err\)  
    \}  
  
  \}  
    
\}  
  
You can put this piece of code in the proper directory - call it from the main method of the "NettyServer.scala" and build the play framework from the source - and then push your application to cloudfoundry - and it will faithfully connect to your database instance.  
  
I have done this - this is how my application\(ooki.cloudfoundry.com\) was running till I wrote this post.  
  
I was not very happy to modify the netty server code just to read database specific details. Hence I rolled up my sleeves - And decided to give the shell script   
approach another go. Following is shell script - that I ended up writing. Needless to say - there must be more efficient way of writing it - but it does the job currently. You are welcome to modify and make it more generic.  
  
  
\#\!/usr/bin/env bash  
  
function processVCAP\_SERVICE\_JSON\_and\_setDBenv\(\)\{  
  echo "\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*"  
  echo "$VCAP\_SERVICES"  
  echo "\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*"  
  db\_settings=\(\)  
  counter=0  
  found="n"  
  IFS=',' read -ra SERVICE\_SETTINGS <<< "$VCAP\_SERVICES"  
  length="$\{\#SERVICE\_SETTINGS\[@\]\}"  
  for \(\(i=0; i<$\{length\}; i++ \)\);  
   do  
    curr\_item=$\{SERVICE\_SETTINGS\[$i\]\}  
    curr\_item="$\(echo $\{curr\_item\} | tr -d '\"'\)"  
    echo "position : "+ "$i" + "and item is : "+ "$curr\_item"  
    \#Take care of password:pbd0e3f367a6c4a36bcc48a3c763a929e\}\}\]\} <\--  
    if \[\[ "$curr\_item" == password\* \]\]; then  
       pwd\_len="$\{\#curr\_item\}"  
       pwd\_len=$pwd\_len-4  
       curr\_item="$\{curr\_item:0:$pwd\_len\}"   
    fi   
  
    if \[\[ "$found" = "y" \]\] || \[\[ "$curr\_item" == credentials\* \]\]; then  
     if \[ "$found" = "n" \]; then  
       \#get rid of 'credentials:\{' part  
       len="$\{\#curr\_item\}"  
       len=$len-1   
       db\_settings\[counter\]="$\{curr\_item:13:$len\}"  
     else  
       db\_settings\[counter\]="$\{curr\_item\}"  
     fi  
     counter=$counter+1  
     found="y"  
     echo counter is : "\{$counter\}"  
    fi  
   done  
     
   echo "ratul your db settings are : "     
   echo "$\{\#db\_settings\}"  
   echo "\!\!\!\!\!\!\!\!\!\!\!\!\!\!\!\!\!\!\!\!\!\!\!\!\!\!\!\!\!\!\!"  
     
   \#prepare the database\_url,database\_user & database\_password and set them in env  
   database\_url=jdbc:postgresql://  
   \#change above in case of MySQL  
   db\_name=  
   host\_name=  
   port\_num=  
   database\_user=  
   database\_password=  
   echo "============================================="  
   for setting in "$\{db\_settings\[@\]\}"  
    do  
      echo \#\#\#\#\#\#\#\#\#\#\#\#\#\#"$\{\#setting\}"      
      set\_len="$\{\#setting\}"  
      set\_len=$set\_len-1;   
      echo "$setting and setting length=$set\_len"  
  
      case "$setting" in  
           name:\*\) db\_name="$\{setting:5:$set\_len\}";  
                  echo "DB name : $db\_name" ;;  
       hostname:\*\) host\_name="$\{setting:9:$set\_len\}";  
          echo "DB host : $host\_name" ;;  
  
       port:\*\) port\_num="$\{setting:5:$set\_len\}";  
          echo "DB port : $port\_num" ;;  
       username:\*\) database\_user="$\{setting:9:$set\_len\}";  
          echo "DB user : $database\_user" ;;  
       password:\*\) database\_password="$\{setting:9:$set\_len\}";  
          echo "DB password : $database\_password" ;;  
      esac  
    done  
  
    database\_url=$database\_url$host\_name:$port\_num/$db\_name  
    export database\_url=$database\_url  
    export database\_password=$database\_password  
    export database\_user=$database\_user  
\}  
processVCAP\_SERVICE\_JSON\_and\_setDBenv  
  
echo "database url : $database\_url"  
  
echo "password : $database\_password"  
  
echo "user : $database\_user"  
  
exec java $JAVA\_OPTS -Dhttp.port=$VCAP\_APP\_PORT -DapplyEvolutions.default=true -cp "\`dirname $0\`/lib/\*" play.core.server.NettyServer \`dirname $0\`  
  
  
  
Be sure to set environment variables accordingly in **application.conf** like so:  
  
db.default.driver=org.postgresql.Driver  
db.default.url=$\{database\_url\}  
db.default.user=$\{database\_user\}  
db.default.password=$\{database\_password\}
