from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
import csv
from pathlib import Path
from RPA.PDF import PDF
import shutil




@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    """
    browser.configure(
        slowmo=1000,
    )
    open_robot_order_website()
    orders = get_orders()
    for row in orders:
        close_annoying_modal()
        fill_the_form(row)
        preview_robot()
        submit_order()
        order_number = order_number_9000()
        pdf_9000(order_number)
        another_robot()
    archive_receipts()

        

def open_robot_order_website():
    """Navigates to the given URL"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")


def get_orders():
    """Downloads file from the given URL and returns orders."""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)
    file_path = Path("orders.csv")
    orders = []
    with file_path.open(mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            orders.append(row)
    return orders

def close_annoying_modal():
    page = browser.page()
    page.click("button:text('OK')")


def fill_the_form(row):
    page = browser.page()
    page.select_option("#head", str(row["Head"]))
    page.click("//div[contains(@class, 'stacked')]/div[{0}]/label".format(row["Body"]))
    page.fill("input[placeholder='Enter the part number for the legs']", str(row["Legs"]))
    page.fill("#address", str(row["Address"]))


def preview_robot():
    page = browser.page()
    page.click("button:text('Preview')")


def submit_order():
    page = browser.page()
    page.click("button:text('ORDER')")
    while True:
        error_check = page.query_selector(".alert.alert-danger")
        if error_check:
            page.click("button:text('ORDER')")
        else:
            break


def order_number_9000():
    page = browser.page()
    order_number = page.locator(".badge.badge-success").inner_html()
    return order_number

def another_robot():
    page = browser.page()
    page.click("button:text('ORDER ANOTHER ROBOT')")


def pdf_9000(order_number):
    pdf_path = store_receipt_as_pdf(order_number)
    screenshot_path = screenshot_robot(order_number)
    embed_screenshot_to_receipt(screenshot_path, pdf_path)


def store_receipt_as_pdf(order_number):
    """Export the data to a pdf file"""
    page = browser.page()
    order_html = page.locator("#order-completion").inner_html()

    pdf = PDF()
    pdf_path = f"output/orders/order_{order_number}.pdf"
    pdf.html_to_pdf(order_html, pdf_path)
    return pdf_path

def screenshot_robot(order_number):
    """Takes screenshot of the ordered bot image"""
    page = browser.page()
    screenshot_path = "output/screenshots/screenshots/{0}.png".format(order_number)
    page.locator("#robot-preview-image").screenshot(path=screenshot_path)
    return screenshot_path

def embed_screenshot_to_receipt(screenshot_path, pdf_path):
    pdf = PDF()
    pdf.add_watermark_image_to_pdf(screenshot_path, pdf_path, pdf_path)

def archive_receipts():
    source_dir = Path("output/orders")
    output_filename = "output/Yeet"
    shutil.make_archive(output_filename, 'zip', root_dir=source_dir)

