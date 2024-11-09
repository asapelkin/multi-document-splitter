
# About

A script for automatically splitting a scan containing multiple documents into separate images, one image per document.

I don't think this script has much real value, as there are certainly ready-made solutions for this task. However, I found it faster to create one from scratch and want to save it for the future usages.

Input:
A single scan containing five documents.
![img](resources/multidocument.png)

Output:
The image is automatically split into five separate images, each containing one document.
![img](resources/card_2.png)
![img](resources/card_3.png)
![img](resources/card_4.png)
![img](resources/card_5.png)
![img](resources/card_6.png)

# Installation

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

# Usage

Run the script with the following command, specifying the input file and output folder:

```bash
./main.py --input_file resources/multidocument.png  --output_folder out
```
