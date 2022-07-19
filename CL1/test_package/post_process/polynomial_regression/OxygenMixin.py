from .PolyRegMixin import PolyRegMixin

# Oygen Poly. Reg. Mixin Class
class OxygenMixinPolyReg(PolyRegMixin):
    
    def polyreg(self, polyorder=3):
        super().polyreg(polyorder)

        # SP. OXYGEN CONSUMPTION RATE in Measured Data
        ocr = self._oxygen_consumption_rate

        # Check OCR is equal to or less than 0
        ocr.mask(ocr <= 0, self._polyreg_sp_rate)

        self._polyreg_sp_rate = ocr
