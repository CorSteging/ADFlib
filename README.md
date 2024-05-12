# ADFlib
A Python library for implementing Abstract Dialectical Frameworks based on the ANGELIC methodology.
This library can be used to model domains as symbolic representations. 
Additional functions include the generation of datasets based on the ADFs and a function that can explains the output of the ADF in natural language. 

The following files are included in this repository:
* ADFlib.py - contains the functions of the ADFlib library
* examples.ipynb - a notebook with examples on how to use the library
* article6.py - an example ADF of Article 6 of the European Convention on Human Rights
* datasets/article6.csv - an dataset generated from the ADF of Article 6. 

This library was used in the following publications:
* [Improving Rationales with Small, Inconsistent and Incomplete Data (JURIX 2023)](https://ebooks.iospress.nl/volumearticle/65567)
* A Hybrid Approach to Legal Textual Entailment (JURISIN 2024, accepted paper)

The implementation of the ADF for Article 6 is based on the paper "Explainable AI tools for legal reasoning about cases: A study on the European Court of Human Rights" by Collenette et al.

ADFlib requires the pandas, math and random library. 