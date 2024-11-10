import pandas as pd
import numpy as np
from math import log2
import json

# Function to pretty-print a dictionary in JSON format
def print_json(data):
    print(json.dumps(data, indent=4))

# Function to calculate entropy
def entropy(data):
    class_counts = data.iloc[:, -1].value_counts()  # Last column is target
    total_records = len(data)
    entropy_value = 0
    for count in class_counts:
        probability = count / total_records
        entropy_value -= probability * log2(probability)
    print(f"Entropy: {entropy_value}")  # Debug print
    return entropy_value

# Function to calculate information gain
def information_gain(data, attribute):
    total_entropy = entropy(data)
    print(f"Total Entropy for {attribute}: {total_entropy}")  # Debug print
    
    # Split data based on the attribute's unique values
    attribute_values = data[attribute].unique()
    weighted_entropy = 0
    for value in attribute_values:
        subset = data[data[attribute] == value]
        subset_entropy = entropy(subset)
        weighted_entropy += (len(subset) / len(data)) * subset_entropy
        print(f"Weighted Entropy for {attribute} = {value}: {weighted_entropy}")  # Debug print
    
    # Information Gain = Entropy before split - Weighted entropy after split
    gain = total_entropy - weighted_entropy
    print(f"Information Gain for {attribute}: {gain}")  # Debug print
    return gain

# Function to find the best attribute to split on
def best_attribute(data):
    attributes = data.columns[:-1]  # Exclude target class column
    best_attr = None
    best_gain = -np.inf
    
    for attribute in attributes:
        print(f"Evaluating {attribute}")  # Debug print
        gain = information_gain(data, attribute)
        if gain > best_gain:
            best_gain = gain
            best_attr = attribute
    
    print(f"Best Attribute to Split: {best_attr} with Gain: {best_gain}")  # Debug print
    return best_attr

# Recursive function to build the decision tree
def build_tree(data):
    # Check for stopping conditions
    if len(data) == 0:
        print("No data left to split.")  # Debug print
        return None
    
    # If all examples have the same class, return a leaf node
    if len(data.iloc[:, -1].unique()) == 1:
        label = data.iloc[:, -1].values[0]
        print(f"Leaf Node created with class: {label}")  # Debug print
        return {'label': label}
    
    # If no attributes left to split on, return the majority class as a leaf
    if len(data.columns) == 1:  # Only target class left
        majority_class = data.iloc[:, -1].mode()[0]
        print(f"Majority class Leaf Node created with class: {majority_class}")  # Debug print
        return {'label': majority_class}
    
    # Find the best attribute to split on
    best_attr = best_attribute(data)
    
    # Create a node for this attribute
    tree = {'attribute': best_attr, 'branches': {}}
    print(f"Creating tree node for attribute: {best_attr}")  # Debug print
    
    # Split the data based on the best attribute
    for value in data[best_attr].unique():
        print(f"Splitting data on {best_attr} = {value}")  # Debug print
        subset = data[data[best_attr] == value].drop(columns=[best_attr])
        tree['branches'][value] = build_tree(subset)
    
    print_json(tree)
    return tree

# Function to print the decision tree
def print_tree(tree, level=0):
    if 'label' in tree:
        print(f"{'    ' * level}Leaf: {tree['label']}")
    else:
        print(f"{'    ' * level}Attribute: {tree['attribute']}")
        for value, subtree in tree['branches'].items():
            print(f"{'    ' * (level + 1)}Value: {value}")
            print_tree(subtree, level + 2)

# Modified predict function that prints the decision path
def predict(tree, record, level=0):
    if 'label' in tree:
        print(f"{' ' * level}Leaf: {tree['label']}")  # Debug print
        return tree['label']
    else:
        attribute = tree['attribute']
        attribute_value = record[attribute]
        print(f"{' ' * level}{attribute}? {attribute_value}")  # Debug print
        
        # Now we recursively predict on the next branch, showing the path
        if attribute_value in tree['branches']:
            print(f"{' ' * (level + 2)}{attribute_value}:")  # Debug print
            return predict(tree['branches'][attribute_value], record, level + 4)
        else:
            print(f"{' ' * (level + 2)}{attribute_value}: (Unknown)")  # Debug print
            return None  # Handle cases where the value does not exist in the tree

# Function to load the dataset from a CSV file and allow user input for target column
def load_data_and_create_tree(csv_file):
    # Load dataset
    data = pd.read_csv(csv_file)
    
    print("\nColumns in the dataset:")
    for idx, col in enumerate(data.columns):
        print(f"{idx}: {col}")
    
    # Allow the user to select the target class column
    target_idx = int(input("\nSelect the target class column by index: "))
    target_class = data.columns[target_idx]
    
    # Reorder columns to make the target class the last column
    data = data[[col for col in data.columns if col != target_class] + [target_class]]

    # Remove columns with unique values (such as 'rid') which do not help with the classification
    data = data.loc[:, data.nunique() != len(data)]
    
    # Build decision tree
    print(f"\nBuilding decision tree with target class: {target_class}")
    tree = build_tree(data)
    
    return tree, target_class, data

