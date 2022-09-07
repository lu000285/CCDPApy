import pandas as pd

###########################################################################
# Product(IgG) Mixin Class
###########################################################################
class ProductMixin:
    # Call Culculation Function
    def in_process(self):
        # Calculate Cumulative Oxygen Concentration Consumed
        self.cumulative_igg_prod()
        
    # Calculate Cumulative IgG Produced
    def cumulative_igg_prod(self, initial_conc=0):
        # IgG produced = xv(i) * v(i) - xv(i-1) * v(i-1)
        igg = self._product_conc            # IgG concentration (10e6 cells/ml)
        v1 = self._v_before_sampling    # Culture Volume Bfore sampling (ml)
        v2 = self._v_after_sampling     # Culture Volume After feeding (ml)

        # Initialize
        s = pd.Series(data=[initial_conc] * len(igg),
                      name='CUM IgG PROD. (mg)')

        for i in range(1, len(igg)):
            si = igg.iat[i] * v1.iat[i] - igg.iat[i-1] * v2.iat[i-1]
            s.iat[i] = s.iat[i-1] + si
        
        # Cumulative IgG Production
        self._cumulative = s / 1000 # Adjust unit to (mg)

    # 
    def disp_inpro_data(self):
        if self._in_process_flag:
            self._inpro_data = pd.concat([self._cumulative],
                                        axis=1)
            print('\n************ IgG In Process Data ************')
            print(self._inpro_data)