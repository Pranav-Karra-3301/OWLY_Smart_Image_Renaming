import json
import os
from datetime import datetime

class IndexManager:
    def __init__(self, index_file='processed_files_index.json'):
        self.index_file = index_file
        self.index = self.load_index()

    def load_index(self):
        if os.path.exists(self.index_file):
            with open(self.index_file, 'r') as f:
                return json.load(f)
        return {}

    def save_index(self):
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=4)

    def is_file_processed(self, file_path):
        return file_path in self.index

    def add_processed_file(self, original_path, new_path, new_filename, description):
        self.index[original_path] = {
            'new_path': new_path,
            'new_filename': new_filename,
            'original_filename': os.path.basename(original_path),
            'processing_date': datetime.now().isoformat(),  # Add the processing date
            'description': description  # Add the description
        }
        self.save_index()

    def get_processed_file_info(self, original_path):
        return self.index.get(original_path)

    def get_all_processed_files(self):
        return self.index
    
    def search(self, query):
        # Simple search that matches the query in filename, description, or original filename
        results = []
        for file_data in self.index.values():
            if (query.lower() in file_data['new_filename'].lower() or 
                query.lower() in file_data['original_filename'].lower() or 
                query.lower() in file_data.get('description', '').lower()):
                results.append(file_data)
        return results