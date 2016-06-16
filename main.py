from selenium import webdriver

from analysers import *
from config import *
from dashboard_handler import *

firebugPath = "C:\\Users\\jamesfraser\\Documents\\traffic\\firebug.xpi"
netexportPath = "C:\\Users\\jamesfraser\\Documents\\traffic\\netExport.xpi"

def get_driver():
    if only_load_times:
        return webdriver.Firefox()

    profile = webdriver.FirefoxProfile()
    profile.add_extension(extension=firebugPath)
    profile.add_extension(extension=netexportPath)
    profile.set_preference("extensions.firebug.currentVersion", "2.0.17")

    # profile.set_preference("extensions.firebug.previousPlacement", 1)
    profile.set_preference("extensions.firebug.allPagesActivation", "on")
    profile.set_preference("extensions.firebug.onByDefault", True)
    profile.set_preference("extensions.firebug.defaultPanelName", "net")
    profile.set_preference("extensions.firebug.net.enableSites", True)

    # set net export preferences
    profile.set_preference("webdriver.log.file", "C:\\Users\\jamesfraser\\Documents\\traffic\\log.txt")
    profile.set_preference("extensions.firebug.netexport.alwaysEnableAutoExport", True)
    profile.set_preference("extensions.firebug.netexport.defaultLogDir",
                           "C:\\Users\\jamesfraser\\PycharmProjects\\LoadTime\\har\\")
    profile.set_preference("extensions.firebug.netexport.defaultFileName", "testHar")
    profile.set_preference("extensions.firebug.netexport.showPreview", False)

    return webdriver.Firefox(firefox_profile=profile)


def get_page_load_timings(driver):
    timings = driver.execute_script("return window.performance.timing;")
    # print(timings)
    # req_start = int(timings['requestStart'])
    req_start = int(timings['responseStart'])
    dom_interactive = int(timings['domContentLoadedEventEnd']) - req_start
    dom_complete = int(timings['domComplete']) - req_start
    return {
        "dom_load": dom_interactive,
        "page_load": dom_complete
    }


def metrics(url, page):
    driver = get_driver()
    if not only_load_times:
        clear_hars()
        time.sleep(2)

    driver.get(url)

    time_metrics = get_page_load_timings(driver)

    dom_secs = time_metrics['dom_load'] / 1000
    page_secs = time_metrics['page_load'] / 1000

    # update_dom_load(dom_secs, page)
    update_graph(time.time(), dom_secs, page, MetricsTypes.dom_load)

    # update_page_load(page_secs, page)
    update_graph(time.time(), page_secs, page, MetricsTypes.page_load)
    if not only_load_times:
        time.sleep(3)
        request_metrics = analyse_unknown()
        #print("{}\t{}\t{}\t{}".format(time_metrics['dom_load'], time_metrics['page_load'], request_metrics['requests'], request_metrics['transferred']))

    driver.quit()

while True:
    for site_page in pages:
        try:
            page_url = base_url['url'] + site_page['url']
            # print()
            # print(page_url)
            # if only_load_times:
            #     print("DomLoad\tLoaded")
            # else:
            #     print("DomLoad\tLoaded\tReqs\tTransferred")
            for x in range(num_samples):
                metrics(page_url, site_page)
        except Exception as e:
            print(e)
