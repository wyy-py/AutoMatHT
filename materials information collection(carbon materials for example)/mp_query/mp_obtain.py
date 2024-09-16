from mp_api.client import MPRester  # must be the latest version 
from pymatgen.io.vasp import Poscar
import pandas as pd
import os


with MPRester("Y4oFeZhadP8CInN0GcdzipsTl7DqINod") as mpr:
    docs = mpr.summary.search(material_ids=["mp-149", "mp-13", "mp-22526"])

example_doc = docs[0]
list_of_available_fields = mpr.summary.available_fields
print("list_of_available_fields", list_of_available_fields)
mpid = example_doc.material_id
formula = example_doc.formula_pretty
example_structure = example_doc.structure
print("mpid", mpid)
print("formula", formula)
print("example_structure", example_structure)


with MPRester("Y4oFeZhadP8CInN0GcdzipsTl7DqINod") as mpr:
    docs = mpr.summary.search(chemsys=["C"], fields=["material_id", "structure"])

# Define a directory to store POSCAR files
output_dir = "mp_structures"
os.makedirs(output_dir, exist_ok=True)

# CSV file to store mp_id information
csv_file_path = "mp_structures.csv"
mp_ids = []

for doc in docs:
   mp_id = doc.material_id
   carbon_structure = doc.structure
   mp_ids.append(mp_id)
   # Save the structure to a POSCAR file
   output_folder = os.path.join(output_dir, mp_id)
   os.makedirs(output_folder, exist_ok=True)
   poscar_file_path = os.path.join(output_folder, 'POSCAR')
   Poscar(carbon_structure).write_file(poscar_file_path)

ids_df = pd.DataFrame(mp_ids, columns=['mp_ids'])
ids_df.to_csv("mp_structures.csv", index=False)
   
