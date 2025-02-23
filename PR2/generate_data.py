# Практична робота №2
# Варіант №4
# Робота з MultiIndex. Створіть багаторівневий індекс і оптимізуйте вибірку за допомогою .xs().

import json
import random
import argparse

NUM_RECORDS = 10000

def generate_data():
    return {
        "region": random.choice(["North", "South", "East", "West"]),
        "category": random.choice(["Shoes", "Cap", "Jacket", "Pants"]),
        "id": random.randint(1, 1000),
        "price": round(random.uniform(10, 500), 2),
        "availability": random.choice([True, False])
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate JSON file with hierarchical data")
    parser.add_argument("--num_records", type=int, default=NUM_RECORDS, help="Number of records to generate")
    parser.add_argument("--path", type=str, default='data.json', help="Output JSON file path")
    args = parser.parse_args()

    data = [generate_data() for _ in range(args.num_records)]
    with open(args.path, "w") as f:
        json.dump(data, f, indent=4)

