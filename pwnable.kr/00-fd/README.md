```
fd@pwnable:~$ ls
fd  fd.c  flag
fd@pwnable:~$ ./fd
pass argv[1] a number
fd@pwnable:~$ cat fd.c 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char buf[32];
int main(int argc, char* argv[], char* envp[]){
	if(argc<2){
		printf("pass argv[1] a number\n");
		return 0;
	}
	int fd = atoi( argv[1] ) - 0x1234;
	int len = 0;
	len = read(fd, buf, 32);
	if(!strcmp("LETMEWIN\n", buf)){
		printf("good job :)\n");
		system("/bin/cat flag");
		exit(0);
	}
	printf("learn about Linux file IO\n");
	return 0;

}
```

File descripter 0 is STDIN

```
fd@pwnable:~$ python
Python 2.7.12 (default, Mar  1 2021, 11:38:31) 
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> 0x1234
4660

fd@pwnable:~$ ./fd 4660    
hello
learn about Linux file IO
fd@pwnable:~$ echo LETMEWIN | ./fd 4660
good job :)
mommy! I think I know what a file descriptor is!!
```
