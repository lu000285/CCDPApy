import pandas as pd

from ..helper_func.helper_func import check_key

from ..Species.Cell import Cell
from ..Species.Oxygen import Oxygen
from ..Species.Product import Product
from ..Species.Metabolite import Metabolite
from ..Species.Metabolite import Metabolite2

###########################################################################
def cumulative_calc(bio_process,
                    feed_name,
                    use_feed_conc=True,
                    use_conc_after_feed=False):

    exp_info = bio_process.get_exp_info()               # Get Experiment Info
    measured_data = bio_process.get_measured_data()     # Get Measured Data

    # Cell
    cell = Cell(experiment_info=exp_info,
                raw_data=measured_data,
                feed_name=feed_name,
                name='Cell')
    cell.in_process()
    cell.set_method_flag(method='cumulative', flag=True)
    bio_process.set_cell(cell)

    # Oxygen
    oxygen = Oxygen(experiment_info=exp_info,
                    raw_data=measured_data,
                    feed_name=feed_name,
                    name='Oxygen')
    oxygen.in_process()
    oxygen.set_method_flag(method='cumulative', flag=True)
    bio_process.set_oxygen(oxygen)

    # Product/IgG
    igg = Product(experiment_info=exp_info,
                  raw_data=measured_data,
                  feed_name=feed_name,
                  name='IgG',)
    igg.in_process()
    igg.set_method_flag(method='cumulative', flag=True)
    bio_process.set_igg(igg)

    # AA Cumulative
    spc_lst = bio_process.get_spc_list()  # Get AA List to Analyze
    spc_dict = {}                        # Initialize
    spc_cumulative_df = pd.DataFrame()   # Initialize
    spc_conc_df = pd.DataFrame()
    spc_conc_after_feed_df = pd.DataFrame()

    for s in spc_lst:
        s = s.upper()   # Name
        conc_before = check_key(measured_data, f'{s} CONC. (mM)')   # Concentration Before Feeding
        conc_after = check_key(measured_data, f'{s} CONC. (mM).1')  # Concentration After Feeding
        feed = check_key(measured_data, f'FEED {s} CONC. (mM)')     # Feed Concentration

        # Check Calculated Cumulative Concentration
        cumulative = check_key(measured_data, f'CUM {s} CONS. (mM)')
        if (not cumulative.any()):
            cumulative = check_key(measured_data, f'CUM {s} PROD. (mM)')

        # Metabolite Object
        spc = Metabolite(experiment_info=exp_info,
                         raw_data=measured_data,
                         feed_name=feed_name,
                         name=s,
                         conc_before_feed=conc_before,
                         conc_after_feed=conc_after,
                         feed_conc=feed,
                         cumulative=cumulative,
                         production=True if (s=='LACTATE' or s=='NH3') else False)
        
        # Calculate Cumulative Consumption/Production
        spc.in_process(use_feed_conc=use_feed_conc, use_conc_after_feed=use_conc_after_feed)
        spc.set_method_flag(method='cumulative', flag=True)
        unit = spc.get_cumulative_unit()    # Unit
        
        spc_cumulative_df['CUM '+s+' '+unit] = spc.get_cumulative()  # Add to DF
        spc_conc_df[conc_before.name] = conc_before
        spc_conc_after_feed_df[s+' (mM) (After Feed)'] = spc.get_conc_after_feed()
        spc_dict[s] = spc    # Add to Dictionary

    # Add to bp obj
    bio_process.set_spc_df(spc_cumulative_df)
    bio_process.set_spc_dict(spc_dict=spc_dict)
    bio_process.set_spc_conc(spc_conc_df)
    bio_process.set_spc_conc_after_feed(conc_after_feed=spc_conc_after_feed_df)

    # Other Spc Cumulative Nitrogen, and AA Carbon
    if(sorted(spc_lst) == sorted(bio_process.get_original_spc_list())):
        cumulative_others(bio_process, feed_name=feed_name)

    # Set in process flag True
    bio_process.set_process_flag(process='in', flag=True)

###########################################################################



