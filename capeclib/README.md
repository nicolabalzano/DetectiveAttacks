# capeclib
Just a simple and lightweight Flask server to get CAPEC info from the official repo.

## Overview
This repository contains a Flask server that provides endpoints to retrieve information about CAPEC (Common Attack Pattern Enumeration and Classification) from the official repository. 

## Installation
To get started, clone this repository to your local machine and install the required dependencies:

```bash
git clone https://github.com/nicolabalzano/capeclib.git
cd capeclib
pip install -r requirements.txt
```
Automatically the server download the json file containing the information regarding the CAPEC at every boot if the commit hash of the folliwing repo change: `https://github.com/mitre/cti/tree/master/capec`.

## Usage
To start the server just run the `app.py`. You can do it like this:

```bash
cd capeclib
py app.py
```

or

```bash
cd capeclib
python app.py
```

The API available now are:

```bash
# Get CAPEC by his ID
<HOST>:<PORT>/get_capec?id=<CAPEC-ID> 
```

```bash
# Get MITRE ATT&CK attack pattern ids by CAPEC-ID
<HOST>:<PORT>/get_attack_patterns_mitre_ids_by_capec?id=<CAPEC-ID> 
```

```bash
# Get CWE ids by CAPEC-ID
<HOST>:<PORT>/get_cwe_ids_by_capec?id=<CAPEC-ID> 
```

The <HOST> is the IP number of machime that run the server, and the <PORT> is `5003`, if you would change, go in `app.py` and change the number in this line `port = int(os.environ.get('PORT', 5003))`.


> [!NOTE] 
> If you need more info or some other methods from this library contact me or open an issue, I will be happy to help.

Enjoy it :)