# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path
import os,binascii

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def test_apb(dut):
    wr_data = random.randint(0, 15) 
    addr    = random.randint(0, 63) # valid address range
    cocotb.log.info('#### Directed Test ######')

    clock = Clock(dut.PCLK, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.PRESETn.value = 0
    await FallingEdge(dut.PCLK)  
    dut.PRESETn.value = 1
    await FallingEdge(dut.PCLK)

    cocotb.log.info('#### Writing DATA ######')
    dut.PSEL.value     = 0 # Setting up initial values
    dut.PENABLE.value  = 0

    await RisingEdge(dut.PCLK)
    dut.PSEL.value = 1
    dut.PWRITE.value = 1
    dut.PADDR.value = addr
    dut.PWDATA.value = wr_data
    await RisingEdge(dut.PCLK)
    dut.PENABLE.value = 1
    await RisingEdge(dut.PCLK)
    cocotb.log.info('WRITE OP: PSEL: %d PWRITE: %d PADDR %d PWDATA %d PREADY %d',dut.PSEL.value, dut.PWRITE.value,dut.PADDR.value,dut.PWDATA.value, dut.PREADY.value)
    
    dut.PSEL.value     = 0
    dut.PENABLE.value  = 0
    dut.PWRITE.value   = 0

    cocotb.log.info('#### Reading DATA ######')
    
    await RisingEdge(dut.PCLK)
    dut.PSEL.value = 1
    dut.PWRITE.value = 0
    dut.PADDR.value = addr
    await RisingEdge(dut.PCLK)
    dut.PENABLE.value = 1
    await RisingEdge(dut.PCLK)
    await RisingEdge(dut.PCLK)
    cocotb.log.info('READ OP: PSEL: %d PWRITE: %d PADDR %d READ_DATA %d PREADY %d',dut.PSEL.value, dut.PWRITE.value,dut.PADDR.value,dut.PRDATA.value,dut.PREADY.value)

    #comparing write and read values
    assert dut.PWDATA.value == dut.PRDATA.value, "Write data is not matching with read data"
    cocotb.log.info('#### End of Directed Test ######')



@cocotb.test()
async def test_slave_err_test(dut):

    wr_data = random.randint(0, 15) 
    addr_err = random.randint(64,100)          # Invalid address 
    op      = random.randint(0,1)
    cocotb.log.info('#### Slave Error Test ######')

    clock = Clock(dut.PCLK, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.PRESETn.value = 0
    await FallingEdge(dut.PCLK)  
    dut.PRESETn.value = 1
    await FallingEdge(dut.PCLK)

    dut.PSEL.value     = 0 # Setting up initial values
    dut.PENABLE.value  = 0

    await RisingEdge(dut.PCLK)
    dut.PSEL.value = 1
    dut.PWRITE.value = op
    dut.PADDR.value = addr_err
    if(op):
        dut.PWDATA.value = wr_data
    else:
        cocotb.log.info('Read operation')
    await RisingEdge(dut.PCLK)
    dut.PENABLE.value = 1
    await RisingEdge(dut.PCLK)
    cocotb.log.info('OP: PSEL: %d PWRITE: %d PADDR %d PWDATA %d PREADY %d',dut.PSEL.value, dut.PWRITE.value,dut.PADDR.value,dut.PWDATA.value, dut.PREADY.value)
    await RisingEdge(dut.PCLK)
    cocotb.log.info('Slave Error response is %d',dut.PSLVERR.value)
    assert(dut.PSLVERR.value == 1), "Slave error is not asserted"

@cocotb.test()
async def reset_test_apb(dut):
    wr_data = random.randint(0, 15) 
    addr    = random.randint(0, 63) # valid address range
    cocotb.log.info('#### Reset Test ######')

    clock = Clock(dut.PCLK, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.PRESETn.value = 0
    await FallingEdge(dut.PCLK)  
    dut.PRESETn.value = 1
    await FallingEdge(dut.PCLK)

    cocotb.log.info('#### Writing DATA ######')
    dut.PSEL.value     = 0 # Setting up initial values
    dut.PENABLE.value  = 0

    await RisingEdge(dut.PCLK)
    dut.PSEL.value = 1
    dut.PWRITE.value = 1
    dut.PADDR.value = addr
    dut.PWDATA.value = wr_data
    await RisingEdge(dut.PCLK)
    dut.PENABLE.value = 1
    await RisingEdge(dut.PCLK)
    cocotb.log.info('WRITE OP: PSEL: %d PWRITE: %d PADDR %d PWDATA %d PREADY %d',dut.PSEL.value, dut.PWRITE.value,dut.PADDR.value,dut.PWDATA.value, dut.PREADY.value)
    
    dut.PSEL.value     = 0
    dut.PENABLE.value  = 0
    dut.PWRITE.value   = 0

    cocotb.log.info('#### Reading DATA ######')
    
    await RisingEdge(dut.PCLK)
    dut.PSEL.value = 1
    dut.PWRITE.value = 0
    dut.PADDR.value = addr
    await RisingEdge(dut.PCLK)
    dut.PENABLE.value = 1
    dut.PRESETn.value = 0            #Enabling RESET during the middle of READ operation
    await RisingEdge(dut.PCLK)
    await RisingEdge(dut.PCLK)
    cocotb.log.info('READ OP: PSEL: %d PWRITE: %d PADDR %d READ_DATA %d PREADY %d',dut.PSEL.value, dut.PWRITE.value,dut.PADDR.value,dut.PRDATA.value,dut.PREADY.value)

    #comparing write and read values
    assert dut.PWDATA.value == dut.PRDATA.value, "Write data is not matching with read data"
    cocotb.log.info('#### End of Reset Test ######')

