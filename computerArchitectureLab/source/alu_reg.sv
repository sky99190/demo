`include "cpu_types_pkg.vh"
`include "alu_reg_if.vh"


 module alu_reg

(input logic CLK, nRST,ihit,dhit,alu_reg_if.auu agif);
   import cpu_types_pkg::*;
   always_ff @(posedge CLK, negedge nRST)begin
      if (nRST==0)begin
	 agif.rdat2_out<=0;
	 agif.instr_out<=0;
	 agif.MtR_out<=0;
	 agif.JAL_out<=0;	 
	 agif.RegWEN_out<=0;
	 agif.halt_out<=0;
	 agif.dWEN_out<=0;
	 agif.dREN_out<=0;
	 agif.imemREN_out<=1;
	 agif.LUI_out<=0;
	 agif.RegDst_out<=0;
	 agif.rt_out<=0;
	 agif.rd_out<=0;
	 agif.port_out_out<=0;
	 agif.instr_imm_out<=0;
	 agif.n_pc_out<=0;
	 
      end else if (dhit==1)begin // if (nRST==0)
	 agif.rdat2_out<=0;
	 agif.instr_out<=0;
	 agif.MtR_out<=0;   
	 agif.RegWEN_out<=0;
	 agif.halt_out<=0;
	 agif.JAL_out<=0;
	 agif.dWEN_out<=0;
	 agif.dREN_out<=0;
	 agif.imemREN_out<=1;
	 agif.LUI_out<=0;
	 agif.RegDst_out<=0;
	 agif.rt_out<=0;
	 agif.rd_out<=0;
	 agif.port_out_out<=0;
	 agif.instr_imm_out<=0;
	 agif.n_pc_out<=0;
	 
      end else if (ihit==1)begin // if ()
	 agif.rdat2_out<=agif.rdat2;
	 agif.instr_out<=agif.instr;
	 agif.MtR_out<=agif.MtR;   
	 agif.RegWEN_out<=agif.RegWEN;
	 agif.halt_out<=agif.halt;
	 agif.JAL_out<=agif.JAL;
	 agif.dWEN_out<=agif.dWEN;
	 agif.dREN_out<=agif.dREN;
	 agif.imemREN_out<=agif.imemREN;
	 agif.LUI_out<=agif.LUI;
	 agif.RegDst_out<=agif.RegDst;
	 agif.rt_out<=agif.rt;
	 agif.rd_out<=agif.rd;
	 agif.port_out_out<=agif.port_out;
	 agif.instr_imm_out<=agif.instr_imm;
	 agif.n_pc_out<=agif.n_pc;
	 
      end else begin
      end
   end // always_ff @
endmodule // alu_reg

      
      
