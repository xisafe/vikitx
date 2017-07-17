# VSerialization Protocol

Vikit 数据序列化协议，数据传输是加密的，因此序列化传输包含两个部分，序列化和加密。

## Serialization

* serialize(obj) 序列化
* unserialize(text) 反序列化

## Crypto

关键接口：

* key：解密的公钥或密码
* enc：加密
* dec：解密