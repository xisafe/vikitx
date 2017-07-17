# ZMQ Sync Reliable Pub-Sub Protocol（ZSRPS）

ZMQ 同步可靠发布-订阅协议（ZSRPS）是基于 ZMQ 本身的 Pub-Sub 模型存在的问题（PUB 无法探知 SUB 的状态），提出的一种补救措施，通过同步锁，心跳机制，来解决原先机制造成的“慢连接”，和状态监测问题。



## License

Not yet



## Goals

ZSRPS 实现了一种可靠的 Pub-Sub 模型通信关系，Pub 方可以侦测到 Sub 方的状态，并且同步订阅状态。

所以 ZSRPS 的目标如下：

* Pub 端可见 Sub 的用户状态
* 订阅状态监控
* 对订阅状态的操作：重连／断开／超时／错误的正确处理
* Pub 对 Sub 不做过多的干涉



## Architecture

### Roles

ZSRPS 定义了两种实体：

* “Client” 用于发送消息（协议内置消息与自定义消息），全文描述简称 Client


* “Server” 用接受消息发送控制指令（协议内置消息与），全文描述简称 Server

### Overall Conversation

#### Step 1：同步建立订阅关系（Shakehands）

1. Client 通过 REQ 请求 Server 端的 REP 地址，以此建立第一个连接交换必要的信息，在请求的时，Client 把自己的 Pub 地址传递给服务器，同时也暴露一个功能不支持拓展的 REP 地址，用于 Server 控制 Client 的状态和进行 ACK 操作。
2. Server 在收到 Client 的第一个请求之后，回复一个收到请求的 ACK
3. 当 Client 收到 ACK 之后，会从发布端发布高频心跳包，心跳包包含一个有效期限（Lease-Time）一般这个有效期限是下一个心跳包的时间，与此同时，也会发送一个 REQ，这个 REQ 包含一个过期时间，当 Server 收到第一个心跳包之后，记录心跳到达的时间，Server 对比 REQ 中的过期时间，如果收到心跳的时间超过了 REQ 中的时间则回复一个 reset 信号，此时 Client 重启，重新进行第一步；如果收到心跳的时间在 REQ 的时间之内，回复一个 established 信号。
4. 当 Client 收到信号的时候，降低心跳包的频率。

#### Step 2：发送数据

数据分为两种：需要 ACK 和 不需要 ACK 的。

* 针对需要 ACK 的数据，Server 收到之后，会向 Client-REP 主动发送一个 ACK 确认信息，然后得到一个 finish  信号，并清理缓存信息。
* 针对不需要 ACK 的数据，Server 收到之后随时进行处理（Heartbeat），不会进行额外多余的操作。

#### Step 3：状态操作

状态有如下操作：

1. 重连：Server 发送一个重连操作，清理缓存，Client 重启。Server 发送一个重连信号，Client 回复 ACK 之后，断开连接重新启动
2. 断开：Server 发送一个断开信号，清理缓存，Client 断开。Server 发送一个重连信号，Client 回复 ACK 以后，断开连接
3. 超时：同重连，但是会额外调用超时处理接口，超时处理用户需要自定义
4. 失败：同断开，但是会额外调用失败处理接口，失败处理用户需要自定义

### 数据结构定义

在 Step1/Step3 中出现的，和 Step2 种，主动 ACK 等信息，都属于 Signal，属于协议内置信息，并且每一个信号都拥有自己的 token，在回复中会确认 token

在 Step2 中传递的数据，需要 ACK 的数据，必须拥有自己的 token，方便 Client 端 ACK 池的确认，但是不需 ACK 的数据包就不必设置 token

### 相关组件协议定义：

Ackpool: ACK 池，装载与 Client 中，用于缓存和确认 ACK。

Cachepool: 缓存收到的数据信息，双向队列，容量一定，便于查看一些历史信息

