from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from active_alchemy import ActiveAlchemy

db = ActiveAlchemy('sqlite:///sale.db')


class Sale(db.Model):
    name = db.Column(db.String())


driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
driver.get(url="https://www.potownstore.com/on-sale")
names = driver.find_elements(By.CSS_SELECTOR, '.name a')
names_list = []
for name in names:
    if name.text == "":
        pass
    else:
        names_list.append(name.text)

current_sale = [sale.name for sale in Sale.query()]
print(current_sale)
for item in names_list:
    if item in current_sale:
        print('this works!')
        current_sale.remove(item)
    else:
        sale_item = Sale.create(name=f"{item}")
        # code for emailing would be done here.

# code for deletion of non-sale items. If items we're not found in name_list, they are not on-sale anymore and must be
# deleted

for sale_item in Sale.query():
    if sale_item.name in current_sale:
        sale_item.delete()
