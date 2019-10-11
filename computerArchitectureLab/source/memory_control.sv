// interface include
`include "cache_control_if.vh"

// memory types
`include "cpu_types_pkg.vh"

module memory_control (
  input CLK, nRST,
  cache_control_if.cc ccif
);
  // type import
  import cpu_types_pkg::*;

  // number of cpus for cc
  parameter CPUS = 2;




typedef enum logic[3:0] {
  IDLE, ARB, INSTR, WRITE,  SNOOP,READ, RAM_CACHE
} state_t;

state_t state,next_state;
logic snoop_idx,next_snoop_idx;
word_t [1:0] next_snoopaddr;
logic [1:0] next_wait;
logic i,next_i;

always_ff @(posedge CLK, negedge nRST)begin
	if(nRST==0)begin
	state<=IDLE;
	snoop_idx<=0;
	i<=0;
	end else begin
	state<=next_state;
	snoop_idx<=next_snoop_idx;
	i<=next_i;
	end
end


always_comb begin
	next_state=state;
	next_snoop_idx=snoop_idx;
	next_i=i;

	case(state)
	IDLE: begin
	if (ccif.dWEN[1] || ccif.dWEN[0]) begin
	next_state = WRITE;
	end else if (ccif.cctrans[1] || ccif.cctrans[0]) begin
	next_state = ARB;
	end else if (ccif.iREN[1] || ccif.iREN[0]) begin
	next_state = INSTR;
	end

	end

	ARB: begin
	if(ccif.dREN[1] || ccif.dREN[0]) begin
	next_state = SNOOP;
	if(ccif.dREN[0]) begin
	  next_snoop_idx = 0;
	end else if (ccif.dREN[1]) begin
	  next_snoop_idx = 1;
	end

	end else begin
	next_state = IDLE;
	end
	end
//||ccif.ccwrite[~snoop_idx]==1
	SNOOP: begin
	if(ccif.cctrans[~snoop_idx]==1)
	next_state = RAM_CACHE;
	else
	next_state = READ;
	end
	//ccwrite=1
	READ: begin
	if (ccif.ramstate == ACCESS && i==0) begin
	next_i=1;
	next_state=READ;
	end else if (ccif.ramstate == ACCESS && i==1) begin
	next_state=IDLE;
	next_i=0;
	end else begin
	next_state=READ;
	end

	end

	
	RAM_CACHE: begin
	if (ccif.ramstate == ACCESS && i==0) begin
	next_i=1;
	next_state=RAM_CACHE;
	end else if (ccif.ramstate == ACCESS && i==1) begin
	next_state=IDLE;
	next_i=0;
	end else begin
	next_state=RAM_CACHE;
	end

	end

	INSTR: begin
	if (ccif.dWEN[1] || ccif.dWEN[0]) begin
	next_state = WRITE;
	end else if (ccif.ramstate == ACCESS)begin
		if (ccif.cctrans[0]==1 || ccif.cctrans[1]==1)begin
		next_state=ARB;
		end else begin
		next_state=IDLE;
		end
	end else begin
	next_state=INSTR;
	end

	end

	WRITE: begin
	if (ccif.ramstate == ACCESS && i==0) begin
	next_i=1;
	next_state=WRITE;
	end else if (ccif.ramstate == ACCESS && i==1) begin
	next_state=IDLE;
	next_i=0;
	end else begin
	next_state=WRITE;
	end

	end
	endcase // state
end
	
	

always_comb begin 

	ccif.iwait[1] = 1; 
	ccif.iwait[0] = 1;
	ccif.iload[1] = 0; 
	ccif.iload[0] = 0;
	ccif.dwait[1] = 1; 
	ccif.dwait[0] = 1;
	ccif.dload[1] = 0; 
	ccif.dload[0] = 0;
	ccif.ramaddr = 0;
	ccif.ramstore = 0;
	ccif.ramWEN = 0;
	ccif.ramREN = 0;
	ccif.ccsnoopaddr[1] = '0; 
	ccif.ccsnoopaddr[0] = '0;
	ccif.ccwait[1] = 0; 
	ccif.ccwait[0] = 0;
	ccif.ccinv[1] = ccif.ccwrite[0];  
	ccif.ccinv[0] = ccif.ccwrite[1];

	case(state)
	IDLE:begin
	end

	WRITE: begin
	if(ccif.dWEN[1]) begin
	ccif.dwait[1] = ccif.ramstate != ACCESS;
	ccif.ramaddr = ccif.daddr[1];
	ccif.ramWEN = ccif.dWEN[1];
	ccif.ramstore = ccif.dstore[1];
	ccif.ccwait[0] = 1;
	end else if (ccif.dWEN[0]) begin
	ccif.dwait[0] = ccif.ramstate != ACCESS;
	ccif.ramaddr = ccif.daddr[0];
	ccif.ramWEN = ccif.dWEN[0];
	ccif.ramstore = ccif.dstore[0];
	ccif.ccwait[1] = 0;
	end
	end

	INSTR: begin
	if(ccif.iREN[1]) begin
	ccif.iload[1] = ccif.ramload;
	ccif.iwait[1] = ccif.ramstate != ACCESS;
	ccif.ramaddr = ccif.iaddr[1];
	ccif.ramREN = ccif.iREN[1];
	end else if (ccif.iREN[0]) begin
	ccif.iload[0] = ccif.ramload;
	ccif.iwait[0] = ccif.ramstate != ACCESS;
	ccif.ramaddr = ccif.iaddr[0];
	ccif.ramREN = ccif.iREN[0];
	end
	end

	ARB: begin
	ccif.ccwait[~next_snoop_idx] = 1;
	ccif.ccsnoopaddr[~next_snoop_idx] = ccif.daddr[next_snoop_idx];
	end



	SNOOP: begin
	ccif.ccsnoopaddr[~snoop_idx] = ccif.daddr[snoop_idx];
	ccif.ccwait[~snoop_idx] = 1;
	end

	RAM_CACHE: begin
	ccif.dwait[~snoop_idx] = ccif.ramstate != ACCESS ? 1 : 0;
	ccif.dwait[snoop_idx] = ccif.ramstate != ACCESS;
	ccif.dload[snoop_idx] = ccif.dstore[~snoop_idx];
	ccif.ramaddr = ccif.daddr[~snoop_idx];
	ccif.ramstore = ccif.dstore[~snoop_idx];
	ccif.ramWEN = 1;
	ccif.ccsnoopaddr[~snoop_idx] = ccif.daddr[snoop_idx];
	ccif.ccwait[~snoop_idx] = 1;
	end

	READ: begin
	ccif.dwait[snoop_idx] = ccif.ramstate != ACCESS ? 1 : 0;
	ccif.dload[snoop_idx] = ccif.ramload;
	ccif.ramaddr = ccif.daddr[snoop_idx];
	ccif.ramREN = ccif.dREN[snoop_idx];
	ccif.ccwait[~snoop_idx] = 1;
	end







	endcase // state
end
endmodule 

