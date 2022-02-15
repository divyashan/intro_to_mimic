import pandas as pd
import numpy as np
import pdb
from sklearn.model_selection import train_test_split
from mimic_paths import admissions_path

ICD_CODE_FIELD = 'icd_code'
MODE_GROUP_MAP = {'ethnicity': ('BLACK/AFRICAN AMERICAN', 'WHITE', 'ASIAN', 'HISPANIC/LATINO'),
                  'gender': ('F', 'M'),
                  'insurance': ('Medicaid', 'Medicare'),
                  'marital_status': ('DIVORCED', 'MARRIED', 'SINGLE')}


# Helper functions for querying IDs 
def get_ids_with_icd_codes(diagnoses, id_type, codes):
    ids = set(diagnoses.loc[diagnoses[ICD_CODE_FIELD].map(lambda x:any([x.startswith(code) 
                                                                        for code in codes])), id_type])
    return ids

def get_ids_with_kws(diagnoses, id_type, kws, descr_field='long_title'):
    ids = set(diagnoses.loc[diagnoses[descr_field].map(lambda x:any([keyword in x.lower() 
                                                                     for keyword in kws])), id_type])
    return ids

def get_idxs_of_group(ids, group_name, category, id_type='hadm_id'):
    admissions = pd.read_csv(admissions_path)
    group_ids = admissions[admissions[category] == group_name][id_type]
    group_ids = sorted(list(set(ids).intersection(set(group_ids))))
    
    id_to_index = {h_id : idx for idx, h_id in enumerate(ids)}
    group_id_idxs = [id_to_index[g_id] for g_id in group_ids]
    return group_id_idxs

def get_idxs_not_of_group(ids, group_name, category, id_type='hadm_id'):
    group_idxs = get_idxs_of_group(ids, group_name, category, id_type)
    all_idxs = list(range(len(ids)))
    not_group_idxs = sorted(list(set(all_idxs).difference(set(group_idxs))))
    return not_group_idxs
                    
# Helper functions for querying symptoms via ICD codes or keywords
def get_icd_code_long_title(names, code):
    code_names = names[names['icd_code'].str.startswith(code)]['long_title']
    return list(code_names)[0]

def get_icd_codes_with_prefix(names, code):
    code_names = names[names['icd_code'].str.startswith(code)]['icd_code']
    return list(code_names)