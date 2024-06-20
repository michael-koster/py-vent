import fitz  # PyMuPDF
from pprint import pprint
import sys
from collections import defaultdict

print(fitz.__doc__)

def hide_layers(pdf_path, search_string):
    exceptions = ['-T--', '-P--', 'V60', 'General']
    print(f"PDF Path: {pdf_path}")
    print(f"Search String: {search_string}")
    print(f"Exceptions: {exceptions}")
    # Open the PDF
    doc = fitz.open(pdf_path)
    ocgs = doc.get_ocgs()
    
    selected_layers = list()
    
    search_strings = [search_string, '----O4-', 'EIN']

    for item in ocgs:
        name = ocgs[item]['name']
        
        for s_string in search_strings:
            
            if s_string in name:
                if exceptions and any([exception in name for exception in exceptions]):
                    #print(f"Layer {item} with name '{name}' will be shown")
                    continue
                else:
                    print(f"Layer {item} with name '{name}' will be hidden")
                    selected_layers.append(item)
            
    if selected_layers:
        doc.set_layer(-1, basestate="OFF", on=selected_layers)
            
        output_pdf_path = "modified_" + pdf_path
        doc.save(output_pdf_path)
        print(f"Modified PDF saved as: {output_pdf_path}")            
    else:
        print("No layers found to hide")

    


def hide_text_layers(pdf_path):
    # Open the PDF
    doc = fitz.open(pdf_path)
    ocgs = doc.get_ocgs()
    
    for item in ocgs:
        name = ocgs[item]['name']
        
        if '-T--' in name:
            print(f"Layer {item} with name '{name}' will be hidden")
            try: 
                doc.set_layer_ui_config(item, -2)
            except:
                print(f"Error: Layer {item} with name '{name}' could not be hidden")
                pass
            #doc.set_layer(-1, off=[item])
    
   
    output_pdf_path = "modified_" + pdf_path
    doc.save(output_pdf_path)
    print(f"Modified PDF saved as: {output_pdf_path}")
    


def show_layers(pdf_path):
    # Open the PDF
    doc = fitz.open(pdf_path)
    ui_layers = doc.layer_ui_configs()
    for item in ui_layers:
        print(f"Layer {item} ")

    
   

def get_layers():
    # Open the PDF
    doc = fitz.open('pdf/Hus_4.pdf')
    page = doc[0]
    pprint(page.get_drawings())
    doc.close()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        pdf_path = sys.argv[1]
        search_string = sys.argv[2]
        hide_layers(pdf_path, search_string)
    elif len(sys.argv) == 2:
        pdf_path = sys.argv[1]
        #hide_text_layers(pdf_path)
        show_layers(pdf_path)
    else:
        get_layers()
        
        
        
        
        


        
