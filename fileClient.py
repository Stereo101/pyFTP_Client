#fileClient.py

import socket
import struct

def send_file(sock,filename):
	length = os.path.getsize(filename)
	sock.sendall(struct.pack("!I",length))
	with open(filename,"rb") as f:
			bytesToSend = f.read(1024)
			sock.send(bytesToSend)
			while(bytesToSend != ""):
				bytesToSend = f.read(1024)
				sock.send(bytesToSend)

def recvall(sock,count):
	buf = b''
	while count:
		newbuf = sock.recv(count)
		if not newbuf: return None
		buf += newbuf
		count -= len(newbuf)
	return buf
	
def recvall_as_file(sock,count,filename):
	file = open(filename,"wb")
	while count:
		newbuf = sock.recv(count)
		if not newbuf: return None
		file.write(newbuf)
		count -= len(newbuf)
	return True
	
def recv_file(sock,filename):
	lengthbuf = recvall(sock,4)
	length, = struct.unpack("!I",lengthbuf)
	recvall_as_file(sock,length,filename)

def send_message(sock,data):
	length = len(data)
	sock.sendall(struct.pack("!I",length))
	sock.sendall(data)
	
def recv_message(sock):
	lengthbuf = recvall(sock,4)
	length, = struct.unpack("!I",lengthbuf)
	return recvall(sock,length)



def main():
	host = input("Enter server IP ->")
	port = int(input("Enter port ->"))
	
	s = socket.socket()
	s.connect((host,port))
	fileList = []
	fileItr = recv_message(s).decode("utf8")
	
	while(fileItr[:7] != "ENDLIST"):
		print(fileItr)
		fileList.append(fileItr[4:])
		fileItr = recv_message(s).decode("utf8")
	
	filename = input("Choose file letter ->")
	send_message(s,filename.encode("utf8"))
	data = recv_message(s)
	if(data.decode("utf8")[:2] == "OK"):
		print("Starting Download")
		recv_file(s,fileList[ord(filename)-97])
		print("Download Complete!")
	else:
		print("Server Response: Not OK to download file")

			
if __name__ == "__main__":
	main()