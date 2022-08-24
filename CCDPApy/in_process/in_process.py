import pandas as pd

from ..helper_func.helper_func import check_key

from ..Species.Cell import Cell
from ..Species.Oxygen import Oxygen
from ..Species.Product import Product
from ..Species.Metabolite import Metabolite
from ..Species.Metabolite import Metabolite2

###########################################################################
def cumulative_calc(bio_process, use_feed_conc=True, use_conc_after_feed=False):
    exp_info = bio_process.get_exp_info()               # Get Experiment Info
    measured_data = bio_process.get_measured_data()     # Get Measured Data

    # Cell
    cell = Cell(experiment_info=exp_info, raw_data=measured_data, name='Cell')
    cell.in_process()
    bio_process.set_cell(cell)  # Add

    # Oxygen
    oxygen = Oxygen(experiment_info=exp_info, raw_data=measured_data, name='Oxygen')
    oxygen.in_process()
    bio_process.set_oxygen(oxygen)  # Add

    # IgG
    igg = Product(experiment_info=exp_info, raw_data=measured_data, name='IgG',)
    igg.in_process()
    bio_process.set_igg(igg)    # Add

    # AA Cumulative
    aa_lst = bio_process.get_aa_list()  # Get AA List to Analyze
    aa_dict = {}                        # Initialize
    aa_cumulative_df = pd.DataFrame()   # Initialize
    aa_conc_df = pd.DataFrame()
    aa_conc_after_feed_df = pd.DataFrame()

    for s in aa_lst:
        s = s.upper()   # Name
        conc_before = check_key(measured_data, f'{s} CONC. (mM)')           # Concentration Before Feeding
        conc_after = check_key(measured_data, f'{s} CONC. (mM).1')          # Concentration After Feeding
        feed = check_key(measured_data, f'FEED {s} CONC. (mM)')             # Feed Concentration

        # Check Calculated Cumulative Concentration
        cumulative = check_key(measured_data, f'CUM {s} CONS. (mM)')
        if (not cumulative.any()):
            cumulative = check_key(measured_data, f'CUM {s} PROD. (mM)')

        # Metabolite Object
        spc = Metabolite(experiment_info=exp_info,
                         raw_data=measured_data,
                         name=s,
                         conc_before_feed=conc_before,
                         conc_after_feed=conc_after,
                         feed_conc=feed,
                         cumulative=cumulative,
                         production=True if (s=='LACTATE' or s=='NH3') else False)
        # Calculate Cumulative Consumption/Production
        spc.in_process(use_feed_conc=use_feed_conc, use_conc_after_feed=use_conc_after_feed)
        unit = spc.get_cumulative_unit()    # Unit
        
        aa_cumulative_df['CUM '+s+' '+unit] = spc.get_cumulative()  # Add to DF
        aa_conc_df[conc_before.name] = conc_before
        aa_conc_after_feed_df[s+' (mM) (After Feed)'] = spc.get_conc_after_feed()
        aa_dict[s] = spc    # Add to Dictionary

    # Add to bp obj
    bio_process.set_aa_df(aa_cumulative_df)
    bio_process.set_aa_dict(aa_dict=aa_dict)
    bio_process.set_aa_conc(aa_conc_df)
    bio_process.set_aa_conc_after_feed(conc_after_feed=aa_conc_after_feed_df)

    # Other Spc Cumulative Nitrogen, and AA Carbon
    if(sorted(aa_lst) == sorted(bio_process.get_original_aa_list())):
        cumulative_others(bio_process)

    return bio_process
###########################################################################



#####################################################################################################################
# Calculate Cumulative for Nitrogen and AA Carbon
#####################################################################################################################
def cumulative_others(bio_process):
    exp_info = bio_process.get_exp_info()
    measured_data = bio_process.get_measured_data()
    aa_dict = bio_process.get_aa_dict()

    ala = aa_dict['Alanine'.upper()].get_cumulative()
    arg = aa_dict['Arginine'.upper()].get_cumulative()
    asn = aa_dict['Asparagine'.upper()].get_cumulative()
    asp = aa_dict['Aspartate'.upper()].get_cumulative()
    cyt = aa_dict['Cystine'.upper()].get_cumulative()
    gln = aa_dict['Glutamine'.upper()].get_cumulative()
    glu = aa_dict['Glutamate'.upper()].get_cumulative()
    gly = aa_dict['Glycine'.upper()].get_cumulative()
    his = aa_dict['Histidine'.upper()].get_cumulative()
    iso = aa_dict['Isoleucine'.upper()].get_cumulative()
    leu = aa_dict['Leucine'.upper()].get_cumulative()
    lys = aa_dict['Lysine'.upper()].get_cumulative()
    met = aa_dict['Methionine'.upper()].get_cumulative()
    nh3 = aa_dict['NH3'.upper()].get_cumulative()
    phe = aa_dict['Phenylalanine'.upper()].get_cumulative()
    pro = aa_dict['Proline'.upper()].get_cumulative()
    ser = aa_dict['Serine'.upper()].get_cumulative()
    thr = aa_dict['Threonine'.upper()].get_cumulative()
    tryp = aa_dict['Tryptophan'.upper()].get_cumulative()
    tyr = aa_dict['Tyrosine'.upper()].get_cumulative()
    val = aa_dict['Valine'.upper()].get_cumulative()

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
                           name='Nitrogen',
                           cumulative=nitrogen_cum)

    nitrogen_w_o_NH3_Ala = Metabolite2(experiment_info=exp_info,
                                       raw_data=measured_data,
                                       name='Nitrogen (w/o NH3, Ala)',
                                       cumulative=nitrogen_w_o_NH3_Ala_cum)

    aa_carbon = Metabolite2(experiment_info=exp_info,
                            raw_data=measured_data,
                            name='AA Carbon',
                            cumulative=aa_carbon_cum)

    # Add obj to aa dict
    aa_dict['NITROGEN'] = nitrogen
    aa_dict['NITROGEN (W/O NH3, ALA)'] = nitrogen_w_o_NH3_Ala
    aa_dict['AA CARBON'] = aa_carbon

    aa_df = bio_process.get_aa_df()
    # Add cumulative consumption to DF
    aa_df['CUM. Nitrogen (mmol)'] = nitrogen_cum
    aa_df['CUM. Nitrogen (w/o NH3, Ala) (mmol)'] = nitrogen_w_o_NH3_Ala_cum
    aa_df['CUM. AA Carbon (mmol)'] = aa_carbon_cum
    
    bio_process.set_aa_df(aa_df)
    bio_process.set_aa_dict(aa_dict=aa_dict)