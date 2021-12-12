// To get a sample executable file for debugging using GDB test.c use gcc test.c -o test 
#include <stdio.h> 

int sub (int x, int y) { 
	int z; 
	z = x - y; 
	return z; 
} 

int main() { 
	int a, b, c; 
	printf("Input 1st Number: "); 
	scanf("%d", &a); 
	printf("Input 1st Number: "); 
	scanf("%d", &b); 
	c = sub(a, b); 
	printf("The subtraction is %d\n", c); 
	return 0; 
}
