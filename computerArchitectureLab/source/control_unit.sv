`include "control_unit_if.vh"
`include "cpu_types_pkg.vh"


module control_unit(
		    control_unit_if.ctu cuif
		    );

   import cpu_types_pkg::*;

   

   always_comb begin
      cuif.LUI=0; 
      cuif.BNE=0; 
      cuif.aluop=ALU_SLL;
      cuif.ALUs=0; 
      cuif.RegDst=0;  
      cuif.Jumps=0; 
      cuif.rs=0; 
      cuif.rt=0; 
      cuif.rd=0; 
      cuif.instr_imm=0; 
      cuif.shamt=0;
      cuif.PCSrc=0; 
      cuif.MtR=0; 
      cuif.RegWEN=0;  
      cuif.JAL=0;  
      cuif.halt=0;  
      cuif.dWEN=0;  
      cuif.dREN=0;  
      cuif.imemREN=1;
      cuif.rs=cuif.instr[25:21];
      cuif.rt=cuif.instr[20:16];
      cuif.instr_imm=cuif.instr[15:0];
      cuif.instr_imm_26=cuif.instr[25:0];
      cuif.rd=cuif.instr[15:11];
      cuif.shamt=cuif.instr[10:6];
      
      if (cuif.instr[31:26]==6'b000000)begin
	  //cuif.rs=cuif.instr[25:21];
          //cuif.rt=cuif.instr[20:16];
          //cuif.rd=cuif.instr[15:11];
	  cuif.RegDst=0;
	  //cuif.shamt={27'b0,cuif.instr[10:6]};
	 
	 casez(cuif.instr[5:0])
	   SLL: begin
	      cuif.aluop=ALU_SLL;
	      cuif.ALUs=2'b01;
	      cuif.RegWEN=1;
	   end

	   SRL: begin
	      cuif.aluop=ALU_SRL;
	      cuif.ALUs=2'b01;
	      cuif.RegWEN=1;
	   end

	   ADDU: begin
	      cuif.aluop=ALU_ADD;
	      cuif.RegWEN=1;
	   end

	   ADD: begin
	      cuif.aluop=ALU_ADD;
	      cuif.RegWEN=1;
	   end

	   SUB: begin
	      cuif.aluop=ALU_SUB;
	      cuif.RegWEN=1;
	   end

	   SUBU:begin
	      cuif.aluop=ALU_SUB;
	      cuif.RegWEN=1;
	   end

	   AND: begin
	      cuif.aluop=ALU_AND;
	      cuif.RegWEN=1;
	   end

	   OR:begin
	      cuif.aluop=ALU_OR;
	      cuif.RegWEN=1;
	   end

	   XOR:begin
	      cuif.aluop=ALU_XOR;
	      cuif.RegWEN=1;
	   end

	   NOR:begin
	      cuif.aluop=ALU_NOR;
	      cuif.RegWEN=1;
	   end

	   SLT:begin
	      cuif.aluop=ALU_SLT;
	      cuif.RegWEN=1;
	   end

	   SLTU:begin
	      cuif.aluop=ALU_SLTU;
	      cuif.RegWEN=1;
	   end

	   JR:begin
	      cuif.Jumps=2;
	   end

	   
	   

	 endcase // casez (cuif.instr[5:0])
      end else if (cuif.instr[31:26]==6'b000011) begin // if (cuif.instr[31:26]==RTYPE)
	 cuif.JAL=1;
	 cuif.RegDst=2;
	 cuif.Jumps=1;
	 cuif.RegWEN=1;
      end else if (cuif.instr[31:26]==6'b000010) begin
	 cuif.Jumps=1;
	 cuif.RegDst=2;
	 
      end else begin
	 cuif.RegDst=1;
	 //cuif.rs=cuif.instr[25:21];
	 //cuif.rt=cuif.instr[20:16];
	 //cuif.instr_imm=cuif.instr[15:0];
         //cuif.instr_imm_26=cuif.instr[25:0];
	 casez(cuif.instr[31:26])
	   BEQ:begin
	      cuif.aluop=ALU_SUB;
	      cuif.PCSrc=1;
	      cuif.Jumps=3;
	      
	   end
	   BNE:begin
	      cuif.aluop=ALU_SUB;
	      cuif.BNE=1;
	      cuif.PCSrc=1;
	      cuif.Jumps=3;
	      
	   end
	   ADDI:begin
	      cuif.aluop=ALU_ADD;
	      cuif.ALUs=2;
	      cuif.RegWEN=1;    
	   end
	   
	   ADDIU:begin
	      cuif.aluop=ALU_ADD;
	      cuif.ALUs=2;
	      cuif.RegWEN=1;
	      
	   end
	   SLTI:begin
	      cuif.aluop=ALU_SLT;
	      cuif.ALUs=2;
	      cuif.RegWEN=1;
	   end
	   SLTIU:begin
	      cuif.aluop=ALU_SLT;
	      cuif.ALUs=2;
	      cuif.RegWEN=1;
	   end
	   ANDI:begin
	      cuif.aluop=ALU_AND;
	      cuif.ALUs=3;
	      cuif.RegWEN=1;
	   end
	   ORI:begin
	      cuif.aluop=ALU_OR;
	      cuif.ALUs=3;
	      cuif.RegWEN=1;
	   end
	   XORI:begin
	      cuif.aluop=ALU_XOR;
	      cuif.ALUs=3;
	      cuif.RegWEN=1;
	   end
	   LUI:begin
	      cuif.LUI=1;
	      cuif.RegWEN=1;
	      
	   end
	   LW:begin
	      cuif.RegWEN=1;
	      cuif.MtR=1;
	      cuif.ALUs=2;
	      cuif.dREN=1;
	      cuif.aluop=ALU_ADD;
	      
	   end
	   SW:begin
	      cuif.dWEN=1;
	      cuif.aluop=ALU_ADD;
	      cuif.ALUs=2;
	      
	   end
	   HALT:begin
	      cuif.halt=1;
	   end

	   LL:begin
		cuif.aluop=ALU_ADD;
		cuif.ALUs=2;
		cuif.MtR=1;
		cuif.dREN=1;
	   end

	   SC:begin
		cuif.aluop=ALU_ADD;
		cuif.ALUs=2;
		cuif.MtR=1;
		cuif.dWEN=1;
	   end
	      
	   

	  
	     
	 endcase // casez (cuif.instr[31:26])
      end // else: !if(cuif.instr[31:26]==J)
   end // always_comb begin
endmodule // control_unit

      
	 
	
	 
	   
	       

	   
      
	      
	 
	 
	 
   
