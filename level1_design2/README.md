# level1_design2: Sequence Detector 1011

  The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![image](https://user-images.githubusercontent.com/105109240/180602190-cb3f5d2c-8aef-42fa-9cdb-6eb0734c6a02.png)

## Verification Environment
  The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. Provided DUT is Sequence Detector.

## Test Scenario
#### Test 1: Directed Testcase 
  The DUT has 3 input pins - clock, reset, inp_bit and one output to represent the detection of the pattern. Test 1 is written as directed testcase as in this case of detection of particular pattern the directed testcase is unaviodable. 
 ![image](https://user-images.githubusercontent.com/105109240/180602659-c2d43589-d04c-4dd4-bf49-bcd2b416f5c4.png)
 
  After Clock generation and Reset de-assertion, test case is orchestrated to produce the 1011 pattern with time interval of rising clock edge. 

```
  await RisingEdge(dut.clk)
  dut.inp_bit.value = 1
```
To make sure the sequence is detected or not, assert is placed at the end of the directed testcase to capture the result.

```
assert dut.seq_seen.value == 1, "No 1011 Sequence Detected"
```
After running the testcase, the assert is failed with the following error:

![image](https://user-images.githubusercontent.com/105109240/180602745-83a478ff-c65d-43c0-acf4-7a85817b59d3.png)

## Design Bug
  Based on the above test input and analysing the design, following is the observation:

Analysing the failing log, we can see that after the state **011** if the input bit is zero it has to step back to the previous state which is **010**, but in this case it is moving into IDLE state which violates the overlapping sequence pattern.

```
Failing one:  60000.00ns INFO     Input: 0 Cur_State 011 Next_State 000 seq_seen 0
```
Following is the pointer to the bug in RTL file:
```
      SEQ_101:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1011;
        else
          next_state = IDLE;       -----> BUG
```
## Design Fix
After fixing the bug:

```
     SEQ_101:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1011;
        else
          next_state = SEQ_10;   -------> FIX
      end
```
we can observe the following in the passing log:
```
Passing one:  60000.00ns INFO     Input: 0 Cur_State 011 Next_State 010 seq_seen 0
```
The updated design is checked in as seq_detect_1011_fix.v

## Verification Strategy
  Two Strategy: 
    1. Directed test
    2. Ranomized test 
  Directed test is explained here [TEST 1](https://github.com/vyomasystems-lab/challenges-rpjayaraman/new/master/level1_design2#test-1-directed-testcase) which is nothing but provding the required input to the design and observing the desired pattern is obtained or not. 
  
  Second on the list is randomized one, where we are randomizing the inp_bit and passing into the design. in this case, probability of obtaining the desired pattern is less. Although it is good to include randomised testcase as it may capture the unexpected bug in the design. In this case, we need to manually check the occurence of pattern, tried my best to add the checker in randomized testcase. Anyway manual look over on the log is required. 
  
## Is the verification complete ?
 Added both Directed and Randomized test case, that should be enough. It will complete if we add the strong checker in the randomized testcase.
  




