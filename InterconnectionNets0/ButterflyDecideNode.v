module ButterflyDecideNode();
    input [3:0] a;
    input [3:0] b;
    output [3:0] z;

    if ((a==4'b'0000)&&(b==4'b'0000))
        assign z = 4'b0000;
    if ((a==4'b'0000)&&(b==4'b'0001))
        assign z = 4'b0001;
    if ((a==4'b'0000)&&(b==4'b'0010))
        assign z = 4'b0010;
    if ((a==4'b'0000)&&(b==4'b'0011))
        assign z = 4'b0011;
    if ((a==4'b'0000)&&(b==4'b'0100))
        assign z = 4'b0100;
    if ((a==4'b'0000)&&(b==4'b'0101))
        assign z = 4'b0101;
    if ((a==4'b'0000)&&(b==4'b'0110))
        assign z = 4'b0110;
    if ((a==4'b'0000)&&(b==4'b'0111))
        assign z = 4'b0111;
    if ((a==4'b'0000)&&(b==4'b'1000))
        assign z = 4'b1000;
    if ((a==4'b'0000)&&(b==4'b'1001))
        assign z = 4'b1001;
    if ((a==4'b'0000)&&(b==4'b'1010))
        assign z = 4'b1010;
    if ((a==4'b'0000)&&(b==4'b'1011))
        assign z = 4'b1011;
    if ((a==4'b'0000)&&(b==4'b'1100))
        assign z = 4'b1100;
    if ((a==4'b'0000)&&(b==4'b'1101))
        assign z = 4'b1101;
    if ((a==4'b'0000)&&(b==4'b'1110))
        assign z = 4'b1110;
    if ((a==4'b'0000)&&(b==4'b'1111))
        assign z = 4'b1111;
    if ((a==4'b'0001)&&(b==4'b'0000))
        assign z = 4'b0001;
    if ((a==4'b'0001)&&(b==4'b'0001))
        assign z = 4'b0000;
    if ((a==4'b'0001)&&(b==4'b'0010))
        assign z = 4'b0011;
    if ((a==4'b'0001)&&(b==4'b'0011))
        assign z = 4'b0010;
    if ((a==4'b'0001)&&(b==4'b'0100))
        assign z = 4'b0101;
    if ((a==4'b'0001)&&(b==4'b'0101))
        assign z = 4'b0100;
    if ((a==4'b'0001)&&(b==4'b'0110))
        assign z = 4'b0111;
    if ((a==4'b'0001)&&(b==4'b'0111))
        assign z = 4'b0110;
    if ((a==4'b'0001)&&(b==4'b'1000))
        assign z = 4'b1001;
    if ((a==4'b'0001)&&(b==4'b'1001))
        assign z = 4'b1000;
    if ((a==4'b'0001)&&(b==4'b'1010))
        assign z = 4'b1011;
    if ((a==4'b'0001)&&(b==4'b'1011))
        assign z = 4'b1010;
    if ((a==4'b'0001)&&(b==4'b'1100))
        assign z = 4'b1101;
    if ((a==4'b'0001)&&(b==4'b'1101))
        assign z = 4'b1100;
    if ((a==4'b'0001)&&(b==4'b'1110))
        assign z = 4'b1111;
    if ((a==4'b'0001)&&(b==4'b'1111))
        assign z = 4'b1110;
    if ((a==4'b'0010)&&(b==4'b'0000))
        assign z = 4'b0010;
    if ((a==4'b'0010)&&(b==4'b'0001))
        assign z = 4'b0011;
    if ((a==4'b'0010)&&(b==4'b'0010))
        assign z = 4'b0000;
    if ((a==4'b'0010)&&(b==4'b'0011))
        assign z = 4'b0001;
    if ((a==4'b'0010)&&(b==4'b'0100))
        assign z = 4'b0110;
    if ((a==4'b'0010)&&(b==4'b'0101))
        assign z = 4'b0111;
    if ((a==4'b'0010)&&(b==4'b'0110))
        assign z = 4'b0100;
    if ((a==4'b'0010)&&(b==4'b'0111))
        assign z = 4'b0101;
    if ((a==4'b'0010)&&(b==4'b'1000))
        assign z = 4'b1010;
    if ((a==4'b'0010)&&(b==4'b'1001))
        assign z = 4'b1011;
    if ((a==4'b'0010)&&(b==4'b'1010))
        assign z = 4'b1000;
    if ((a==4'b'0010)&&(b==4'b'1011))
        assign z = 4'b1001;
    if ((a==4'b'0010)&&(b==4'b'1100))
        assign z = 4'b1110;
    if ((a==4'b'0010)&&(b==4'b'1101))
        assign z = 4'b1111;
    if ((a==4'b'0010)&&(b==4'b'1110))
        assign z = 4'b1100;
    if ((a==4'b'0010)&&(b==4'b'1111))
        assign z = 4'b1101;
    if ((a==4'b'0011)&&(b==4'b'0000))
        assign z = 4'b0011;
    if ((a==4'b'0011)&&(b==4'b'0001))
        assign z = 4'b0010;
    if ((a==4'b'0011)&&(b==4'b'0010))
        assign z = 4'b0001;
    if ((a==4'b'0011)&&(b==4'b'0011))
        assign z = 4'b0000;
    if ((a==4'b'0011)&&(b==4'b'0100))
        assign z = 4'b0111;
    if ((a==4'b'0011)&&(b==4'b'0101))
        assign z = 4'b0110;
    if ((a==4'b'0011)&&(b==4'b'0110))
        assign z = 4'b0101;
    if ((a==4'b'0011)&&(b==4'b'0111))
        assign z = 4'b0100;
    if ((a==4'b'0011)&&(b==4'b'1000))
        assign z = 4'b1011;
    if ((a==4'b'0011)&&(b==4'b'1001))
        assign z = 4'b1010;
    if ((a==4'b'0011)&&(b==4'b'1010))
        assign z = 4'b1001;
    if ((a==4'b'0011)&&(b==4'b'1011))
        assign z = 4'b1000;
    if ((a==4'b'0011)&&(b==4'b'1100))
        assign z = 4'b1111;
    if ((a==4'b'0011)&&(b==4'b'1101))
        assign z = 4'b1110;
    if ((a==4'b'0011)&&(b==4'b'1110))
        assign z = 4'b1101;
    if ((a==4'b'0011)&&(b==4'b'1111))
        assign z = 4'b1100;
    if ((a==4'b'0100)&&(b==4'b'0000))
        assign z = 4'b0100;
    if ((a==4'b'0100)&&(b==4'b'0001))
        assign z = 4'b0101;
    if ((a==4'b'0100)&&(b==4'b'0010))
        assign z = 4'b0110;
    if ((a==4'b'0100)&&(b==4'b'0011))
        assign z = 4'b0111;
    if ((a==4'b'0100)&&(b==4'b'0100))
        assign z = 4'b0000;
    if ((a==4'b'0100)&&(b==4'b'0101))
        assign z = 4'b0001;
    if ((a==4'b'0100)&&(b==4'b'0110))
        assign z = 4'b0010;
    if ((a==4'b'0100)&&(b==4'b'0111))
        assign z = 4'b0011;
    if ((a==4'b'0100)&&(b==4'b'1000))
        assign z = 4'b1100;
    if ((a==4'b'0100)&&(b==4'b'1001))
        assign z = 4'b1101;
    if ((a==4'b'0100)&&(b==4'b'1010))
        assign z = 4'b1110;
    if ((a==4'b'0100)&&(b==4'b'1011))
        assign z = 4'b1111;
    if ((a==4'b'0100)&&(b==4'b'1100))
        assign z = 4'b1000;
    if ((a==4'b'0100)&&(b==4'b'1101))
        assign z = 4'b1001;
    if ((a==4'b'0100)&&(b==4'b'1110))
        assign z = 4'b1010;
    if ((a==4'b'0100)&&(b==4'b'1111))
        assign z = 4'b1011;
    if ((a==4'b'0101)&&(b==4'b'0000))
        assign z = 4'b0101;
    if ((a==4'b'0101)&&(b==4'b'0001))
        assign z = 4'b0100;
    if ((a==4'b'0101)&&(b==4'b'0010))
        assign z = 4'b0111;
    if ((a==4'b'0101)&&(b==4'b'0011))
        assign z = 4'b0110;
    if ((a==4'b'0101)&&(b==4'b'0100))
        assign z = 4'b0001;
    if ((a==4'b'0101)&&(b==4'b'0101))
        assign z = 4'b0000;
    if ((a==4'b'0101)&&(b==4'b'0110))
        assign z = 4'b0011;
    if ((a==4'b'0101)&&(b==4'b'0111))
        assign z = 4'b0010;
    if ((a==4'b'0101)&&(b==4'b'1000))
        assign z = 4'b1101;
    if ((a==4'b'0101)&&(b==4'b'1001))
        assign z = 4'b1100;
    if ((a==4'b'0101)&&(b==4'b'1010))
        assign z = 4'b1111;
    if ((a==4'b'0101)&&(b==4'b'1011))
        assign z = 4'b1110;
    if ((a==4'b'0101)&&(b==4'b'1100))
        assign z = 4'b1001;
    if ((a==4'b'0101)&&(b==4'b'1101))
        assign z = 4'b1000;
    if ((a==4'b'0101)&&(b==4'b'1110))
        assign z = 4'b1011;
    if ((a==4'b'0101)&&(b==4'b'1111))
        assign z = 4'b1010;
    if ((a==4'b'0110)&&(b==4'b'0000))
        assign z = 4'b0110;
    if ((a==4'b'0110)&&(b==4'b'0001))
        assign z = 4'b0111;
    if ((a==4'b'0110)&&(b==4'b'0010))
        assign z = 4'b0100;
    if ((a==4'b'0110)&&(b==4'b'0011))
        assign z = 4'b0101;
    if ((a==4'b'0110)&&(b==4'b'0100))
        assign z = 4'b0010;
    if ((a==4'b'0110)&&(b==4'b'0101))
        assign z = 4'b0011;
    if ((a==4'b'0110)&&(b==4'b'0110))
        assign z = 4'b0000;
    if ((a==4'b'0110)&&(b==4'b'0111))
        assign z = 4'b0001;
    if ((a==4'b'0110)&&(b==4'b'1000))
        assign z = 4'b1110;
    if ((a==4'b'0110)&&(b==4'b'1001))
        assign z = 4'b1111;
    if ((a==4'b'0110)&&(b==4'b'1010))
        assign z = 4'b1100;
    if ((a==4'b'0110)&&(b==4'b'1011))
        assign z = 4'b1101;
    if ((a==4'b'0110)&&(b==4'b'1100))
        assign z = 4'b1010;
    if ((a==4'b'0110)&&(b==4'b'1101))
        assign z = 4'b1011;
    if ((a==4'b'0110)&&(b==4'b'1110))
        assign z = 4'b1000;
    if ((a==4'b'0110)&&(b==4'b'1111))
        assign z = 4'b1001;
    if ((a==4'b'0111)&&(b==4'b'0000))
        assign z = 4'b0111;
    if ((a==4'b'0111)&&(b==4'b'0001))
        assign z = 4'b0110;
    if ((a==4'b'0111)&&(b==4'b'0010))
        assign z = 4'b0101;
    if ((a==4'b'0111)&&(b==4'b'0011))
        assign z = 4'b0100;
    if ((a==4'b'0111)&&(b==4'b'0100))
        assign z = 4'b0011;
    if ((a==4'b'0111)&&(b==4'b'0101))
        assign z = 4'b0010;
    if ((a==4'b'0111)&&(b==4'b'0110))
        assign z = 4'b0001;
    if ((a==4'b'0111)&&(b==4'b'0111))
        assign z = 4'b0000;
    if ((a==4'b'0111)&&(b==4'b'1000))
        assign z = 4'b1111;
    if ((a==4'b'0111)&&(b==4'b'1001))
        assign z = 4'b1110;
    if ((a==4'b'0111)&&(b==4'b'1010))
        assign z = 4'b1101;
    if ((a==4'b'0111)&&(b==4'b'1011))
        assign z = 4'b1100;
    if ((a==4'b'0111)&&(b==4'b'1100))
        assign z = 4'b1011;
    if ((a==4'b'0111)&&(b==4'b'1101))
        assign z = 4'b1010;
    if ((a==4'b'0111)&&(b==4'b'1110))
        assign z = 4'b1001;
    if ((a==4'b'0111)&&(b==4'b'1111))
        assign z = 4'b1000;
    if ((a==4'b'1000)&&(b==4'b'0000))
        assign z = 4'b1000;
    if ((a==4'b'1000)&&(b==4'b'0001))
        assign z = 4'b1001;
    if ((a==4'b'1000)&&(b==4'b'0010))
        assign z = 4'b1010;
    if ((a==4'b'1000)&&(b==4'b'0011))
        assign z = 4'b1011;
    if ((a==4'b'1000)&&(b==4'b'0100))
        assign z = 4'b1100;
    if ((a==4'b'1000)&&(b==4'b'0101))
        assign z = 4'b1101;
    if ((a==4'b'1000)&&(b==4'b'0110))
        assign z = 4'b1110;
    if ((a==4'b'1000)&&(b==4'b'0111))
        assign z = 4'b1111;
    if ((a==4'b'1000)&&(b==4'b'1000))
        assign z = 4'b0000;
    if ((a==4'b'1000)&&(b==4'b'1001))
        assign z = 4'b0001;
    if ((a==4'b'1000)&&(b==4'b'1010))
        assign z = 4'b0010;
    if ((a==4'b'1000)&&(b==4'b'1011))
        assign z = 4'b0011;
    if ((a==4'b'1000)&&(b==4'b'1100))
        assign z = 4'b0100;
    if ((a==4'b'1000)&&(b==4'b'1101))
        assign z = 4'b0101;
    if ((a==4'b'1000)&&(b==4'b'1110))
        assign z = 4'b0110;
    if ((a==4'b'1000)&&(b==4'b'1111))
        assign z = 4'b0111;
    if ((a==4'b'1001)&&(b==4'b'0000))
        assign z = 4'b1001;
    if ((a==4'b'1001)&&(b==4'b'0001))
        assign z = 4'b1000;
    if ((a==4'b'1001)&&(b==4'b'0010))
        assign z = 4'b1011;
    if ((a==4'b'1001)&&(b==4'b'0011))
        assign z = 4'b1010;
    if ((a==4'b'1001)&&(b==4'b'0100))
        assign z = 4'b1101;
    if ((a==4'b'1001)&&(b==4'b'0101))
        assign z = 4'b1100;
    if ((a==4'b'1001)&&(b==4'b'0110))
        assign z = 4'b1111;
    if ((a==4'b'1001)&&(b==4'b'0111))
        assign z = 4'b1110;
    if ((a==4'b'1001)&&(b==4'b'1000))
        assign z = 4'b0001;
    if ((a==4'b'1001)&&(b==4'b'1001))
        assign z = 4'b0000;
    if ((a==4'b'1001)&&(b==4'b'1010))
        assign z = 4'b0011;
    if ((a==4'b'1001)&&(b==4'b'1011))
        assign z = 4'b0010;
    if ((a==4'b'1001)&&(b==4'b'1100))
        assign z = 4'b0101;
    if ((a==4'b'1001)&&(b==4'b'1101))
        assign z = 4'b0100;
    if ((a==4'b'1001)&&(b==4'b'1110))
        assign z = 4'b0111;
    if ((a==4'b'1001)&&(b==4'b'1111))
        assign z = 4'b0110;
    if ((a==4'b'1010)&&(b==4'b'0000))
        assign z = 4'b1010;
    if ((a==4'b'1010)&&(b==4'b'0001))
        assign z = 4'b1011;
    if ((a==4'b'1010)&&(b==4'b'0010))
        assign z = 4'b1000;
    if ((a==4'b'1010)&&(b==4'b'0011))
        assign z = 4'b1001;
    if ((a==4'b'1010)&&(b==4'b'0100))
        assign z = 4'b1110;
    if ((a==4'b'1010)&&(b==4'b'0101))
        assign z = 4'b1111;
    if ((a==4'b'1010)&&(b==4'b'0110))
        assign z = 4'b1100;
    if ((a==4'b'1010)&&(b==4'b'0111))
        assign z = 4'b1101;
    if ((a==4'b'1010)&&(b==4'b'1000))
        assign z = 4'b0010;
    if ((a==4'b'1010)&&(b==4'b'1001))
        assign z = 4'b0011;
    if ((a==4'b'1010)&&(b==4'b'1010))
        assign z = 4'b0000;
    if ((a==4'b'1010)&&(b==4'b'1011))
        assign z = 4'b0001;
    if ((a==4'b'1010)&&(b==4'b'1100))
        assign z = 4'b0110;
    if ((a==4'b'1010)&&(b==4'b'1101))
        assign z = 4'b0111;
    if ((a==4'b'1010)&&(b==4'b'1110))
        assign z = 4'b0100;
    if ((a==4'b'1010)&&(b==4'b'1111))
        assign z = 4'b0101;
    if ((a==4'b'1011)&&(b==4'b'0000))
        assign z = 4'b1011;
    if ((a==4'b'1011)&&(b==4'b'0001))
        assign z = 4'b1010;
    if ((a==4'b'1011)&&(b==4'b'0010))
        assign z = 4'b1001;
    if ((a==4'b'1011)&&(b==4'b'0011))
        assign z = 4'b1000;
    if ((a==4'b'1011)&&(b==4'b'0100))
        assign z = 4'b1111;
    if ((a==4'b'1011)&&(b==4'b'0101))
        assign z = 4'b1110;
    if ((a==4'b'1011)&&(b==4'b'0110))
        assign z = 4'b1101;
    if ((a==4'b'1011)&&(b==4'b'0111))
        assign z = 4'b1100;
    if ((a==4'b'1011)&&(b==4'b'1000))
        assign z = 4'b0011;
    if ((a==4'b'1011)&&(b==4'b'1001))
        assign z = 4'b0010;
    if ((a==4'b'1011)&&(b==4'b'1010))
        assign z = 4'b0001;
    if ((a==4'b'1011)&&(b==4'b'1011))
        assign z = 4'b0000;
    if ((a==4'b'1011)&&(b==4'b'1100))
        assign z = 4'b0111;
    if ((a==4'b'1011)&&(b==4'b'1101))
        assign z = 4'b0110;
    if ((a==4'b'1011)&&(b==4'b'1110))
        assign z = 4'b0101;
    if ((a==4'b'1011)&&(b==4'b'1111))
        assign z = 4'b0100;
    if ((a==4'b'1100)&&(b==4'b'0000))
        assign z = 4'b1100;
    if ((a==4'b'1100)&&(b==4'b'0001))
        assign z = 4'b1101;
    if ((a==4'b'1100)&&(b==4'b'0010))
        assign z = 4'b1110;
    if ((a==4'b'1100)&&(b==4'b'0011))
        assign z = 4'b1111;
    if ((a==4'b'1100)&&(b==4'b'0100))
        assign z = 4'b1000;
    if ((a==4'b'1100)&&(b==4'b'0101))
        assign z = 4'b1001;
    if ((a==4'b'1100)&&(b==4'b'0110))
        assign z = 4'b1010;
    if ((a==4'b'1100)&&(b==4'b'0111))
        assign z = 4'b1011;
    if ((a==4'b'1100)&&(b==4'b'1000))
        assign z = 4'b0100;
    if ((a==4'b'1100)&&(b==4'b'1001))
        assign z = 4'b0101;
    if ((a==4'b'1100)&&(b==4'b'1010))
        assign z = 4'b0110;
    if ((a==4'b'1100)&&(b==4'b'1011))
        assign z = 4'b0111;
    if ((a==4'b'1100)&&(b==4'b'1100))
        assign z = 4'b0000;
    if ((a==4'b'1100)&&(b==4'b'1101))
        assign z = 4'b0001;
    if ((a==4'b'1100)&&(b==4'b'1110))
        assign z = 4'b0010;
    if ((a==4'b'1100)&&(b==4'b'1111))
        assign z = 4'b0011;
    if ((a==4'b'1101)&&(b==4'b'0000))
        assign z = 4'b1101;
    if ((a==4'b'1101)&&(b==4'b'0001))
        assign z = 4'b1100;
    if ((a==4'b'1101)&&(b==4'b'0010))
        assign z = 4'b1111;
    if ((a==4'b'1101)&&(b==4'b'0011))
        assign z = 4'b1110;
    if ((a==4'b'1101)&&(b==4'b'0100))
        assign z = 4'b1001;
    if ((a==4'b'1101)&&(b==4'b'0101))
        assign z = 4'b1000;
    if ((a==4'b'1101)&&(b==4'b'0110))
        assign z = 4'b1011;
    if ((a==4'b'1101)&&(b==4'b'0111))
        assign z = 4'b1010;
    if ((a==4'b'1101)&&(b==4'b'1000))
        assign z = 4'b0101;
    if ((a==4'b'1101)&&(b==4'b'1001))
        assign z = 4'b0100;
    if ((a==4'b'1101)&&(b==4'b'1010))
        assign z = 4'b0111;
    if ((a==4'b'1101)&&(b==4'b'1011))
        assign z = 4'b0110;
    if ((a==4'b'1101)&&(b==4'b'1100))
        assign z = 4'b0001;
    if ((a==4'b'1101)&&(b==4'b'1101))
        assign z = 4'b0000;
    if ((a==4'b'1101)&&(b==4'b'1110))
        assign z = 4'b0011;
    if ((a==4'b'1101)&&(b==4'b'1111))
        assign z = 4'b0010;
    if ((a==4'b'1110)&&(b==4'b'0000))
        assign z = 4'b1110;
    if ((a==4'b'1110)&&(b==4'b'0001))
        assign z = 4'b1111;
    if ((a==4'b'1110)&&(b==4'b'0010))
        assign z = 4'b1100;
    if ((a==4'b'1110)&&(b==4'b'0011))
        assign z = 4'b1101;
    if ((a==4'b'1110)&&(b==4'b'0100))
        assign z = 4'b1010;
    if ((a==4'b'1110)&&(b==4'b'0101))
        assign z = 4'b1011;
    if ((a==4'b'1110)&&(b==4'b'0110))
        assign z = 4'b1000;
    if ((a==4'b'1110)&&(b==4'b'0111))
        assign z = 4'b1001;
    if ((a==4'b'1110)&&(b==4'b'1000))
        assign z = 4'b0110;
    if ((a==4'b'1110)&&(b==4'b'1001))
        assign z = 4'b0111;
    if ((a==4'b'1110)&&(b==4'b'1010))
        assign z = 4'b0100;
    if ((a==4'b'1110)&&(b==4'b'1011))
        assign z = 4'b0101;
    if ((a==4'b'1110)&&(b==4'b'1100))
        assign z = 4'b0010;
    if ((a==4'b'1110)&&(b==4'b'1101))
        assign z = 4'b0011;
    if ((a==4'b'1110)&&(b==4'b'1110))
        assign z = 4'b0000;
    if ((a==4'b'1110)&&(b==4'b'1111))
        assign z = 4'b0001;
    if ((a==4'b'1111)&&(b==4'b'0000))
        assign z = 4'b1111;
    if ((a==4'b'1111)&&(b==4'b'0001))
        assign z = 4'b1110;
    if ((a==4'b'1111)&&(b==4'b'0010))
        assign z = 4'b1101;
    if ((a==4'b'1111)&&(b==4'b'0011))
        assign z = 4'b1100;
    if ((a==4'b'1111)&&(b==4'b'0100))
        assign z = 4'b1011;
    if ((a==4'b'1111)&&(b==4'b'0101))
        assign z = 4'b1010;
    if ((a==4'b'1111)&&(b==4'b'0110))
        assign z = 4'b1001;
    if ((a==4'b'1111)&&(b==4'b'0111))
        assign z = 4'b1000;
    if ((a==4'b'1111)&&(b==4'b'1000))
        assign z = 4'b0111;
    if ((a==4'b'1111)&&(b==4'b'1001))
        assign z = 4'b0110;
    if ((a==4'b'1111)&&(b==4'b'1010))
        assign z = 4'b0101;
    if ((a==4'b'1111)&&(b==4'b'1011))
        assign z = 4'b0100;
    if ((a==4'b'1111)&&(b==4'b'1100))
        assign z = 4'b0011;
    if ((a==4'b'1111)&&(b==4'b'1101))
        assign z = 4'b0010;
    if ((a==4'b'1111)&&(b==4'b'1110))
        assign z = 4'b0001;
    if ((a==4'b'1111)&&(b==4'b'1111))
        assign z = 4'b0000;

endmodule