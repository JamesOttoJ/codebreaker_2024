var msgpack = require("msgpack-lite");
var buffer = msgpack.encode({"v": "N-00-001", "t": (new Date()).getTime() + 40000, "m": 0xEA60EA60, "d": 772});
console.log(buffer)
