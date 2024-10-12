import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

async def cycle_counter(dut):
    while True:
        await RisingEdge(dut.hclk)
        dut.cycle_cnt.value = dut.cycle_cnt.value + 1

# R type
@cocotb.test()
async def test_add(dut):
    clock = Clock(dut.hclk, 10, units="ns") # 100MHz clk signal
    cocotb.start_soon(clock.start())

    # sys reset
    dut.hrstn.value = 0
    await Timer(10, units="ns")
    dut.hrstn.value = 1

    # cycle_counter++
    dut.cycle_cnt.value = 0
    cocotb.start_soon(cycle_counter(dut))

    # Test R-Type Instruction (ADD)
    dut.inst_in.value = 0b00000000000100001000000110110011  # add
    await Timer(60, units="ns")
    assert dut.dec_add.value == 1, "ADD signal not set correctly"

# I type
@cocotb.test()
async def test_addi(dut):
    clock = Clock(dut.hclk, 10, units="ns") # 100MHz
    cocotb.start_soon(clock.start())

    # reset
    dut.hrstn.value = 0
    await Timer(10, units="ns")
    dut.hrstn.value = 1

    # cycle_counter++
    dut.cycle_cnt.value = 0
    cocotb.start_soon(cycle_counter(dut))

    dut.inst_in.value = 0b00000000000100001000000010010011 # addi
    await Timer(60, units="ns")
    assert dut.dec_addi.value == 1, "dec_addi signal incorrect"
    assert dut.dec_imm_en.value == 1, "Immediate enable signal incorrect"
    assert dut.dec_rd.value == 1, "dec_rd incorrect"
    assert dut.dec_rs1.value == 1, "dec_rs1 incorrect"

# S type
@cocotb.test()
async def test_switch(dut):
    # 100MHz clk signal
    clock = Clock(dut.hclk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # reset signal
    dut.hrstn.value = 0
    await Timer(10, units="ns")
    dut.hrstn.value = 1

    # update cycle_counter
    dut.cycle_cnt.value = 0
    cocotb.start_soon(cycle_counter(dut))

    dut.inst_in.value = 0b00000000001100001010000000100011 # sw
    await Timer(60, units="ns")
    assert dut.dec_sw.value == 1, "dec_sw signal incorrect"
    # assert dut.dec_rs1.value == 1, "TEMP"
    # assert dut.dec_rs2.value == 1, "TEMP"
    # assert dut.dec_store_en.value == 1, "TEMP"

# B type
@cocotb.test()
async def test_beq(dut):
    # 100MHz clk signal
    clock = Clock(dut.hclk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # reset signal
    dut.hrstn.value = 0
    await Timer(10, units="ns")
    dut.hrstn.value = 1

    # update cycle_counter
    dut.cycle_cnt.value = 0
    cocotb.start_soon(cycle_counter(dut))

    dut.inst_in.value = 0b00000000000100001000000001100011 # beq
    await Timer(60, units="ns")
    assert dut.dec_beq.value == 1, "dec_sw signal incorrect"
    # assert dut.dec_rs1.value == 1, "TEMP"
    # assert dut.dec_rs2.value == 1, "TEMP"
    # assert dut.dec_store_en.value == 1, "TEMP"

# U type
@cocotb.test()
async def test_lui(dut):
    # 100MHz clk signal
    clock = Clock(dut.hclk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # reset signal
    dut.hrstn.value = 0
    await Timer(10, units="ns")
    dut.hrstn.value = 1

    # update cycle_counter
    dut.cycle_cnt.value = 0
    cocotb.start_soon(cycle_counter(dut))

    dut.inst_in.value = 0b00000000000000000001000010110111 # lui
    await Timer(60, units="ns")
    assert dut.dec_lui.value == 1, "dec_lui signal incorrect"
    # assert dut.dec_rs1.value == 1, "TEMP"
    # assert dut.dec_rs2.value == 1, "TEMP"
    # assert dut.dec_store_en.value == 1, "TEMP"

# J type
@cocotb.test()
async def test_jal(dut):
    # 100MHz clk signal
    clock = Clock(dut.hclk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # reset signal
    dut.hrstn.value = 0
    await Timer(10, units="ns")
    dut.hrstn.value = 1

    # update cycle_counter
    dut.cycle_cnt.value = 0
    cocotb.start_soon(cycle_counter(dut))

    dut.inst_in.value = 0b00000000000000000001000011101111 # jal
    await Timer(60, units="ns")
    assert dut.dec_jal.value == 1, "dec_jal signal incorrect"

# R & I type
@cocotb.test()
async def test_add_addi(dut):
    # 100MHz clk signal
    clock = Clock(dut.hclk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # reset signal
    dut.hrstn.value = 0
    await Timer(10, units="ns")
    dut.hrstn.value = 1

    # update cycle_counter
    dut.cycle_cnt.value = 0
    cocotb.start_soon(cycle_counter(dut))

    dut.inst_in.value = 0b00000000000100001000000110110011  # add
    await Timer(50, units="ns")
    assert dut.dec_add.value == 1, "dec_add signal incorrect"

    dut.inst_in.value = 0b00000000000100001000000010010011  # addi
    await Timer(100, units="ns")
    assert dut.dec_addi.value == 1, "dec_addi signal incorrect"
    assert dut.dec_imm_en.value == 1, "dec_imm_en signal incorrect"
    assert dut.dec_rd.value == 1, "dec_rd incorrect"
    assert dut.dec_rs1.value == 1, "dec_rs1 incorrect"

