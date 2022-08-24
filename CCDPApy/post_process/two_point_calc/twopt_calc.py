import pandas as pd

###########################################################################
def twopt_calc(bio_process):
    # Cell
    cell = bio_process.get_cell()
    cell.post_process_twopt()

    # Oxygen
    oxygen = bio_process.get_oxygen()
    oxygen.post_process_twopt()

    # IgG
    igg = bio_process.get_igg()
    igg.post_process_twopt()

    # AA
    aa_dict = bio_process.get_aa_dict()
    aa_list = bio_process.get_aa_list()
    aa_rate_twopt_df = pd.DataFrame()   # Initialize

    for aa_name in aa_list:
        aa_dict[aa_name].sp_rate_twopt()
        title = f'Two-Pt. Calc. q{aa_name.capitalize()} (mmol/109 cell/hr)'

        aa_rate_twopt_df[title] = aa_dict[aa_name].get_sp_rate()

    # Add to bp
    bio_process.set_post_twopt(aa_rate_twopt_df)

    # Nitrogen and AA Carbon
    if(sorted(aa_list) == sorted(bio_process.get_original_aa_list())):
        sp_rate_others(bio_process)

    # Ratio Calc
    ratio_calc(bio_process)

    return bio_process
###########################################################################

###########################################################################
# Calculate Specific Rate for Nitrogne and AA carbon
def sp_rate_others(bio_process):
    aa_dict = bio_process.get_aa_dict()

    qAla = aa_dict['Alanine'.upper()].get_sp_rate()
    qArg = aa_dict['Arginine'.upper()].get_sp_rate()
    qAsn = aa_dict['Asparagine'.upper()].get_sp_rate()
    qAsp = aa_dict['Aspartate'.upper()].get_sp_rate()
    qCys = aa_dict['Cystine'.upper()].get_sp_rate()
    qGln = aa_dict['Glutamine'.upper()].get_sp_rate()
    qGlu = aa_dict['Glutamate'.upper()].get_sp_rate()
    qGly = aa_dict['Glycine'.upper()].get_sp_rate()
    qHis = aa_dict['Histidine'.upper()].get_sp_rate()
    qIso = aa_dict['Isoleucine'.upper()].get_sp_rate()
    qLeu = aa_dict['Leucine'.upper()].get_sp_rate()
    qLys = aa_dict['Lysine'.upper()].get_sp_rate()
    qMet = aa_dict['Methionine'.upper()].get_sp_rate()
    qNh3 = aa_dict['Nh3'.upper()].get_sp_rate()
    qPhe = aa_dict['Phenylalanine'.upper()].get_sp_rate()
    qPro = aa_dict['Proline'.upper()].get_sp_rate()
    qSer = aa_dict['Serine'.upper()].get_sp_rate()
    qThr = aa_dict['Threonine'.upper()].get_sp_rate()
    qTry = aa_dict['Tryptophan'.upper()].get_sp_rate()
    qTyr = aa_dict['Tyrosine'.upper()].get_sp_rate()
    qVal = aa_dict['Valine'.upper()].get_sp_rate()

    # Nitrogen
    x = qAla*1 + qArg*4 + qAsn*2 + qAsp*1 + qCys*1
    y = qGln*2 + qGlu*1 + qGly*1 + qHis*3 + qIso*1
    z = qLeu*1 + qLys*2 + qMet*1 - qNh3 + qPhe*1 + qPro*1
    w = qSer*1 + qThr*1 + qTry*1 + qTyr*1 + qVal*1
    qNitrogen = x + y + z + w
    qNitrogen = qNitrogen.rename('qNitrogen (mmol/109 cells/hr)')

    # Nitrogen (w/o NH3, Ala)
    qNitrogen_w_o_NH3_Ala = (-qAla*1 + qNh3*1 + qNitrogen)
    qNitrogen_w_o_NH3_Ala = qNitrogen_w_o_NH3_Ala.rename('qNitrogen (w/o NH3, Ala) (mmol/109 cells/hr)')

    # aaC (mmol/109 cells/hr)
    x = qAla*3 + qArg*6 + qAsn*4 + qAsp*4 + qCys*6
    y = qGln*5 + qGlu*5 + qGly*2 + qHis*6 + qIso*6
    z = qLeu*6 + qLys*6 + qMet*5 + qPhe*9 + qPro*5
    w = qSer*3 + qThr*4 + qTry*4 + qTyr*9 + qVal*5
    qaac = x + y + z + w
    qaac = qaac.rename('qaaC (mmol/109 cells/hr)')

    # aaC (consumption only)
    x = qAla.abs()*3 + qArg.abs()*6 + qAsn.abs()*4 + qAsp.abs()*4 + qCys.abs()*6
    y = qGln.abs()*5 + qGlu.abs()*5 + qGly.abs()*2 + qHis.abs()*6 + qIso.abs()*6
    z = qLeu.abs()*6 + qLys.abs()*6 + qMet.abs()*5 + qPhe.abs()*9 + qPro.abs()*5
    w = qSer.abs()*3 + qThr.abs()*4 + qTry.abs()*4 + qTyr.abs()*9 + qVal.abs()*5
    qaac_cons = (x + y + z + w + qaac) / 2
    qaac_cons = qaac_cons.rename('qaaC (consumption only) (mmol/109 cells/hr)')

    # Add to obj
    aa_dict['NITROGEN'].set_sp_rate(qNitrogen)
    aa_dict['NITROGEN (W/O NH3, ALA)'].set_sp_rate(qNitrogen_w_o_NH3_Ala)
    aa_dict['AA CARBON'].set_sp_rate(pd.concat([qaac, qaac_cons], axis=1))

    # Add to DF
    df = bio_process.get_post_twopt()
    df['Two-Pt. Calc. qNitrogen (mmol/109 cells/hr)'] = qNitrogen
    df['Two-Pt. Calc. qNitrogen (w/o NH3, Ala) (mmol/109 cells/hr)'] = qNitrogen_w_o_NH3_Ala
    df['Two-Pt. Calc. qaaC (mmol/109 cells/hr)'] = qaac
    df['Two-Pt. Calc. qaaC (consumption only) (mmol/109 cells/hr)'] = qaac_cons
    bio_process.set_post_twopt(df)
