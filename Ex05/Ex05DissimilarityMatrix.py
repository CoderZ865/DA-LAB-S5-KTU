"""
Write a python program to find the dissimilarity of nominal, numeric and mixed attribute types






"""

import math, csv, pandas as pd


def minkowski_distance(A, B, p):
    if isinstance(A, (int, float)) and isinstance(B, (int, float)):
        A, B = [A], [B]
    
    if len(A) != len(B):
        raise ValueError("Objects must have the same dimension.")

    powered_difference = [abs(a - b)**p for a, b in zip(A, B)]
    distance = math.pow(sum(powered_difference), 1 / p)

    return distance


def normalize(attribute):
    """Normalize a list of numbers to the range [0, 1]."""
    min_val = min(attribute)
    max_val = max(attribute)
    return [(x - min_val) / (max_val - min_val) for x in attribute]


def print_matrix(Type, matrix):
    print()
    print(f'{Type} dissimilarity matrix')
    print('........'*len(matrix))
    for i in matrix:
        for j in i:
            print(f"{float(j):.2}\t",end="")
        print()
    print('........'*len(matrix))
    print()


def select_attribute(Name, df, attribute_type):
    selected_attribute = None
    valid_attributes = df.select_dtypes(include=[attribute_type]).columns.tolist()
    
    while selected_attribute not in valid_attributes:
        selected_attribute = input(f"Select a {attribute_type} attribute to store into {Name}: ")
        if selected_attribute not in valid_attributes:
            print("Invalid selection. Please choose a valid attribute name from the following options:")
            print(valid_attributes)

    print(f"You selected: {selected_attribute} for {Name}")
    return df[selected_attribute]


def nominal_dissimilarity_matrix(attribute, matrix):
    for i in range(len(attribute)):
        temp = []
        for j in range(i + 1):  # Loop only up to the diagonal (i + 1)
            if attribute[i] == attribute[j]:
                temp.append(0)
            else:
                temp.append(1)
        matrix.append(temp)
    print_matrix('Nominal', matrix)


def numeric_dissimilarity_matrix(attribute, matrix, p):
    for i in range(len(attribute)):
        temp = []
        for j in range(i + 1):  # Loop only up to the diagonal (i + 1)
            temp.append(minkowski_distance(attribute[i],attribute[j],p))
        matrix.append(temp)
    print_matrix('Numeric', matrix)


def mixed_dissimilarity_matrix(*matrices):
    number_of_matrices = len(matrices)
    if number_of_matrices == 1:
        return matrices[0]  # Return the single matrix if only one is provided
    
    # Initialize an empty result matrix
    size = len(matrices[0])  # Assume all matrices are of the same size
    result = [[0 for j in range(i+1)] for i in range(size)]
    
    # Sum corresponding elements from each triangular matrix
    for matrix in matrices:
        for i in range(size):
            for j in range(i + 1):  # Only process lower triangular part
                result[i][j] += matrix[i][j]

    for i in range(size):
        for j in range(i + 1):
            result[i][j] /= number_of_matrices
    
    print_matrix('mixed',result)


while True:
    try:
        metrics = int(input('''
                            Which distance metric to use?
                            1. Manhattan
                            2. Euclidean
                            3. Intermediate
                            your option: '''))
        if metrics in [1, 2, 3]:  # Check if the input is within the desired range
            break
        else:
            print("Please enter a valid option: 1, 2, or 3.")
    except ValueError:
        print("Invalid input. Please enter an integer: 1, 2, or 3.")

p = 1.5 if metrics == 3 else metrics

def main():
    # nominal_data = input("Enter nominal attributes (comma-separated): ").split(',')
    # nominal_data = [item.strip() for item in nominal_data]  # Remove any extra spaces

    # numeric_data = input("Enter numeric attributes (comma-separated): ").split(',')
    # numeric_data = [float(item.strip()) for item in numeric_data]  # Convert to float and strip spaces

    # with open("Ex05\Ex05data.csv", 'r') as datfile:
    #     reader = csv.reader(datfile)

    #     nominal_data = []
    #     numeric_data = []

    #     for row in reader:
    #         nominal_data.append(row[0])
    #         numeric_data.append(int(row[1]))

    # print(f'Nominal Data: {nominal_data}\nNumeric Data: {numeric_data}')

    file_path="Ex05\Ex05data.csv"
    df = pd.read_csv(file_path)

    nominal_attributes = df.select_dtypes(include=['object']).columns.tolist()
    numeric_attributes = df.select_dtypes(include=['number']).columns.tolist()

    print("Attributes found:")
    print(f"Nominal Attributes: {nominal_attributes}")
    print(f"Numeric Attributes: {numeric_attributes}")

    nominal_data = select_attribute("nominal_data",df, "object")
    numeric_data = select_attribute("numeric_data",df, "number")

    nominal_matrix = []
    numeric_matrix = []

    nominal_dissimilarity_matrix(nominal_data, nominal_matrix)
    numeric_dissimilarity_matrix(normalize(numeric_data), numeric_matrix, p)
    mixed_dissimilarity_matrix(nominal_matrix, numeric_matrix)


if __name__ == "__main__":
    main()
