from threading import Timer
def printhello():
	print("hellp")
	t=Timer(2,printhello)
	t.start()
if __name__ == '__main__':
	printhello()
	print("ere")