import os, json, pdfplumber, re, pandas as pd, io, numpy as np
from datetime import datetime
from dateutil import parser

COUNTRY_MAPPING = {
    # Afghanistan
    "Afghanistan": "AF", "AFG": "AF",

    # Albania
    "Albania": "AL", "ALB": "AL",

    # Algeria
    "Algeria": "DZ", "DZA": "DZ",

    # Andorra
    "Andorra": "AD", "AND": "AD",

    # Angola
    "Angola": "AO", "AGO": "AO",

    # Argentina
    "Argentina": "AR", "ARG": "AR",

    # Armenia
    "Armenia": "AM", "ARM": "AM",

    # Australia
    "Australia": "AU", "AUS": "AU",

    # Austria
    "Austria": "AT", "AUT": "AT",

    # Azerbaijan
    "Azerbaijan": "AZ", "AZE": "AZ",

    # Bahamas
    "Bahamas": "BS", "BHS": "BS",

    # Bahrain
    "Bahrain": "BH", "BHR": "BH",

    # Bangladesh
    "Bangladesh": "BD", "BGD": "BD",

    # Barbados
    "Barbados": "BB", "BRB": "BB",

    # Belarus
    "Belarus": "BY", "BLR": "BY",

    # Belgium
    "Belgium": "BE", "BEL": "BE",

    # Belize
    "Belize": "BZ", "BLZ": "BZ",

    # Benin
    "Benin": "BJ", "BEN": "BJ",

    # Bhutan
    "Bhutan": "BT", "BTN": "BT",

    # Bolivia
    "Bolivia": "BO", "BOL": "BO",

    # Bosnia and Herzegovina
    "Bosnia and Herzegovina": "BA", "BIH": "BA",

    # Botswana
    "Botswana": "BW", "BWA": "BW",

    # Brazil
    "Brazil": "BR", "BRA": "BR", "Brasil": "BR",

    # Brunei
    "Brunei": "BN", "BRN": "BN",

    # Bulgaria
    "Bulgaria": "BG", "BGR": "BG",

    # Canada
    "Canada": "CA", "CAN": "CA",

    # China
    "China": "CN", "CHN": "CN", "People's Republic of China": "CN",

    # Colombia
    "Colombia": "CO", "COL": "CO",

    # Denmark
    "Denmark": "DK", "DNK": "DK",

    # Egypt
    "Egypt": "EG", "EGY": "EG",

    # Finland
    "Finland": "FI", "FIN": "FI", "Suomi": "FI",

    # France
    "France": "FR", "FRA": "FR", "République Française": "FR",

    # Germany
    "Germany": "DE", "DEU": "DE", "Deutschland": "DE",

    # India
    "India": "IN", "IND": "IN", "Bharat": "IN", "Hindustan": "IN",

    # Indonesia
    "Indonesia": "ID", "IDN": "ID",

    # Iran
    "Iran": "IR", "IRN": "IR",

    # Iraq
    "Iraq": "IQ", "IRQ": "IQ",

    # Ireland
    "Ireland": "IE", "IRL": "IE",

    # Israel
    "Israel": "IL", "ISR": "IL",

    # Italy
    "Italy": "IT", "ITA": "IT", "Italia": "IT",

    # Japan
    "Japan": "JP", "JPN": "JP", "Nippon": "JP",

    # Malaysia
    "Malaysia": "MY", "MYS": "MY",

    # Mexico
    "Mexico": "MX", "MEX": "MX", "México": "MX",

    # Netherlands
    "Netherlands": "NL", "NLD": "NL", "Holland": "NL", "Nederland": "NL",

    # New Zealand
    "New Zealand": "NZ", "NZL": "NZ",

    # Nigeria
    "Nigeria": "NG", "NGA": "NG",

    # North Korea
    "North Korea": "KP", "PRK": "KP", "Democratic People's Republic of Korea": "KP",

    # Norway
    "Norway": "NO", "NOR": "NO", "Norge": "NO",

    # Pakistan
    "Pakistan": "PK", "PAK": "PK",

    # Philippines
    "Philippines": "PH", "PHL": "PH",

    # Poland
    "Poland": "PL", "POL": "PL",

    # Portugal
    "Portugal": "PT", "PRT": "PT",

    # Russia
    "Russia": "RU", "RUS": "RU", "Russian Federation": "RU",

    # Saudi Arabia
    "Saudi Arabia": "SA", "SAU": "SA", "KSA": "SA",

    # Singapore
    "Singapore": "SG", "SGP": "SG",

    # South Africa
    "South Africa": "ZA", "ZAF": "ZA", "RSA": "ZA",

    # South Korea
    "South Korea": "KR", "KOR": "KR", "Republic of Korea": "KR",

    # Spain
    "Spain": "ES", "ESP": "ES", "España": "ES",

    # Sweden
    "Sweden": "SE", "SWE": "SE", "Sverige": "SE",

    # Switzerland
    "Switzerland": "CH", "CHE": "CH", "Swiss Confederation": "CH",

    # Taiwan
    "Taiwan": "TW", "TWN": "TW", "Republic of China": "TW",

    # Thailand
    "Thailand": "TH", "THA": "TH",

    # Turkey
    "Turkey": "TR", "TUR": "TR", "Türkiye": "TR",

    # Ukraine
    "Ukraine": "UA", "UKR": "UA",

    # United Arab Emirates
    "United Arab Emirates": "AE", "UAE": "AE", "Emirates": "AE",

    # United Kingdom
    "United Kingdom": "UK", 
    "GBR": "UK", 
    "GB": "UK", 
    "U.K.": "UK", 
    "Britain": "UK", 
    "U.K": "UK",

    # United States
    "United States": "US", "USA": "US", "U.S.A": "US", "America": "US", "U.S.": "US",

    # Venezuela
    "Venezuela": "VE", "VEN": "VE",

    # Vietnam
    "Vietnam": "VN", "VNM": "VN", "Viet Nam": "VN",

    # Yemen
    "Yemen": "YE", "YEM": "YE",

    # Zimbabwe
    "Zimbabwe": "ZW", "ZWE": "ZW"
}


