module switch(x,sel,y);
	input [2:0] x;
	input [1:0] sel;
	output [11:0] y;
	reg [11:0] z;
	reg [2:0] a;
	assign a = 3'b000;
	
	always @(sel) begin
		case (sel)
			0: z = {a,a,a,x};
			1: z = {a,a,x,a};
			2: z = {a,x,a,a};
			3: z = {x,a,a,a};
		endcase
	end
	assign y = z;

endmodule

