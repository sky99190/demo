
`include "cpu_types_pkg.vh"
  import cpu_types_pkg::*;
module PC(
input logic CLK, nRST,pcEN,bm,bs,bing,ihit,
input word_t new_pc,instr,reg_loc,PC_INIT,
output word_t pcounter, n_pc
	  );
   logic [13:0] ext_sign;
   
   always_ff @(posedge CLK, negedge nRST) begin
      if (nRST==0) begin
	 pcounter<=PC_INIT;
      end else if (bing==1&&ihit==1)begin
	 pcounter<=new_pc;
      end else if ((instr[31:26]==6'b101||instr[31:26]==6'b100)&&pcEN)begin
	 if (bm==0)begin
	    pcounter<=new_pc;
	 end else begin
	    pcounter<=(n_pc+{ext_sign,instr[15:0],2'b0});
	 end
     
      end else if ((instr[31:26]==6'b10||instr[31:26]==6'b11)&&pcEN)begin
	 pcounter<={n_pc[31:28],instr[25:0],2'b0};
      end else if (pcEN&&instr[31:26]==0&&instr[5:0]==6'b1000)begin
	 pcounter<=reg_loc;
      end else if (pcEN==1)begin
	 pcounter<=new_pc;
      end else begin
	 
         
      end
   end // always_ff @ (posedge CLK, negedge nRST)
   


   assign n_pc=pcounter+4;
   assign ext_sign= (instr[15]==1) ? 14'b11111111111111 : 14'b0;
endmodule // PC

   





	  
	
	   
