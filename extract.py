import concurrent.futures
import typing

from vtkmodules.vtkCommonDataModel import vtkStructuredGrid
from vtkmodules.vtkFiltersCore import vtkArrayCalculator
from vtkmodules.vtkFiltersExtraction import vtkExtractGrid
from vtkmodules.vtkIOXML import vtkXMLStructuredGridReader, vtkXMLStructuredGridWriter

from src.data import EXTRACTED_DIR, FILENAMES, ORIGINAL_DIR

if not EXTRACTED_DIR.exists():
    EXTRACTED_DIR.mkdir()


def extract(filename: str):
    print(f"Extracting {filename}...")

    reader = vtkXMLStructuredGridReader()
    reader.SetFileName(str(ORIGINAL_DIR / filename))

    reader.SetPointArrayStatus("u", 1)
    reader.SetPointArrayStatus("v", 1)
    reader.SetPointArrayStatus("w", 1)
    reader.SetPointArrayStatus("theta", 1)
    reader.SetPointArrayStatus("O2", 1)
    reader.SetPointArrayStatus("rhowatervapor", 0)
    reader.SetPointArrayStatus("rhof_1", 1)
    reader.SetPointArrayStatus("convht_1", 0)
    reader.SetPointArrayStatus("frhosiesrad_1", 0)
    reader.Update()

    reader_output = typing.cast(vtkStructuredGrid, reader.GetOutput())
    reader_output.GetPointData().SetActiveScalars("theta")

    extractor = vtkExtractGrid()
    extractor.SetInputData(reader_output)
    extractor.SetVOI(322, 700, 150, 349, 0, 44)
    extractor.SetSampleRate(2, 2, 1)
    extractor.Update()

    calculator = vtkArrayCalculator()
    calculator.SetInputData(typing.cast(vtkStructuredGrid, extractor.GetOutput()))
    calculator.SetAttributeTypeToPointData()
    calculator.AddScalarArrayName("u")
    calculator.AddScalarArrayName("v")
    calculator.AddScalarArrayName("w")
    calculator.SetFunction("u*iHat+v*jHat+w*kHat")
    calculator.SetResultArrayName("wind")
    calculator.Update()

    calculator_output = typing.cast(vtkStructuredGrid, calculator.GetOutput())
    calculator_output.GetPointData().RemoveArray("u")
    calculator_output.GetPointData().RemoveArray("v")
    calculator_output.GetPointData().RemoveArray("w")

    writer = vtkXMLStructuredGridWriter()
    writer.SetInputData(calculator_output)
    writer.SetFileName(str(EXTRACTED_DIR / filename))
    writer.Write()

    print(f"Extracted {filename}.")


with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(extract, FILENAMES)
