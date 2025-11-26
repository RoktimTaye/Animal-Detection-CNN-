import json
import os

notebook_path = 'c:/Users/Raktim/Desktop/Machine-Learning(Animal Detection)/Detect.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the cell with callback definitions
callback_cell_index = -1
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "checkpoint_cb =" in source and "reduce_lr =" in source:
            callback_cell_index = i
            break

if callback_cell_index != -1:
    # Add backup_cb definition
    cell = nb['cells'][callback_cell_index]
    # Check if already added
    if not any("backup_cb =" in line for line in cell['source']):
        # Remove the closing bracket of the previous list if it was there (it wasn't a list, just lines)
        # Append new lines
        new_lines = [
            ",\n",
            "    \"# BackupAndRestore callback for resumable training\\n\",\n",
            "    \"backup_dir = os.path.join(os.getcwd(), 'backup')\\n\",\n",
            "    \"if not os.path.exists(backup_dir):\\n\",\n",
            "    \"    os.makedirs(backup_dir)\\n\",\n",
            "    \"backup_cb = keras.callbacks.BackupAndRestore(backup_dir=backup_dir)\"\n"
        ]
        # Insert before the closing bracket of the source list
        # The source is a list of strings. The last line is likely the closing bracket of the list inside the cell source?
        # No, the source is just lines of code.
        # Let's look at the previous content:
        # "reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6)"
        # We need to append to the list of source lines.
        
        # The last line currently is:
        # "    \"reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6)\"\n"
        # We want to add more lines.
        
        # Actually, looking at the file content from previous steps:
        # "source": [
        #  "checkpoint_cb = ...\n",
        #  ...
        #  "reduce_lr = ...\n"
        # ]
        
        # So we just append to nb['cells'][callback_cell_index]['source']
        
        # But wait, the previous content was inside a list?
        # "source": [
        #  "checkpoint_cb = ...",
        # ]
        
        # So I just append strings to this list.
        
        nb['cells'][callback_cell_index]['source'].append("\n")
        nb['cells'][callback_cell_index]['source'].append("# BackupAndRestore callback for resumable training\n")
        nb['cells'][callback_cell_index]['source'].append("backup_dir = os.path.join(os.getcwd(), 'backup')\n")
        nb['cells'][callback_cell_index]['source'].append("if not os.path.exists(backup_dir):\n")
        nb['cells'][callback_cell_index]['source'].append("    os.makedirs(backup_dir)\n")
        nb['cells'][callback_cell_index]['source'].append("backup_cb = keras.callbacks.BackupAndRestore(backup_dir=backup_dir)\n")
        
        print("Added backup_cb definition.")

# Find the cell with model.fit
fit_cell_index = -1
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "model.fit" in source and "callbacks=[" in source:
            fit_cell_index = i
            break

if fit_cell_index != -1:
    cell = nb['cells'][fit_cell_index]
    # Modify the callbacks list
    new_source = []
    for line in cell['source']:
        if "callbacks=[" in line and "backup_cb" not in line:
            # Replace the line
            new_line = line.replace("callbacks=[checkpoint_cb, earlystop_cb, reduce_lr]", "callbacks=[checkpoint_cb, earlystop_cb, reduce_lr, backup_cb]")
            new_source.append(new_line)
        else:
            new_source.append(line)
    
    nb['cells'][fit_cell_index]['source'] = new_source
    print("Updated model.fit callbacks.")

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook modified successfully.")
