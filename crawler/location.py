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
    titles = []
    connect_links = []
    addresses = []
    images=[]
    data=[]
    def crawl(url,x):
        driver.get(url)
        for page in range(3, x+3):
            for id in range(2, 27):
                select_title = f'//*[@id="app"]/div/div[1]/div[2]/div/div[{id}]/a/div[2]/div[1]/h4'
                select_address = f'//*[@id="app"]/div/div[1]/div[2]/div/div[{id}]/a/div[2]/div[1]/div'
                select_link = f'//*[@id="app"]/div/div[1]/div[2]/div/div[{id}]/a'
               
                try:
                    elem_title = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, select_title))).text
                    titles.append(elem_title)

                    elem_address = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, select_address))).text
                    addresses.append(elem_address)

                    elem_link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, select_link))).get_attribute("href")
                    connect_links.append(elem_link)
                    
                    
                except Exception as e:
                    continue
            if page !=x+2:
                # Chuyển sang trang tiếp theo
                try:
                    next_page_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="app"]/div/div[1]/ul/li[{page}]/a')))
                    next_page_button.click()
                    print(f'Successfully navigated to page {page-1}')
                    time.sleep(2)
                except Exception as e:
                    continue   
    def detail(url,i):                
        try:
            driver.get(url)
            elem_image=WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="app"]/div/div[1]/div/div[1]/img'))).get_attribute("src")
            images[i]=elem_image 
        except Exception:
                return  
            
    url=["https://shopeefood.vn/da-nang/danh-sach-dia-diem-phuc-vu-food-giao-tan-noi",
         "https://shopeefood.vn/da-nang/food/danh-sach-dia-diem-phuc-vu-hotpot-giao-tan-noi",
         "https://shopeefood.vn/da-nang/food/danh-sach-dia-diem-phuc-vu-drink-giao-tan-noi",
         "https://shopeefood.vn/da-nang/food/danh-sach-dia-diem-phuc-vu-rice-giao-tan-noi",
         "https://shopeefood.vn/da-nang/food/danh-sach-dia-diem-phuc-vu-pizza-pasta-burger,cake-pastry-giao-tan-noi",
         "https://shopeefood.vn/da-nang/food/danh-sach-dia-diem-phuc-vu-sushi,chicken-giao-tan-noi",
         "https://shopeefood.vn/da-nang/food/danh-sach-dia-diem-phuc-vu-soup-based,vegetarian-giao-tan-noi"
         ]
    
    for i in range(len(url)):
        crawl(url[i],8)
        time.sleep(5)
       
        
    for i in range(len(connect_links)):
        images.append(" ")
        detail(connect_links[i],i) 
        print(str(i)+"\n"+titles[i]+"\n"+addresses[i]+"\n"+images[i]+"\n"+connect_links[i]+"\n")
        if images[i]!=" ":
            data.append([titles[i],addresses[i],images[i],connect_links[i]])
        time.sleep(1)
        
    unique_data = list(set(tuple(row) for row in data))     
    #save
    fields = ['Title', 'Address', 'Image','Connect_links']
    csv_file = 'data.csv'
    with open(csv_file, mode='w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(fields)
  
        for title, address, image, connect_link in unique_data:
            if image!=" ": 
                writer.writerow([title, address, image,connect_link])

        print("Dữ liệu đã được lưu vào tệp CSV thành công.")
    
    time.sleep(5)
    driver.quit()

if __name__ == '__main__':
    run()
