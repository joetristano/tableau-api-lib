import urllib
import pandas as pd


def flatten_dict_column(df, keys, col_name, add_col_prefix=True):
    """
    Extract the specified Pandas DataFrame dict column ('col_name'), creating new columns from the given keys.
    :param pd.DataFrame df: the Pandas DataFrame whose dict column will be flattened
    :param list keys: the keys of the dict column which will be extracted into new columns
    :param str col_name: the name of the Pandas DataFrame column whose content will be flattened
    :param bool add_col_prefix: adds the original 'col_name' value as a prefix to generated columns if True
    :return: pd.DataFrame
    """
    for key in keys:
        if add_col_prefix is True:
            df[col_name + '_' + key] = df[col_name].apply(lambda col: col[key])
        elif add_col_prefix is False:
            df[key] = df[col_name].apply(lambda col: col[key])
        else:
            raise ValueError("The 'add_col_prefix' value must be set to either True or False.")
    df.drop(columns=[col_name], inplace=True)
    return df


def flatten_dict_list_column(df, col_name):
    """
    Extract the dicts contained within the specified list column ('col_name'), creating new rows and columns.
    :param pd.DataFrame df: the Pandas DataFrame whose list of dicts (column) will be flattened
    :param str col_name: the name of the Pandas DataFrame column whose content will be flattened
    :return: pd.DataFrame
    """
    flattened_col_df = pd.DataFrame()
    for index, row in df.iterrows():
        temp_df = pd.DataFrame(row[col_name])
        temp_df.index = [index] * temp_df.shape[0]
        flattened_col_df = flattened_col_df.append(temp_df)
    new_df = df.drop(columns=[col_name]).join(flattened_col_df, how='inner')
    return new_df


def get_server_netloc(server_address):
    return urllib.parse.urlparse(server_address).netloc
