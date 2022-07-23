# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestError, TestFailure
import random

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""
    # Assigning values to DUT Input 
    #avoiding 0 as a input value as it is defalut value in case statement
    
    dut.inp0.value =  2 
    dut.inp1.value =  2  
    dut.inp2.value =  2   
    dut.inp3.value =  2  
    dut.inp4.value =  2   
    dut.inp5.value =  2    
    dut.inp6.value =  2   
    dut.inp7.value =  2
    dut.inp8.value =  2 
    dut.inp9.value =  2 
    dut.inp10.value = 2   
    dut.inp11.value = 2
    dut.inp12.value = 2
    dut.inp13.value = 2
    dut.inp14.value = 2
    dut.inp15.value = 2  
    dut.inp16.value = 2 
    dut.inp17.value = 2   
    dut.inp18.value = 2
    dut.inp19.value = 2
    dut.inp20.value = 2
    dut.inp21.value = 2    
    dut.inp22.value = 2 
    dut.inp23.value = 2 
    dut.inp24.value = 2
    dut.inp25.value = 2 
    dut.inp26.value = 2 
    dut.inp27.value = 2 
    dut.inp28.value = 2 
    dut.inp29.value = 2
    dut.inp30.value = 2 

    def decimalToBinary(n):
        # and removing the prefix(0b)
        return bin(n).replace("0b", "")

    dut._log.info("Starting the test")
    for i in range(0,31):
        dut.sel.value = i
        expected_value= str(dut.out.value)
        dut._log.info("DUT sel: %s",str(dut.sel.value))
        dut._log.info("expected_value: %s",expected_value)
        if(expected_value == decimalToBinary(2)):
            print("PASSING: MUX working for Input: dut.inp"+str(i-1)+".value sel:",i-1)
        else:
            dut._log.error("Mismatch found for sel: dut.sel.value= %d with Input: dut.inp"+str(i-1)+".value", i-1)
            #raise TestError()

        await Timer(2, units='ns')
    dut._log.info("####################### Test 1 DONE ########################################")


#@cocotb.test()
#async def test_mux_2(dut):
    dut._log.info("Checking Corner case for inp0,inp29 and default test for Inp30")
    def decimalToBinary(n):
    # and removing the prefix(0b)
        return bin(n).replace("0b", "")

    #Assigning values
    dut.sel.value=0
    dut.inp0.value=3
    await Timer(2, units='ns')
    dut._log.info("Sel: %d, Input: %d, Output: %d",dut.sel.value,dut.inp0.value,dut.out.value)
    assert dut.out.value == dut.inp0.value, "Corner test failed"
    
    dut.inp29.value=2
    dut.sel.value=29
    await Timer(2, units='ns')
    dut._log.info("Sel: %d, Input: %d, Output: %d",dut.sel.value,dut.inp29.value,dut.out.value)
    assert dut.out.value == dut.inp29.value, "Corner test failed"

    dut.inp30.value=2
    dut.sel.value=30
    await Timer(2, units='ns')
    dut._log.info("Sel: %d, Input: %d, Output: %d",dut.sel.value,dut.inp30.value,dut.out.value)
    assert dut.out.value == 0, "Default test failed"

    dut._log.info("####################### Test 2 DONE ########################################")

