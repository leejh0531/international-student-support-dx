import os
import shutil
import tempfile
import unittest
from pathlib import Path

import pandas as pd
from src.data_utils import DATA_DIR, filter_requirements, load_table, search_faq, validate_dataset


class DataTests(unittest.TestCase):
    def test_real_dataset_and_faculty_scope(self):
        tables = validate_dataset()
        self.assertEqual(len(tables), 6)
        requirements, departments = tables['academic_requirements.csv'], tables['departments.csv']
        self.assertTrue(filter_requirements(requirements, departments, 'ej').empty)
        aj = filter_requirements(requirements, departments, 'aj')
        self.assertEqual(set(aj.department_id), {'aj', 'all_system_design'})
        self.assertEqual(len(filter_requirements(requirements, departments)), len(requirements))

    def test_year_and_other_filters_combine(self):
        requirements = load_table('academic_requirements.csv')
        departments = load_table('departments.csv')
        older = requirements.copy()
        older['admission_year'] = '2025'
        rows = pd.concat([requirements, older])
        result = filter_requirements(rows, departments, 'aj', requirement_type='promotion',
                                     stage='1_to_2', admission_year='2026')
        self.assertEqual(result.requirement_id.tolist(), ['aj_2026_promotion_1_to_2'])

    def test_literal_search_special_characters_and_nulls(self):
        rows = pd.DataFrame({'question_ja': ['[test]', None, 'plain'],
                             'question_en': ['Hello', 'a.b', None],
                             'answer_ja': ['', '', ''], 'answer_en': ['', '', ''],
                             'category_id': ['a', 'b', 'c']})
        self.assertEqual(search_faq(rows, '[').index.tolist(), [0])
        self.assertEqual(search_faq(rows, '.').index.tolist(), [1])
        self.assertEqual(search_faq(rows, 'HELLO').index.tolist(), [0])
        self.assertEqual(len(search_faq(rows, '')), 3)
        self.assertTrue(search_faq(rows, '*').empty)

    def test_paths_do_not_depend_on_working_directory(self):
        previous = Path.cwd()
        try:
            with tempfile.TemporaryDirectory() as directory:
                os.chdir(directory)
                self.assertEqual(len(validate_dataset()), 6)
        finally:
            os.chdir(previous)

    def test_broken_dataset_rejected(self):
        cases = [('academic_requirements.csv', 'stage', None),
                 ('support_faq.csv', 'category_id', 'missing-category'),
                 ('academic_requirements.csv', 'source_id', 'missing-source'),
                 ('academic_requirements.csv', 'department_id', 'all_missing'),
                 ('departments.csv', 'faculty_id', 'missing-faculty'),
                 ('academic_requirements.csv', 'confidence', 'invalid'),
                 ('support_categories.csv', 'category_id', '')]
        for filename, column, value in cases:
            with self.subTest(filename=filename, column=column), tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / 'data'
                shutil.copytree(DATA_DIR, target)
                rows = pd.read_csv(target / filename, dtype=str, keep_default_na=False)
                if value is None:
                    rows = rows.drop(columns=[column])
                else:
                    rows.loc[0, column] = value
                rows.to_csv(target / filename, index=False)
                with self.assertRaises(ValueError):
                    validate_dataset(target)

    def test_duplicate_ids_and_missing_files_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'data'
            shutil.copytree(DATA_DIR, target)
            rows = pd.read_csv(target / 'support_faq.csv', dtype=str)
            rows.loc[1, 'faq_id'] = rows.loc[0, 'faq_id']
            rows.to_csv(target / 'support_faq.csv', index=False)
            with self.assertRaises(ValueError):
                validate_dataset(target)
            (target / 'support_categories.csv').unlink()
            with self.assertRaises(FileNotFoundError):
                validate_dataset(target)


if __name__ == '__main__':
    unittest.main()
