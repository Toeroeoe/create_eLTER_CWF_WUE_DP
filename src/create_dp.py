import os
from netCDF4 import MFDataset, Dataset
import yaml
import numpy as np

def get_nc_files_from_config(config_path: str, group: str) -> list[str]:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        if not isinstance(config, dict):
            raise ValueError("Configuration file is empty or invalid.")
    nc_files = []
    dir_path = config['paths'][group]
    for file in os.listdir(dir_path):
        if file.endswith('.nc'):
            nc_files.append(os.path.join(dir_path, file))
    return nc_files

def open_mfdataset_from_config(config_path: str, group: str) -> MFDataset:
    nc_files = get_nc_files_from_config(config_path, group)
    if not nc_files:
        raise FileNotFoundError("No NetCDF files found in the specified directories.")
    mfdataset = MFDataset(nc_files)
    return mfdataset

def save_selected_variables(ds: Dataset, 
                            new_ds: Dataset, 
                            group: str,
                            variables: list[str],
                            var_names: dict[str, str],
                            var_attrs: dict[str, dict],
                            var_factor: dict[str, float]) -> None:
        
        # Copy selected variables
        for var_name in variables:
            if var_name in ds.variables:

                var = ds.variables[var_name]

                var_name_dst = var_names.get(var_name, var_name)

                if var_name in new_ds.variables:
                    var_name_dst = var_name_dst + f"_{group}"

                print(f"writing variable {var_name}: {var_name_dst}, {var.dimensions}, {var.dtype}")

                new_var = new_ds.createVariable(var_name_dst, var.dtype, var.dimensions)
                new_var[:] = (var[:] * var_factor.get(var_name_dst, 1.0)).astype('float32')

                # Variable attributes
                for attr, key in var_attrs.get(var_name_dst, {}).items():
                    new_var.setncattr(attr, key)

            else:
                print(f"Warning: Variable {var_name} not found in dataset.")

def main():
    # Settings
    config_path = 'config.yaml'
    out_dir = '../out/CWF_WUE_DP/'
    out_file = 'out.nc'
    groups = ['coords', 'grid', 'pft', 'forcings']
    
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, out_file)

    # Open config
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    print("Loaded config:", config)
    variables_dict = config['variables'] if isinstance(config, dict) and 'variables' in config else {}

    if not variables_dict:
        print("No variables found for any group.")
        return

    # Read settings from config
    dims_dict = config['dimensions'] if isinstance(config, dict) and 'dimensions' in config else {}
    names_dict = config['variable_names'] if isinstance(config, dict) and 'variable_names' in config else {}
    var_attrs_dict = config['variable_attributes'] if isinstance(config, dict) and 'variable_attributes' in config else {}
    var_factor_dict = config['variable_factor'] if isinstance(config, dict) and 'variable_factor' in config else {}
    global_attrs_dict = config['global_attributes'] if isinstance(config, dict) and 'global_attributes' in config else {}
    
    # Make the dataset
    with Dataset(out_path, 'w', format='NETCDF4_CLASSIC') as new_ds:
        
        # Create new NetCDF4 file
        # Copy dimensions
        for dim, props in dims_dict.items():
            new_ds.createDimension(dim, size=(props['size'] if not props['limited'] else None))
        
        # Create time coordinate variable and array
        time_var = new_ds.createVariable('time', 'int32', 'time')
        time_arr = (np.repeat(np.arange(1, 365, dims_dict['time']['day_step'])[:, np.newaxis], 
                              dims_dict['time']['years'],
                              axis=1)\
                           + 365 * np.arange(0, dims_dict['time']['years'])).T.flatten()

        time_var[:] = time_arr

        # Set time variable attributes
        for attr, key in var_attrs_dict.get('time', {}).items():
            time_var.setncattr(attr, key)

        # Copy global attributes
        for attr, key in global_attrs_dict.items():
            new_ds.setncattr(attr, key)
            
        # Copy variables
        for group in groups:
            ds = open_mfdataset_from_config(config_path, group)
            variables = variables_dict.get(group, [])
            save_selected_variables(ds, new_ds, group, variables, names_dict, var_attrs_dict, var_factor_dict)
            print(f"Saved selected variables for group {group} to {out_path}")

        # Calculate Ecosystem Water-Use Efficiency
        if 'GPP' in new_ds.variables and 'ET' in new_ds.variables:
            print("Both GPP and ET variables are present.")
            gpp = new_ds.variables['GPP']
            et = new_ds.variables['ET']
            # Perform operations with gpp and et
            ewue = np.where(et[:] != 0, gpp[:] / et[:], np.nan).astype('float32')
            ewue = np.where(((ewue > 0) & (ewue < 30)), ewue, np.nan).astype('float32')
            print(f"writing variable EWUE: EWUE, {gpp.dimensions}, float32")
            new_var = new_ds.createVariable('EWUE', 'float32', gpp.dimensions)
            new_var[:] = ewue
            for attr, key in var_attrs_dict.get('EWUE', {}).items():
                    new_var.setncattr(attr, key)

        # Calculate Transpiration Water-Use Efficiency
        if 'GPP' in new_ds.variables and 'Tr' in new_ds.variables:
            print("Both GPP and Tr variables are present.")
            gpp = new_ds.variables['GPP']
            tr = new_ds.variables['Tr']
            # Perform operations with gpp and tr
            twue = np.where(tr[:] != 0, gpp[:] / tr[:], np.nan).astype('float32')
            twue = np.where(((twue > 0) & (twue < 30)), twue, np.nan).astype('float32')
            print(f"writing variable TWUE: TWUE, {gpp.dimensions}, float32")
            new_var = new_ds.createVariable('TWUE', 'float32', gpp.dimensions)
            new_var[:] = twue
            for attr, key in var_attrs_dict.get('TWUE', {}).items():
                    new_var.setncattr(attr, key)

        # Calculate Inherent Water-Use Efficiency
        if 'GPP' in new_ds.variables and 'Tr' in new_ds.variables and 'VPD' in new_ds.variables:
            print("GPP, Tr and VPD variables are present.")
            gpp = new_ds.variables['GPP']
            tr = new_ds.variables['Tr']
            vpd = new_ds.variables['VPD']
            # Perform operations with gpp and tr
            gc = np.where(vpd[:] != 0, tr[:] / vpd[:], np.nan)
            iwue = np.where(gc[:] != 0, gpp[:] / gc[:], np.nan).astype('float32')
            iwue = np.where(((iwue > 0) & (iwue < 30)), iwue, np.nan).astype('float32')
            print(f"writing variable IWUE: IWUE, {gpp.dimensions}, float32")
            new_var = new_ds.createVariable('IWUE', 'float32', gpp.dimensions)
            new_var[:] = iwue
            for attr, key in var_attrs_dict.get('IWUE', {}).items():
                    new_var.setncattr(attr, key)

if __name__ == "__main__":
    main()