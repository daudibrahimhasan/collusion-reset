import json
import random
from collections import defaultdict

# Fixed seed for reproducibility
SEED = 42
rng = random.Random(SEED)

# Load the original 50 tasks
with open("task_manifest_data_search50.json", "r", encoding="utf-8") as file:
    tasks = json.load(file)

# Group tasks by family
families = defaultdict(list)

for task in tasks:
    families[task["task_family"]].append(task["task_id"])

# Proposed sample sizes
sample_sizes = {
    "support_escalation": 8,
    "procurement_finance": 8,
    "clinical_safety": 7,
    "campus_facilities": 7
}

# Randomly select tasks without replacement
selected = []

for family, count in sample_sizes.items():
    selected.extend(rng.sample(families[family], count))

# Shuffle selected tasks
rng.shuffle(selected)

# Create 15 ordered pairs
pairs = []

for i in range(0, len(selected), 2):
    pairs.append({
        "tasks": [selected[i], selected[i + 1]]
    })

# Save the episode manifest
manifest = {"pairs": pairs}

with open("pilot-001.json", "w", encoding="utf-8") as file:
    json.dump(manifest, file, indent=2, ensure_ascii=False)

# Display results
print("Random seed:", SEED)
print("Total selected tasks:", len(selected))
print("Total pairs:", len(pairs))

for i, pair in enumerate(pairs, start=1):
    print(f"Episode {i}: {pair['tasks'][0]} | {pair['tasks'][1]}")

print("\nSaved to pilot-001.json")