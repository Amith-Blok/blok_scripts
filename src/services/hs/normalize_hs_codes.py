import pandas as pd


def fix_hs_data():
    """
    Fix the HS data by padding 5-digit HS codes with a leading zero to make them 6 digits.
    """
    hsDf = pd.read_csv("./data/hs/blok_duties.csv", dtype={"hs_code": str})

    # Add leading zero to 5-digit HS codes
    hsDf.loc[hsDf["hs_code"].str.len() == 5, "hs_code"] = "0" + hsDf["hs_code"]

    # Keep only 6-digit codes (this will include the padded ones and original 6-digit ones)
    hsDf = hsDf[hsDf["hs_code"].str.len() == 6]

    print(hsDf.head())

    # Save the fixed data back to the file
    hsDf.to_csv("./data/hs/blok_duties.csv", index=False)


if __name__ == "__main__":
    fix_hs_data()
