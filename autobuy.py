import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from stock import send_email_alert


SITES = {
    "Scan": {
        "url": "https://www.scan.co.uk/products/msi-nvidia-geforce-rtx-5090-suprim-soc-32gb-gddr7-ray-tracing-graphics-card",
        "in_stock_selector": "div.stockText span:contains('In Stock')",
        "price_selector": "div.price div.h2"
    },
    "Overclockers": {
        "url": "https://www.overclockers.co.uk/msi-geforce-rtx-5090-suprim-soc-32gb-gddr7-pci-express-graphics-card-gra-msi-04275.html",
        "in_stock_selector": "li.availability span.in-stock",
        "price_selector": "div.price-wrap h4"
    },
    "Currys": {
        "url": "https://www.currys.co.uk/products/msi-geforce-rtx-5090-32-gb-suprim-soc-graphics-card-10275141.html",
        "in_stock_selector": "button.add-to-basket:not([disabled])",
        "price_selector": "div.p-price"
    }
}


def check_stock():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        while True:
            for site_name, config in SITES.items():
                driver.get(config["url"])
                time.sleep(5)  # 等待页面加载

                try:
                    # 检查库存状态
                    in_stock = False
                    if site_name == "Scan":
                        in_stock = "In Stock" in driver.find_element(By.CSS_SELECTOR, "div.stockText").text
                    elif site_name == "Overclockers":
                        in_stock = len(driver.find_elements(By.CSS_SELECTOR, "li.availability span.in-stock")) > 0
                    elif site_name == "Currys":
                        in_stock = len(
                            driver.find_elements(By.CSS_SELECTOR, "button.add-to-basket:not([disabled])")) > 0

                    # 获取价格
                    try:
                        price = driver.find_element(By.CSS_SELECTOR, config["price_selector"]).text.strip()
                    except:
                        price = "价格获取失败"

                    if in_stock:
                        message = f"{site_name} 有货！\n价格: {price}\n立即购买: {config['url']}"
                        print(message)
                        send_email_alert(f"【库存警报】{site_name} RTX 5090有货", message)
                        # 可以在这里添加自动下单逻辑

                except Exception as e:
                    print(f"{site_name} 检测失败: {str(e)}")

                time.sleep(10)  # 每个网站间隔10秒

            print(f"全站扫描完成，等待5分钟后重新扫描...")
            time.sleep(300)  # 5分钟间隔

    finally:
        driver.quit()


if __name__ == "__main__":

    # 先测试邮件功能
    send_email_alert("系统启动", "开始监控显卡库存")
    check_stock()