module test;
	reg [2:0] x;
	reg [1:0] sel;
	reg [11:0] y;

	switch sw1(x,sel,y);

	initial begin
		x = 3'b111;
		sel = 2'b01;

		#5
		$display("y = %b", y);

		$finish();
	end

endmodule