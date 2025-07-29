"""
STK Produktion Digital Twin - Comprehensive Demo
Task 1 Implementation Showcase

This demo demonstrates:
1. Complex business attribute relationships
2. Scenario-based simulation runs
3. Cycle detection and resolution
4. LangGraph orchestration in action
5. Evaluation metrics and business insights

Author: Nidhir Bhavsar
Purpose: Circonomit Hiring Challenge Demonstration
"""

import sys
import json
from stk_simulation import (
    STKSimulation, Block, Attribute, AttributeType, 
    SimulationEvaluator
)

def create_energy_cost_calculator():
    """Business logic for energy cost calculation"""
    def calculate_energy_cost(deps, metadata):
        base_energy_price = deps.get("base_energy_price", 0.15)  # €/kWh
        production_volume = deps.get("production_volume", 1000)  # units
        energy_per_unit = metadata.get("energy_per_unit", 2.5)  # kWh/unit
        
        total_energy_cost = base_energy_price * production_volume * energy_per_unit
        return round(total_energy_cost, 2)
    
    return calculate_energy_cost

def create_production_cost_calculator():
    """Business logic for total production cost"""
    def calculate_production_cost(deps, metadata):
        material_cost = deps.get("material_cost", 0)
        energy_cost = deps.get("energy_cost", 0)
        labor_cost = deps.get("labor_cost", 0)
        overhead_factor = metadata.get("overhead_factor", 1.15)
        
        base_cost = material_cost + energy_cost + labor_cost
        total_cost = base_cost * overhead_factor
        return round(total_cost, 2)
    
    return calculate_production_cost

def create_profit_margin_calculator():
    """Business logic for profit margin calculation"""
    def calculate_profit_margin(deps, metadata):
        selling_price = deps.get("selling_price", 0)  # €/unit
        production_cost_total = deps.get("production_cost", 0)  # Total €
        production_volume = deps.get("production_volume", 1000)  # units
        
        if selling_price == 0 or production_volume == 0:
            return 0.0
        
        # Convert total production cost to per-unit cost
        production_cost_per_unit = production_cost_total / production_volume
        
        # Calculate profit margin: (selling_price - cost_per_unit) / selling_price * 100
        profit_margin = ((selling_price - production_cost_per_unit) / selling_price) * 100
        return round(profit_margin, 2)
    
    return calculate_profit_margin

def create_market_demand_calculator():
    """Business logic for market demand based on price sensitivity"""
    def calculate_market_demand(deps, metadata):
        base_demand = metadata.get("base_demand", 1200)
        selling_price = deps.get("selling_price", 50)
        price_elasticity = metadata.get("price_elasticity", -0.8)
        base_price = metadata.get("base_price", 45)
        
        # Price elasticity formula: % change in demand = elasticity * % change in price
        price_change_pct = (selling_price - base_price) / base_price
        demand_change_pct = price_elasticity * price_change_pct
        adjusted_demand = base_demand * (1 + demand_change_pct)
        
        return max(0, round(adjusted_demand))
    
    return calculate_market_demand

def create_adaptive_pricing_calculator():
    """Business logic for adaptive pricing based on costs and competition"""
    def calculate_adaptive_price(deps, metadata):
        production_cost = deps.get("production_cost", 0)
        market_demand = deps.get("market_demand", 1000)
        target_margin = metadata.get("target_margin", 25)  # %
        max_price = metadata.get("max_price", 65)
        
        # Cost-plus pricing with demand adjustment
        base_price = production_cost * (1 + target_margin / 100)
        
        # Demand-based adjustment (higher demand = higher price tolerance)
        demand_factor = min(1.2, market_demand / 1000)  # Cap at 20% increase
        adjusted_price = base_price * demand_factor
        
        return min(adjusted_price, max_price)
    
    return calculate_adaptive_price

