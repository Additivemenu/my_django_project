print("hello")


import pandas as pd
import random
from faker import Faker

# Initialize faker for generating random names and hobbies
fake = Faker()

# Generate 1 million rows of data
rows = 1_000_000
data = {
    "Name": [fake.name() for _ in range(rows)],
    "Age": [random.randint(18, 90) for _ in range(rows)],
    "Hobbies": [fake.word() for _ in range(rows)]
}
df = pd.DataFrame(data)

# Save to an Excel file
df.to_excel("large_excel_file_people_1M_rows.xlsx", index=False)
