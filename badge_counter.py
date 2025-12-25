"""
Badge Counter Module
Provides reusable functions to count Google Cloud Skills Boost badges from public profile URLs.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    """Sets up a headless Chrome browser instance."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def get_badge_count(driver, profile_url: str):
    """
    Counts the number of earned badges on a Google Cloud Skills Boost public profile.
    
    Args:
        driver: Selenium WebDriver instance
        profile_url: URL of the public profile
        
    Returns:
        int: Number of badges found, or 0 if error occurs
    """
    try:
        driver.get(profile_url)
        # Wait up to 15 seconds for the individual badge elements to be visible.
        # The selector 'div.profile-badge' targets each badge card.
        wait = WebDriverWait(driver, 15)
        
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.profile-badge"))
        )
        
        # Find all elements that match the selector for an individual badge.
        badge_elements = driver.find_elements(By.CSS_SELECTOR, "div.profile-badge")
        
        # The count is simply the number of badge elements found.
        count = len(badge_elements)
        return count
        
    except Exception as e:
        # This will catch timeouts if no badges are found or other errors.
        print(f"  - Error scraping {profile_url}: No badges found or page failed to load. Error: {e}")
        return 0  # Return 0 if no badges are found or an error occurs.


def count_badges_from_url(profile_url: str):
    """
    Convenience function to count badges from a URL without managing the driver.
    Creates a driver, counts badges, and closes the driver.
    
    Args:
        profile_url: URL of the public profile
        
    Returns:
        int: Number of badges found, or 0 if error occurs
    """
    driver = setup_driver()
    try:
        count = get_badge_count(driver, profile_url)
        return count
    finally:
        driver.quit()