###########################################################################

###########################################################################
# Ratio Caluculaions
def ratio_calc(bio_process):
    aa_dict = bio_process.get_aa_dict()
    df = bio_process.get_post_twopt()

    if ('Glucose'.upper() in aa_dict.keys()):
        dG = aa_dict['Glucose'.upper()].get_sp_rate()
        # DL/DG
        if ('Lactate'.upper() in aa_dict.keys()):
            dL = aa_dict['Lactate'.upper()].get_sp_rate()
            df['Two-Pt. Calc. DL/DG (mmol/mmol)'] = dL / dG

        # qO2/qGlc
        oxygen = bio_process.get_oxygen()
        qO2 = oxygen.get_sp_rate_md()
        qGlc = dG
        df['Two-Pt. Calc. qO2/qGlc (mmol/mmol)'] = qO2 / qGlc

        if ('Glutamine'.upper() in aa_dict.keys()):
            # qGln/qGlc
            qGln = aa_dict['Glutamine'.upper()].get_sp_rate()
            df['Two-Pt. Calc. qGln/qGlc (mmol/mmol)'] = qGln / qGlc

    # qNH3/qGln
    if ('NH3'.upper() in aa_dict.keys() and 'Glutamine'.upper() in aa_dict.keys()):
        qNH3 = aa_dict['NH3'].get_sp_rate()
        qGln = aa_dict['Glutamine'.upper()].get_sp_rate()
        df['Two-Pt. Calc. qNH3/qGln (mmol/mmol)'] = qNH3 / qGln
###########################################################################