"""
ログイン機能の共通ベースクラス
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def create_chrome_driver(headless: bool = True, incognito: bool = True) -> webdriver.Chrome:
    """Chromeドライバーを作成する共通関数
    
    Args:
        headless: ヘッドレスモードで実行するかどうか
        incognito: シークレットモードで実行するかどうか
    
    Returns:
        webdriver.Chrome: 初期化されたChromeドライバー
    """
    options = webdriver.ChromeOptions()
    
    # 基本的な安定性オプション
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")
    else:
        options.add_argument("--start-maximized")
    
    # 自動化検出回避
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    if incognito:
        options.add_argument("--incognito")
    
    # ページ読み込みタイムアウト設定
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_settings.popups": 0,
        "profile.managed_default_content_settings.images": 2
    })

    try:
        # ChromeDriverManagerを使用してChromeDriverを取得
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"ChromeDriverManager初期化エラー: {e}")
        try:
            # フォールバック1: システムのChromeDriverを使用
            driver = webdriver.Chrome(options=options)
        except Exception as e2:
            print(f"システムChromeDriver初期化エラー: {e2}")
            # フォールバック2: 最小限のオプションで再試行
            minimal_options = webdriver.ChromeOptions()
            if headless:
                minimal_options.add_argument("--headless")
            minimal_options.add_argument("--no-sandbox")
            minimal_options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(options=minimal_options)

    # タイムアウト設定を強化
    driver.set_page_load_timeout(60)  # ページ読み込みタイムアウト60秒
    driver.implicitly_wait(10)  # 要素待機タイムアウト10秒
    
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
    )

    return driver


def create_webdriver_wait(driver: webdriver.Chrome, timeout: int = 10) -> WebDriverWait:
    """WebDriverWaitオブジェクトを作成する共通関数
    
    Args:
        driver: WebDriverオブジェクト
        timeout: タイムアウト時間（秒）
    
    Returns:
        WebDriverWait: WebDriverWaitオブジェクト
    """
    return WebDriverWait(driver, timeout)