def setup_stk_production_model() -> STKSimulation:
    """
    Create STK Produktion's complete business model with realistic dependencies
    """
    print("🏭 Setting up STK Produktion Digital Twin...")
    
    simulation = STKSimulation("stk_production_demo")
    
    # === SUPPLY CHAIN BLOCK ===
    supply_block = Block("supply_001", "Supply Chain Management")
    
    # Input attributes
    supply_block.add_attribute(Attribute(
        "base_energy_price", "Base Energy Price (€/kWh)", 
        AttributeType.INPUT, 0.15
    ))
    
    supply_block.add_attribute(Attribute(
        "material_cost", "Raw Material Cost (€)", 
        AttributeType.INPUT, 25000, 
        metadata={"material_type": "plastic_metal_blend"}
    ))
    
    supply_block.add_attribute(Attribute(
        "labor_cost", "Direct Labor Cost (€)", 
        AttributeType.INPUT, 15000
    ))
    
    # === PRODUCTION BLOCK ===
    production_block = Block("production_001", "Production Operations")
    
    production_block.add_attribute(Attribute(
        "production_volume", "Production Volume (units)", 
        AttributeType.INPUT, 1000,
        metadata={"capacity_limit": 2000}
    ))
    
    # Calculated energy cost based on production volume
    production_block.add_attribute(Attribute(
        "energy_cost", "Total Energy Cost (€)", 
        AttributeType.CALCULATED,
        dependencies=["base_energy_price", "production_volume"],
        calculation_logic=create_energy_cost_calculator(),
        metadata={"energy_per_unit": 2.5}
    ))
    
    # Total production cost
    production_block.add_attribute(Attribute(
        "production_cost", "Total Production Cost (€)", 
        AttributeType.CALCULATED,
        dependencies=["material_cost", "energy_cost", "labor_cost"],
        calculation_logic=create_production_cost_calculator(),
        metadata={"overhead_factor": 1.15}
    ))
    
    # === MARKET BLOCK ===
    market_block = Block("market_001", "Market & Pricing")
    
    # Market demand calculation
    market_block.add_attribute(Attribute(
        "market_demand", "Market Demand (units)", 
        AttributeType.CALCULATED,
        dependencies=["selling_price"],
        calculation_logic=create_market_demand_calculator(),
        metadata={
            "base_demand": 1200,
            "price_elasticity": -0.8,
            "base_price": 45
        }
    ))
    
    # Adaptive pricing (creates potential cycle with market_demand)
    market_block.add_attribute(Attribute(
        "selling_price", "Selling Price (€/unit)", 
        AttributeType.CALCULATED,
        dependencies=["production_cost", "market_demand"],
        calculation_logic=create_adaptive_pricing_calculator(),
        metadata={
            "target_margin": 25,
            "max_price": 65
        }
    ))
    
    # === FINANCIAL BLOCK ===
    financial_block = Block("financial_001", "Financial Performance")
    
    # Profit margin calculation
    financial_block.add_attribute(Attribute(
        "profit_margin", "Profit Margin (%)", 
        AttributeType.CALCULATED,
        dependencies=["selling_price", "production_cost", "production_volume"],
        calculation_logic=create_profit_margin_calculator()
    ))
    
    # Add blocks to simulation
    simulation.add_block(supply_block)
    simulation.add_block(production_block)
    simulation.add_block(market_block)
    simulation.add_block(financial_block)
    
    print(f"✅ Model setup complete:")
    print(f"   📦 {len(simulation.blocks)} business blocks")
    print(f"   📊 {sum(len(block.attributes) for block in simulation.blocks.values())} total attributes")
    print(f"   🔗 Complex interdependencies established")
    
    return simulation

def run_baseline_scenario(simulation: STKSimulation):
    """Run baseline scenario - normal operating conditions"""
    print("\n" + "="*60)
    print("📊 SCENARIO 1: Baseline Operations")
    print("="*60)
    print("Normal operating conditions - no external shocks")
    
    # No overrides - use default values
    results = simulation.run_simulation()
    
    print(f"\n📋 Results Summary:")
    print(f"   Status: {results['status']}")
    print(f"   Execution Time: {results['execution_time']:.3f}s")
    print(f"   Cycles Resolved: {results['cycles_resolved']}")
    
    if results['calculated_values']:
        print(f"\n💰 Key Business Metrics:")
        values = results['calculated_values']
        print(f"   Energy Cost: €{values.get('energy_cost', 'N/A')}")
        print(f"   Production Cost: €{values.get('production_cost', 'N/A')}")
        print(f"   Selling Price: €{values.get('selling_price', 'N/A')}/unit")
        print(f"   Market Demand: {values.get('market_demand', 'N/A')} units")
        print(f"   Profit Margin: {values.get('profit_margin', 'N/A')}%")
    
    return results

