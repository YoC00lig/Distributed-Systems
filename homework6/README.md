<h1>💛 System for the Orthopedic Center</h1>
<p>We are managing an orthopedic department in a hospital with three types of users: Doctors, Technicians, and Administrators. Doctors order tests and receive results asynchronously. Technicians, each capable of performing two types of tests (e.g., knee, hip), accept test orders and send back results to the ordering doctor. If multiple technicians can perform the same test, only one handles each request. Administrators log all activities and can send messages to everyone. The hospital treats hip, knee, and elbow injuries.</p>

<h1>💛 Users</h1>
<p><b>(Remember to provide the correct path to the file on your computer in the commands below.)</b></p>
<h2>👨‍💻 Administrator</h2>
<p>To compile Administrator: </p>

```
javac -cp "$LIB_PATH/slf4j-api-1.7.29.jar:$LIB_PATH/slf4j-simple-1.6.2.jar:$LIB_PATH/amqp-client-5.11.0.jar" Administrator.java
```

<p>To run Administrator: </p>

```
java -cp ".:$LIB_PATH/slf4j-api-1.7.29.jar:$LIB_PATH/slf4j-simple-1.6.2.jar:$LIB_PATH/amqp-client-5.11.0.jar" Administrator
```

<h2>👨‍⚕️ Doctor</h2>
<p>To compile Doctor: </p>

```
javac -cp "$LIB_PATH/slf4j-api-1.7.29.jar:$LIB_PATH/slf4j-simple-1.6.2.jar:$LIB_PATH/amqp-client-5.11.0.jar" Doctor.java

```

<p>To run Doctor: </p>

```
java -cp ".:$LIB_PATH/slf4j-api-1.7.29.jar:$LIB_PATH/slf4j-simple-1.6.2.jar:$LIB_PATH/amqp-client-5.11.0.jar" Doctor DoctorName
 
```

<p>Where "DoctorName" is a name to identify doctor. </p>

<h2>👨‍🔬 Technician</h2>
<p>To compile Technician:</p>

```
javac -cp "$LIB_PATH/slf4j-api-1.7.29.jar:$LIB_PATH/slf4j-simple-1.6.2.jar:$LIB_PATH/amqp-client-5.11.0.jar" Technician.java
```

<p>To run Technician: </p>

```
java -cp ".:$LIB_PATH/slf4j-api-1.7.29.jar:$LIB_PATH/slf4j-simple-1.6.2.jar:$LIB_PATH/amqp-client-5.11.0.jar" Technician 1
  
```

<p>Where 1 is a type of Technician (can be 1 or 2)</p>
