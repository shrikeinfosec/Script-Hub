# Generate Markdown Report

This script allows me to quickly generate a `.pdf` report from a markdown file, using the [Eisvogel](https://github.com/Wandmalfarbe/pandoc-latex-template/blob/master/eisvogel.tex) Latex template as a base.

# Pre-Requisites

## Install Pandoc

In order to use this script, you'll need to have [Pandoc](https://pandoc.org/) installed to run the `pandoc` command.

I recommend using [Chocolatey](https://chocolatey.org/) to do this.

Installation command:

```ps
choco install pandoc
```

## Install the Eisvogel template

You'll also need to download the [Eisvogel template](https://github.com/Wandmalfarbe/pandoc-latex-template/blob/master/eisvogel.tex) to the following directory (creating, if necessary):

```
%appdata%/pandoc/templates/eisvogel.tex
```

## Prepare your Markdown file

You'll need to ensure your Markdown file has the relevant properties contained in the front-matter. For a full list of options, please see the [following link.](https://github.com/Wandmalfarbe/pandoc-latex-template#custom-template-variables)

Here is an example of some of the properties that I include in my document:

```yaml
---
title: "Document Title goes here"
date: 2023-01-06
lastmod: 2023-01-06
subtitle: "Subtitle goes here"
author: "Your name goes here"
toc: yes
titlepage: true
titlepage-color: "3d3d3d"
titlepage-text-color: "FFFFFF"
titlepage-rule-color: "FFFFFF"
titlepage-rule-height: 2
book: true
classoption: oneside
code-block-font-size: \scriptsize
---
```

# Usage

Run the script and provide a location of a `.md` file. The script will automatically generate a `.pdf` file in the same directory as the source file.

Command to run the generation:

```powershell
./generate_report.ps1 '/path/to/file/My Super Cool Document.md'
```

Output:

```powershell
=====
Selected File: "My Super Cool Document.md"
File Path: "/path/to/file/My Super Cool Document.md"
Directory: "/path/to/file"
Output Filename: "My Super Cool Document.pdf"
=====

Generating PDF Report...

PDF Report Generation complete.
You can find your file at "/path/to/file/My Super Cool Document.pdf"
```

---

> **Note**
>
> _You may need to adjust your permissions settings for running `.ps1` files. Please follow the provided instructions within the PowerShell terminal to do this._
