# Traduce ORICE platforma in limbaj PSIE
from .psie_kernel import Signal, Context

class PSIEAdapter:
    def traduce(self, entitate_straina):
        # orice entitate straina devine Semnal PSIE
        return Signal(
            kind=entitate_straina.get("type", "necunoscut"),
            payload=entitate_straina,
            source=entitate_straina.get("platforma", "univers"),
            confidence=entitate_straina.get("incredere", 0.5)
        )
    def aliniaza(self, semnal, context):
        # foloseste Kernel-ul tau deja publicat
        from .psie_kernel import PSIEKernel
        kernel = PSIEKernel()
        return kernel.arbitrate(semnal, context)