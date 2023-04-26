import concurrent.futures
import shutil
import typing

from vtkmodules.vtkCommonDataModel import vtkImageData, vtkStructuredGrid
from vtkmodules.vtkFiltersCore import vtkArrayCalculator, vtkProbeFilter
from vtkmodules.vtkFiltersExtraction import vtkExtractGrid
from vtkmodules.vtkIOXML import (
    vtkXMLImageDataWriter,
    vtkXMLStructuredGridReader,
    vtkXMLStructuredGridWriter,
)

from src.data import EXTRACTED_DIR, FILE_IDS, IMAGE_DATA_DIR, ORIGINAL_DIR, to_filename


def extract(file_id: int):
    writer = vtkXMLStructuredGridWriter()
    print(f"Extracting {to_filename(file_id, writer.GetDefaultFileExtension())}...")

    reader = vtkXMLStructuredGridReader()
    reader.SetFileName(
        str(ORIGINAL_DIR / to_filename(file_id, writer.GetDefaultFileExtension()))
    )

    # remove unused arrays
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

    # extract region of interest & subsample
    extractor = vtkExtractGrid()
    extractor.SetInputData(reader_output)
    extractor.SetVOI(322, 700, 150, 349, 0, 44)
    extractor.SetSampleRate(2, 2, 1)
    extractor.Update()

    # combine u, v, w scalars into wind vector
    calculator = vtkArrayCalculator()
    calculator.SetInputData(typing.cast(vtkStructuredGrid, extractor.GetOutput()))
    calculator.SetAttributeTypeToPointData()
    calculator.AddScalarArrayName("u")
    calculator.AddScalarArrayName("v")
    calculator.AddScalarArrayName("w")
    calculator.SetFunction("u*iHat+v*jHat+w*kHat")
    calculator.SetResultArrayName("wind")
    calculator.Update()

    # remove u, v, w scalars
    calculator_output = typing.cast(vtkStructuredGrid, calculator.GetOutput())
    calculator_output.GetPointData().RemoveArray("u")
    calculator_output.GetPointData().RemoveArray("v")
    calculator_output.GetPointData().RemoveArray("w")

    writer.SetInputData(calculator_output)
    writer.SetFileName(
        str(EXTRACTED_DIR / to_filename(file_id, writer.GetDefaultFileExtension()))
    )
    writer.Write()

    convert_to_image_data(calculator_output, file_id)

    print(f"Extracted {to_filename(file_id, writer.GetDefaultFileExtension())}.")


def convert_to_image_data(structured_grid: vtkStructuredGrid, file_id: int):
    copied = vtkStructuredGrid()
    copied.DeepCopy(structured_grid)

    copied.GetPointData().SetActiveScalars("theta")
    copied.GetPointData().RemoveArray("wind")
    copied.GetPointData().RemoveArray("O2")
    copied.GetPointData().RemoveArray("rhof_1")

    image_data = vtkImageData()
    image_data.SetExtent([round(v) for v in copied.GetBounds()])
    image_data.SetSpacing(4, 4, 1)

    probe_filter = vtkProbeFilter()
    probe_filter.SetInputData(image_data)
    probe_filter.SetSourceData(copied)
    probe_filter.Update()

    probe_output = typing.cast(vtkImageData, probe_filter.GetOutput())
    probe_output.GetPointData().SetActiveScalars("theta")
    probe_output.GetPointData().RemoveArray("vtkValidPointMask")

    writer = vtkXMLImageDataWriter()
    writer.SetInputData(probe_output)
    writer.SetFileName(
        str(IMAGE_DATA_DIR / to_filename(file_id, writer.GetDefaultFileExtension()))
    )
    writer.Write()


def main():
    shutil.rmtree(EXTRACTED_DIR, ignore_errors=True)
    EXTRACTED_DIR.mkdir()
    shutil.rmtree(IMAGE_DATA_DIR, ignore_errors=True)
    IMAGE_DATA_DIR.mkdir()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(extract, FILE_IDS)


if __name__ == "__main__":
    main()
