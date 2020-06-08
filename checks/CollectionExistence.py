# vim:ts=8:sw=8:tw=0:noet 

import logging as log

from yapsy.IPlugin import IPlugin
from customwarnings import DataCheckWarningLevel,DataCheckWarning,DataCheckEntityType

class CollectionExistence(IPlugin):
	def check(self, dir, args):
		warnings = []
		log.info("Running collection existence checks (CollectionExistence)")
		for biobank in dir.getBiobanks():
			collections = dir.getGraphBiobankCollectionsFromBiobank(biobank['id'])
			if len(collections.edges) < 1:
				warning = DataCheckWarning(self.__class__.__name__, "", dir.getBiobankNN(biobank['id']), DataCheckWarningLevel.ERROR, biobank['id'], DataCheckEntityType.BIOBANK, "Missing at least one collection for biobank")
				warnings.append(warning)
		return warnings
