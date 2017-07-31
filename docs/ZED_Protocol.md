# Zmq Exchange Device Protocol(ZED)

ZED 全称 Zmq Exchange Device 是一个基于 ZMQ 开发的消息交换机，起到缓存信息，交换信息的作用。



## 目标：

解决多对多的信息交换问题，在入端所有的生产信息的设备（生产者）都是平等的，在消息出口（消费者）也是平等的，在 vikitx 中主要解决 service 执行任务和返回结果的问题，当然必须是同类型任务才可以使用同一个路由键。



## 名词：

* Entry：接入点
* Ackpool：确认消息是否被接受，重发消息
* Cache_queue：消息队列缓存器
* Router：路由器装置
* Exchanger：交换设备
* Endpoint：客户端终端点



## 功能：

* 缓存：设置缓存队列，从交换机 Entry 进入的消息，被输入进缓存队列，缓存队列的入队和出队可以设置数据库接口存入任务（或者恢复上一次任务），消息出口负责从消息队列中取出消息，进行路由
* 路由功能：进入交换系统的消息体必须有一个关键字段，RKEY（Router-Key）这个路由值决定了消息被送到具体哪一个路由器中。接下来列举可能出现的情况：
  * 路由存在：当路由存在时，消息被送入 KEY 对应的路由中
  * 路由不存在：路由不存在，如果设置了缓存数据库，则会被存入缓存数据库的 ERROR 表单，如果没设置缓存数据库，则会给发送消息的终端点返回一个，Failed 信号
* 反馈机制：
  * 从 Exchanger 到消息生产者的反馈，这里有三种情况：
    * 成功：返回 ACK 信号（立即返回）
    * 失败：返回 Failed 信号（立即或者延时）
    * 超时：返回 Failed 信号（延时）
  * 从消息消费者到 Exchanger 的反馈：
    * 成功：返回 ACK 信号，这时候 Exchanger 会把 Ackpool 中这条消息清除掉
    * 失败：返回 Failed 信号，这时候 Exchanger 会把消息重新推入队列等待路由键下的消费者处理这条消息
    * 超时：如果既没有接收到 ACK 也没有接收到 Failed，这时候则清除掉（如果设置了缓存数据库，则把该消息存入数据库中）



## 数据结构定义：

### 消息体说明

```Python
class _Msg(object):
    def __init__(self, id, router_key, messgae, **options):
        self._id = id
        self._rkey = router_key
        self._message = message
    
   	@property
    def id(self):
        return self._id
    @property
    def router_key(self):
        return self._rkey
    @property
    def message(self):
        return self._message
    def finished(self):
        #
        # finished
		# 
    def ack(self):
        self.finished()
```

一个内部流通的消息体大致定义如上。

### 消息路由表

消息路由表记录每条消息在交换机中的生存周期，可以根据 KEY 对消息实体进行各种操作，操作如下：

* 注册一条新的消息
* 删除一条消息
* 查询消息的特定键值
* 当然在消息进入路由表的时候，会设置一个自动清除的时间，这个时间往往设置为一个小时，在此期间 ID 不可以冲突。

除此之外，消息路由是无状态的，如果消息路由表重启了，则所有消息都必须重新注册才能进行路由操作

