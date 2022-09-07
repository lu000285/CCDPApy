import pandas as pd

###########################################################################
# Oxygen Mixin Class
###########################################################################
class OxygenMixin:
    # Call Calculation Function
    def in_process(self):
        # Calculate Cumulative Oxygen Concentration Consumed
        self.cumulative_oxy_cons()

    # Calculate Cumulative Oxygen Concentration Consumed
    def cumulative_oxy_cons(self, initial_conc=0):
        oxy = self._oxygen_consumed     # Concentration of Oxygen Consumed
        v1 = self._v_before_sampling    # Culture Volume Before Sampling
        v2 = self._v_after_sampling     # Culture Volume After Sampling

        # Initialize
        s = pd.Series([initial_conc] * len(oxy),
                      name = 'CUM OXYGEN CONS. (mmol)')

        for i in range(1, len(oxy)):
            s.iat[i] = s.iat[i-1] + (oxy.iat[i] * v1.iat[i] - oxy.iat[i-1] * v2.iat[i-1]) / 1000

        # Cumulative Consumption
        self._cumulative = s

    # Display
    def disp_inpro_data(self):
        if self._in_process_flag:
            self._inpro_data = pd.concat([self._cumulative],
                                        axis=1)
            print('\n************ Oxygen In Process Data ************')
            print(self._inpro_data)


