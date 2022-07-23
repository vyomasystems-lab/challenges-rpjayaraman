# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def test_seq_bug1(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    cocotb.log.info('#### CTB: Develop your test here! ######')
    cocotb.log.info('#### Directed Test ######')
    cocotb.log.info('Initial status - Current State %s Next State %s seq_seen %s', dut.current_state.value,dut.next_state.value,dut.seq_seen.value)
    
    await RisingEdge(dut.clk)
    dut.inp_bit.value = 1
    await RisingEdge(dut.clk)
    cocotb.log.info('Input: %d Cur_State %s Next_State %s seq_seen %s', dut.inp_bit.value,dut.current_state.value,dut.next_state.value,dut.seq_seen.value)

    dut.inp_bit.value = 0
    await RisingEdge(dut.clk)
    cocotb.log.info('Input: %d Cur_State %s Next_State %s seq_seen %s', dut.inp_bit.value,dut.current_state.value,dut.next_state.value,dut.seq_seen.value)
   
    dut.inp_bit.value = 1
    await RisingEdge(dut.clk)
    cocotb.log.info('Input: %d Cur_State %s Next_State %s seq_seen %s', dut.inp_bit.value,dut.current_state.value,dut.next_state.value,dut.seq_seen.value)

    dut.inp_bit.value = 0
    await RisingEdge(dut.clk)

    cocotb.log.info('Input: %d Cur_State %s Next_State %s seq_seen %s', dut.inp_bit.value,dut.current_state.value,dut.next_state.value,dut.seq_seen.value)

    dut.inp_bit.value = 1
    await RisingEdge(dut.clk)

    cocotb.log.info('Input: %d Cur_State %s Next_State %s seq_seen %s', dut.inp_bit.value,dut.current_state.value,dut.next_state.value,dut.seq_seen.value)

    dut.inp_bit.value = 1
    await RisingEdge(dut.clk)
    cocotb.log.info('Input: %d Cur_State %s Next_State %s seq_seen %s', dut.inp_bit.value,dut.current_state.value,dut.next_state.value,dut.seq_seen.value)
    
    await RisingEdge(dut.clk)
    assert dut.seq_seen.value == 1, "No 1011 Sequence Detected"
    cocotb.log.info('#### End of Directed Test ######')

@cocotb.test()
async def test_seq_bug2(dut):
    """Randomised Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock
    err_count = 0
    pass_count = 0

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    cocotb.log.info('#### Randomized Test -> START ! ######')

    for i in range (1,50):
        dut.inp_bit.value = random.randint(0, 1)
        await RisingEdge(dut.clk)
        cocotb.log.info('Loop: %d Input: %d Cur_State %s Next_State %s seq_seen %s',i,dut.inp_bit.value,dut.current_state.value,dut.next_state.value,dut.seq_seen.value)
        if (i>=4):
            if(dut.seq_seen.value):
                pass_count += 1
                cocotb.log.info('PASSING seq_seen: %d',dut.seq_seen.value)
            else:
                err_count += 1
                dut._log.error("No 1011 Sequence Detected i Random test")


        else:
            print("Count is too less to detect SEQ")

    cocotb.log.info('Total number of pass count %d',pass_count)
    cocotb.log.info('Total number of error count %d',err_count)
    assert err_count == 1, "No 1011 Sequence Detected"




