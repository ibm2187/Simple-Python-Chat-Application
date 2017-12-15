#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#line above is needed to build public key .pem files
#lines below needed to import libraries
from threading import Thread
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import MD5
import select
import socket
import sys
from threading import Thread
while True:
	try:#intializaiton of program
		server_address ='192.168.0.108'
		port = input("what is the port? ")
		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		host = socket.gethostname()
		s.bind((server_address,port))
		s.listen(5)
		c,addr = s.accept()
		sys.stdout.write('%')
		#public and private key generation for Host A
		Brandom_generator = Random.new().read
		Bkey_private = RSA.generate(1024, Brandom_generator)
		Bkey_public = Bkey_private.publickey()
		#recieve public key from Allice
		data= c.recv(1024)
		print repr(data)
		inkey = RSA.importKey(data)
		#prepare and send public key to allice
		f = open('Bkey_public.pem', 'wb')
		f.write(Bkey_public.exportKey('PEM'))
		f.close()
		f = open('Bkey_public.pem', 'rb')
		l=f.read()
		c.send(l)
		f.close()
		#functions to decode, sign, encode and verify messages
		def decodeB(indata):
			return Bkey_private.decrypt(indata)
		def signB(msg):
			return Bkey_private.decrypt(msg)
		def encodeA(indata):
			return inkey.encrypt(indata,1024)
		def verifyA(indata):
			return inkey.encrypt(indata,1024)
		#thread to write, encode, sign and send messages
		def write():
			while True:
				write=raw_input()
				sign = signB(write)
				encode = encodeA(sign)
				c.send(encode[0])
				sys.stdout.write('%')
		#thread to recieve, decode and verify messages
		def read():
			while True:
				data = c.recv(1024)
				if data:
					print "message recieved"
					print repr(data)
					decode = decodeB(data)
					print repr(decode)
					message = verifyA(decode)
					print message, addr
		#thread initialization
		t1=Thread(target = write)
		t2=Thread (target = read)
		t1.start()
		t2.start()
		t1.join()
		t2.join()
	except:
		print "error"
		
