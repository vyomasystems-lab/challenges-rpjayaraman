# See LICENSE.vyoma for details

TOPLEVEL_LANG ?= verilog

PWD=$(shell pwd)

VERILOG_SOURCES = $(PWD)/apb_v3_sram.v               # provide your design path

TOPLEVEL :=  apb_v3_sram         # design file
MODULE   :=  test_apb_v3_sram   # test file

include $(shell cocotb-config --makefiles)/Makefile.sim

clean_all: clean
	rm -rf *.xml sim_build __pycache__ 
