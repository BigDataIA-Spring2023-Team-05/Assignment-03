import pandas as pd 
import numpy as np
dataframe = pd.DataFrame({'Calls': np.random.randint(0,4,24), 'Time of the Day': pd.date_range('00:00', '23:00', freq='H')})
print(dataframe)