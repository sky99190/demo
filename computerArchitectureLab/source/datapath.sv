// data path interface
`include "datapath_cache_if.vh"
`include "control_unit_if.vh"
`include "register_file_if.vh"
`include "alu_if.vh"
`include "alu_reg_if.vh"
`include "reg_reg_if.vh"
`include "mem_reg_if.vh"

// alu op, mips op, and instruction type
`include "cpu_types_pkg.vh"

module datapath (
  input logic CLK, nRST,
  datapath_cache_if.dp dpif
);
  // import types
  import cpu_types_pkg::*;
  //parameter PC_INIT = 0;
   word_t new_pc,pcounter,n_pc,n_pc_0;
   logic[13:0] ext_sign;
   word_t Jumpaddr;
   word_t Branchaddr;
   word_t temp_instr;
   word_t r3_pc_out;
   word_t ra;
   word_t fwd0;
   word_t fwd1;
   word_t new_A;
   word_t new_B;
   word_t reg_loc;
   word_t bd;
   word_t bd0;
   word_t Branchaddr0;
   word_t Branchaddr1; 

//   word_t fwd2;
   
   
   
   
   logic stay;
   logic flush;
   logic pcEN;
   logic bs;
   logic bm;
   logic bing;
   logic branch_flush;

   logic [1:0] FWs0;
   logic [1:0] FWs1;
   logic [1:0] FWs2;
   logic [1:0] bc;
   

   
  // pc init
  parameter PC_INIT = 0;

  register_file_if rfif();
  alu_if aluif();
  control_unit_if cuif();
   reg_reg_if rrgif();
   alu_reg_if agif();
   mem_reg_if memg();
   
   
  

   reg_reg r0(.CLK(CLK), .nRST(nRST), .stay(stay), .ihit(dpif.ihit), .rrgif(rrgif),.bf(branch_flush));
   
   alu_reg r1(.CLK(CLK),.nRST(nRST),.ihit(dpif.ihit),.dhit(dpif.dhit),.agif(agif));

   mem_reg r2(.CLK(CLK),.nRST(nRST),.ihit(dpif.ihit),.dhit(dpif.dhit),.memg(memg));

   instr_reg	r3(.CLK(CLK),.nRST(nRST),.ihit(dpif.ihit),.dhit(dpif.dhit),.stay(stay),.flush(flush),.instr_in(dpif.imemload),.pc_in(n_pc),.pc_out(r3_pc_out),.instr_out(temp_instr),.bf(branch_flush),.bm(bm));
 
  control_unit CU(cuif);

  PC pgc(.instr(dpif.imemload),.reg_loc(reg_loc), .CLK(CLK), .nRST(nRST), .pcEN(pcEN), .new_pc(new_pc), .pcounter(pcounter), .n_pc(n_pc),.bm(bm),.bs(bs),.bing(bing),.ihit(dpif.ihit),.PC_INIT(PC_INIT));

  register_file RGF(CLK, nRST, stay, dpif.dhit, dpif.imemload, n_pc, reg_loc, rfif);
  alu ALU(aluif);
  opcode_t opF; 
  assign opF = opcode_t'(dpif.imemload[31:26]);
  funct_t funcF; 
  assign funcF = funct_t'(dpif.imemload[5:0]);

  opcode_t opD; 
  assign opD = opcode_t'(temp_instr[31:26]);
  funct_t funcD; 
  assign funcD = funct_t'(temp_instr[5:0]);

  opcode_t opX; 
  assign opX = opcode_t'(rrgif.instr_out[31:26]);
  funct_t funcX; 
  assign funcX = funct_t'(rrgif.instr_out[5:0]);

  opcode_t opM; 
  assign opM = opcode_t'(agif.instr_out[31:26]);
  funct_t funcM; 
  assign funcM = funct_t'(agif.instr_out[5:0]);


 /* opcode_t opW; 
  assign opW = opcode_t'(memg.instr_out[31:26]);
  funct_t funcW; 
  assign funcW = funct_t'(memg.instr_out[5:0]);
*/




   always_comb begin
      stay=0;
      flush=0;
   
      
      if (((opF==J)||(opF==RTYPE)&&(funcF==JR))&&dpif.dhit==0)begin
	 stay=0;
  	 flush=1;
      
      end else if (opF==JAL&&dpif.dhit==0)begin
	 if (opD==BEQ||opD==BNE||opX==BNE||opX==BEQ)begin
		stay=1;
	 end else begin
		flush=1;
	 end
      end else if ((opD==LW||opD==LUI||opD==LL||opD==SW)&&dpif.dhit==0)begin
         if ((dpif.imemload[25:21]!=0&&dpif.imemload[25:21]==temp_instr[20:16]||dpif.imemload[20:16]!=0&&dpif.imemload[20:16]==temp_instr[20:16])&&(opF==RTYPE||opF==BNE||opF==BEQ||opF==SW||opF==SC||opF==LL))begin
	     stay=1;
         end else if ((dpif.imemload[25:21]!=0)&&(dpif.imemload[25:21]==temp_instr[20:16])&&opF!=RTYPE)begin
             stay=1;
         end else begin
	     stay=0; 
         end

      end else begin	 
         stay=0;
      end // else: !if(opF==RTYPE)
   end // always_comb begin
   


  always_ff @(posedge CLK, negedge nRST)begin
     if (nRST==0)begin
	fwd0<=0;
	fwd1<=0;
     end else if (dpif.ihit==1)begin
	fwd0<=aluif.port_out;
	fwd1<=rfif.wdat;
     end else begin
     end

     if (nRST==0)begin
	FWs0<=0;
     end else if (dpif.dhit==1||dpif.ihit==0)begin
	
     end else if (opD==RTYPE&&rrgif.instr[25:21]!=0&&(rrgif.instr[25:21]==rrgif.instr_out[20:16])&&(opX!=RTYPE)&&(opX!=LW&&opX!=SW&&opX!=BNE&&opX!=BEQ&&opX!=LL&&opX!=SC))begin
	FWs0<=1;
     end else if (opD==RTYPE&&rrgif.instr[25:21]!=0&&rrgif.instr[25:21]==rrgif.instr_out[15:11]&&opX==RTYPE)begin
	FWs0<=1;
     end else if (opD==RTYPE&&rrgif.instr[25:21]!=0&&(rrgif.instr[25:21]==agif.instr_out[20:16])&&(opM!=RTYPE)&&(opM!=LW&&opM!=SW&&opM!=BNE&&opM!=BEQ&&opM!=LL&&opM!=SC))begin
	FWs0<=2;
     end else if (opD==RTYPE&&rrgif.instr[25:21]!=0&&rrgif.instr[25:21]==agif.instr_out[15:11]&&opM==RTYPE)begin
	FWs0<=2;
     end else if ((opD!=SC)&&opD!=RTYPE&&cuif.rs!=0&&cuif.rs==rrgif.instr_out[20:16]&&(opX!=RTYPE&&opX!=LW&&opX!=SW&&opX!=BNE&&opX!=BEQ&&opX!=LL&&opX!=SC))begin
	FWs0<=1;
     end else if ((opD!=SC)&&opD!=RTYPE&&cuif.rs!=0&&cuif.rs==rrgif.instr_out[15:11]&&(opX==RTYPE))begin
	FWs0<=1;
     end else if ((opD!=SC)&&opD!=RTYPE&&cuif.rs!=0&&cuif.rs==agif.instr_out[20:16]&&(opM!=RTYPE&&opM!=LW&&opM!=SW&&opM!=BNE&&opM!=BEQ&&opM!=LL&&opM!=SC))begin
	FWs0<=2;
     end else if ((opD!=SC)&&opD!=RTYPE&&cuif.rs!=0&&cuif.rs==agif.instr_out[15:11]&&(opM==RTYPE))begin
	FWs0<=2;
     end else begin
	FWs0<=0;
     end

     if (nRST==0)begin
	FWs1<=0;
     end else if (dpif.dhit==1||dpif.ihit==0)begin

     end else if (opD==RTYPE&&funcD!=SLL&&funcD!=SRL&&rrgif.instr[20:16]!=0&&(rrgif.instr[20:16]==rrgif.instr_out[20:16])&&(opX!=RTYPE)&&(opX!=SW&&opX!=BNE&&opX!=BEQ&&opX!=SC))begin
	FWs1<=1;
     end else if (opD==RTYPE&&funcD!=SLL&&funcD!=SRL&&rrgif.instr[20:16]!=0&&rrgif.instr[20:16]==rrgif.instr_out[15:11]&&opX==RTYPE)begin
	FWs1<=1;
     end else if (opD==RTYPE&&funcD!=SLL&&funcD!=SRL&&rrgif.instr[20:16]!=0&&(rrgif.instr[20:16]==agif.instr_out[20:16])&&(opM!=RTYPE)&&(opM!=SW&&opM!=BNE&&opM!=BEQ&&opM!=SC))begin
	FWs1<=2;
     end else if (opD==RTYPE&&funcD!=SLL&&funcD!=SRL&&rrgif.instr[20:16]!=0&&rrgif.instr[20:16]==agif.instr_out[15:11]&&opM==RTYPE)begin
	FWs1<=2;
     end else if ((opD==BNE||opD==BEQ)&&cuif.rt!=0&&cuif.rt==rrgif.instr_out[20:16]&&(opX!=RTYPE&&opX!=SW&&opX!=BNE&&opX!=BEQ&&opX!=SC))begin
	FWs1<=1;
     end else if ((opD==BNE||opD==BEQ)&&cuif.rt!=0&&cuif.rt==rrgif.instr_out[15:11]&&(opX==RTYPE))begin
	FWs1<=1;
     end else if ((opD==BNE||opD==BEQ)&&cuif.rt!=0&&cuif.rt==agif.instr_out[20:16]&&(opM!=RTYPE&&opM!=SW&&opM!=BNE&&opM!=BEQ&&opM!=SC))begin
	FWs1<=2;
     end else if ((opD==BNE||opD==BEQ)&&cuif.rt!=0&&cuif.rt==agif.instr_out[15:11]&&(opM==RTYPE))begin
	FWs1<=2;   
     end else begin
	FWs1<=0;
     end

     if (nRST==0)begin
	FWs2<=0;
     end else if (dpif.dhit==1||dpif.ihit==0)begin

     end else if ((opD==SW||opD==SC)&&cuif.rt!=0&&cuif.rt==rrgif.instr_out[20:16]&&(opX!=RTYPE&&opX!=SW&&opX!=BNE&&opX!=BEQ&&opX!=LL&&opX!=SC))begin
	FWs2<=1;
     end else if ((opD==SW||opD==SC)&&cuif.rt!=0&&cuif.rt==rrgif.instr_out[15:11]&&(opX==RTYPE))begin
	FWs2<=1;
     end else if ((opD==SW||opD==SC)&&cuif.rt!=0&&cuif.rt==agif.instr_out[20:16]&&(opM!=RTYPE&&opM!=SW&&opM!=BNE&&opM!=BEQ&&opM!=LL&&opM!=SC))begin
	FWs2<=2;
     end else if ((opD==SW||opD==SC)&&cuif.rt!=0&&cuif.rt==agif.instr_out[15:11]&&(opM==RTYPE))begin
	FWs2<=2;	
      end else begin
	FWs2<=0;
      end
	   
  end
   
   assign bm=bc[1];
   always_ff @(posedge CLK, negedge nRST)begin
   if (nRST==0)begin
 	bc<=0;
   end else if (bing==1&&branch_flush==0)begin
	bc[0]<=0;
   end else if (branch_flush==1&&dpif.dhit==0)begin
	bc<=bc+1;
   end
   end	

  assign ext_sign= (rrgif.instr_imm_out[15]==1) ? 14'b11111111111111 : 14'b0;
  
  assign Jumpaddr={rrgif.n_pc_out[31:28],rrgif.instr_imm_26_out,2'b00};
  
  always_comb begin
	
	Branchaddr0=0;
	Branchaddr1=0;
	if (bm==0&&bs==1)begin
		Branchaddr0=rrgif.n_pc_out+{ext_sign,rrgif.instr_imm_out,2'b0};
	end else if (stay==1)begin
		Branchaddr0=n_pc-4;
	end else if (opF==RTYPE&&funcF==JR)begin
		Branchaddr0=reg_loc;
	end else if (opF==J||opF==JAL)begin
		Branchaddr0={n_pc[31:28],dpif.imemload[25:0],2'b0};
	end else begin
		Branchaddr0=n_pc;
	end

	if (bs==0&&bm==1)begin
		Branchaddr1=rrgif.n_pc_out;
	end else if (stay==1)begin
		Branchaddr1=n_pc-4;
	end else if (opF==RTYPE&&funcF==JR)begin
		Branchaddr1=reg_loc;
	end else if (opF==J||opF==JAL)begin
		Branchaddr1={n_pc[31:28],dpif.imemload[25:0],2'b0};
	end else begin
		Branchaddr1=n_pc;
	end
  end




  assign Branchaddr= bm==1 ? Branchaddr1 : Branchaddr0;
  assign bing=(opX==BNE||opX==BEQ)&&dpif.dhit==0;
  assign bs=(rrgif.BNE_out^aluif.Zero)&&rrgif.PCSrc_out;
  assign bd=(rrgif.n_pc_out+{ext_sign,rrgif.instr_imm_out,2'b0});
  assign bd0=(n_pc+{14'b11111111111111,dpif.imemload[15:0],2'b0});
  assign branch_flush=(bs==1&&bm==0||bs==0&&bm==1)&&(opX==BNE||opX==BEQ)&&dpif.dhit==0;
  //assign stay=0;
  
  assign pcEN=branch_flush||(dpif.ihit && !stay) ;

//dpif out
   assign dpif.imemREN=1;
   assign dpif.dmemWEN=agif.dWEN_out;
   assign dpif.dmemREN=agif.dREN_out;
   
  assign dpif.imemaddr=pcounter;
   
  assign dpif.dmemstore=agif.rdat2_out;
  assign dpif.dmemaddr=agif.port_out_out;

//instr_reg

//register file

  assign rfif.WEN=agif.RegWEN_out& (dpif.ihit | dpif.dhit);
  assign rfif.wsel=agif.RegDst_out==0 ? agif.rd_out : (agif.RegDst_out==1 ? agif.rt_out : 5'b11111);
  assign rfif.rsel1=cuif.rs;
  assign rfif.rsel2=cuif.rt;

  assign rfif.wdat=agif.LUI_out ? {agif.instr_imm_out,16'b0}: (agif.JAL_out ? agif.n_pc_out : (agif.MtR_out==1 ? dpif.dmemload : agif.port_out_out));

//reg_reg
   assign  rrgif.instr=temp_instr;
   assign  rrgif.rdat1=rfif.rdat1;   
   assign  rrgif.rdat2=rfif.rdat2;
   assign  rrgif.instr_imm_26=cuif.instr_imm_26;
   assign  rrgif.n_pc=r3_pc_out;
   assign  rrgif.PCSrc=cuif.PCSrc;
   assign  rrgif.MtR=cuif.MtR;
   assign  rrgif.RegWEN=cuif.RegWEN;
   assign  rrgif.JAL=cuif.JAL;
   assign  rrgif.halt=cuif.halt;
   assign  rrgif.dWEN=cuif.dWEN;
   assign  rrgif.dREN=cuif.dREN;
   assign  rrgif.imemREN=cuif.imemREN;
   assign  rrgif.LUI=cuif.LUI;
   assign  rrgif.BNE=cuif.BNE;
   assign  rrgif.aluop=cuif.aluop;
   assign  rrgif.ALUs=cuif.ALUs;
   assign  rrgif.RegDst=cuif.RegDst;
   assign  rrgif.Jumps=cuif.Jumps;
   assign  rrgif.rs=cuif.rs;
   assign  rrgif.rt=cuif.rt;
   assign  rrgif.rd=cuif.rd;
   assign  rrgif.instr_imm=cuif.instr_imm;
   assign  rrgif.shamt=cuif.shamt;
//ALU
  
  assign  new_A= FWs0==1 ? fwd0 : (FWs0==2 ? fwd1 : 0 );
  assign  new_B= FWs1==1 ? fwd0 : (FWs1==2 ? fwd1 : 0 );
  assign aluif.port_A= FWs0!=0 ? new_A : rrgif.rdat1_out;
  //assign spy=FWs1!=0 ? new_B : rrgif.rdat2_out;
  assign aluif.port_B= rrgif.ALUs_out==1?  rrgif.shamt_out : FWs1!=0 ? new_B : rrgif.ALUs_out==0 ? rrgif.rdat2_out:  (rrgif.ALUs_out==2&&rrgif.instr_imm_out[15]==1) ? {16'hFFFF, rrgif.instr_imm_out} : {16'h0, rrgif.instr_imm_out};
  assign aluif.aluop=rrgif.aluop_out;

//alu_reg
  assign agif.rdat2= FWs2==1 ? fwd0 : (FWs2==2 ? fwd1 : rrgif.rdat2_out );
  assign agif.instr=rrgif.instr_out;
  assign agif.MtR=rrgif.MtR_out;
  assign agif.JAL=rrgif.JAL_out;	 
  assign agif.RegWEN=rrgif.RegWEN_out;
  assign agif.halt=rrgif.halt_out;
  assign agif.dWEN=rrgif.dWEN_out;
  assign agif.dREN=rrgif.dREN_out;
  assign agif.imemREN=rrgif.imemREN_out;
  assign agif.LUI=rrgif.LUI_out;
  assign agif.RegDst=rrgif.RegDst_out;
  assign agif.rt=rrgif.rt_out;
  assign agif.rd=rrgif.rd_out;
  assign agif.port_out=aluif.port_out;
  assign agif.instr_imm=rrgif.instr_imm_out;
  assign agif.n_pc=rrgif.n_pc_out;


/*
	 memg.instr;
	 memg.port_out;
	 memg.n_pc;
	 memg.JAL;
	 memg.LUI;
	 memg.MtR;
	 memg.dmemload;
	 memg.RegWEN;
	 memg.RegDst;
	 memg.instr_imm;
	 memg.rt; 
	 memg.rd;
	 memg.imemREN;
	 memg.halt;
*/
//PC
  assign new_pc=rrgif. Jumps_out==0 ? n_pc: (rrgif.Jumps_out==1 ? Jumpaddr : (rrgif.Jumps_out==2 ? rrgif.rdat1_out : Branchaddr));

//control unit
  assign cuif.instr=temp_instr;



  always_ff @ (posedge CLK, negedge nRST) begin
   if (nRST==0)begin
      	dpif.halt<=0;
   end else if (agif.halt_out==1) begin
	dpif.halt<=1;
   end else begin
   end
end

	
assign dpif.datomic=opM==LL||opM==SC;


endmodule
