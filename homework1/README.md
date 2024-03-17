<h1>🧡 Simple Client-Server Application (Chat)</h1>

<p>This task involves creating a chat application with both TCP and UDP communication capabilities, where TCP handles general chat messages and UDP handles multimedia messages, with the option to use multicast for broadcasting messages as an alternative to direct UDP transmission.</p>

<p>🔸 <b>The task was to develop a chat application with specific requirements:</b </p>
<ol>
  <li>Clients connect to the server using the TCP protocol.</li>
  <li>The server accepts messages from each client and broadcasts them to the others, along with the client's ID/nickname.</li>
  <li>The server is multithreaded - each client connection should have its own thread.</li>
  <li>Additionally, an extra UDP channel needs to be implemented:
    <ul>
      <li>Both server and each client open an additional UDP channel (with the same port number as TCP).</li>
      <li>When the client enters the 'U' command, a message is sent via UDP to the server, which broadcasts it to the other clients.</li>
      <li>The message simulates multimedia data (e.g., ASCII Art).</li>
    </ul>
  </li>
  <li>Implement the above point in a multicast version:
    <ul>
      <li>Not instead of, but as an alternative option (command 'M').</li>
      <li>Multicast sends directly to all clients via a group address (the server may, but does not have to receive).</li>
    </ul>
  </li>
</ol>

<img src="https://github.com/YoC00lig/Distributed-Systems/blob/main/homework1/homework1.gif">

<h1>🧡 How to run it?</h1>
<p>1. Change the directory to the one where the solution files are located.</p>

```
cd homework1
```

<p>2. In one console, run the server implementation file by entering the command:</p>

```
python ChatServer.py
```

<p>3. Run the client implementation file in subsequent consoles by entering the command:</p>

```
python ChatClient.py
```

<p>4. Follow the instructions that will appear after running the client file.</p>
