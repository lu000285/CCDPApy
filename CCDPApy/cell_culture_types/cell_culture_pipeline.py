from CCDPApy.cell_culture_types.fed_batch.cell_culture_data.cell_culture_data_handler import FedBatchCellCultureDataHandler
from CCDPApy.cell_culture_types.perfusion.cell_culture_data.cell_culture_data_handler import PerfusionCellCultureDataHandler
from CCDPApy.helper import input_path

def cell_culture_pipeline(cell_culture_type, file, parameters):
    ''''''

    if cell_culture_type=='perfusion':
        cell_culture_data_handler = PerfusionCellCultureDataHandler
    elif cell_culture_type=='fed-batch':
        cell_culture_data_handler = FedBatchCellCultureDataHandler
    else:
        return
    
    # call cell culture data handler
    cell_culture = cell_culture_data_handler(parameters=parameters)

    # load data file
    file_path = input_path(file_name=file)
    cell_culture.load_data(file=file_path)

    # data-processing
    cell_culture.perform_data_process()

    return cell_culture

