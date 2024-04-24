import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

def run():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    service = Service(executable_path=r'C:/Users/LENOVO/OneDrive - The University of Technology/Desktop/0_0/aurora/Python/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    time.sleep(5)
    
    items = []
    price_items = []
    id_item = []
    id_location = []  # Khởi tạo id_location trước khi sử dụng
    images = []
    data = []

    csv_file = 'C:/Users/LENOVO/OneDrive - The University of Technology/Desktop/0_0/aurora/Python/location.csv'
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        id = 1
        for row in reader:
            url = row[4]
            index = row[0]
            try:
                driver.get(url)
                items_temp=[]
                price_temp=[]
                elems = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'item-restaurant-name'))) 
                for elem in elems:
                    items_temp.append(elem.text)               
                elems = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'current-price')))
                for elem in elems:
                    price_temp.append(elem.text)  
                
                print(len(elems))
                for i in range(len(elems)):
                    try: 
                        temp = i + 2
                        elem = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,f"#restaurant-item > div > div > div:nth-child({temp}) > div > div.col-auto.item-restaurant-img > button > img"))).get_attribute("src")
                        images.append(elem)
                        id_location.append(str(index))
                        id_item.append(str(id))
                        items.append(items_temp[i])
                        price_items.append(price_temp[i])
                        data.append([id_item[id-1],id_location[id-1],items[id-1],price_items[id-1],images[id-1]])
                        print(f'{i}   {id}  {index}')
                        id = id + 1
                    except Exception as e:
                        print({e})
                        continue                                       

            except Exception as e:                
                print({e})
                continue
            
    for i in range(len(items)):
        print(f'{id_location[i]}  {str(id_item[i])}  {items[i]}  {price_items[i]}  {images[i]}')
    
       
    # Lưu dữ liệu vào tệp CSV mới
    fields = [ 'Id_item','Id_location', 'Item', 'Price', 'Image']
    csv_file = 'item.csv'
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(fields)
  
        for id_item,id_location,item,price,image in data:
            writer.writerow([id_item,id_location,item,price,image])

    print("Dữ liệu đã được lưu vào tệp CSV thành công.")
    
    time.sleep(5)
    driver.quit()

if __name__ == '__main__':
    run()
