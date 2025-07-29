#!/usr/bin/env python3
"""
Debug script to trace selling price calculation issues
"""

from stk_demo import setup_stk_production_model

def debug_calculation_values():
    """Debug the calculation values step by step"""
    print("🔍 DEBUGGING CALCULATION VALUES")
    print("=" * 60)
    
    # Create the STK model
    simulation = setup_stk_production_model()
    
    # Check all attributes and their current values
    print("\n📊 All Attributes Before Simulation:")
    for block_id, block in simulation.blocks.items():
        print(f"\n📦 Block: {block.name}")
        for attr_id, attr in block.attributes.items():
            print(f"   {attr_id}: {attr.name} = {attr.value} (Type: {attr.attribute_type.value})")
            if attr.dependencies:
                print(f"      Dependencies: {attr.dependencies}")
    
    # Check the dependency graph
    print(f"\n🔗 Dependency Graph:")
    print(f"   Nodes: {simulation.dependency_graph.nodes}")
    print(f"   Edges: {dict(simulation.dependency_graph.edges)}")
    
    # Check for cycles
    cycles = simulation.dependency_graph.find_cycles()
    print(f"\n🔄 Cycles Detected: {len(cycles)}")
    for i, cycle in enumerate(cycles, 1):
        print(f"   Cycle {i}: {' → '.join(cycle)}")
    
    # Run simulation and trace execution
    print(f"\n⚙️ Running Simulation with Debug...")
    results = simulation.run_simulation()
    
    print(f"\n📋 Final Results:")
    print(f"   Status: {results['status']}")
    
    if results.get('calculated_values'):
        print(f"\n💰 Calculated Values:")
        for key, value in results['calculated_values'].items():
            attr = simulation._find_attribute_by_id(key)
            attr_name = attr.name if attr else key
            print(f"   {attr_name}: {value}")
    
    # Check specific selling_price calculation
    selling_price_attr = simulation._find_attribute_by_id("selling_price")
    if selling_price_attr:
        print(f"\n🔍 Selling Price Attribute Details:")
        print(f"   ID: {selling_price_attr.id}")
        print(f"   Name: {selling_price_attr.name}")
        print(f"   Dependencies: {selling_price_attr.dependencies}")
        print(f"   Current Value: {selling_price_attr.value}")
        print(f"   Has Calculation Logic: {selling_price_attr.calculation_logic is not None}")
    
    # Check production cost
    production_cost_attr = simulation._find_attribute_by_id("production_cost")
    if production_cost_attr:
        print(f"\n🏭 Production Cost Details:")
        print(f"   Value: {production_cost_attr.value}")
        print(f"   Dependencies: {production_cost_attr.dependencies}")

def test_selling_price_calculation_directly():
    """Test the selling price calculation logic directly"""
    print(f"\n🧪 TESTING SELLING PRICE CALCULATION DIRECTLY")
    print("=" * 60)
    
    from stk_demo import create_adaptive_pricing_calculator
    
    # Create the calculation function
    calc_func = create_adaptive_pricing_calculator()
    
    # Test with realistic values
    test_deps = {
        "production_cost": 46431.25,  # Realistic production cost
        "market_demand": 1000  # Default market demand
    }
    
    test_metadata = {
        "target_margin": 25,
        "max_price": 65
    }
    
    print(f"Test Input:")
    print(f"   production_cost: €{test_deps['production_cost']}")
    print(f"   market_demand: {test_deps['market_demand']} units")
    print(f"   target_margin: {test_metadata['target_margin']}%")
    print(f"   max_price: €{test_metadata['max_price']}")
    
    result = calc_func(test_deps, test_metadata)
    
    print(f"\nCalculation Steps:")
    base_price = test_deps["production_cost"] * (1 + test_metadata["target_margin"] / 100)
    demand_factor = min(1.2, test_deps["market_demand"] / 1000)
    adjusted_price = base_price * demand_factor
    final_price = min(adjusted_price, test_metadata["max_price"])
    
    print(f"   base_price = {test_deps['production_cost']} * 1.25 = €{base_price:.2f}")
    print(f"   demand_factor = min(1.2, {test_deps['market_demand']}/1000) = {demand_factor}")
    print(f"   adjusted_price = {base_price:.2f} * {demand_factor} = €{adjusted_price:.2f}")
    print(f"   final_price = min({adjusted_price:.2f}, {test_metadata['max_price']}) = €{final_price:.2f}")
    
    print(f"\n📊 Result: €{result:.2f}")

if __name__ == "__main__":
    debug_calculation_values()
    test_selling_price_calculation_directly() 