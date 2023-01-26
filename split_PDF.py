#Please install following dependencies to run this code...
#pip install PyPDF2==2.12.1
#pip install appJar

from PyPDF2 import PdfFileWriter, PdfFileReader
from pathlib import Path
from appJar import gui

def split_pages(input_file, page_range, out_file):
    """ This function takes the inserted PDF file and copies a specified range of pages into a new PDF file
    Arguments:
        input_file: The source file
        Splitting range: for example: 1,2,4-10,...
        out_file: File name - Saved as a PDF file to your selected location
    """
    output = PdfFileWriter()
    input_pdf = PdfFileReader(open(input_file, "rb"))
    output_file = open(out_file, "wb")

    #range = "2,5,7-9,12, 14-20"
    range_list = list()

    for item in page_range.split(','):
        if '-' in item:
            x,y = item.split('-')
            range_list.extend(range(int(x), int(y)+1))
        else:
            range_list.append(int(item))
    #print(result) // 2,5,7,8,9,12,14,...,20

    for p in range_list:
        try:
            output.addPage(input_pdf.getPage(p - 1)) #pages are 0 indexed
        except IndexError:
            # Alert the user and stop adding pages
            app.infoBox("Info", "Range exceeded number of pages in input.\nFile will still be saved.")
            break
    output.write(output_file)

    if(app.questionBox("File Save", "Your PDF successfully saved. Do you want to quit?")):
        app.stop()


def validate_inputs(input_file, output_dir, range, file_name):
    errorsFlag = False
    errorMesssage = []

    # Make sure a PDF is selected
    if Path(input_file).suffix.upper() != ".PDF":
        errorsFlag = True
        errorMesssage.append("Please select a PDF input file")

    # Make sure a range is selected
    if len(range) < 1:
        errorsFlag = True
        errorMesssage.append("Please enter a valid page range")

    # Check for a valid directory
    if not(Path(output_dir)).exists():
        errorsFlag = True
        errorMesssage.append("Please Select a valid output directory")

    # Check for a file name
    if len(file_name) < 1:
        errorsFlag = True
        errorMesssage.append("Please enter a file name")
        
    if "pdf" in file_name:
        errorsFlag = False
    else:
        errorsFlag = True
        errorMesssage.append("Please enter a file pdf extension")

    return(errorsFlag, errorMesssage)


def press(button):
    if button == "Process":
        src_file = app.getEntry("Input_File")
        dest_dir = app.getEntry("Output_Directory")
        page_range = app.getEntry("Page_Ranges")
        out_file = app.getEntry("Output_name")
        errors, displayErrorMsg = validate_inputs(src_file, dest_dir, page_range, out_file)
        if errors:
            app.errorBox("Error", "\n".join(displayErrorMsg), parent=None)
        else:
            split_pages(src_file, page_range, Path(dest_dir, out_file))
    else:
        app.stop()


# Design interactive user interfaces (GUI)
app = gui("PDF Splitter Program", useTtk=True)
app.setTtkTheme("default")

#Size of the output window
app.setSize(500, 200)

# Input form fields
app.addLabel("Choose Source PDF File")
app.addFileEntry("Input_File")

app.addLabel("Select Output Directory")
app.addDirectoryEntry("Output_Directory")

app.addLabel("Output file name, 'Your_File_Name.pdf'")
app.addEntry("Output_name")

app.addLabel("Page Ranges: 1,4,5-7,8 = 1,4,5,6,7,8")
app.addEntry("Page_Ranges")

# Do some action on button click and quit to exist the application window
app.addButtons(["Process", "Quit"], press)

# start the GUI
app.go()
