`include "alu_if.vh"
`include "cpu_types_pkg.vh"

module alu(
	   alu_if.alu alublock
	   );
   import cpu_types_pkg::*;

   always_comb begin
      alublock.port_out=0;
      alublock.Overflow=0;
      casez(alublock.aluop)
	ALU_SLL:begin
	   alublock.port_out=alublock.port_A << alublock.port_B;
	   end
	  
	ALU_SRL:begin
	   alublock.port_out=alublock.port_A >> alublock.port_B;
	   end
	ALU_ADD:begin
	   alublock.port_out=$signed(alublock.port_A) + $signed(alublock.port_B);
	   //if((alublock.port_A[31]==alublock.port_B[31])&&(alublock.port_A[31]!=alublock.port_out[31]) alublock.Overflow=1;
	     // else alublock.Overflow=0;
	   alublock.Overflow=(alublock.port_A[31]==alublock.port_B[31])&&(alublock.port_A[31]!=alublock.port_out[31])?1:0;
	   end
	ALU_SUB:begin
	   alublock.port_out=$signed(alublock.port_A) - $signed(alublock.port_B);
	     // if((alublock.port_A[31]!=alublock.port_B[31])&&(alublock.port_A[31]!=alublock.port_out[31]) alublock.Overflow=1;
	     // else alublock.Overflow=0;
	   alublock.Overflow=(alublock.port_A[31]!=alublock.port_B[31])&&(alublock.port_A[31]!=alublock.port_out[31])?1:0;
	end
	ALU_AND:begin
	   alublock.port_out=alublock.port_A & alublock.port_B;
	   end
	ALU_OR:begin
	   alublock.port_out=alublock.port_A | alublock.port_B;
	   end
	ALU_XOR:begin
	   alublock.port_out=alublock.port_A ^ alublock.port_B;
	   end
	ALU_NOR:begin
	   alublock.port_out=~(alublock.port_A | alublock.port_B);
	   end
	ALU_SLT:begin
	   alublock.port_out=$signed(alublock.port_A) < $signed(alublock.port_B);
	   end
	ALU_SLTU:begin
	   alublock.port_out=$unsigned(alublock.port_A) < $unsigned(alublock.port_B);
	end
      endcase // casez (alublock.aluop)
   end // always_comb

   assign alublock.Zero=alublock.port_out==0;
   assign alublock.Negative=alublock.port_out[31];

endmodule // alu
