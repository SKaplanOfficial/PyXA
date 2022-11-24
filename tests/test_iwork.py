import PyXA
import unittest

class TestiWork(unittest.TestCase):
    def setUp(self):
        self.pages = PyXA.Application("Pages")
        self.numbers = PyXA.Application("Numbers")
        self.keynote = PyXA.Application("Keynote")

    def test_iwork_application_type(self):
        self.assertIsInstance(self.pages, PyXA.XABaseScriptable.XASBApplication)
        self.assertIsInstance(self.numbers, PyXA.XABaseScriptable.XASBApplication)
        self.assertIsInstance(self.keynote, PyXA.XABaseScriptable.XASBApplication)

        self.assertIsInstance(self.pages, PyXA.apps.iWorkApplicationBase.XAiWorkApplication)
        self.assertIsInstance(self.numbers, PyXA.apps.iWorkApplicationBase.XAiWorkApplication)
        self.assertIsInstance(self.keynote, PyXA.apps.iWorkApplicationBase.XAiWorkApplication)

        self.assertIsInstance(self.pages, PyXA.apps.Pages.XAPagesApplication)
        self.assertIsInstance(self.numbers, PyXA.apps.Numbers.XANumbersApplication)
        self.assertIsInstance(self.keynote, PyXA.apps.Keynote.XAKeynoteApplication)

    def test_iwork_new_document(self):
        d1 = self.pages.new_document()
        d2 = self.numbers.new_document()
        d3 = self.keynote.new_document()

        self.assertIsInstance(d1, PyXA.apps.iWorkApplicationBase.XAiWorkDocument)
        self.assertIsInstance(d2, PyXA.apps.iWorkApplicationBase.XAiWorkDocument)
        self.assertIsInstance(d3, PyXA.apps.iWorkApplicationBase.XAiWorkDocument)

        self.assertIsInstance(d1, PyXA.apps.Pages.XAPagesDocument)
        self.assertIsInstance(d2, PyXA.apps.Numbers.XANumbersDocument)
        self.assertIsInstance(d3, PyXA.apps.Keynote.XAKeynoteDocument)

    def test_iwork_containers(self):
        d1 = self.pages.documents()[0]
        d2 = self.numbers.documents()[0]
        d3 = self.keynote.documents()[0]
        
        pages = d1.pages()
        sheets = d2.sheets()
        slides = d3.slides()

        self.assertIsInstance(pages, PyXA.apps.iWorkApplicationBase.XAiWorkContainerList)
        self.assertIsInstance(sheets, PyXA.apps.iWorkApplicationBase.XAiWorkContainerList)
        self.assertIsInstance(slides, PyXA.apps.iWorkApplicationBase.XAiWorkContainerList)

        self.assertIsInstance(pages, PyXA.apps.Pages.XAPagesContainerList)
        self.assertIsInstance(sheets, PyXA.apps.Numbers.XANumbersContainerList)
        self.assertIsInstance(slides, PyXA.apps.Keynote.XAKeynoteContainerList)

        self.assertIsInstance(pages, PyXA.apps.Pages.XAPagesPageList)
        self.assertIsInstance(sheets, PyXA.apps.Numbers.XANumbersSheetList)
        self.assertIsInstance(slides, PyXA.apps.Keynote.XAKeynoteSlideList)

        i1 = pages[0]
        i2 = sheets[0]
        i3 = slides[0]

        self.assertIsInstance(i1, PyXA.apps.iWorkApplicationBase.XAiWorkContainer)
        self.assertIsInstance(i2, PyXA.apps.iWorkApplicationBase.XAiWorkContainer)
        self.assertIsInstance(i3, PyXA.apps.iWorkApplicationBase.XAiWorkContainer)

        self.assertIsInstance(i1, PyXA.apps.Pages.XAPagesContainer)
        self.assertIsInstance(i2, PyXA.apps.Numbers.XANumbersContainer)
        self.assertIsInstance(i3, PyXA.apps.Keynote.XAKeynoteContainer)

        self.assertIsInstance(i1, PyXA.apps.Pages.XAPagesPage)
        self.assertIsInstance(i2, PyXA.apps.Numbers.XANumbersSheet)
        self.assertIsInstance(i3, PyXA.apps.Keynote.XAKeynoteSlide)

if __name__ == '__main__':
    unittest.main()