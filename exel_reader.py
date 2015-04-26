from openpyxl import load_workbook
#docs/Cheese.xlsx
class exel_reader:
    """
        Implements the IoT Fridge API
    """
    def __init__(self, doc_path):
        self.wb = load_workbook(filename = doc_path)
        self.sheet_names = self.wb.get_sheet_names()

    def getUPC(self):
    	ret = []
    	for value in  self.wb[self.sheet_names[0]].get_cell_collection():
    		val = str(value.value)
    		if val.isdigit():
    			ret.append(val)
    	return ret