import re

import pandas as pd

def transform_wroclaw_data(df):
    df = _transform_data(df)
    df = _add_location(df)
    return df


def transform_word_data(df):
    df = _transform_data(df)
    return df


def _transform_data(df):
    df = _convert_column_names_to_snake_case(df)
    df = _trim_values(df)
    df = _drop_if_empty(df)
    df = _parse_to_valid_types(df)
    df = _lowercase_columns_values(df)
    return df


def _convert_column_names_to_snake_case(df):
    """
    Convert column names in a DataFrame to snake_case.
    :param df: pandas DataFrame
    :return: pandas DataFrame with column names in snake_case
    """
    df.columns = [
        re.sub(r'(?<!^)(?=[A-Z])', '_', col).lower().replace(" ", "_")
        for col in df.columns
    ]
    return df


def _lowercase_columns_values(df):
    """
    Convert values to lowercase for specified columns.
    :param df: pandas DataFrame
    :param col_list: List of columns to process
    :return: pandas DataFrame with updated values
    """
    for col in df.columns:
        df[col] = df[col].str.lower() if df[col].dtype == 'object' else df[col]
    return df


def _drop_if_empty(df):
    necessary_columns = ['year', 'sector']
    df = df.dropna(subset=necessary_columns)
    return df


def _trim_values(df):
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    return df


def _parse_to_valid_types(df):
    datetime_columns = ['year']
    numeric_columns = [col for col in df.columns if col not in ['year', 'sector', 'subsector']]

    for col in datetime_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce', format='%Y')

    for col in numeric_columns:
        if col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].str.replace(" ", "").astype(float, errors='coerce')

    return df

def _add_location(df):
    df['country'] = 'Poland'
    df['city'] = 'Wroclaw'

    return df