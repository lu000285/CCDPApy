
from ..pre_process.pre_process import pre_process as preProcess
from ..in_process.in_process import cumulative_calc
from ..post_process.two_point_calc.twopt_calc import twopt_calc
from ..post_process.polynomial_regression.polynomial_regression import polyreg_calc
from ..post_process.rolling_regression.rolling_regression import rolling_regression

class BioProcessMixin():
    def pre_process(self):
        preProcess(bio_process=self)

    def in_process(self, use_feed_conc, use_conc_after_feed):
        cumulative_calc(bio_process=self,
                        use_feed_conc=use_feed_conc,
                        use_conc_after_feed=use_conc_after_feed)

    def twopt(self):
        twopt_calc(bio_process=self)

    def polyreg(self, polyorder_file=None):
        polyreg_calc(bio_process=self, polyorder_file=polyorder_file)

    def rollreg(self, order=3, windows=6):
        rolling_regression(bio_process=self, order=order, windows=windows)
