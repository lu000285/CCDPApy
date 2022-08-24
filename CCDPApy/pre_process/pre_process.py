from test_package.Species.MeasuredData import MeasuredData


###########################################################################

###########################################################################
def pre_process(bio_process):
    exp_info = bio_process.get_exp_info()
    measured_data = bio_process.get_measured_data()

    md = MeasuredData(experiment_info=exp_info,
                      raw_data=measured_data)

    pre_data = md.get_pre_data()

    bio_process.set_pre_process(pre_data)

    return bio_process

###########################################################################