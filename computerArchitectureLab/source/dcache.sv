`include "cpu_types_pkg.vh"
`include "datapath_cache_if.vh"
`include "caches_if.vh"
import cpu_types_pkg::*;

module dcache (
	input logic CLK, nRST,
	datapath_cache_if dcif,
	caches_if.dcache cif
);

typedef enum logic[4:0] {
	IDLE, WRITE, WRITE_1, WRITE_2, WRITE_3, READ, READ_1, READ_2, DYING, FLUSH1, FLUSH2, WRITE_CNT, HALT, CHECKING, SHARING1,SHARING2, INV
} state_t;

   state_t state;
   state_t next_state;
   dcachef_t cachef, snoopf;

   word_t vv[7:0];
   word_t vw[7:0];
   word_t wv[7:0];
   word_t ww[7:0];
   logic [25:0]v_tag [7:0];
   logic [25:0]w_tag [7:0];
   logic [7:0] valid_v;
   logic [7:0] valid_w;
   logic [7:0] dirty_v;
   logic [7:0] dirty_w;
   logic [4:0] cc;
   logic [4:0] cc_next;
   logic       ven,wen,xven,xwen;
   logic [7:0] nb;
   logic nb_next;
   logic [2:0] cdex;
   logic j,next_j;
   logic [1:0] snoop_hit, next_snoop_hit;
   logic snoop_dt;

   //logic [2:0] index;
   word_t count,count_next;
   //logic       offset;
   logic       miss;
   integer     i;
   //logic [25:0] tag;
   
   logic [25:0]v_tag_next ;
   logic [25:0]w_tag_next ;
   logic   valid_v_next;
   logic   valid_w_next;
   word_t vv_next,vw_next,wv_next,ww_next;
   word_t dirty_v_next,dirty_w_next;
   logic cs;


   word_t link_reg, next_link_reg;
   logic valid_link, next_valid_link;
   assign cdex=cc[2:0]-1;
   
   //assign index=dcif.dmemaddr[5:3];
   //assign tag=dcif.dmemaddr[32:6];
   //assign offset=dcif.dmemaddr[2];
   assign cachef=dcachef_t'(dcif.dmemaddr);
   assign snoopf=dcachef_t'(cif.ccsnoopaddr);

   //assign dcif.dhit = (dcif.dmemREN==1&&((v_tag[cachef.idx] == cachef.tag && valid_v[cachef.idx] == 1) || (w_tag[cachef.idx] == cachef.tag && valid_w[cachef.idx] == 1))||dcif.dmemWEN==1&&((v_tag[cachef.idx] == cachef.tag) || (w_tag[cachef.idx] == cachef.tag))) ? 1'b1 : 1'b0;
   

   assign cs=state==CHECKING||state==SHARING1||state==SHARING2;

   always_ff @(posedge CLK, negedge nRST)begin
      if (nRST==0)begin
	 
	 count<=0;
	 state<=IDLE;
	 cc<=0;
	 j<=0;
	 snoop_hit<=0;
	 link_reg<=0;
	 valid_link<=0;
	 for (i=0;i<8;i++)begin
	    vv[i]<=0;
	    vw[i]<=0;
	    wv[i]<=0;
	    ww[i]<=0;
	    v_tag[i]<=0;
	    w_tag[i]<=0;
	    valid_v[i]<=0;
	    valid_w[i]<=0;
	    dirty_v[i]<=0;
	    dirty_w[i]<=0;
	    nb[i]<=0;
	    
	 end
      end else if (cs)begin
	 vv[snoopf.idx]<=vv_next;
	 vw[snoopf.idx]<=vw_next;
	 wv[snoopf.idx]<=wv_next;
	 ww[snoopf.idx]<=ww_next;
	 valid_v[snoopf.idx]<=valid_v_next;
	 valid_w[snoopf.idx]<=valid_w_next;
	 dirty_v[snoopf.idx]<=dirty_v_next;
	 dirty_w[snoopf.idx]<=dirty_w_next;
	 v_tag[snoopf.idx]<=v_tag_next;
	 w_tag[snoopf.idx]<=w_tag_next;
	 state<=next_state;
	 count<=count_next;
	 cc<=cc_next;
	 nb[snoopf.idx]<=nb_next;
	 j<=next_j;
	 snoop_hit<=next_snoop_hit;

	 link_reg<=next_link_reg;
	 valid_link<=next_valid_link;

      end else begin // if (nRST==0)
	 vv[cachef.idx]<=vv_next;
	 vw[cachef.idx]<=vw_next;
	 wv[cachef.idx]<=wv_next;
	 ww[cachef.idx]<=ww_next;
	 
	 valid_v[cachef.idx]<=valid_v_next;
	 valid_w[cachef.idx]<=valid_w_next;
	 dirty_v[cachef.idx]<=dirty_v_next;
	 dirty_w[cachef.idx]<=dirty_w_next;
	 v_tag[cachef.idx]<=v_tag_next;
	 w_tag[cachef.idx]<=w_tag_next;
	 state<=next_state;
	 count<=count_next;
	 cc<=cc_next;
	 nb[cachef.idx]<=nb_next;
	 j<=next_j;
	 snoop_hit<=next_snoop_hit;

	 link_reg<=next_link_reg;
	 valid_link<=next_valid_link;

      end // else: !if(nRST==0)
   end // always_ff @
   

   always_comb begin
      next_state=state;
      cc_next=cc;
      next_snoop_hit=snoop_hit;
      snoop_dt=0;
      cif.cctrans=0;
     
      
      case(state)
	IDLE:begin
	   if (dcif.halt==1)begin
	      next_state=DYING;
	   end else if (cif.ccwait==1)begin
	      next_state=CHECKING;
	   end else if (miss==1)begin
	      if (nb[cachef.idx]==0)begin
		 cif.cctrans=~dirty_v[cachef.idx];
		 if (dirty_v[cachef.idx]==1)begin
		    next_state=WRITE_1;
		 end else begin
		    next_state=READ_1;
		 end

	      end else begin
		 cif.cctrans=~dirty_w[cachef.idx];
		 if (dirty_w[cachef.idx]==1)begin
		    next_state=WRITE_1;
		 end else begin
		    next_state=READ_1;
		 end
	      end
	   end else begin
	      next_state=IDLE;
	   end
	   
	   
	end // case: IDLE
	

	WRITE_1:begin
	   if (cif.dwait==0)begin
	      next_state=WRITE_2;
	   end else begin
	      next_state=WRITE_1;
	   end
	end

	WRITE_2:begin
	   if (cif.dwait==0)begin
	      next_state=READ_1;
	   end else begin
	      next_state=WRITE_2;
	   end
	end
	   
	

	READ_1:begin
	   cif.cctrans = ~cif.ccwait;
	   if (cif.ccwait==1)begin
	      next_state=CHECKING;
	   end else if (cif.dwait==0)begin
	      next_state=READ_2;
	   end else begin
	      next_state=READ_1;
	   end
	end
	
	
	

	READ_2:begin
	   if (cif.dwait==0)begin
	      next_state=IDLE;
	   end else begin
	      next_state=READ_2;
	   end
	end
     
	DYING:begin
	   cc_next=cc+1;
	   
	   if (cc==5'b10000)begin
	      next_state=HALT;
	   end else if ((cc[3]==0&&dirty_v[cc[2:0]]==1&&valid_v[cc[2:0]]==1)||(cc[3]==1&&dirty_w[cc[2:0]]==1&&valid_w[cc[2:0]]==1))begin
	      next_state=FLUSH1;
	   end else begin
	      next_state=DYING;
	   end
	   
	end
	
    
	
	
	FLUSH1:begin
	   
	   
	   if (cif.dwait==0)begin
	      next_state=FLUSH2;
	   end else begin
	      next_state=FLUSH1;
	   end
	   
	end
	
	FLUSH2:begin
	   
	   
	   if (cif.dwait==0)begin
	      next_state=DYING;
	   end else begin
	      next_state=FLUSH2;
	   end
	end
	
	WRITE_CNT:begin
	   if (cif.dwait==0)begin
	      next_state=HALT;
	   end else begin
	      next_state=WRITE_CNT;
	   end
	   
	end

	HALT:begin
	   next_state=HALT;
	   
	end


	CHECKING:begin
	   

	   if(cif.ccwait==1)begin

	      if (snoopf.tag==v_tag[snoopf.idx])begin
		next_snoop_hit[0]=1;
		snoop_dt=dirty_v[snoopf.idx];
		next_state=snoop_dt==1 ? SHARING1 : CHECKING;
	      end else begin
		next_snoop_hit[0]=0;
	      end

	      if (snoopf.tag==w_tag[snoopf.idx])begin
		next_snoop_hit[1]=1;
		snoop_dt=dirty_w[snoopf.idx];
		next_state=snoop_dt==1 ? SHARING1 : CHECKING;
	      end else begin
		next_snoop_hit[1]=0;
	      end

	      if(next_snoop_hit==0) begin
		next_state=CHECKING;
	      end
	
	      cif.cctrans = snoop_dt;

	   end else begin
	      next_state=IDLE;
	   end

	

	end // case: CHECKING
	
	
	SHARING1:begin

	   if (cif.dwait == 0 ) begin
	      next_state=SHARING2;
	   end else begin
	      next_state=SHARING1;
	   end
	end
	
	
	SHARING2:begin

	   if (cif.dwait == 0 ) begin
	      next_state=INV;
	   end else begin
	      next_state=SHARING2;
	   end
	end
	


	INV:begin
	    next_state=IDLE;
	end
	
      endcase // casez (state)

	
      
   end // block: next_state=state;
   
   


  





	 
   always_comb begin 
      v_tag_next= cs==0 ? v_tag[cachef.idx] : v_tag[snoopf.idx];
      w_tag_next = cs==0 ? w_tag[cachef.idx] : w_tag[snoopf.idx];
      valid_v_next= cs==0 ? valid_v[cachef.idx] : valid_v[snoopf.idx];
      valid_w_next= cs==0 ? valid_w[cachef.idx] : valid_w[snoopf.idx];
      vv_next= cs==0 ? vv[cachef.idx] : vv[snoopf.idx];
      vw_next= cs==0 ? vw[cachef.idx] : vw[snoopf.idx];
      wv_next= cs==0 ? wv[cachef.idx] : wv[snoopf.idx];
      ww_next= cs==0 ? ww[cachef.idx] : ww[snoopf.idx];
      dirty_v_next= cs==0 ? dirty_v[cachef.idx] : dirty_v[snoopf.idx];
      dirty_w_next= cs==0 ? dirty_w[cachef.idx] : dirty_w[snoopf.idx];
      count_next=count;
      nb_next= cs==0 ? nb[cachef.idx] : nb[snoopf.idx];
      cif.dstore=0;
      cif.dREN=0;
      cif.dWEN=0;
      cif.daddr=0;
      miss=0;
      dcif.dhit=0;
      dcif.dmemload=0;
      next_link_reg=link_reg;
      next_valid_link=valid_link;
      
      
      
      case(state)
	IDLE:begin
	   if (dcif.halt==1) begin


	   end else if (dcif.dmemREN==1) begin//416
	      if (dcif.datomic==1)begin//417
		 next_link_reg=dcif.dmemaddr;
		 next_valid_link=1;
	      end else begin
	      end

	      if ((cachef.tag == v_tag[cachef.idx]) && valid_v[cachef.idx]==1) begin		       
		 dcif.dmemload = xwen==1 ? vw[cachef.idx]:vv[cachef.idx];
		 nb_next = 1;
		 dcif.dhit=1;
		 count_next=count+1;
		 
	      end else if ((cachef.tag == w_tag[cachef.idx]) && valid_w[cachef.idx]==1) begin
		 dcif.dmemload = xwen==1 ? ww[cachef.idx]:wv[cachef.idx];
		 nb_next = 0;
		 dcif.dhit=1;	
		 count_next=count+1;
		 
	      end else begin
		 miss = 1;
		 count_next=count-1;
		 
		 if (nb[cachef.idx]==0)begin
			dirty_v_next=0;
			valid_v_next=1;
		 end else begin
			dirty_w_next=0;
			valid_w_next=1;
		 end
	 		
		 
	      end
	   end else if (dcif.dmemWEN==1) begin      //~416,449
	     if (dcif.datomic==1)begin              //450
		dcif.dmemload=((dcif.dmemaddr==link_reg)&&(valid_link==1));
	      if (dcif.dmemaddr==link_reg&&valid_link==1)begin   //452
		
	 		if (cachef.tag == v_tag[cachef.idx])begin
				if (!dirty_v[cachef.idx]&&valid_v[cachef.idx])begin
					miss=1;
					dirty_v_next=1;
					nb_next=0;
				end else begin
					next_link_reg=0;
					next_valid_link=0;
					dcif.dhit=1;
					dirty_v_next=1;	
					nb_next=1;
					count_next=count+1;
					if (xwen==1)begin
						vw_next=dcif.dmemstore;
					end else begin
						vv_next=dcif.dmemstore;
					end
				end	
			end else if (cachef.tag == w_tag[cachef.idx])begin
				if (!dirty_w[cachef.idx]&&valid_w[cachef.idx])begin
					miss=1;
					dirty_w_next=1;
					nb_next=1;
				end else begin
					next_link_reg=0;
					next_valid_link=0;
					dcif.dhit=1;
					dirty_w_next=1;	
					nb_next=0;
					count_next=count+1;
					if (xwen==1)begin
						ww_next=dcif.dmemstore;
					end else begin
						wv_next=dcif.dmemstore;
					end
				end	
			end else begin     
				miss = 1;
				count_next=count-1;
			 	
				if (nb[cachef.idx]==0)begin
					dirty_v_next=0;
					valid_v_next=1;
				end else begin
					dirty_w_next=0;
					valid_w_next=1;
				end
			end
		
		      end else begin    //452
			   //dcif.dmemload=0;
			   dcif.dhit=1;
		      end
	
	     end else begin     //~450,511
		if (dcif.dmemaddr==link_reg)begin
			next_link_reg=0;
			next_valid_link=0;
		end else begin
		end
		if (cachef.tag == v_tag[cachef.idx])begin
			if (!dirty_v[cachef.idx]&&valid_v[cachef.idx])begin
				miss=1;
				dirty_v_next=1;
				nb_next=0;
			end else begin
				dcif.dhit=1;
				dirty_v_next=1;	
				nb_next=1;
				count_next=count+1;
				if (xwen==1)begin
					vw_next=dcif.dmemstore;
				end else begin
					vv_next=dcif.dmemstore;
				end
			end	
		end else if (cachef.tag == w_tag[cachef.idx])begin
			if (!dirty_w[cachef.idx]&&valid_w[cachef.idx])begin
				miss=1;
				dirty_w_next=1;
				nb_next=1;
			end else begin
				dcif.dhit=1;
				dirty_w_next=1;	
				nb_next=0;
				count_next=count+1;
				if (xwen==1)begin
					ww_next=dcif.dmemstore;
				end else begin
					wv_next=dcif.dmemstore;
				end
			end	
		end else begin
			miss = 1;
			count_next=count-1;
		 	
			if (nb[cachef.idx]==0)begin
				dirty_v_next=0;
				valid_v_next=1;
			end else begin
				dirty_w_next=0;
				valid_w_next=1;
			end
			
		end
	     end    //~511


	   end else begin//~449
		
		 
		 
	   end
	end
			

		

























/*





	      if ((cachef.tag == v_tag[cachef.idx])) begin
		 dirty_v_next=1;
		 nb_next = 1;
		 dcif.dhit=1;
		 count_next=count+1;
		 
		 if(xwen == 0) begin
		    vv_next = dcif.dmemstore;
		 end else begin 
		    vw_next = dcif.dmemstore;
		 end
		 
	      end else if ((cachef.tag == w_tag[cachef.idx])) begin
		 dirty_w_next=1;
		 nb_next = 0;
		 dcif.dhit=1;
		 count_next=count+1;
		 
		 if(xwen == 0) begin
		    wv_next = dcif.dmemstore;
		 end else begin
		    ww_next = dcif.dmemstore;
		 end
		 
	      end else begin
		 miss = 1;
		 count_next=count-1;
		 
		 if (nb[cachef.idx]==0)begin
			dirty_v_next=0;
			valid_v_next=1;
		 end else begin
			dirty_w_next=0;
			valid_w_next=1;
		 end
		 
	      end
	   end // if (dcif.dmemWEN)
	   
	   
	end

*/
	/*
	WRITE:begin
	   if(dcif.dhit==1)begin
	      casez({ven,wen,xven,xwen})
		4'b1010:vv_next=dcif.dmemstore;
		4'b1001:vw_next=dcif.dmemstore;
		4'b0110:wv_next=dcif.dmemstore;
		4'b0101:ww_next=dcif.dmemstore;
	      endcase // casez ({ven,wen,xven,xwen})
	      count_next=count+1;
	   end else begin // if (dhit==1)
	      count_next=count-1;
	   end // else: !if(dhit==1)
	   
	   if(dcif.dhit==1&&ven==1)begin
	      dirty_v_next=1;
	      nb_next=0;
  
	   end else if (dcif.dhit==1&&wen==1)begin
	      dirty_w_next=1;
	      nb_next=1;
	      
	   end else begin
	   end

	end
	*/
	WRITE_1:begin
	   cif.dWEN=1;
	   if(nb[cachef.idx]==0) begin
	      cif.daddr = {v_tag[cachef.idx], cachef.idx, 3'b0};
	      cif.dstore = vv[cachef.idx];
	   end else begin
	      cif.daddr = {w_tag[cachef.idx], cachef.idx, 3'b0};
	      cif.dstore = wv[cachef.idx];
	   end
	end 
	
	WRITE_2:begin
	   cif.dWEN=1;
	   if(nb[cachef.idx]==0) begin
	      cif.daddr = {v_tag[cachef.idx], cachef.idx, 3'b100};
	      cif.dstore = vw[cachef.idx];
	   end else begin
	      cif.daddr = {w_tag[cachef.idx], cachef.idx, 3'b100};
	      cif.dstore = ww[cachef.idx];
	   end
	end
	
//	WRITE_3:begin
	   
//	end
	/*
	READ:begin
	   if(dcif.dhit==1)begin
	      casez({ven,wen,xven,xwen})
		4'b1010:dcif.dmemload=vv[cachef.idx];
		4'b1001:dcif.dmemload=vw[cachef.idx];
		4'b0110:dcif.dmemload=wv[cachef.idx];
		4'b0101:dcif.dmemload=ww[cachef.idx];
	      endcase // casez ({ven,wen,xven,xwen})
	      count_next=count+1;
	   end else begin
	      count_next=count-1;
	   end // else: !if(dcif.dhit==1)


	   if(dcif.dhit==1&&ven==1)begin
       
	      nb_next=0;
  
	   end else if (dcif.dhit==1&&wen==1)begin
	     
	      nb_next=1;
	      
	   end else begin
	   end
	   
	end
	*/
	READ_1:begin
	   cif.dREN=1;
	   cif.daddr={cachef.tag,cachef.idx,3'b0};
	   
	   if (nb[cachef.idx]==0)begin
	      vv_next=cif.dload;
	   end else begin
	      wv_next=cif.dload;
	   end		     
	end
	
	READ_2:begin
	   cif.dREN=1;
	   cif.daddr={cachef.tag,cachef.idx,3'b100};
	   
	   if (nb[cachef.idx]==0)begin
	      vw_next=cif.dload;
	      v_tag_next=cachef.tag;
	      //dirty_v_next=0;
	      //valid_v_next=1;
	   end else begin
	      ww_next=cif.dload;
	      w_tag_next=cachef.tag;
	      //dirty_w_next=0;
	      //valid_w_next=1; 
	   end
	end
	
	DYING:begin
	end
	
	FLUSH1:begin
	   cif.dWEN=1;
	   if (cc-1<8)begin
	      cif.daddr={v_tag[cdex],cdex,3'b0};
	      cif.dstore=vv[cdex];
	   end else begin
	      cif.daddr={w_tag[cdex],cdex,3'b0};
	      cif.dstore=wv[cdex];
	   end
	   
	end
	
	FLUSH2:begin
	   cif.dWEN=1;
	   if (cc-1<8)begin
	      cif.daddr={v_tag[cdex],cdex,3'b100};
	      cif.dstore=vw[cdex];
	   end else begin
	      cif.daddr={w_tag[cdex],cdex,3'b100};
	      cif.dstore=ww[cdex];
	   end
	end
	
	WRITE_CNT:begin
	   cif.dWEN=1;
	   cif.daddr=32'h3100;
	   cif.dstore=count;
	end

	HALT:begin
	end

	CHECKING:begin
	   if(cif.ccinv==1 && ~snoop_dt) begin
		if (next_snoop_hit[0]==1)begin
			v_tag_next=0;
      			valid_v_next=0;
      			vv_next=0;
      			vw_next=0;
      			dirty_v_next=0;
		end
		if (next_snoop_hit[1]==1)begin
			w_tag_next =0;
			valid_w_next=0;
			wv_next=0;
      			ww_next=0;
			dirty_w_next=0;
		end	
	   end
	end


	SHARING1:begin
	   if (snoop_hit[0]==1)begin
		cif.daddr = {v_tag[snoopf.idx], snoopf.idx, 3'b000};
		cif.dstore = vv[snoopf.idx];
		dirty_v_next = 0;
	   end else if (snoop_hit[1]==1)begin
		cif.daddr = {w_tag[snoopf.idx], snoopf.idx, 3'b000};
		cif.dstore = wv[snoopf.idx];
		dirty_w_next = 0;
	   end

	end

	SHARING2:begin
	   if (snoop_hit[0]==1)begin
		cif.daddr = {v_tag[snoopf.idx], snoopf.idx, 3'b100};
		cif.dstore = vw[snoopf.idx];
		dirty_v_next = 0;
	   end else if (snoop_hit[1]==1)begin
		cif.daddr = {w_tag[snoopf.idx], snoopf.idx, 3'b100};
		cif.dstore = ww[snoopf.idx];
		dirty_w_next = 0;
	   end

	end

	INV:begin
	   if(cif.ccinv==1 ) begin
		if (snoop_hit[0]==1)begin
			v_tag_next=0;
      			valid_v_next=0;
      			vv_next=0;
      			vw_next=0;
      			dirty_v_next=0;
		end
		if (snoop_hit[1]==1)begin
			w_tag_next =0;
			valid_w_next=0;
			wv_next=0;
      			ww_next=0;
			dirty_w_next=0;
		end	
	   end
	end



      endcase // casez (state)
   end // always_comb
   
   
   
   assign ven = (v_tag[cachef.idx] == cachef.tag);
   assign wen = (w_tag[cachef.idx] == cachef.tag);
   assign xven = (cachef.blkoff == 0);
   assign xwen = (cachef.blkoff == 1);
   assign dcif.flushed= (state==HALT) ? 1 : 0;
   assign cif.ccwrite=dcif.dmemWEN;
   
   
endmodule // dcache


 /*  
  
  if ((dirty_v[cachef.idx]==1)||(dirty_w[cachef.idx]==1))begin
		 next_state=WRITE_1;
	      end else begin
		 next_state=WRITE_3;
	      end
	WRITE_2:begin
	   if (cif.dwait==0)begin
	      if(dcif.dmemWEN==1)begin
		 next_state=WRITE_3;
	      end else if (dcif.dmemREN==1)begin
		 next_state=READ_1;
	      end else begin
		 next_state=WRITE_2;
	      end
	   end else begin
	      next_state=WRITE_2;
	   end // else: !if(ccif.dwait==0)
	   
	end

	WRITE_3:begin
	   if (dcif.dhit==1)begin
	      next_state=IDLE;
	   end else begin
	      next_state=WRITE_3;
	   end
	   
	end
  
  if ((dirty_v[cachef.idx]==1&&valid_v[cachef.idx]==0)||(dirty_w[cachef.idx]==1&&valid_w[cachef.idx]==0))begin
		 next_state=WRITE_1;
	      end else begin
		 next_state=READ_1;
	      end
*/	
