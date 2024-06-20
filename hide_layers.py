import fitz  # PyMuPDF

def hide_non_matching_layers(pdf_path, keywords):
    # Open the PDF document
    document = fitz.open(pdf_path)
    
    # Get all optional content groups (OCGs)
    ocgs = document.get_ocgs()
    
    # Identify OCGs that do not match any of the keywords
    ocgs_to_hide = []
    for xref, ocg in ocgs.items():
        if not any(keyword in ocg['name'] for keyword in keywords):
            ocgs_to_hide.append(xref)
    
    # Set the layers' visibility
    document.set_layer(-1, off=ocgs_to_hide)
    
    # Save the modified document
    output_path = "modified_" + pdf_path
    document.save(output_path)
    print(f"Modified PDF saved as: {output_path}")

if __name__ == "__main__":
    pdf_path = input("Enter the path to the PDF file: ")
    keywords_input = input("Enter the keywords to match (comma-separated): ")
    keywords = [kw.strip() for kw in keywords_input.split(",")]
    
    hide_non_matching_layers(pdf_path, keywords)
