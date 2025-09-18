import pandas as pd


def format_hs_data():
    """
    Formats HS (Harmonized System) code data by extracting 6-digit codes with their
    hierarchical context (chapter and heading names).

    The HS code system has a hierarchical structure:
    - 2-digit codes: Chapters (broad categories)
    - 4-digit codes: Headings (subdivisions of chapters)
    - 6-digit codes: Subheadings (specific product classifications)

    This function processes the raw HS data and creates a formatted output containing
    only the 6-digit codes along with their parent chapter and heading names.
    """
    # Load the raw HS code data, ensuring Code column is treated as string
    hsDf = pd.read_csv("./data/hs_code.csv", dtype={"Code": str})

    # Clean the data by removing any leading/trailing whitespace
    hsDf["Code"] = hsDf["Code"].astype(str).str.strip()
    hsDf["NameEn"] = hsDf["NameEn"].astype(str).str.strip()

    # Initialize lists to collect the formatted results
    codes, names, chapters, headings = [], [], [], []

    # Track the current chapter and heading context as we iterate through the data
    current_chapter_name = None
    current_heading_name = None

    # Process each row in the HS data
    for _, row in hsDf.iterrows():
        code = row["Code"]
        name = row["NameEn"]

        # Check if this is a 2-digit chapter code
        if code.isdigit() and len(code) == 2:
            # Update the current chapter context for subsequent codes
            current_chapter_name = name

        # Check if this is a 4-digit heading code
        elif code.isdigit() and len(code) == 4:
            # Update the current heading context for subsequent codes
            current_heading_name = name

        # Check if this is a 6-digit subheading code (our target data)
        elif code.isdigit() and len(code) == 6:
            # Collect the 6-digit code along with its hierarchical context
            codes.append(code)
            names.append(name)
            chapters.append(current_chapter_name)
            headings.append(current_heading_name)

    # Create the formatted DataFrame with the collected 6-digit codes
    result = pd.DataFrame(
        {"code": codes, "subheading": names, "chapter": chapters, "heading": headings}
    )

    # Save the formatted data to a new CSV file
    result.to_csv("./data/hs_code_formatted.csv", index=False)

    # Display a preview of the formatted data
    print(result.head())
