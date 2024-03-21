<h1>💜 Simple Weather App - RESTful API</h1>

<p>This project is a simple web service that accomplishes a functionality using open REST APIs. The task is to create a service that:</p>
<ol>
  <li>Provides the client with a static HTML page containing a form to gather request parameters.</li>
  <li>Receives requests from the client.</li>
  <li>The server is multithreaded - each client connection should have its own thread.</li>
  <li>Queries public services (various endpoints, preferably multiple services) for the data needed to construct a response.</li>
  <li>Processes the received responses (e.g., calculating averages, finding extremes, comparing values from different services).</li>
  <li>Generates and sends a response to the client (static HTML page with the results).</li>
</ol>

<h1>💜 How to run it?</h1>
<p>1. Make sure you have installed all the python libraries contained in weather.py file and uvicorn.</p>
<p>2. Change the directory to the one where the solution files are located.</p>

```
cd homework2
```

<p>3. Starts a web server:</p>

```
uvicorn weather:app --reload
```

<p>4. Open <a href="http://localhost:8000">http://localhost:8000</a> in your browser.</p>
