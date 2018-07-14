import re

from yapsy.IPlugin import IPlugin
from customwarnings import DataCheckWarningLevel,DataCheckWarning

class CheckCollectionContents(IPlugin):
	def check(self, dir):
		warnings = []
		for collection in dir.getCollections():
			OoM = collection['order_of_magnitude']['id']

			materials = []
			if 'materials' in collection:
				for m in collection['materials']['items']:
					materials.append(m['id'])
			
			data_categories = []
			if 'data_categories' in collection:
				for c in collection['data_categories']['items']:
					data_categories.append(c['id'])

			types = []
			if 'type' in collection:
				for t in collection['type']['items']:
					types.append(t['id'])

			if len(types) < 1:
				warning = DataCheckWarning("", dir.getCollectionNN(collection['id']), DataCheckWarningLevel.ERROR, collection['id'], "Collection type not provided")
				warnings.append(warning)


			if OoM > 4:
				subCollections = dir.getCollectionsDescendants(collection['id'])
				if len(subCollections) < 1:
					warning = DataCheckWarning("", dir.getCollectionNN(collection['id']), DataCheckWarningLevel.INFO, collection['id'], "Suspicious situation: large collection without subcollections")
					warnings.append(warning)

			if((not 'data_access_fee' in collection or collection['data_access_fee'] == False) and 
					(not 'data_access_joint_project' in collection or collection['data_access_joint_project'] == False) and 
					(not 'data_access_uri' in collection or re.search('^\s*$', collection['data_access_uri']))):
				warning = DataCheckWarning("", dir.getCollectionNN(collection['id']), DataCheckWarningLevel.ERROR, collection['id'], "No data access mode enabled and no data access policy URI provided for collection")
				warnings.append(warning)

			if((not 'sample_access_fee' in collection or collection['sample_access_fee'] == False) and 
					(not 'sample_access_joint_project' in collection or collection['sample_access_joint_project'] == False) and 
					(not 'sample_access_uri' in collection or re.search('^\s*$', collection['sample_access_uri']))):
				warning = DataCheckWarning("", dir.getCollectionNN(collection['id']), DataCheckWarningLevel.ERROR, collection['id'], "No sample access mode enabled and no sample access policy URI provided for collection")
				warnings.append(warning)

			if 'HOSPITAL' in types or 'DISEASE_SPECIFIC' in types or 'RD' in types:
				diagnoses = []
				if 'diagnosis_available' in collection:
					for d in collection['diagnosis_available']['items']:
						diagnoses.append(d['id'])
				if len(diagnoses) < 1:
					warning = DataCheckWarning("", dir.getCollectionNN(collection['id']), DataCheckWarningLevel.ERROR, collection['id'], "No diagnoses provide for HOSPITAL or DISEASE_SPECIFIC or RD collection")
					warnings.append(warning)

			if 'BIOLOGICAL_SAMPLES' in data_categories and len(materials) == 0:
				warning = DataCheckWarning("", dir.getCollectionNN(collection['id']), DataCheckWarningLevel.ERROR, collection['id'], "No material types are provided while biological samples are collected")
				warnings.append(warning)

			if 'IMAGING_DATA' in data_categories:
				modalities = []
				if 'imaging_modality' in collection:
					for m in collection['imaging_modality']['items']:
						modalities.append(m['id'])
				if len(modalities) < 1:
					warning = DataCheckWarning("", dir.getCollectionNN(collection['id']), DataCheckWarningLevel.ERROR, collection['id'], "No image modalities provided for image collection")
					warnings.append(warning)

				image_dataset_types = []
				if 'image_dataset_type' in collection:
					for idt in collection['image_dataset_type']['items']:
						image_dataset_types.append(idt['id'])
				if len(image_dataset_types) < 1:
					warning = DataCheckWarning("", dir.getCollectionNN(collection['id']), DataCheckWarningLevel.WARNING, collection['id'], "No image dataset types provided for image collection")
					warnings.append(warning)


		return warnings