def execute(question: str, parameter, file_bytes):
        print(f"File Name: {os.path.basename(__file__)[0]}")
        
        xls_file = io.BytesIO(file_bytes)
        cutoff_date, target_product, target_country = get_dynamic_parameters(question)
        total = calculate_margin(xls_file, cutoff_date, target_product, target_country)
        return total
        
def clean_country(country):
    """Standardizes country names based on the mapping."""
    return COUNTRY_MAPPING.get(str(country).strip().title(), str(country).strip())

def clean_product(product):
    """Extracts only the product name before the slash."""
    return str(product).split("/")[0].strip()

def clean_currency(value):
    """Removes 'USD', extra spaces, and converts to float."""
    if pd.isna(value) or value == '':
        return np.nan
    try:
        return float(str(value).replace("USD", "").replace(",", "").strip())
    except ValueError:
        return np.nan

def clean_date(date):
    """Converts various date formats to a standard format."""
    try:
        return pd.to_datetime(date, errors='coerce', infer_datetime_format=True)
    except Exception as e:
        return np.nan

def calculate_margin(xls_file, cutoff_date, target_product, target_country):
    """Reads the sales Excel file, cleans data, applies filters, and computes total margin."""

    # Load dataset
    try:
        df = pd.read_excel(xls_file)
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_", regex=True)

    # Handling variations in column names (like "Product/Code")
    column_aliases = {
        "product/code": "product",
        "sales_amount": "sales",
        "cost_amount": "cost",
        "transaction_date": "date"
    }
    df.rename(columns={k: v for k, v in column_aliases.items() if k in df.columns}, inplace=True)

    # Debugging: Print available columns
    #print("📌 Available Columns:", df.columns.tolist())

    # Required columns after normalization
    required_columns = {'product', 'country', 'sales', 'cost', 'date'}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        print(f"❌ Missing Columns: {missing_columns}")
        return None

    # Clean relevant columns
    df['country'] = df['country'].map(clean_country).fillna(df['country'])
    df['product'] = df['product'].apply(clean_product)
    df['sales'] = df['sales'].apply(clean_currency)
    df['cost'] = df['cost'].apply(clean_currency)
    df['date'] = df['date'].apply(clean_date)

    # Fill missing cost values (assume cost = 50% of sales)
    df['cost'].fillna(df['sales'] * 0.5, inplace=True)

    # Convert cutoff_date to datetime
    cutoff_date = pd.to_datetime(cutoff_date, errors='coerce')
    #print(type(cutoff_date))
    cutoff_date = np.datetime64(cutoff_date)
    #print(type(cutoff_date))

    if pd.isna(cutoff_date):
        print("❌ Invalid cutoff date format. Please provide a valid date.")
        return None
    
    #print(df)
    
    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=False)
    # Apply filters
    filtered_df = df[
        (df['product'] == target_product) &
        (df['country'] == target_country) &
        (df['date'] <= cutoff_date)
    ]
    #print(filtered_df)
    # Compute total sales and total cost
    total_sales = filtered_df['sales'].sum()
    total_cost = filtered_df['cost'].sum()

    # Compute margin
    total_margin = (total_sales - total_cost) / total_sales if total_sales != 0 else 0

    print("\n📊 Results:")
    print(f"🔹 Total Transactions Found: {len(filtered_df)}")
    print(f"📊 Total Sales: ${total_sales:,.2f}")
    print(f"📉 Total Cost: ${total_cost:,.2f}")
    print(f"✅ Total Margin: {total_margin:.2%}")
    tolal_margin_per = f"{total_margin:.2%}"
    return tolal_margin_per

def clean_date_string(date_str):
    """Removes the timezone description in parentheses."""
    return re.sub(r"\s*\(.*\)$", "", date_str)

def get_dynamic_parameters(question):
    """Extracts dynamic parameters from the question."""
    try:
        date_matches = re.findall(r"before (.+?) for", question)
        product_matches = re.findall(r"for ([\w\s]+) sold in", question)
        country_matches = re.findall(r"sold in ([\w\s]+)", question)

        extracted_date = None
        if date_matches:
            cleaned_date = clean_date_string(date_matches[-1])  # Remove extra text
            extracted_date = parser.parse(cleaned_date)  # Parse clean date
        # Take the last occurrence if multiple matches exist
        extracted_date = extracted_date.isoformat() if extracted_date else None
        product = product_matches[-1].strip() if product_matches else None
        country = country_matches[-1].strip() if country_matches else None

        return extracted_date, product, country
    except AttributeError:
        print("❌ Error extracting dynamic parameters from the question.")
        return None, None, None