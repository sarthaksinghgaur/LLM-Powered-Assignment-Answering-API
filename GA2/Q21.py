import os, json

def execute(question: str, parameter):
    return generate_markdown()
    
def generate_markdown():
    return """# Step Count Analysis

## Introduction
Tracking daily steps is a great way to monitor physical activity and stay motivated. This analysis examines my step count over a week, comparing it with past trends and my friends' activity levels.

## Methodology
To conduct this analysis, I:

1. Logged daily step counts using a fitness tracker.
2. Compared my weekly average with previous weeks.
3. Compared my steps with friends using shared data.
4. Visualized the data using a simple Python script.

## Data Collection
I used the `step_tracker` app to record my steps daily. Below is an example of how the data is structured:

```json
{
    "Monday": 7500,
    "Tuesday": 8200,
    "Wednesday": 6400,
    "Thursday": 9000,
    "Friday": 10000,
    "Saturday": 12000,
    "Sunday": 11000
}
```

## Weekly Comparison
The following table shows my step count compared to my friend's:

| Day       | My Steps | Friend's Steps |
|-----------|---------|---------------|
| Monday    | 7500    | 7800          |
| Tuesday   | 8200    | 8100          |
| Wednesday | 6400    | 6700          |
| Thursday  | 9000    | 9100          |
| Friday    | 10000   | 9800          |
| Saturday  | 12000   | 11500         |
| Sunday    | 11000   | 11200         |

## Key Observations
- **Friday had the highest step count** in the weekdays.
- *Wednesday had the lowest activity*, possibly due to workload.
- My friend's step count was generally similar to mine.

## Insights & Next Steps
> "A journey of a thousand miles begins with a single step."

To improve, I plan to:
- **Increase my mid-week activity** by taking short walks.
- Join a weekend challenge with friends.
- Use `step_tracker.compare()` to analyze long-term trends.

## Visualization
Here’s an example plot generated using Matplotlib:

```python
import matplotlib.pyplot as plt

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
my_steps = [7500, 8200, 6400, 9000, 10000, 12000, 11000]
friend_steps = [7800, 8100, 6700, 9100, 9800, 11500, 11200]

plt.plot(days, my_steps, label="My Steps", marker="o")
plt.plot(days, friend_steps, label="Friend's Steps", marker="s")
plt.xlabel("Day of the Week")
plt.ylabel("Step Count")
plt.legend()
plt.title("Weekly Step Count Comparison")
plt.show()
```

## Additional Resources
For more step tracking tools, visit [Fitbit](https://www.fitbit.com/).

## Image Example
Here’s a sample fitness tracker interface:

![Step Tracker](https://example.com/step_tracker.jpg)"""