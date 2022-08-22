module test;
	parameter M = 29;
	parameter N = 40; // M + 11
	reg [40:0] packeti;
	reg [40:0] packeto;

	reg channel;
	reg [29:0] data;
	reg [3:0] a;
	reg [3:0] b;
	reg [2:0] lvl;

	ButterflyNodeD #1 bfnd1 (packeti,channel,packeto);

	initial begin
		a = 4'b1011;
		b = 4'b0011;
		data = 50;
		lvl = 3'b011;
		packeti = {data,a,b,lvl};

		#1

		$display("channel = %d", channel);
		$display("packeti = %b", packeti);
		$display("packeto = %b", packeto);
		$display("data = %b", data);
		$display("a = %b", a);
		$display("b = %b", b);
		$display("lvl = %b", lvl);
		$finish();
	end

endmodule