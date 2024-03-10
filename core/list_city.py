from core.color import co 
import os

### 0.7 show all city in time zone ###
def list_time_city(cityin):
    print(f"[*]  List of available city in {cityin}:\n")
    os.system(f"ls /usr/share/zoneinfo/{cityin}")
    return cityin
