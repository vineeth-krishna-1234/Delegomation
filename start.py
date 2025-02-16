from automation_scripts.instahyre import InstaHyre
from configs import INSTAHYRE_CONFIGS


for config in InstaHyre:
    instance = InstaHyre(config=config)
    instance.start()
