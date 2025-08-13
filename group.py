import pandas as pd

def find_groups(df):
    """
    Groups rows in a DataFrame based on shared values in any column.
    
    Args:
        df (pd.DataFrame): The input DataFrame.
        
    Returns:
        list: A list of lists, where each inner list represents a group of row indices.
    """
    groups = []
    # Create a set to keep track of rows that have already been assigned to a group
    grouped_rows = set()
    
    # Iterate through each row of the DataFrame
    for i in range(len(df)):
        # If the row has already been grouped, skip it
        if i in grouped_rows:
            continue
        
        # Start a new group with the current row
        current_group = {i}
        # Get the values of the current row
        current_values = set(df.iloc[i].values)
        
        # Iterate through the rest of the rows
        for j in range(i + 1, len(df)):
            # If the row has already been grouped, skip it
            if j in grouped_rows:
                continue
            
            # Check if there is any common value between the current row and the other row
            if not current_values.isdisjoint(set(df.iloc[j].values)):
                # If there's a match, add the row to the current group
                current_group.add(j)
                # Add the new row's values to the set of values to check against
                current_values.update(set(df.iloc[j].values))

        # Add all rows from the new group to the set of grouped rows
        grouped_rows.update(current_group)
        # Add the new group (as a list of indices) to the list of groups
        groups.append(list(current_group))
    
    return groups

# Sample data
data = {'id': [1, 2, 3, 4, 5],
        'country': ['AUS', 'AUS', 'NZL', 'USA', 'NZL'],
        'occupation': ['Doctor', 'Chef', 'Doctor', 'Engineer', 'Musician']}
df = pd.DataFrame(data)

# Find the groups
groups = find_groups(df)

# Print the groups
print("Groups of row indices:", groups)

# To see the actual rows in each group, you can use the indices:
print("\nGroups of rows:")
for group_indices in groups:
    print(df.iloc[group_indices])
    print("-" * 20)

# To add a 'group_id' column to the original DataFrame
df['group_id'] = None
group_id_counter = 0
for group_indices in groups:
    df.loc[group_indices, 'group_id'] = group_id_counter
    group_id_counter += 1

print("\nDataFrame with a new 'group_id' column:")
print(df)
