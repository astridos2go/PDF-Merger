__version__ = "1.0"

from tkinter import Tk, Toplevel, StringVar
from tkinter.filedialog import askopenfilenames
from tkinter.ttk import Frame, Progressbar, Labelframe, Label, Button

from PyPDF2 import PdfFileMerger


class Application(Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title('PDF Merger')
        
        self.files = []
        self.file_names = []
        self.output_file = StringVar()
        self.pdfMerger = None
        self.progressLabel = None
        self.progressMarker = None
        
        self.draw_GUI()

    def draw_GUI(self):

        def __menu():
            ...

        def __file_select():
            frame = Frame(self)

            load_button = Button(frame, text='Browse', command=self.load_files)
            load_button.grid(row=0, column=0, padx=5, pady=5)

        def __start():
            self.mergePDFButton = Button(self, text="Merge", command=self.mergePDFs)
            self.mergePDFButton.grid(row=0, column=1, padx=5, pady=5)

    def load_files(self):
        new_files = askopenfilenames(title="Select PDF files to load", filetypes={("*.pdf")})
        for file in new_files:
            ...
        
    def mergePDFs(self):
        self.outputFileName = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes={("*.pdf", ".pdf")})

        progressWindow = Toplevel(self)
        progressWindow.wm_title("Merging PDFs...")

        self.progressMarker = Progressbar(progressWindow, mode='determinate', maximum=100)
        self.progressMarker.grid(row=1, column=0)

        self.progressLabel = Label(progressWindow, text="Merging PDFs...: 0 %")
        self.progressLabel.grid(row=0, column=0)

        self.pdfMerger = PDFMerger()
        self.pdfMerger.mergePDFs(self.fileNames, self.outputFileName, self.incrementProgressBarBy, self.incrementProgressLabelBy)

        progressWindow.destroy()

    def __clearPDFLabelFrame(self):
        PDFLabelFrameChildren = self.PDFLabelFrame.winfo_children()

        for child in PDFLabelFrameChildren:
            child.destroy()
    
    def __createChosenPDFLabels(self, pdfList):
        for index in range(len(pdfList)):
            currentFilePath = pdfList[index]
            currentFilePath = currentFilePath.split("/")

            lastSplitItemIndex = len(currentFilePath) - 1
            currentFileName = currentFilePath[lastSplitItemIndex]

            Label(self.PDFLabelFrame, text=currentFileName).grid(row=index, column=0, columnspan=2)

    def incrementProgressBarBy(self, incrementBy):
        self.progressMarker['value'] += incrementBy
        self.master.update()

    def incrementProgressLabelBy(self, progressIncrement):
        currentText = self.progressLabel.cget("text")

        currentTextAsList = currentText.split(' ')

        currentProgressPercentage = float(currentTextAsList[len(currentTextAsList) - 2])
        currentProgressPercentage += progressIncrement

        currentTextAsList[len(currentTextAsList) - 2] = str(currentProgressPercentage)

        separator = " " 
        newText = separator.join(currentTextAsList)

        self.progressLabel.configure(text=newText)
        self.master.update()


class PDFMerger():

    def __init__(self):
        self.pdfMerger = PdfFileMerger()

    def mergePDFs(self, listOfPDFsToMerge, outputFile, incrementProgressBarBy, incrementProgressLabelBy):
        for pdf in listOfPDFsToMerge:
            self.pdfMerger.append(pdf)
            incrementProgressBarBy((100 / len(listOfPDFsToMerge)))
            incrementProgressLabelBy((100 / len(listOfPDFsToMerge)))
            
        self.pdfMerger.write(outputFile)
        self.pdfMerger.close()


app = Application()
app.mainloop()
