# level3_design: APB SLAVE SRAM CORE

  The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![image](https://user-images.githubusercontent.com/105109240/182204713-72b260b6-3084-4b3f-8355-b87748ede286.png)


## Verification Environment
  The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. Provided DUT is Sequence Detector.

## APB DESIGN

DUT from : https://github.com/courageheart/AMBA_APB_SRAM

  APB slave SRAM core (Design) as a slave of APB Master (Testbench). SRAM as a slave is a memory core used to write and read data via APB bus interface. The slave core also supports an error response in case of accessing out of bound address either for reading or writing, wait state and along with resizable memory block.
  
  ![image](https://user-images.githubusercontent.com/105109240/182030138-101ef0cf-294c-40dd-a44d-4a302adbee3f.png)

### Pin Description 
![image](https://user-images.githubusercontent.com/105109240/182030307-35caf6d2-ac29-4f25-9544-f52bfcbecd73.png)


### APB FSM
  The operation of APB can we summarized in the following state diagram,
  ![image](https://user-images.githubusercontent.com/105109240/182030273-16804dbf-5590-488c-9e51-695c7de4253c.png)

### Write/Read Operation
  The Write transfer requires address, write, slave select, and write data. After moving from SETUP state, assertion of PENABLE indicates the start of ACCESS state. At the end of ACCESS state write transfer will take place if PWRITE is 1. In case of read transfer, it follows the same except the PWRITE will be LOW indicating the READ transfer is taking place.
  
  Fig 1:WRITE OPERATION
  
  
![image](https://user-images.githubusercontent.com/105109240/182205780-7010a446-a0cf-46e6-b79c-5977c3a15145.png)

  
  Fig 2:READ OPERATION 
  
![image](https://user-images.githubusercontent.com/105109240/182205824-968ca175-b617-4f41-8061-0e3e98bcc9aa.png)

One notable feature in APB 3 is slave error response pin. This pin will get toggled if the write/read transfer take place in the out of bound address. 

## Test Scenario
#### Test 1 - Write/Read operation
  
  In [test 1](https://github.com/vyomasystems-lab/challenges-rpjayaraman/blob/master/level3_design/test_apb_v3_sram.py) we are performing read/write with randomized wr_data within the valid address range. Here in the DUT we have mentioned the memory size as 64. Performing read/write with in the valid address won't create slave error response. 
  For Write/read we have to go through the IDLE, SETUP, ACCESS Phase. If the phase transfer is valid, then we can be able to read the data from the address where we performed the write operation. if not, that indicates the failure of data transfer.  To verify this, we have added simple checker to validate the operation.
  
  ```
      #comparing write and read values
    assert dut.PWDATA.value == dut.PRDATA.value, "Write data is not matching with read data"
  ```
  
  Before the injection of bug, we can see the test is passing in [output log](https://github.com/vyomasystems-lab/challenges-rpjayaraman/blob/master/level3_design/apb_sram_passing.log)
  
  ### Test 2 - Accessing Invalid address range
   The motive of the test 2 is to check the PSLVERR assertion. We reproduced the scenario by trying to perform write/read in the out of bound address / invalid address (say > 64) along with the checker. Checker will fail if there is no assertion of PSLVERR. 
   
    
        assert(dut.PSLVERR.value == 1), "Slave error is not asserted"
    
    
  Both test 1 and 2 passing output can be seen in [apb_sram_passing.log](https://github.com/vyomasystems-lab/challenges-rpjayaraman/blob/master/level3_design/apb_sram_passing.log)
  
### Test 3 - Reset in the middle
  It is mandatory to test the design by asserting the reset in the middle of operation to make sure the design is working properly. Here we have asserted reset in during the READ operation. As a result our checker should be able to catch the issue by asserting a FAIL. As we expected the test 3 failed with mismatch in write and read value. we can also observe from the log that READ value is 0 due to the reset.

![image](https://user-images.githubusercontent.com/105109240/182206856-bac7b88e-69ac-4816-a1ce-9c6d6a7f4774.png)

  ```
  130000.00ns INFO     #### Reset Test ######
145000.00ns INFO     #### Writing DATA ######
170000.00ns INFO     WRITE OP: PSEL: 1 PWRITE: 1 PADDR 27 PWDATA 13 PREADY 1
170000.00ns INFO     #### Reading DATA ######
210000.00ns INFO     READ OP: PSEL: 1 PWRITE: 0 PADDR 27 READ_DATA 0 PREADY 0
210000.00ns INFO     reset_test_apb failed
                     Traceback (most recent call last):
                       File "/workspace/Data-science-with-Python/challenges-rpjayaraman-master/level3_design/test_apb_v3_sram.py", line 148, in reset_test_apb
                         assert dut.PWDATA.value == dut.PRDATA.value, "Write data is not matching with read data"
                     AssertionError: Write data is not matching with read data
                    
  ```
## Design BUG
  In order to make sure the test is working as expected and also we required to capture the bug. I have decided to inject bug in the APB 3 feature which is the Slave error response.
  
  we can see the bug in the below code, where the PSLVERR value is supposed to be 1, but it is 0.
  
  
 ![image](https://user-images.githubusercontent.com/105109240/182031226-61bd0ad5-bc17-48f4-a217-3b74a0961f84.png)

This bug will turn off the purpose of the PSLVERR pin. As we have injected the bug, it is time to run the test to make sure it captures the injected bug. 

![image](https://user-images.githubusercontent.com/105109240/182206331-e45eca08-21ea-4df9-bfd5-92da2b44e781.png)

As expected, the bug is captured in the test 2, where it checks for the assertion of PSLVERR. Read operation is performed on the addr 72, which is definitely an invalid address. By flipping the bit to 1, it will make the test pass.
 
## Verification Strategy

Three cases:
 1. Check Write/Read operation
 2. Check PSLVERR feature
 3. Reset in the middle of the operation

    
  The purpose of the test 1 is to test the write/read operation and it is validated with the help of checker at the end of the test. 
  The intention of the test 2 is to check the PSLVERR feature. So we need to create a neagtive testbench to perform the undesired action. As a result of negative test case, the PSLVERR pin should be asserted. checker on the PSLVERR pin will make sure the intent of the test is captured.
  The test 3 is kind of a negative testing, where we are pulling the reset at the middle of the operation and expecting the test to fail.

## Is the verification complete?
   Partially YES. We have tested the main feature Write/Read operation,  insertion of reset at the middle of test scenario and PSLVERR feature.we have covered the most of the design. However checking on wait state can also be performed to make the verification complete.
    
  Credits: 
  [1] https://github.com/courageheart/AMBA_APB_SRAM
  [2] http://web.eecs.umich.edu/~prabal/teaching/eecs373-f12/readings/ARM_AMBA3_APB.pdf

