```
col@pwnable:~$ ls
col  col.c  flag
col@pwnable:~$ cat col.c 
#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;
unsigned long check_password(const char* p){
	int* ip = (int*)p;
	int i;
	int res=0;
	for(i=0; i<5; i++){
		res += ip[i];
	}
	return res;
}

int main(int argc, char* argv[]){
	if(argc<2){
		printf("usage : %s [passcode]\n", argv[0]);
		return 0;
	}
	if(strlen(argv[1]) != 20){
		printf("passcode length should be 20 bytes\n");
		return 0;
	}

	if(hashcode == check_password( argv[1] )){
		system("/bin/cat flag");
		return 0;
	}
	else
		printf("wrong passcode.\n");
	return 0;
}
col@pwnable:~$ ./col
usage : ./col [passcode]
```

Testing a string

```
# ./a.out aaaaaaaaaaaaaaaaaaaa
res: 0
res: 61616161
res: c2c2c2c2
res: 24242423
res: 85858584
wrong passcode.
```

Adding some print statements we can see that the program basically takes a 20
char string chunks it into 5 parts starting at index 0, casts each part into
INTs, adds all 5 INTs together, ignores the remaining bytes, and compares the
sum of the 5 INTs to the hashcode. 

```
# ./a.out 00000000000000000000
res: 0
res: 30303030
res: 60606060
res: 90909090
res: c0c0c0c0
res: f0f0f0f0
cmp: 21dd09ec
wrong passcode.
dist(hashcode, passcode) == cf13e704
````

The issue then becomes that through standard means in BASH the smallest string
chunks that can be sent are `00000000==0x30303030`, which is already over the
value of the target hash. We can solve this by overflowing the `uint32_t` until
it equals the hash value with only values in the ASCII table that BASH will not
try to interpret, or we can find another means to enter in any value. 

Since the program does not read from STDIN, `xargs` and `echo` can be used to
reach the desired effect. Note that the program will not accept NULLs in the buffer.

```
# echo -en "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" | xargs --null ./a.out
passcode length should be 20 bytes
# echo -en "\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01" | xargs --null ./a.out
res: 0
res: 1010101
res: 2020202
res: 3030303
res: 4040404
wrong passcode.
dist(hashcode, passcode) == 1cd804e7
```

Now all that needs to be done is to divide the hash by 5 and add the remainder
back in the 4th of the last byte since the hash value does not divide evenly.

```
# python
Python 3.9.6 (default, Jun 30 2021, 10:22:16) 
[GCC 11.1.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> hex(int(0x21DD09EC/5))
'0x6c5cec8'
>>> hex((0x6c5cec8*4)+0x6c5cecc)
'0x21dd09ec'
...
col@pwnable:~$ echo -ne "\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xcc\xce\xc5\x06" | xargs --null ./col
daddy! I just managed to create a hash collision :)
```
