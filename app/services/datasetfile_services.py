import os
import uuid
from io import BytesIO
from datetime import datetime

import pandas as pd
import numpy as np

from flask import current_app, session
from flask_login import current_user
from app import db
from app.models.DatasetFile.model import DatasetFile


class DatasetFileService:
    # Columns required in the dataset
    required_cols = [
        "Product ID",
        "Customer ID",
        "Order Date",
        "Quantity",
        "Sales",
    ]

    # ID columns of the dataset
    idcols = ["Product ID", "Customer ID"]

    # Numerical columns of the dataset
    numcols = ["Quantity", "Sales"]

    # Date column of the dataset
    datecol = "Order Date"

    @staticmethod
    def save_datasetfile(file, ml_process):
        """Saves the user-uploaded dataset file, as well as its metadata in the database."""
        try:
            # Convert the file into a DataFrame
            df = DatasetFileService.convert_to_df(file)
            df = df[DatasetFileService.required_cols]

            # Set the correct folder
            folder = DatasetFileService.set_correct_folder(ml_process)

            # Preprocess the dataset
            df_preprocessed = DatasetFileService.preprocess_dataset(df, ml_process)

            # Generate a unique filename
            unique_filename = DatasetFileService.generate_unique_filename(file)

            # Create the full file path
            file_path = os.path.join(folder, os.path.basename(unique_filename))

            # Set the file path into the session
            session["dataset_file_path"] = file_path

            # Convert the file into a CSV string
            df_csv_string = DatasetFileService.convert_to_csv(df_preprocessed)

            # Save the CSV content to the file
            with open(file_path, "wb") as f:
                f.write(df_csv_string.getvalue())

            # Save the metadata to the database
            metadata = DatasetFile(
                file_path=file_path,
                upload_datetime=datetime.utcnow(),
                branch_id=current_user.id,
            )

            # Add to the db and commit
            db.session.add(metadata)
            db.session.commit()
            dataset_file_id = metadata.id

            return (
                True,
                dataset_file_id,
            )  # Return True and the dataset file id if all operations are successful

        except Exception as e:
            print(f"Error while saving dataset file: {e}")
            db.session.rollback()  # In case of failure, rollback the session
            return False  # Return False

    @staticmethod
    def get_session_dataframe():
        file_path = session.get("dataset_file_path")

        with open(file_path, "rb") as file:
            return pd.read_csv(file)

    @staticmethod
    def preprocess_dataset(df, ml_process):
        """Cleans the dataset, engineers features, and scales the dataset."""
        df_cleaned = DatasetFileService.clean_dataset(df)
        df_engineered = DatasetFileService.engineer_features(df_cleaned, ml_process)

        df_preprocessed = df_engineered.copy()
        return df_preprocessed

    @staticmethod
    def clean_dataset(df):
        """Cleans the dataset by dropping missing values and duplicates, and ensuring
        correct datatype of ID and date columns."""

        # Drop missing values and duplicates
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)

        #  Convert date column to datetime
        df[DatasetFileService.datecol] = pd.to_datetime(df[DatasetFileService.datecol])

        # Convert ID columns into string
        for col in DatasetFileService.idcols:
            df[col] = df[col].astype(str)

        return df

    @staticmethod
    def engineer_features(df, ml_process):
        """Engineers features according to the ML process."""
        if ml_process == "segmentation":
            from app.services.segmentation_services import SegmentationService

            df_engineered = SegmentationService.engineer_features(df)
            return df_engineered
        else:
            raise ValueError(f"Unsupported ML process {ml_process}")

    @staticmethod
    def set_correct_folder(ml_process):
        """Returns the correct folder based on the ML process."""
        folder_map = {
            "optimization": current_app.config["UPLOAD_FOLDER_OPTIMIZATION"],
            "prediction": current_app.config["UPLOAD_FOLDER_PREDICTION"],
            "segmentation": current_app.config["UPLOAD_FOLDER_SEGMENTATION"],
        }

        if ml_process not in folder_map:
            raise ValueError(f"Invalid ML process, {ml_process}")

        return folder_map[ml_process]

    @staticmethod
    def generate_unique_filename(file):
        """Generates a unique filename."""

        # Generate a UUID
        unique_id = str(uuid.uuid4())[:8]  # Shorten UUID to 8 chars

        # Combine the UUID and the file extension
        unique_filename = f"{unique_id}_{file.filename}.csv"
        return unique_filename

    @staticmethod
    def convert_to_csv(df_engineered):
        """Converts the feature-engineered dataset into a csv string."""

        # Save the converted dataframe into a BytesIO object
        output = BytesIO()
        df_engineered.to_csv(output, index=False)  # Saving CSV to BytesIO buffer
        output.seek(0)  # Rewind to the start of the file

        return output  # Return the in-memory CSV file

    @staticmethod
    def convert_to_df(file):
        """Converts files into a Pandas Dataframe."""
        # Excel
        if file.filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file)

        # JSON
        elif file.filename.endswith(".json"):
            df = pd.read_json(file)

        # CSV
        else:
            df = pd.read_csv(file)

        return df

    @staticmethod
    def validate_datasetfile(file):
        """Validates the user-uploaded dataset."""
        df = DatasetFileService.convert_to_df(file)

        # Check first for missing columns
        if DatasetFileService.has_missing_cols(df):
            return False

        # Check if all columns have correct datatype
        if not DatasetFileService.has_correct_dtypes(df):
            return False

        return True

    @staticmethod
    def has_missing_cols(df):
        """Checks if required columns exist in the dataset."""
        missing_cols = [
            col for col in DatasetFileService.required_cols if col not in df.columns
        ]

        # Return True if 'missing_cols' has values, False otherwise
        return bool(missing_cols)

    @staticmethod
    def has_correct_dtypes(df):
        """Checks if the dataset columns have the correct datatypes."""
        valid_datecol = DatasetFileService.validate_datecol(df)
        valid_numcols = DatasetFileService.validate_numcols(df)
        has_correct_dtypes = valid_datecol and valid_numcols

        return has_correct_dtypes

    @staticmethod
    def validate_numcols(df):
        """Validates the datatype of numerical columns in the dataset."""
        for col in DatasetFileService.numcols:

            # Return False if any column is of incorrect datatype
            if not np.issubdtype(df[col].dtype, np.number):
                return False

        # Return True if all columns have correct datatype
        return True

    @staticmethod
    def validate_datecol(df):
        """Validates the datatype of date column in the dataset."""
        # Convert the date column to datetime datatype, convert to NaN if not possible
        df[DatasetFileService.datecol] = pd.to_datetime(
            df[DatasetFileService.datecol], errors="coerce"
        )

        # Return True if all values are valid
        return not df[DatasetFileService.datecol].isna().any()
