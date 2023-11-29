import pdf2image
import pytesseract
from PIL import Image

def extract_images(): 
    image = pdf2image.convert_from_path('invoice-sample.pdf')
    for pagenumber, page in enumerate(image):
        detected_text = pytesseract.image_to_string(page)
        print(detected_text)
def extract_images_from_pdf(pdf_path, output_dir):
    images = []
    pdf_document = fitz.open(pdf_path)
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        images_from_page = page.get_images(full=True)
        for img_index, img in enumerate(images_from_page):
            base_image = pdf_document.extract_image(img[0])
            image_data = base_image["image"]
            image_filename = f"{output_dir}/page_{page_number + 1}_img_{img_index + 1}.png"
            with open(image_filename, "wb") as img_file:
                img_file.write(image_data)
            images.append(image_filename)
    pdf_document.close()
    return images

def perform_ocr_on_images(images):
    extracted_texts = []
    for image_path in images:
        try:
            extracted_text = pytesseract.image_to_string(Image.open(image_path))
            extracted_texts.append(extracted_text.strip())
            print(f"OCR Result for {image_path}: {extracted_text}")
        except Exception as e:
            print(f"Error performing OCR on {image_path}: {e}")
    return extracted_texts

def main():
    pdf_path = "Germany.pdf"  # Replace with the actual path to your PDF file
    output_dir = "output/images"  # Output directory for extracted images

    try:
        images = extract_images_from_pdf(pdf_path, output_dir)
        extracted_texts = perform_ocr_on_images(images)
        print("Extracted Texts:", extracted_texts)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()