# Example usage
if __name__ == "__main__":
    csv_file = input("Enter the CSV file path: ")
    
    # Load the dataset and build the decision tree
    tree, target_class, data = load_data_and_create_tree(csv_file)
    
    # Print the built decision tree
    print("\nDecision Tree:")
    print_tree(tree)
    
    # Example prediction
    print("\nMake a prediction:")
    record = {}
    for feature in data.columns[:-1]:
        value = input(f"Enter value for {feature}: ")
        record[feature] = value
    
    prediction = predict(tree, record)
    print(f"\nPredicted class: {prediction} (Target class: {target_class})")

'''
Sure! Here's a summarized explanation of each function in the provided code:

 1. `entropy(data)`
   - Purpose: Calculates the entropy of the dataset (a measure of uncertainty or impurity).
   - Input: `data` (a DataFrame of examples with features and target class).
   - Output: The entropy value, a float representing the level of uncertainty (higher entropy means more uncertainty).
   - Process: Counts the distribution of classes in the target column and computes the entropy using the formula:  
     \[
     \text{Entropy} = - \sum_{i=1}^{n} p_i \log_2 p_i
     \]
     where \(p_i\) is the probability of class \(i\).

 2. `information_gain(data, attribute)`
   - Purpose: Calculates the information gain from splitting the dataset by a given attribute (used for decision tree construction).
   - Input: `data` (the dataset) and `attribute` (a feature/column in the dataset).
   - Output: The information gain value, a float, representing how much uncertainty is reduced by splitting on the attribute.
   - Process:  
     - Calculates the total entropy of the dataset.
     - Splits the dataset based on the attribute’s unique values, calculates the weighted entropy for each subset, and computes the information gain as the difference between the total entropy and the weighted entropy.

 3. `best_attribute(data)`
   - Purpose: Determines the best attribute to split the data on by maximizing information gain.
   - Input: `data` (the dataset).
   - Output: The name of the attribute (column) that provides the highest information gain.
   - Process:  
     - Loops over each attribute (excluding the target class) and calculates its information gain using the `information_gain` function.
     - Returns the attribute with the highest gain.

 4. `build_tree(data)`
   - Purpose: Recursively builds a decision tree based on the dataset.
   - Input: `data` (the dataset).
   - Output: A dictionary representing the decision tree, where each node is either an attribute (for splitting) or a leaf (with the class label).
   - Process:  
     - Checks stopping conditions (if the data is empty, all examples are of the same class, or no attributes are left to split on).
     - Finds the best attribute to split on using `best_attribute`.
     - Recursively splits the data and creates a tree, where each branch represents a split by a feature.

 5. `print_tree(tree, level=0)`
   - Purpose: Prints the decision tree in a readable, hierarchical format.
   - Input: `tree` (a dictionary representing the decision tree), `level` (indentation level, default is 0).
   - Output: None (prints the tree structure to the console).
   - Process:  
     - Recursively prints the tree, indenting child nodes according to their depth in the tree.
     - If the node is a leaf, it prints the class label; if it’s an attribute node, it prints the attribute and its possible values.

 6. `predict(tree, record, level=0)`
   - Purpose: Makes a prediction for a given record by traversing the decision tree.
   - Input: `tree` (the decision tree), `record` (a dictionary representing the input features of a single example), and `level` (indentation level for printing the decision path).
   - Output: The predicted class label.
   - Process:  
     - Recursively traverses the tree based on the values in `record`.
     - At each node, checks the value of the attribute in the record and follows the corresponding branch until a leaf is reached, which gives the predicted class.

 7. `load_data_and_create_tree(csv_file)`
   - Purpose: Loads a dataset from a CSV file, allows the user to select the target class column, builds a decision tree, and returns the tree and relevant data.
   - Input: `csv_file` (the path to the CSV file).
   - Output: The decision tree, the target class, and the cleaned dataset.
   - Process:  
     - Loads the dataset using `pd.read_csv`.
     - Prompts the user to select the target class column.
     - Reorders columns so the target class is last.
     - Removes any columns that have unique values (such as `rid`), as they don't provide useful information for the decision tree.
     - Builds and returns the decision tree using `build_tree`.

 Key Concepts:
- Entropy: A measure of the unpredictability or impurity in a dataset.
- Information Gain: The reduction in entropy (uncertainty) after splitting the data based on an attribute.
- Decision Tree: A tree structure where each internal node represents a decision based on an attribute, and each leaf node represents a class label.

These functions together implement the core logic of building a decision tree for classification using the ID3 algorithm. The decision tree splits the data based on attributes that maximize information gain, recursively creating a tree structure to classify new examples.
'''