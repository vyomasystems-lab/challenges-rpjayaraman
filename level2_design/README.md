# level2_design: Bitmanipulation Coprocessor
  The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.
  
  ## Verification Environment
  The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. Provided DUT is Bitmanipulation Coprocessor.
  
## Test Scenario
#### Test : Directed Testcase 
The DUT has 4 inputs and 1 outputs. Since the size of the input (32 bit) has large state space randomizing the enitre input won't be appropriate and the chance of hitting the bug is very minimal and it is very time and resource intensive process. so it is worth to spend time in extracing input patterns from model_mkbitmanip.py file. In this way it will be kind of directed test and also it explores all possible pattern exhaustively. The exhaustive in nature helps us to find the bugs in the design. 

![image](https://user-images.githubusercontent.com/105109240/182024605-4d863576-0f2d-47ce-9634-38a236b4f2e1.png)

As we can see from the [test file](https://github.com/vyomasystems-lab/challenges-rpjayaraman/blob/master/level2_design/test_mkbitmanip.py) combination of tb_opcode, tb_func3,  tb_func7,  tb_imm_val_1 in a nested for loop would do the magic. 

## Design Bug
 So with the mentioned testbench we have exericesed the following list instruction:
 ```
 --ANDN 1
--BDEP 39
--BEXT 40
--BFP  60
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
 
 
