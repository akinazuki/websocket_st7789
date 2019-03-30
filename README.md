# websocket_st7789
A Websocket Bridge of ST7789

### Install
```bash
pip install websocket-server RPi.GPIO Pillow spidev numpy wiringpi
```

### Usage
```bash
python3 run.py
```

### Key Event

```
{
    "name":"KEY1",
    "key":16,
    "method":"key_press"
}
```

### Key Map

![KEYMAP.jpg](https://i.loli.net/2019/03/30/5c9f32f9e8226.jpg)



### API

#### Render Image to Screen
```
{
  "method": "picture",
  "data": "/9j/4QlQaH......" //base64 of image
}
```

##### Response
```
{
  "method": "picture",
  "status": true
}
```
---

Clear Screen
```
{
  "method": "clear"
}
```
##### Response
```
{
  "method": "clear",
  "status": true
}
```
----