def run_energy_crisis_scenario(simulation: STKSimulation):
    """Run energy crisis scenario - energy prices spike"""
    print("\n" + "="*60)
    print("⚡ SCENARIO 2: Energy Price Crisis")
    print("="*60)
    print("Energy prices spike to 250% of normal levels")
    
    # Energy price shock: 0.15 -> 0.375 €/kWh
    simulation.set_scenario_override("base_energy_price", 0.375)
    
    results = simulation.run_simulation()
    
    print(f"\n📋 Results Summary:")
    print(f"   Status: {results['status']}")
    print(f"   Execution Time: {results['execution_time']:.3f}s")
    print(f"   Cycles Resolved: {results['cycles_resolved']}")
    
    if results['calculated_values']:
        print(f"\n💰 Impact Analysis:")
        values = results['calculated_values']
        print(f"   Energy Cost: €{values.get('energy_cost', 'N/A')} (+150% increase)")
        print(f"   Production Cost: €{values.get('production_cost', 'N/A')}")
        print(f"   Selling Price: €{values.get('selling_price', 'N/A')}/unit")
        print(f"   Market Demand: {values.get('market_demand', 'N/A')} units")
        print(f"   Profit Margin: {values.get('profit_margin', 'N/A')}%")
        
        # Business insights
        profit_margin = values.get('profit_margin', 0)
        if profit_margin < 10:
            print(f"   ⚠️  WARNING: Low profit margin - consider operational adjustments")
        
        market_demand = values.get('market_demand', 0)
        if market_demand < 800:
            print(f"   ⚠️  WARNING: Reduced market demand - pricing impact detected")
    
    return results

def run_supply_disruption_scenario(simulation: STKSimulation):
    """Run supply chain disruption scenario"""
    print("\n" + "="*60)
    print("🚚 SCENARIO 3: Supply Chain Disruption")
    print("="*60)
    print("Material costs increase due to supply constraints")
    
    # Supply chain disruption: material costs increase by 40%
    simulation.set_scenario_override("material_cost", 35000)  # +40% from 25000
    simulation.set_scenario_override("base_energy_price", 0.15)  # Reset energy price
    
    results = simulation.run_simulation()
    
    print(f"\n📋 Results Summary:")
    print(f"   Status: {results['status']}")
    print(f"   Execution Time: {results['execution_time']:.3f}s")
    
    if results['calculated_values']:
        print(f"\n💰 Supply Chain Impact:")
        values = results['calculated_values']
        print(f"   Material Cost: €{values.get('material_cost', 'N/A')} (+40% increase)")
        print(f"   Production Cost: €{values.get('production_cost', 'N/A')}")
        print(f"   Selling Price: €{values.get('selling_price', 'N/A')}/unit")
        print(f"   Profit Margin: {values.get('profit_margin', 'N/A')}%")
    
    return results

def run_optimization_scenario(simulation: STKSimulation):
    """Run production optimization scenario"""
    print("\n" + "="*60)
    print("🎯 SCENARIO 4: Production Optimization")
    print("="*60)
    print("Optimize production volume for maximum efficiency")
    
    # Reset overrides and optimize production volume
    simulation.scenario_overrides.clear()
    simulation.set_scenario_override("production_volume", 1400)  # Increase production
    simulation.set_scenario_override("labor_cost", 12000)  # Efficiency gains
    
    results = simulation.run_simulation()
    
    print(f"\n📋 Results Summary:")
    print(f"   Status: {results['status']}")
    print(f"   Execution Time: {results['execution_time']:.3f}s")
    
    if results['calculated_values']:
        print(f"\n💰 Optimization Results:")
        values = results['calculated_values']
        print(f"   Production Volume: {values.get('production_volume', 'N/A')} units (+40%)")
        print(f"   Labor Cost: €{values.get('labor_cost', 'N/A')} (efficiency gains)")
        print(f"   Energy Cost: €{values.get('energy_cost', 'N/A')}")
        print(f"   Production Cost: €{values.get('production_cost', 'N/A')}")
        print(f"   Profit Margin: {values.get('profit_margin', 'N/A')}%")
    
    return results

def evaluate_all_scenarios(scenario_results):
    """Comprehensive evaluation of all scenarios"""
    print("\n" + "="*60)
    print("📈 COMPREHENSIVE SCENARIO EVALUATION")
    print("="*60)
    
    for i, (scenario_name, results) in enumerate(scenario_results, 1):
        print(f"\n🔍 Scenario {i}: {scenario_name}")
        
        if results['status'] == 'completed':
            # Calculate quality metrics
            simulation = STKSimulation()  # Dummy for evaluation
            quality_metrics = SimulationEvaluator.evaluate_simulation_quality(simulation, results)
            
            print(f"   Overall Quality Score: {quality_metrics['overall_quality']:.2f}/1.00")
            print(f"   Accuracy: {quality_metrics['accuracy']:.2f}")
            print(f"   Performance: {quality_metrics['performance']:.2f}")
            print(f"   Robustness: {quality_metrics['robustness']:.2f}")
            print(f"   Business Relevance: {quality_metrics['business_relevance']:.2f}")
            
            # Business insights
            values = results.get('calculated_values', {})
            profit_margin = values.get('profit_margin', 0)
            
            if profit_margin > 20:
                print(f"   💚 Strong profitability")
            elif profit_margin > 10:
                print(f"   💛 Moderate profitability")
            else:
                print(f"   ❤️ Profitability concern")
        else:
            print(f"   ❌ Scenario failed: {results.get('error_message', 'Unknown error')}")

