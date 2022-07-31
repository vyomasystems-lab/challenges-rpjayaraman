# level2_design: Bitmanipulation Coprocessor
  The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.
  ![image](https://user-images.githubusercontent.com/105109240/182028705-eb31261a-1b2a-4729-9d1a-6e03d667ea3d.png)

  ## Verification Environment
  The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. Provided DUT is Bitmanipulation Coprocessor.
  
## Test Scenario
#### Test : Directed Testcase 
  The DUT has 4 inputs and 1 outputs. The design is nothing but ALU, the expectation of the DV folks to exercise all the instruction with the available input pins. The pass and fail condition is based on the **valid bit** in mav_putvalue.
Since the size of the input (32 bit) has large state space randomizing the entire input won't be appropriate and the chance of hitting the bug is very minimal and it is very time and resource intensive process. so it is worth to spend time in extracting input patterns from model_mkbitmanip.py file. In this way it will be kind of directed test and also it explores all possible pattern exhaustively. The exhaustive in nature helps us to find the bugs in the design. 

![image](https://user-images.githubusercontent.com/105109240/182024605-4d863576-0f2d-47ce-9634-38a236b4f2e1.png)

As we can see from the [test file](https://github.com/vyomasystems-lab/challenges-rpjayaraman/blob/master/level2_design/test_mkbitmanip.py) combination of tb_opcode, tb_func3,  tb_func7,  tb_imm_val_1 in a nested for loop would do the magic. 

## Design Bug
 So with the mentioned testbench we have exercised the following list instruction:
 ```
 --ANDN 1         
--BDEP 39         
--BEXT 40         
--BFP  60 / 
--SLO function
--CLMUL  32
--CLMULH  33
--CLMULR  34
--CLZ   21
--CRC32.B 26
--CRC32C.B 29
--CRC32C.H  30
--CRC32C.W  31
--CRC32.H  27
--CRC32.W  28
--CTZ    22
--GORC 15 (check)
--GORCI 57
--GREV  16 (should check)
--GREVI  58
--MAX 36
--MAXU 38
--MIN  35
--MINU  37
--ORN 2
--PACK 41
--PACKH 45
--PACKU 42
--PCNT   23
--ROL  6
--ROR  7
--RORI  48
--SBCLR   11
--SBCLRI   49
--SBEXT  14
--SBEXTI  52
--SBINV  13
--SBINVI  51
--SBSET   12
--SBSETI   50
--SEXT.B  24
--SEXT.H  25
--SH1ADD  8
--SH2ADD  9
--SH3ADD  10
--SHFL  53
--SHFLI  55 (check)
--SLO  4
--SLO function
--SLOI  46
--SRO  5
--SROI 47
--UNSHFL  54
--UNSHFLI  56  (check)
--XNOR 3
 ```
 For the detailed information of each and every instruction, we can always refer the [output.log](https://github.com/vyomasystems-lab/challenges-rpjayaraman/blob/master/level2_design/output.log) 
 
 ## Failed Instructions
 
  We have added simple checker with if condition to capture the all status along with the pass and fail count. As assert terminated the simulation whenever the bug gets popped up, we are using the below approach to keep track of bugs.
  ```
   if(dut_output == expected_mav_putvalue):
                        dut._log.info("PASSING: Expected behaviour is observed")
                        pass_count += 1
                    else:
                        print("FAIL: mav_putvalue_instr",hex(dut.mav_putvalue_instr.value) ,error_message)
                        err_count += 1
 ```
 
 Following is the bug captured by the python test.
 
 ```
** --ANDN 1**
     0.01ns INFO     Instruction     =0x40007033
     0.01ns INFO     DUT OUTPUT      =0xb
     0.01ns INFO     EXPECTED OUTPUT =0x1
FAIL: mav_putvalue_instr 0x40007033 Value mismatch DUT = 0xb does not match MODEL = 0x1
 ```
 
 However, since we missed out to include **func7_2bit** into the instruction generator we have missed checking the following 5 instruction. Total instruction in model file is 59. Our tese generated 54 instruction, missing the below instruction.
 
 ![image](https://user-images.githubusercontent.com/105109240/182028495-94b9b1a8-6be3-4446-9d02-5f9c104ac0ff.png)

```
CMIX  17
CMOV 18
FSL 19
FSR  20(check)
FSRI  59
```

Adding **func7_2bit** would made the verification complete and there is a slight probability we may missed to capture the bug. 

In other hand, test also checks the invalid instruction and our checker caught those. we can refer the [Invalid_Instr.list](https://github.com/vyomasystems-lab/challenges-rpjayaraman/blob/master/level2_design/Invalid_Instr.list). Around 737 invalid instruction has been checked in this case.

## Verification Strategy
  It is a bit mix of Directed and Exhaustive. Being 32 bit input, It won't be the right way to randomize the entire input. So extracted the input pattern from the model file and with the help of nested for loop, we iterated through all valid and Invalid instruction. 

## Is the verification complete ?
  NO. As we are aware of the missing of func7_2bit in instruction generator, we missed out to verify 5 instructions. However, we got one design bug and tested invalid instruction case.
