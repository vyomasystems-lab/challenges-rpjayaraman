# See LICENSE.iitm for details
# See LICENSE.vyoma for details

import random
import sys
import cocotb
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock

from model_mkbitmanip import *

# Clock Generation
@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(1) 
        signal.value <= 1
        yield Timer(1) 

# Sample Test
@cocotb.test()
def run_test(dut):

    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    # input transaction
    mav_putvalue_src1 = 0x5
    mav_putvalue_src2 = 0x5
    mav_putvalue_src3 = 0x4

    pass_count =0 
    err_count = 0
    
    tb_opcode = [0b0110011,0b0010011]

    tb_func3 = [0b00000000000000000111000000000000,
    0b00000000000000000110000000000000,
    0b00000000000000000100000000000000,
    0b00000000000000000001000000000000,
    0b00000000000000000101000000000000,
    0b00000000000000000010000000000001,
    0b00000000000000000011000000000000]

    tb_func7 = [0b01000000000000000000000000000000,
    0b00100000000000000000000000000000,
    0b01100000000000000000000000000000,
    0b01001000000000000000000000000000,
    0b00101000000000000000000000000000,
    0b01101000000000000000000000000000,
    0b00001010000000000000000000000000,
    0b00001000000000000000000000000000]

    tb_imm_val_1 = [0b00000000000000000000000000000000,
    0b00000000000100000000000000000000,
    0b00000000001000000000000000000000,
    0b00000000010000000000000000000000,
    0b00000000010100000000000000000000,
    0b00000001000000000000000000000000,
    0b00000001000100000000000000000000,
    0b00000001001000000000000000000000,
    0b00000001100000000000000000000000,
    0b00000001100100000000000000000000,
    0b00000001101000000000000000000000]

    for i in tb_opcode:
        for j in tb_func3:
            for k in tb_func7:
                for l in tb_imm_val_1:
                    bin_out=bin(i|j|k|l)[2:] #removing base info
                    #print("Binary Instr value",bin_out)
                    final= int(bin_out,2)
                    #print("Instr value",final)
                    print("------------------------------------------------")
                    mav_putvalue_instr = final
                     # expected output from the model
                    expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)
                    # driving the input transaction
                    dut.mav_putvalue_src1.value = mav_putvalue_src1
                    dut.mav_putvalue_src2.value = mav_putvalue_src2
                    dut.mav_putvalue_src3.value = mav_putvalue_src3
                    dut.EN_mav_putvalue.value = 1
                    dut.mav_putvalue_instr.value = mav_putvalue_instr
  
                    yield Timer(1) 

                    # obtaining the output
                    dut_output = dut.mav_putvalue.value

                    cocotb.log.info(f'Instruction     ={hex(dut.mav_putvalue_instr.value)}')
                    cocotb.log.info(f'DUT OUTPUT      ={hex(dut_output)}')
                    cocotb.log.info(f'EXPECTED OUTPUT ={hex(expected_mav_putvalue)}')
    
                    # comparison
                    error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
                    #assert dut_output == expected_mav_putvalue, error_message
                    if(dut_output == expected_mav_putvalue):
                        dut._log.info("PASSING: Expected behaviour is observed")
                        pass_count += 1
                    else:
                        print("FAIL: mav_putvalue_instr",hex(dut.mav_putvalue_instr.value) ,error_message)
                        err_count += 1
    cocotb.log.info("Pass count: %0d Error count %0d",pass_count,err_count)
    assert err_count == 0, "Test Failed"

   
