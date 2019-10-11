`include "cpu_types_pkg.vh"
`include "mem_reg_if.vh"
import cpu_types_pkg::*;
module mem_reg(
	       input logic 	   CLK, nRST, ihit, dhit,
	       mem_reg_if.megf memg
	       );
   always_ff @(posedge CLK, negedge nRST) begin
      if (nRST==0)begin
	 memg.instr_out<=0;
	 memg.port_out_out<=0;
	 memg.n_pc_out<=0;
	 memg.JAL_out<=0;
	 memg.LUI_out<=0;
	 memg.MtR_out<=0;
	 memg.dmemload_out<=0;
	 memg.RegWEN_out<=0;
	 memg.RegDst_out<=0;
	 memg.instr_imm_out<=0;
	 memg.rt_out<=0; 
	 memg.rd_out<=0;
	 memg.imemREN_out<=1;
	 memg.halt_out<=0;
      end else if (ihit || dhit )begin // if (nRST==1)
	 memg.instr_out<=memg.instr;
	 memg.port_out_out<=memg.port_out;
	 memg.n_pc_out<=memg.n_pc;
	 memg.JAL_out<=memg.JAL;
	 memg.LUI_out<=memg.LUI;
	 memg.MtR_out<=memg.MtR;
	 memg.dmemload_out<=memg.dmemload;
	 memg.RegWEN_out<=memg.RegWEN;
	 memg.RegDst_out<=memg.RegDst;
	 memg.instr_imm_out<=memg.instr_imm;
	 memg.rt_out<=memg.rt; 
	 memg.rd_out<=memg.rd;
	 memg.imemREN_out<=memg.imemREN;
	 memg.halt_out<=memg.halt;
      end // if (ihit | dhit )
      else begin
      end // else: !if(ihit | dhit )
   end // always_ff @
endmodule // mem_reg

	 
