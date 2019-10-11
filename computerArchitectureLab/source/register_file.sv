
`include "register_file_if.vh"
`include "cpu_types_pkg.vh"
import cpu_types_pkg::*;
module register_file(
  input logic CLK, nRST,stay,dhit,
  input word_t instr,n_pc,
  output word_t reg_loc,
  register_file_if.rf rfif
  
  
);
   logic [31:0]	     data[31:0];
   int 		     i;
   
   
  // assign data[0]=0;
   
   
 

  always_ff @(posedge CLK or negedge nRST)
  begin
    if (!nRST)
    begin
       for (i=0;i<32;i=i+1)begin
            data[i]<='0;
       end
       
    end else begin
      if (rfif.WEN && rfif.wsel!=0)begin
	 data[rfif.wsel]<=rfif.wdat;
      end else begin
      end
       
    end // else: !if(!nRST)
     
    if (nRST==0)begin
       data[5'b11111]<=0;
    end else if (stay==1||dhit==1)begin
    end else if (instr[31:26]==6'b11)begin
       data[5'b11111]<=n_pc;
    end else begin
    end
   
  end
  assign rfif.rdat1=data[rfif.rsel1];
  assign rfif.rdat2=data[rfif.rsel2];
  assign reg_loc=data[instr[25:21]];
   
     
endmodule
