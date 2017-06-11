#include <stdio.h>

void main() {
	int i;
	int n;
	int wave_result;
	int wave;
	float fper;
	float mystep_period;
	float mystep_count;
	//float new_position[local_pincount];
	int wave_diff;
	float vel_cmd;
	float scale;
	unsigned periodns=10000000;

	vel_cmd=3;
	scale=1000;
	printf("test\n");
	fper=(1/(vel_cmd*scale));
	printf("fper %f\n", fper);
	mystep_period=fper*1e6;
	printf("msp %f\n", mystep_period);
	mystep_count=periodns/(fper*1e9);
	printf("msc %f\n", mystep_count);
	
								
}