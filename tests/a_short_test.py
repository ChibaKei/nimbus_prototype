import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import heaven, pdeco, town
from database import cast_db_manager, heaven_schedule_db_manager


#heaven.heaven_login("2510021932","i7Qt5Jnj",False)
#heaven.heaven_store_update("2510021932","i7Qt5Jnj",False)
#pdeco.pdeco_login('あい', '61563696', '0316', False)
#print(pdeco.get_pdeco_easy_login('あい', '61563696', '0316', False))
#print(pdeco.pdeco_easy_login('あい', False))
#print(pdeco.heaven_kitene('あいす'))



"""infos = cast_db_manager.get_casts_info()
for info in infos:
    print(info)
    print(pdeco.get_pdeco_easy_login(info[0], info[2], info[3], False))"""

driver = town.town_login("dieselchiba@central-agent.co.jp", "dieselchiba", False)
print(driver.current_url)
