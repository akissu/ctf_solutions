#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;
unsigned long check_password(const char* p){
	int* ip = (int*)p;
	int i;
	int res=0;
	for(i=0; i<5; i++){
    printf("res: %x\n", res);
		res += ip[i];
	}
  printf("res: %x\n", res);
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

	unsigned long res = check_password( argv[1] );
	if(hashcode == res){
		system("/bin/cat flag");
		return 0;
	}
	else
		printf("cmp: %x\n", hashcode);
		printf("wrong passcode.\n");
    if(hashcode > res)
      printf("dist(hashcode, passcode) == %x\n", hashcode - res);
    else
      printf("dist(hashcode, passcode) == %x\n", res - hashcode);
	return 0;
}
