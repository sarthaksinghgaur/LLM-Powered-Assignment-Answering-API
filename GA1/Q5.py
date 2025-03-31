import os, json

def execute(question: str, parameter):
    result = evaluate_excel_formula_manual(parameter["sheet_formula"])
    return result
    
def evaluate_excel_formula_manual(formula):
    """
    Manual implementation of the specific formula
    =SUM(TAKE(SORTBY(array, sort_array), 1, 13))
    """
    try:
        # Extract the arrays from the formula
        import re
        pattern = r"=SUM\(TAKE\(SORTBY\(\{([^}]*)\}, \{([^}]*)\}\), (\d+), (\d+)\)\)"
        match = re.match(pattern, formula)
        
        if not match:
            raise ValueError("Formula format not recognized")

        # Convert string arrays to Python lists
        def str_to_list(s):
            return [int(x) for x in s.strip('{}').split(',')]

        array = str_to_list(match.group(1))
        sort_array = str_to_list(match.group(2))
        
        first_number = int(match.group(3))  # 1
        second_number = int(match.group(4)) # 13

        # Implement SORTBY - sort array based on sort_array
        paired = list(zip(array, sort_array))
        paired.sort(key=lambda x: x[first_number])
        sorted_array = [x[0] for x in paired]

        # Implement TAKE - get first 13 elements
        taken = sorted_array[:second_number]

        # Implement SUM
        return sum(taken)

    except Exception as e:
        print(f"Error evaluating formula: {e}")
        return None