def demonstrate_cycle_detection():
    """Demonstrate cycle detection and resolution capabilities"""
    print("\n" + "="*60)
    print("🔄 CYCLE DETECTION DEMONSTRATION")
    print("="*60)
    
    print("The STK model contains a designed cycle:")
    print("   selling_price → market_demand → selling_price")
    print("\nLangGraph agents detect and resolve this cycle using:")
    print("   • Business-aware resolution strategies")
    print("   • Temporal dampening for price feedback")
    print("   • Iterative convergence algorithms")
    
    # Create simple cycle example
    cycle_sim = STKSimulation("cycle_demo")
    
    # Block with cyclic dependencies
    cycle_block = Block("cycle_001", "Cycle Example")
    
    # Create simple A → B → A cycle
    cycle_block.add_attribute(Attribute(
        "price", "Product Price", AttributeType.CALCULATED,
        dependencies=["demand"],
        calculation_logic=lambda deps, meta: deps.get("demand", 100) * 0.05 + 40
    ))
    
    cycle_block.add_attribute(Attribute(
        "demand", "Market Demand", AttributeType.CALCULATED,
        dependencies=["price"],
        calculation_logic=lambda deps, meta: max(50, 1500 - deps.get("price", 50) * 20)
    ))
    
    cycle_sim.add_block(cycle_block)
    
    print(f"\n🔍 Cycle Detection Analysis:")
    cycles = cycle_sim.dependency_graph.find_cycles()
    print(f"   Cycles Found: {len(cycles)}")
    for i, cycle in enumerate(cycles, 1):
        print(f"   Cycle {i}: {' → '.join(cycle)}")
    
    # Run simulation to show resolution
    print(f"\n⚙️ Running cycle resolution...")
    results = cycle_sim.run_simulation()
    
    if results['status'] == 'completed':
        print(f"   ✅ Cycles successfully resolved")
        print(f"   Execution time: {results['execution_time']:.3f}s")
    else:
        print(f"   ❌ Resolution failed: {results.get('error_message')}")

def main():
    """Main demonstration orchestration"""
    print("🏭 STK PRODUKTION DIGITAL TWIN - COMPREHENSIVE DEMO")
    print("Circonomit Hiring Challenge - Task 1 Implementation")
    print("=" * 60)
    print("Demonstrating agentic decision infrastructure using LangGraph")
    print("Author: Nidhir Bhavsar")
    print("=" * 60)
    
    try:
        # Setup the complete STK production model
        simulation = setup_stk_production_model()
        
        # Run multiple scenarios
        scenario_results = []
        
        # Baseline scenario
        baseline_results = run_baseline_scenario(simulation)
        scenario_results.append(("Baseline Operations", baseline_results))
        
        # Energy crisis scenario
        energy_results = run_energy_crisis_scenario(simulation)
        scenario_results.append(("Energy Price Crisis", energy_results))
        
        # Supply disruption scenario
        supply_results = run_supply_disruption_scenario(simulation)
        scenario_results.append(("Supply Chain Disruption", supply_results))
        
        # Optimization scenario
        optimization_results = run_optimization_scenario(simulation)
        scenario_results.append(("Production Optimization", optimization_results))
        
        # Comprehensive evaluation
        evaluate_all_scenarios(scenario_results)
        
        # Cycle detection demonstration
        demonstrate_cycle_detection()
        
        print("\n" + "="*60)
        print("🎉 DEMONSTRATION COMPLETE")
        print("="*60)
        print("Key Achievements Demonstrated:")
        print("   ✅ Complex business model simulation")
        print("   ✅ LangGraph agentic orchestration")
        print("   ✅ Cycle detection and resolution")
        print("   ✅ Scenario-based decision support")
        print("   ✅ Real-time business insights")
        print("   ✅ Comprehensive evaluation framework")
        
        print("\nThis demonstrates STK Produktion's digital twin capability")
        print("for intelligent decision-making in uncertain environments.")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 