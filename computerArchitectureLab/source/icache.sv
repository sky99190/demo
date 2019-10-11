`include "cpu_types_pkg.vh"
`include "datapath_cache_if.vh"
`include "caches_if.vh"
import cpu_types_pkg::*;

module icache (
	input logic CLK, nRST,
	datapath_cache_if dcif,
	caches_if.icache cif
);

   integer 	    i;
   logic [25:0]     tag [15:0];
   logic [3:0] 	    index;
   logic [15:0]     valid;
   word_t data[15:0];

   
   logic 	    miss;

   assign index=dcif.imemaddr[5:2];
   assign cif.iREN= miss ? dcif.imemREN : 0;
   assign cif.iaddr= miss ? dcif.imemaddr : 0;
   
   always_ff @(posedge CLK, negedge nRST)begin
	if (nRST==0)begin
	 for (i=0;i<16;i++)begin
	    tag[i]<=0;
	    data[i]<=0;
	    valid[i]<=0;
	    end
	 end else if (cif.iwait==0)begin
	    tag[index]<=dcif.imemaddr[31:6];
	    data[index]<=cif.iload;
	    valid[index]<=1;
	 end else begin
	   
	 end
	end // if (nRST==0)
      
   
	always_comb begin
	   if(dcif.halt==1)begin
	      miss=0;
	      dcif.ihit=0;
	      dcif.imemload=0;
	   end else if(dcif.imemREN==1 && dcif.dmemREN==0 && dcif.dmemWEN==0)begin
	      if (valid[index]==1 && dcif.imemaddr[31:6]==tag[index])begin
		 miss=0;
		 dcif.ihit=1;
		 dcif.imemload=data[index];
	      end else begin
		 miss=1;
		 dcif.ihit=~cif.iwait;
		 dcif.imemload=cif.iload;
	      end
	   end else begin // if (dcif.imemREN==1 && dcif.dmemREN==0 && dcif.dmemWEN==0)
	      miss=0;
	      dcif.ihit=0;
	      dcif.imemload=0;
	   end // else: !if(dcif.imemREN==1 && dcif.dmemREN==0 && dcif.dmemWEN==0)
	end // always_comb

   

endmodule // icache
