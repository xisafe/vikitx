# VACK Protocol

本文描述了 Vikitx Ack 的 ACK 机制。



## 目标

建立一套可靠的应用层数据包 ACK 机制

* 发送出一个需要 ACK 的数据包，可以实现在等待期间内，数据包缓存
* 随时可以重新发送，并且可以根据需要刷新 ACK 时间
* 超时之后调用 ACK 超时处理接口



## 接口

1. resend(token) 重新主动发送 ACK 信息。
2. reset(token) 重置 ACK 等待时间。
3. regist_timeout_callback(callback) 注册超时回调函数，回调函数第一个参数是数据包的内容，第二个参数是数据包发送的时间。
4. regist_send_callback(callback) 注册发送数据包的接口。