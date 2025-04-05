import socket
sock = socket.create_connection(("smtp.qq.com", 465), timeout=10)
print("端口连接成功")
sock.close()