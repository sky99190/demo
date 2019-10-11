`include "cpu_types_pkg.vh"
`include "reg_reg_if.vh"
 import cpu_types_pkg::*;
module reg_reg(
   input logic 	       CLK, nRST,stay,ihit,bf,
   reg_reg_if.rrg rrgif
   );

   always_ff @(posedge CLK, negedge nRST)begin
      if (nRST==0)begin
	 rrgif.instr_out<=0;
	 rrgif.rdat1_out<=0;
	 rrgif.rdat2_out<=0;
	 rrgif.instr_imm_26_out<=0;
	 rrgif.n_pc_out<=0;
	 rrgif.PCSrc_out<=0;
	 rrgif.MtR_out<=0;
	 rrgif.RegWEN_out<=0;
	 rrgif.JAL_out<=0;
	 rrgif.halt_out<=0;
	 rrgif.dWEN_out<=0;
	 rrgif.dREN_out<=0;
	 rrgif.imemREN_out<=1;
	 rrgif.LUI_out<=0;
	 rrgif.BNE_out<=0;
	 rrgif.aluop_out<=ALU_SLL;
	 rrgif.ALUs_out<=0;
	 rrgif.RegDst_out<=0;
	 rrgif.Jumps_out<=0;
	 rrgif.rs_out<=0;
	 rrgif.rt_out<=0;
	 rrgif.rd_out<=0;
	 rrgif.instr_imm_out<=0;
	 rrgif.shamt_out<=0;
	 rrgif.immload_out<=0;
      end else if (bf==1)begin // if (nRST==0)
	 rrgif.instr_out<=0;
	 rrgif.rdat1_out<=0;
	 rrgif.rdat2_out<=0;
	 rrgif.instr_imm_26_out<=0;
	 rrgif.n_pc_out<=0;
	 rrgif.PCSrc_out<=0;
	 rrgif.MtR_out<=0;
	 rrgif.RegWEN_out<=0;
	 rrgif.JAL_out<=0;
	 rrgif.halt_out<=0;
	 rrgif.dWEN_out<=0;
	 rrgif.dREN_out<=0;
	 rrgif.imemREN_out<=1;
	 rrgif.LUI_out<=0;
	 rrgif.BNE_out<=0;
	 rrgif.aluop_out<=ALU_SLL;
	 rrgif.ALUs_out<=0;
	 rrgif.RegDst_out<=0;
	 rrgif.Jumps_out<=0;
	 rrgif.rs_out<=0;
	 rrgif.rt_out<=0;
	 rrgif.rd_out<=0;
	 rrgif.instr_imm_out<=0;
	 rrgif.shamt_out<=0;
	 rrgif.immload_out<=0;
      end else if (ihit==1)begin // if (flush==1 || stay==1)
	 rrgif.instr_out<=rrgif.instr;
	 rrgif.rdat1_out<=rrgif.rdat1;
	 rrgif.rdat2_out<=rrgif.rdat2;
	 rrgif.instr_imm_26_out<=rrgif.instr_imm_26;
	 rrgif.n_pc_out<=rrgif.n_pc;
	 rrgif.PCSrc_out<=rrgif.PCSrc;
	 rrgif.MtR_out<=rrgif.MtR;
	 rrgif.RegWEN_out<=rrgif.RegWEN;
	 rrgif.JAL_out<=rrgif.JAL;
	 rrgif.halt_out<=rrgif.halt;
	 rrgif.dWEN_out<=rrgif.dWEN;
	 rrgif.dREN_out<=rrgif.dREN;
	 rrgif.imemREN_out<=rrgif.imemREN;
	 rrgif.LUI_out<=rrgif.LUI;
	 rrgif.BNE_out<=rrgif.BNE;
	 rrgif.aluop_out<=rrgif.aluop;
	 rrgif.ALUs_out<=rrgif.ALUs;
	 rrgif.RegDst_out<=rrgif.RegDst;
	 rrgif.Jumps_out<=rrgif.Jumps;
	 rrgif.rs_out<=rrgif.rs;
	 rrgif.rt_out<=rrgif.rt;
	 rrgif.rd_out<=rrgif.rd;
	 rrgif.instr_imm_out<=rrgif.instr_imm;
	 rrgif.immload_out<=rrgif.immload;
	 rrgif.shamt_out<=rrgif.shamt;
      end else begin
      end // else: !if(ihit==1)

     
	 
   end // always_ff @
   
endmodule // pip_reg


   
   
