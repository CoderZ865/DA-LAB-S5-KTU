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

'''