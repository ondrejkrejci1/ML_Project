import pandas as pd
import glob

def merge_csv_files():
    csv_files = glob.glob('*.csv')

    output_filename = 'data_complete.csv'
    if output_filename in csv_files:
        csv_files.remove(output_filename)

    if not csv_files:
        return


    dataframes = []

    for file in csv_files:
        try:
            df = pd.read_csv(file)
            dataframes.append(df)
        except Exception as e:
            print(f"{file}: {e}")

    combined_df = pd.concat(dataframes, ignore_index=True)

    combined_df.to_csv(output_filename, index=False, encoding='utf-8-sig')

    print(f"Number of collected decathlons: {len(combined_df)}")


merge_csv_files()