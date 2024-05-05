<h1>❤️ Dynamic Invocation</h1>
<p>The aim of this task is to demonstrate the functionality of dynamic invocation on the middleware client side. Dynamic invocation refers to a scenario where knowledge of the remote object or service interface is not required during compilation but only during runtime. </p>

<h1>❤️ How to run it?</h1>

<h2>Generate slice files:</h2>

<p>Java Files: </p>

````
slice2java --output-dir generated slice/calculator.ice
````

<p>C++ files:</p>
 
Change directory to client directory and run:

````
slice2cpp  ./slice/calculator.ice
````
<h2>Run Server</h2>


<h2>Run Client:</h2>

<p>To compile:</p>

````
c++ -c -std=c++11 -DICE_CPP11_MAPPING -pthread IceClient.cpp calculator.cpp
c++ -std=c++11 -o IceClient IceClient.o -pthread -lIce++11
````

<p>To run program: </p>

`````
./IceClient
`````

<p>To remove unused files: </p>

``````
rm -f IceClient IceClient.o calculator.o
``````
