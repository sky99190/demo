`include "cpu_types_pkg.vh"

import cpu_types_pkg::*; 
 
module instr_reg(
   input       word_t instr_in,
   input       word_t pc_in,
   input logic bf,bm,
   output      word_t pc_out,
   output      word_t instr_out,

   input logic CLK, nRST, ihit,dhit, stay, flush
   );

   
   

   always_ff @(posedge CLK or negedge nRST) begin
      if (nRST==0) begin
	 instr_out<=0;
	 pc_out<=0;

      end else if (bf==1)begin
	 instr_out<=0;
	 pc_out<=0;

      end else if (flush==1)begin
	 instr_out<=0;
	 pc_out<=0;
	
      end else if (stay==1)begin
	 instr_out<=0;
	 pc_out<=0;
	
      
      end else if (ihit==1 )begin
	 instr_out<=instr_in;
	 pc_out<=pc_in;

	 
      end else begin
      end
      
   end
endmodule // instr_reg

   
	 

	 
