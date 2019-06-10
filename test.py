import os, sys, time, datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

_USERNAME = "USERNAME"
if sys.argv[1] is not None:
    _USERNAME = str(sys.argv[1])
    print(f'Set username to {_USERNAME}')
    
_PASSWORD = "PASSWORD"
if sys.argv[2] is not None:
    _PASSWORD = str(sys.argv[2])
    print(f'Set password to {_PASSWORD}')

path = os.path.dirname(os.path.abspath(__file__))
now = datetime.datetime.now()

#print(f'Current folder : {path}')
chromedriver_path = path + "/chromedriver"
logfile_path = f'{path}/log_{now.strftime("%Y-%m-%d-%H%M")}.txt'
#print(f'log_pat = {logfile_path}')


### Init a Chrome driver v75
options = webdriver.ChromeOptions()
### Disable GUI display
options.add_argument("headless")

driver = webdriver.Chrome(executable_path=chromedriver_path, service_log_path=logfile_path, chrome_options=options)

### set timeout to 5 sec while driver tried to find element
driver.implicitly_wait(5)

### open target URL site
driver.get("http://172.16.0.70")
#driver.maximize_window()

# error check
assert "GitLab" in driver.title

# fill-in username
user = driver.find_element_by_id("username")
if user is None:
  print(f"Can't find user in DOM")
  sys.exit(0)
    
user.clear()
user.send_keys(_USERNAME)

# fill-in password
password = driver.find_element_by_id("password")
if password is None:
  print(f"Can't find password in DOM")
  sys.exit(0)
    
password.clear()
password.send_keys(_PASSWORD)

# set actions handler
actions = ActionChains(driver)

if actions is None:
  print(f"Can't get actions object")
  sys.exit(0)

# perform click login
login_btn = driver.find_element_by_name("commit")
if login_btn is None:
  print(f"Can't find login_btn in DOM")
  sys.exit(0)
    
# left click -> click(), right click -> context_click()
actions.move_to_element(login_btn)
actions.click(login_btn)
actions.perform()

# error check
assert "Projects" in driver.title

calculates = driver.find_elements_by_class_name("project-name")
total_len = len(calculates)
print(f"Total len = {total_len:5}")

index = 0

while index < total_len:
  driver.refresh()
  all_projects = driver.find_elements_by_class_name("project-name")
  item = all_projects[index]
  print(f"{index} Project name : {item.text}")
  actions.move_to_element(item)
  actions.click(item)
  actions.perform()
  clone_addr = driver.find_element_by_name("project_clone")
  if clone_addr is None:
    print(f"Can't find object")
    sys.exit(0)
        
  print(f" -> Address : {clone_addr.get_attribute('value')}")
  index = index + 1
  driver.back()

driver.close()
