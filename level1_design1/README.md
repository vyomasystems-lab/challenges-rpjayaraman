# level1_design1: MUX DESIGN VERIFICATION

  The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.
![image](https://user-images.githubusercontent.com/105109240/180593031-50bd5537-66ac-45ca-8a05-1c12f87a6b37.png)

## Verification Environment
  The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. Provided DUT is MUX:

### Test 1: Checking all MUX input values
  FIRST STEP is to assign the value to the input pins i.e inp0 to inp30.
Value assigned to the input is 2 (non-zero value) as the default value of the case statemnet provided is zero made me to select non-zero values to the input and it   will be easy to write checker.
  SECOND STEP to slect the sel pin in MUX. Since the sel is 5-bit width, for loop becomes the automatic choice to iterate through all sel pin range from 0 to 29 and added checking mechanism to check the assigned input values to dut out put value. 

#### Checker
```
        if(expected_value == decimalToBinary(2)):
            print("PASSING: MUX working for Input: dut.inp"+str(i-1)+".value sel:",i-1)
        else:
            dut._log.error("Mismatch found for sel: dut.sel.value= %d with Input: dut.inp"+str(i-1)+".value", i-1)
```
As a result, the following error is seen in inp12
```
    26.00ns INFO     DUT sel: 01100
    26.00ns INFO     expected_value: 00
    26.00ns ERROR    Mismatch found for sel: dut.sel.value= 12 with Input: dut.inp12.value
```
## Design Bug
  Based on the above testcase, it is evident from the fact that output value of inp12 is zero.It is picking the default value (00) as the inp12 was not included in the design file.
```
 5'b01101: out = inp12;
 5'b01101: out = inp13;
```
By modifying the sel value from  **5'b01101 ->  5'b01100.** it will resolve the issue. 

## Design Fix
  Updating the design and re-running the test makes the test pass.

![image](https://user-images.githubusercontent.com/105109240/180594474-ed255a65-4764-4962-91a8-d50bca22a0f7.png)

The updated design is checked in as [mux_fix.v](https://github.com/vyomasystems-lab/challenges-rpjayaraman/blob/master/level1_design1/mux_fix.log) and log [mux_fix.log](https://github.com/vyomasystems-lab/challenges-rpjayaraman/blob/master/level1_design1/mux_fix.log)

## Verification Strategy

  - Test 1:  Assigns all the input to a constant value (other than 00), enables the mux sel and checker checks the output value with the constant value.
  - Test 2: It is test case to check the corner condition such as inp0 and inp29. It also checks for the default value when the out off bound input (inp30) is selected.  
## Is the verification complete ?
 Since the bit width is 5. it is easy to perform exhaustive verification that has been done in [TEST 1](https://github.com/vyomasystems-lab/challenges-rpjayaraman/new/master/level1_design1#test-1-checking-all-mux-input-values) and Exercised corner case and default case. Hence the verification is complete. 
