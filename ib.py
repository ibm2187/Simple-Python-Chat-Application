#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#the line above is needed to create the public.pem files
#below are library importing lines
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import MD5
import socket
import sys
from threading import Thread
while True:
	try:#initialization of program
		server_address ='192.168.0.108'
		port = input("what is the port? ")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((server_address ,port))
		sys.stdout.write('%')
		#public and private key generation for Host A
		Arandom_generator = Random.new().read
		Akey_private = RSA.generate(1024, Arandom_generator)
		Akey_public = Akey_private.publickey()
		#preparing the .pem files, with its contents sent to Bob
		f = open('Akey_public.pem', 'wb')
		f.write(Akey_public.exportKey('PEM'))
		f.close()
		f = open('Akey_public.pem', 'rb')
		l=f.read()
		s.send(l)
		f.close()
		#await allice's public key
		data= s.recv(1024)
		print repr(data)
		inkey = RSA.importKey(data)
		#functions to sign,encode,decode and verify messages
		def signA(msg):
			return Akey_private.decrypt(msg)
		def encodeB(indata):
			return inkey.encrypt(indata,1024)
		def decodeA(indata):
			return Akey_private.decrypt(indata)
		def verifyB(indata):
			return inkey.encrypt(indata,1024)
		#thread to write, encode, sign and send messages
		def write():
			while True:
			    line = raw_input()
			    signed= signA(line)
			    print repr(signed)
			    encode=encodeB(signed)
			    print repr (encode)
			    s.send(encode[0])
			    sys.stdout.write('%')
		#thread to recieve, decode and verify messages
		def read():
			while True:
				data = s.recv(1024)
				if data:
					print "message recieved"
					print repr(data)
					decode = decodeA(data)
					print repr(decode)
					verify=verifyB(decode)
					print repr (verify),server_address
					
		#threads intialization
		t1=Thread(target = write)
		t2=Thread (target = read)
		t1.start()
		t2.start()
		t1.join()
		t2.join()
	except:
		print " error"
		s.close()
