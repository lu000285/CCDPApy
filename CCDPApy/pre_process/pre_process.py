from concurrent.futures import process
from CCDPApy.Species.MeasuredData import MeasuredData
###########################################################################

###########################################################################
def pre_process(bio_process, feed_name):
    '''
    '''
    exp_info = bio_process.get_exp_info()           # Experiment Info DF
    measured_data = bio_process.get_measured_data() # Measured Data Info DF

    md = MeasuredData(experiment_info=exp_info,
                      raw_data=measured_data,
                      feed_name=feed_name)

    pre_data = md.get_pre_data()
    feed_added = md.get_feed_added()

    bio_process.set_process_flag(process='pre', flag=True) # Set pre process flag True
    bio_process.set_pre_process_df(pre_data)
    bio_process.set_feed_added(feed_added)

###########################################################################