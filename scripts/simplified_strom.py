#!/usr/bin/env python3
"""Simplified Strom-inspired auto-evolution for Hermes Agent.

Focuses on prompt optimization and lesson learning without 
requiring direct Hermes CLI integration (which needs interactive setup).

Uses simulated fitness evaluation and hindsight-based learning.
"""

import json
import os
import random
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

HERMES_CACHE = os.path.expanduser("~/.hermes/cache")


class SimplifiedStromEvolution:
    """Simplified Strom evolution without CLI dependency issues."""

    def __init__(self):
        self.run_count = 0
        self.fitness_history: List[Dict] = []
        self.best_fitness = 0.0
        self.best_prompt = ""
        self.lessons_saved = 0

    def evaluate_fitness_simulated(self, prompt: str, task_difficulty: str = "medium") -> Dict:
        """Simulate fitness evaluation based on prompt characteristics."""
        self.run_count += 1
        timestamp = datetime.now().isoformat()

        fitness = 0.5  # base score

        if any(kw in prompt.lower() for kw in ["organize", "classify", "simple", "step"]):
            fitness += 0.2

        if 20 < len(prompt) < 200:
            fitness += 0.1

        difficulty_scores = {"simple": 0.1, "medium": 0.0, "complex": -0.1}
        fitness += difficulty_scores.get(task_difficulty, 0.0)

        fitness = min(max(fitness, 0.0), 1.0)

        metrics = {
            "run_id": self.run_count,
            "timestamp": timestamp,
            "prompt": prompt,
            "fitness": fitness,
            "success": fitness >= 0.5,
            "task_difficulty": task_difficulty,
            "prompt_length": len(prompt),
        }

        self.fitness_history.append(metrics)

        if len(self.fitness_history) > 15:
            self.fitness_history = self.fitness_history[-15:]

        return metrics

    def mutate_prompt(self, prompt: str, fitness: float) -> str:
        """Apply mutation to prompt based on fitness."""
        if fitness >= 0.8:
            if "step" not in prompt.lower():
                return prompt + " Use passos claros e concisos."
            elif "conciso" not in prompt.lower():
                return prompt.replace("passos claros", "passos muito concisos")
            return prompt + " Otimize para clareza máxima."
        elif fitness < 0.4:
            structuring_keywords = [
                "Primeiro, organize por tipo:",
                "Etapa 1: Classifique os itens",
                "Step 1: Sort by category",
            ]
            return random.choice(structuring_keywords) + " " + prompt
        else:
            if "claridade" not in prompt.lower():
                return prompt + " Priorize clareza na resposta."
            return prompt

    def run_cycle(self, prompt: str, iterations: int = 3, 
                  task_difficulty: str = "medium") -> Dict:
        """Run one evolution cycle."""
        print("=" * 55)
        print("SIMPLIFIED STROM EVOLUTION")
        print("=" * 55)
        print(f"
Task: {prompt[:60]}...")
        print(f"Iterations: {iterations}")
        print(f"Difficulty: {task_difficulty}")
        print()

        best_fitness = 0.0
        best_metrics = None

        for i in range(iterations):
            print(f"--- Cycle {i+1}/{iterations} ---")

            metrics = self.evaluate_fitness_simulated(prompt, task_difficulty)
            fitness = metrics["fitness"]

            print(f"Fitness: {fitness:.2f} | Success: {metrics['success']}")
            print(f"Prompt length: {metrics['prompt_length']}")

            if fitness > best_fitness:
                best_fitness = fitness
                best_metrics = metrics
                print("  -> NEW BEST!")

            if i < iterations - 1:
                prompt = self.mutate_prompt(prompt, fitness)
                print(f"  -> Mutated prompt")

        self._save_lesson(best_metrics, best_fitness)

        print("
" + "=" * 55)
        print(f"BEST FITNESS: {best_fitness:.2f}")
        print("=" * 55)

        return {
            "best_fitness": best_fitness,
            "best_metrics": best_metrics,
            "total_cycles": iterations,
            "evolution_prompt": prompt,
        }

    def _save_lesson(self, metrics: Optional[Dict], fitness: float):
        """Save lesson using hindsight pattern."""
        lesson = {
            "timestamp": datetime.now().isoformat(),
            "fitness": fitness,
            "run_count": self.run_count,
            "lessons": self._extract_lessons(metrics),
        }

        lessons_dir = os.path.join(HERMES_CACHE, "lessons")
        os.makedirs(lessons_dir, exist_ok=True)

        lesson_file = os.path.join(
            lessons_dir,
            f"lesson_{self.run_count}_{int(fitness*100)}.json",
        )

        try:
            with open(lesson_file, "w") as f:
                json.dump(lesson, f, indent=2, ensure_ascii=False)
            self.lessons_saved += 1
            print(f"
Lesson saved: {lesson_file}")
        except Exception as e:
            print(f"
Could not save lesson: {e}")

    def _extract_lessons(self, metrics: Optional[Dict]) -> List[str]:
        """Extract actionable lessons."""
        lessons = []

        if not metrics:
            lessons.append("No data to extract lessons from")
            return lessons

        if metrics["success"] or metrics["fitness"] >= 0.5:
            lessons.append("Current approach is effective - maintain structured prompt")
            lessons.append(f"Prompt of {metrics['prompt_length']} chars worked well")
        else:
            lessons.append("Prompt needs restructuring")
            lessons.append("Add classification keywords (simple/medium/complex)")

        lessons.append("Compression threshold 20 saves credits")
        lessons.append("Save this lesson for reuse in future sessions via hindsight plugin")

        return lessons


def main():
    if len(sys.argv) < 2:
        print("Usage: simplified_strom.py <prompt> [iterations] [difficulty]")
        print("Difficulty: simple | medium | complex")
        print("Example: simplified_strom.py 'Classify these files' 3 medium")
        sys.exit(1)

    user_prompt = sys.argv[1]
    iterations = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    difficulty = sys.argv[3] if len(sys.argv) > 3 else "medium"

    evolver = SimplifiedStromEvolution()

    print("
" + "=" * 65)
    print("HERMES SIMPLIFIED STROM EVOLUTION")
    print("=" * 65)
    print(f"
Task: {user_prompt}")
    print(f"Iterations: {iterations}")
    print(f"Difficulty: {difficulty}")
    print("
Starting auto-evolution cycle...
")

    results = evolver.run_cycle(user_prompt, iterations, difficulty)

    print("
" + "=" * 65)
    if results["best_fitness"] >= 0.6:
        print("Optimization effective - lessons preserved via hindsight")
    else:
        print("Consider running again with different parameters")
    print("=" * 65)

    print(f"
Summary:")
    print(f"  - Runs: {evolver.run_count}")
    print(f"  - Best fitness: {results['best_fitness']:.2f}")
    print(f"  - Lessons saved: {evolver.lessons_saved}")


if __name__ == "__main__":
    main()
