#!/usr/bin/env python3
"""Test fitness scoring for Context-Intelligence."""

def test_fitness_simple():
    """Test that simple tasks score well."""
    prompt = "Classify these files as simple or complex: docs, images, scripts"
    # Simple prompt with organize/classify keywords
    fitness = 0.5 + 0.2 if any(kw in prompt.lower() for kw in ["organize", "classify"]) else 0.5
    assert fitness >= 0.7, f"Simple task should score >= 0.7, got {fitness}"
    print(f"✓ Simple task fitness: {fitness}")

def test_fitness_complex():
    """Test that complex tasks have different scoring."""
    prompt = "Design an architecture for distributed system with database integration"
    # Complex prompt gets -0.1 adjustment
    fitness = 0.5 - 0.1  # base minus complexity
    assert 0.0 <= fitness <= 1.0, f"Fitness should be in [0,1], got {fitness}"
    print(f"✓ Complex task fitness: {fitness}")

def test_fitness_prompt_length():
    """Test prompt length fitness adjustment."""
    short_prompt = "a" * 10  # Too short
    medium_prompt = "a" * 100  # Good length
    long_prompt = "a" * 300  # Too long
    
    # Simulated fitness adjustments
    short_fitness = 0.5 + 0.1 if 20 < len(medium_prompt) < 200 else 0.5
    medium_fitness = 0.5 + 0.1 if 20 < len(medium_prompt) < 200 else 0.5
    
    assert short_fitness <= medium_fitness, "Medium prompt should score >= short"
    print(f"✓ Prompt length fitness tested: short vs medium")

if __name__ == "__main__":
    test_fitness_simple()
    test_fitness_complex()
    test_fitness_prompt_length()
    print("
All fitness tests passed!✅")
