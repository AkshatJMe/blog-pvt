+++
title = "From WebSockets to SSE: Real-Time Communication in System Design"
description = "When developing modern web or mobile applications, real-time data transmission has become a critical feature for delivering seamless user experiences. Technologies like WebSockets, Server-Sent Events, or real-time databases are often used to achieve this functionality efficiently."
imagesq = "/images/blog/real-time-communication-methods/square.webp"
image = "/images/blog/real-time-communication-methods/thumb.webp"
authorName = "akshat-jain"
date = 2022-08-15T00:00:00+05:30
tags = ["System Design", "Web Sockets"]
+++
When building modern web or mobile applications, it’s often important to send and receive data **in real time**  like getting new chat messages, notifications, or live updates. Here are four common ways to do that:

---

### 1. **Short Polling**

- **What It Is**: The client (like a browser) keeps asking the server for new data over and over again at fixed intervals (e.g., every 5 seconds).
- **How It Works**:
    - The client sends a request.
    - The server replies right away with data (if any).
    - The client waits a few seconds, then repeats the request.
- **Pros**:
    - Easy to set up.
    - Uses basic HTTP — no special setup needed.
- **Cons**:
    - Can be wasteful — sending requests even when there's nothing new.
    - More server load and delayed updates.
- **Use Case Example**: Simple dashboards that refresh data every few seconds.

---

### 2. **Long Polling**

- **What It Is**: The client sends a request and waits. The server doesn’t respond until there’s new data to send (or a timeout happens).
- **How It Works**:
    - The client makes a request.
    - The server keeps the connection open until it has something to send.
    - When the data arrives, the server responds and the client immediately starts a new request.
- **Pros**:
    - Reduces unnecessary traffic — only responds when there’s new data.
    - Still works over standard HTTP.
- **Cons**:
    - Can tie up server resources.
    - More complex than short polling.
- **Use Case Example**: Comment updates on a blog or forum.

---

### 3. **WebSockets**

- **What It Is**: A fast, two-way communication channel between the client and server that stays open.
- **How It Works**:
    - The connection starts as a regular HTTP request, then switches (or "upgrades") to a WebSocket connection.
    - After that, both sides can send messages anytime — instantly and continuously.
- **Pros**:
    - Very fast and efficient.
    - Supports real-time, bidirectional communication.
- **Cons**:
    - Needs both server and client to support WebSockets.
    - Harder to scale and manage compared to simple HTTP.
- **Use Case Example**: Chat apps, live sports scores, multiplayer games.

---

### 4. **Server-Sent Events (SSE)**

- **What It Is**: The server can send updates to the client over a single open connection — but only from server to client.
- **How It Works**:
    - The client makes a request to the server to start listening for updates.
    - The server keeps the connection open and pushes updates as they happen.
    - The client doesn’t have to ask again.
- **Pros**:
    - Simple and lightweight for one-way updates.
    - Great for sending frequent updates like stock prices or notifications.
- **Cons**:
    - Only works one way (server → client).
    - Doesn’t support binary data out of the box.
- **Use Case Example**: News tickers, live notifications, weather updates.

---

## 🧾 Summary Table

| Method | Communication | Complexity | Efficiency | Ideal For |
| --- | --- | --- | --- | --- |
| Short Polling | Client → Server | Easy | Low | Simple apps, quick prototyping |
| Long Polling | Client → Server | Medium | Medium | Semi-live updates |
| WebSockets | Two-way | Advanced | High | Real-time apps (chat, games) |
| Server-Sent Events | Server → Client | Easy | High | Notifications, live data feeds |

---

Each method has its strengths and is best suited for specific types of real-time needs. Your choice depends on:

- How often data changes
- Whether you need two-way communication
- How complex your app needs to be