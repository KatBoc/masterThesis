import re
import pandas as pd


def transform_wroclaw_data(df):
    df = _melt_wroclaw_columns(df)
    df = _transform_data(df)
    df = _add_location(df)
    distinct_values = df['sector'].unique()
    print(distinct_values)
    return df


def _assign_sector(df):
    df.rename(columns={'sector': 'subsector'}, inplace=True)
    mapping = {
        'building': 'buildings',
        'electricity/heat': 'buildings',
        'transportation': 'transport',
        'bunker fuels': 'transport',
        'total excluding lucf': 'other',
        'total including lucf': 'other',
        'energy': 'buildings',
        'industrial processes': 'buildings',
        'agriculture': 'other',
        'waste': 'other',
        'land-use change and forestry': 'other',
        'manufacturing/construction': 'other',
        'other fuel combustion': 'other',
        'fugitive emissions': 'other'
    }
    df['sector'] = df['subsector'].map(mapping).fillna('other')  # Default to 'other' if not in mapping

    return df


def transform_world_data(df):
    df = _melt_world_columns(df)
    df = _transform_data(df)
    df = _assign_sector(df)
    df.drop('source', axis=1, inplace=True)
    distinct_values = df['sector'].unique()
    print(distinct_values)
    return df


def _melt_world_columns(df):
    df = df.melt(
        id_vars=['Country', 'Source', 'Sector', 'Gas'],
        var_name='year',
        value_name='emission')
    return df

def _melt_wroclaw_columns(df):
    df = df.melt(
        id_vars=['Sector', 'Subsector', 'Year'],
        var_name='fuel_type',
        value_name='emission'
                )
    return df



def _transform_data(df):
    df = _convert_column_names_to_snake_case(df)
    df = _trim_values(df)
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
    # df.rename(columns={'l_p_g': 'lpg'}, inplace=True)
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
    numeric_columns = [col for col in df.columns if
                       col not in ['country','source','year', 'sector', 'subsector', 'fuel_type']]
    emissions_columns = ['emission']

    for col in datetime_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce', format='%Y')

    for col in emissions_columns:
        if col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].str.replace(" ", "").astype(float,
                                                              errors='coerce')

    return df


def _add_location(df):
    df['country'] = 'Poland'
    df['city'] = 'Wroclaw'

    return df
