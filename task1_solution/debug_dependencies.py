#!/usr/bin/env python3
"""
Debug script to examine dependency graph structure
"""

from stk_simulation import STKSimulation, Block, Attribute, AttributeType

def debug_dependency_graph():
    """Debug the dependency graph construction"""
    print("🔍 DEBUGGING DEPENDENCY GRAPH")
    print("=" * 60)
    
    # Create simple simulation
    sim = STKSimulation("debug_test")
    
    # Create simple block
    test_block = Block("test_001", "Test Block")
    
    # Add input attributes
    input_a = Attribute("input_a", "Input A", AttributeType.INPUT, 10)
    input_b = Attribute("input_b", "Input B", AttributeType.INPUT, 20)
    
    # Add calculated attribute
    output_c = Attribute(
        "output_c", "Output C", AttributeType.CALCULATED,
        dependencies=["input_a", "input_b"],
        calculation_logic=lambda deps, meta: deps.get("input_a", 0) + deps.get("input_b", 0)
    )
    
    test_block.add_attribute(input_a)
    test_block.add_attribute(input_b)
    test_block.add_attribute(output_c)
    
    sim.add_block(test_block)
    
    print("📊 Dependency Graph Analysis:")
    print(f"   Nodes: {sim.dependency_graph.nodes}")
    print(f"   Edges: {dict(sim.dependency_graph.edges)}")
    print(f"   Reverse Edges: {dict(sim.dependency_graph.reverse_edges)}")
    
    print("\n🔍 Expected execution order: input_a, input_b, then output_c")
    
    # Check in-degree manually
    in_degree = {}
    for node in sim.dependency_graph.nodes:
        in_degree[node] = 0
    
    for node in sim.dependency_graph.nodes:
        for dep in sim.dependency_graph.edges[node]:
            in_degree[dep] += 1
    
    print(f"   In-degrees: {in_degree}")
    
    # Check what should be processed first (in-degree = 0)
    zero_in_degree = [node for node in sim.dependency_graph.nodes if in_degree[node] == 0]
    print(f"   Zero in-degree (process first): {zero_in_degree}")
    
    # Try topological sort
    try:
        order = sim.dependency_graph.topological_sort()
        print(f"   Topological order: {order}")
        print("   ✅ Topological sort succeeded")
    except Exception as e:
        print(f"   ❌ Topological sort failed: {e}")
    
    return True

if __name__ == "__main__":
    debug_dependency_graph() 