#####################################################################################################################
# Calculate Cumulative for Nitrogen and AA Carbon
#####################################################################################################################
def cumulative_others(bio_process, feed_name):
    exp_info = bio_process.get_exp_info()
    measured_data = bio_process.get_measured_data()
    spc_dict = bio_process.get_spc_dict()
    special_spc_dict = bio_process.get_special_spc_dict()

    ala = spc_dict['Alanine'.upper()].get_cumulative()
    arg = spc_dict['Arginine'.upper()].get_cumulative()
    asn = spc_dict['Asparagine'.upper()].get_cumulative()
    asp = spc_dict['Aspartate'.upper()].get_cumulative()
    cyt = spc_dict['Cystine'.upper()].get_cumulative()
    gln = spc_dict['Glutamine'.upper()].get_cumulative()
    glu = spc_dict['Glutamate'.upper()].get_cumulative()
    gly = spc_dict['Glycine'.upper()].get_cumulative()
    his = spc_dict['Histidine'.upper()].get_cumulative()
    iso = spc_dict['Isoleucine'.upper()].get_cumulative()
    leu = spc_dict['Leucine'.upper()].get_cumulative()
    lys = spc_dict['Lysine'.upper()].get_cumulative()
    met = spc_dict['Methionine'.upper()].get_cumulative()
    nh3 = spc_dict['NH3'.upper()].get_cumulative()
    phe = spc_dict['Phenylalanine'.upper()].get_cumulative()
    pro = spc_dict['Proline'.upper()].get_cumulative()
    ser = spc_dict['Serine'.upper()].get_cumulative()
    thr = spc_dict['Threonine'.upper()].get_cumulative()
    tryp = spc_dict['Tryptophan'.upper()].get_cumulative()
    tyr = spc_dict['Tyrosine'.upper()].get_cumulative()
    val = spc_dict['Valine'.upper()].get_cumulative()

    # Calculate cumulative consumption
    # NITROGEN
    nitrogen_cum = (ala*1 + arg*4 + asn*2 + asp*1 + cyt*2 + gln*2 + glu*1 + gly*1 +\
                    his*3 + iso*1 + leu*1 + lys*2 + met*1 - nh3*1 + phe*1 + pro*1 +\
                    ser*1 + thr*1 + tryp*2 + tyr*1 + val*1).rename('CUM. Nitrogen (mmol)')

    # NITROGEN (w/o NH3, Ala)
    nitrogen_w_o_NH3_Ala_cum = (ala*1 + nh3*1 + nitrogen_cum).rename('CUM. Nitrogen (w/o NH3, Ala) (mmol)')

    # AA CARBON
    aa_carbon_cum = (-ala*3 + arg*6 + asn*4 + asp*4 + cyt*6 + gln*5 + glu*5 + gly*2 +\
                 his*6 + iso*6 + leu*6 + lys*6 + met*5 + phe*9 + pro*5 + ser*3 +\
                 thr*4 + tryp*11 + tyr*9 + val*5).rename('CUM. AA Carbon (mmol)')

    # Metabolite2 obj
    nitrogen = Metabolite2(experiment_info=exp_info,
                           raw_data=measured_data,
                           feed_name=feed_name,
                           name='Nitrogen',
                           cumulative=nitrogen_cum)
    nitrogen.set_method_flag(method='cumulative', flag=True)

    nitrogen_w_o_NH3_Ala = Metabolite2(experiment_info=exp_info,
                                       raw_data=measured_data,
                                       feed_name=feed_name,
                                       name='Nitrogen (w/o NH3, Ala)',
                                       cumulative=nitrogen_w_o_NH3_Ala_cum)
    nitrogen_w_o_NH3_Ala.set_method_flag(method='cumulative', flag=True)

    aa_carbon = Metabolite2(experiment_info=exp_info,
                            raw_data=measured_data,
                            feed_name=feed_name,
                            name='AA Carbon',
                            cumulative=aa_carbon_cum)
    aa_carbon.set_method_flag(method='cumulative', flag=True)

    # Add obj to aa dict
    special_spc_dict['NITROGEN'] = nitrogen
    special_spc_dict['NITROGEN (W/O NH3, ALA)'] = nitrogen_w_o_NH3_Ala
    special_spc_dict['AA CARBON'] = aa_carbon

    spc_df = bio_process.get_spc_df()
    # Add cumulative consumption to DF
    spc_df['CUM. Nitrogen (mmol)'] = nitrogen_cum
    spc_df['CUM. Nitrogen (w/o NH3, Ala) (mmol)'] = nitrogen_w_o_NH3_Ala_cum
    spc_df['CUM. AA Carbon (mmol)'] = aa_carbon_cum
    
    #bio_process.set_spc_df(spc_df)
    bio_process.set_spcial_spc_dict(spc_dict=special_spc_dict)