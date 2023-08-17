# Salty Reporter

This is an experimental tool to generate reports similar to those from
[microSALT](https://github.com/Clinical-Genomics/microSALT), but based on the
analysis results from [JASEN](https://github.com/genomic-medicine-sweden/JASEN).

The aim is initially primarily to find out if there are any discrepancies
between the data from microSALT and JASEN, in order to guide the further work
on possibly replacing microSALT with JASEN for bacterial epityping.

It is not yet a MTP/Medicinal Technological Product. Whether it will be in the
future remains to see.

## Usage

1. Get the result file from running JASEN, for example the example output file
   `p1000_result.json`
2. Run salty reporter on the JASEN results like this:
   ```bash
   python saltyreporter/main.py -i <jasen_result.json> -o <some_html_file.html>
   ```
