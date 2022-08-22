module ButterflyNodeD(packeti, channel, packeto);
	parameter M = 29;
	parameter N = 40; // M + 11
	parameter r = 1; // b01 = 1, b11 = 3, b111 = 7, etc
	input [40:0] packeti;
	output channel;
	output [40:0] packeto;

	reg [29:0] data;
	reg [3:0] a;
	reg [3:0] b;
	reg [2:0] lvl,lvl2;
	reg [3:0] z;


	assign data = packeti[40:11];
	assign a = packeti[10:7];
	assign b = packeti[6:3];
	assign lvl = packeti[2:0];

	//ButterflyDecideNode bdn1(a,b,z);

	// This seems to be ButterflyDecideNode:
	assign z = a^b;

	assign channel = (z >> lvl)&r;
	assign lvl2 = lvl + 1;
	assign packeto = {data,a,b,lvl2};

endmodule

