#!/usr/bin/env python3
"""
Simple test to debug STK simulation core functionality
"""

from stk_simulation import STKSimulation, Block, Attribute, AttributeType

def test_simple_simulation():
    """Test basic simulation without cycles"""
    print("🧪 Testing Simple Simulation (No Cycles)")
    print("=" * 50)
    
    # Create simple simulation
    sim = STKSimulation("test_simple")
    
    # Create simple block
    test_block = Block("test_001", "Test Block")
    
    # Add input attributes
    test_block.add_attribute(Attribute(
        "input_a", "Input A", AttributeType.INPUT, 10
    ))
    
    test_block.add_attribute(Attribute(
        "input_b", "Input B", AttributeType.INPUT, 20
    ))
    
    # Add calculated attribute (no cycle)
    test_block.add_attribute(Attribute(
        "output_c", "Output C", AttributeType.CALCULATED,
        dependencies=["input_a", "input_b"],
        calculation_logic=lambda deps, meta: deps.get("input_a", 0) + deps.get("input_b", 0)
    ))
    
    sim.add_block(test_block)
    
    print(f"📊 Block setup:")
    print(f"   Attributes: {len(test_block.attributes)}")
    print(f"   Dependencies: {len(sim.dependency_graph.edges)}")
    
    # Check for cycles
    cycles = sim.dependency_graph.find_cycles()
    print(f"   Cycles detected: {len(cycles)}")
    
    if cycles:
        print(f"   Cycle details: {cycles}")
    
    # Run simulation
    print(f"\n⚙️ Running simulation...")
    results = sim.run_simulation()
    
    print(f"\n📋 Results:")
    print(f"   Status: {results['status']}")
    print(f"   Execution Time: {results['execution_time']:.3f}s")
    
    if results.get('calculated_values'):
        print(f"   Calculated Values:")
        for key, value in results['calculated_values'].items():
            attr = sim._find_attribute_by_id(key)
            attr_name = attr.name if attr else key
            print(f"     {attr_name}: {value}")
    
    if results.get('error_message'):
        print(f"   Error: {results['error_message']}")
    
    return results['status'] == 'completed'

def test_cycle_simulation():
    """Test simulation with intentional cycle"""
    print("\n🔄 Testing Cycle Detection & Resolution")
    print("=" * 50)
    
    # Create simulation with cycle
    sim = STKSimulation("test_cycle")
    
    # Create block with cycle
    cycle_block = Block("cycle_001", "Cycle Test Block")
    
    # Create A -> B -> A cycle
    cycle_block.add_attribute(Attribute(
        "attr_a", "Attribute A", AttributeType.CALCULATED,
        dependencies=["attr_b"],
        calculation_logic=lambda deps, meta: deps.get("attr_b", 50) * 1.1
    ))
    
    cycle_block.add_attribute(Attribute(
        "attr_b", "Attribute B", AttributeType.CALCULATED,
        dependencies=["attr_a"],
        calculation_logic=lambda deps, meta: deps.get("attr_a", 100) * 0.9
    ))
    
    sim.add_block(cycle_block)
    
    print(f"📊 Cycle test setup:")
    print(f"   Attributes: {len(cycle_block.attributes)}")
    
    # Check for cycles
    cycles = sim.dependency_graph.find_cycles()
    print(f"   Cycles detected: {len(cycles)}")
    
    if cycles:
        print(f"   Cycle details: {cycles}")
    
    # Run simulation
    print(f"\n⚙️ Running cycle resolution...")
    results = sim.run_simulation()
    
    print(f"\n📋 Results:")
    print(f"   Status: {results['status']}")
    print(f"   Execution Time: {results['execution_time']:.3f}s")
    
    if results.get('calculated_values'):
        print(f"   Calculated Values:")
        for key, value in results['calculated_values'].items():
            attr = sim._find_attribute_by_id(key)
            attr_name = attr.name if attr else key
            print(f"     {attr_name}: {value}")
    
    if results.get('error_message'):
        print(f"   Error: {results['error_message']}")
    
    return results['status'] == 'completed'

def main():
    print("🧪 BASIC STK SIMULATION TESTING")
    print("Testing core functionality step by step")
    print("=" * 60)
    
    # Test 1: Simple simulation
    test1_passed = test_simple_simulation()
    
    # Test 2: Cycle simulation  
    test2_passed = test_cycle_simulation()
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"   Simple Simulation: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"   Cycle Resolution:  {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print(f"\n🎉 All tests passed! Core functionality is working.")
        return 0
    else:
        print(f"\n⚠️ Some tests failed. Debug needed.")
        return 1

if __name__ == "__main__":
    exit(main()) 