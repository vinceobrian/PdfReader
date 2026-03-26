Uploading this to GitHub is a fantastic next step\! A strong `README.md` is the "front page" of your project—it tells other developers (and potential employers) exactly what your app does, how to use it, and how to run it on their own machines.

Here is a complete, professional `README.md` file tailored specifically to the app we just built.

### Step 1: Create a `requirements.txt` file

Before creating the README, create a file named `requirements.txt` in your project folder so others can easily install the dependencies. Paste this inside:

```text
streamlit
pandas
pdfplumber
plotly
```

### Step 2: Create the `README.md` file

Create a new file named `README.md` in the same folder as your `app.py` and paste the following Markdown code into it:

````markdown
# 📄 Candidate Shift & Timezone Dashboard

A modern, interactive web application built with **Python** and **Streamlit** that extracts candidate data from PDF files, analyzes it, and presents it in a dynamic dashboard. 

This tool is designed to help recruiters or managers quickly visualize candidate timezones and preferred working shifts using interactive **Plotly** graphs.

## ✨ Features
* **PDF Data Extraction:** Uses `pdfplumber` to extract tabular data directly from uploaded PDF files.
* **Smart Search:** Instantly search for specific candidates by Name or Email address.
* **Dynamic Filtering:** Filter the candidate pool by local timezone or preferred shift.
* **Interactive Data Visualization:** * Bar charts tracking headcount per timezone.
  * Donut charts visualizing the distribution of preferred shifts.
* **CSV Export:** Download the cleaned, filtered data as a CSV file with one click.

## 🛠️ Technologies Used
* **Python 3.8+**
* **Streamlit** (Web framework & UI)
* **Pandas** (Data manipulation & cleaning)
* **Plotly Express** (Interactive charting)
* **pdfplumber** (PDF parsing & table extraction)

## 🚀 How to Run Locally

**1. Clone the repository**
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
````

**2. Install dependencies**
It is recommended to use a virtual environment. Once activated, install the required packages:

```bash
pip install -r requirements.txt
```

**3. Run the Streamlit app**

```bash
streamlit run app.py
```

The app will automatically open in your default web browser at `http://localhost:8501`.

## ⚠️ Known Limitations (PDF Formatting)

PDFs are notoriously unstructured. This application currently relies on standard table extraction techniques.

  * **Supported:** Native PDFs generated from software (like Google Forms, Word, or Excel) with distinct tabular spacing or visual grid lines.
  * **Not Supported:** Scanned documents (images of text) or flat text without a clear table structure. *(Future updates may include OCR or Regex fallbacks for these edge cases).*

## 🤝 Contributing

Contributions, issues, and feature requests are welcome\! 

-----

*Built with ❤️ using Streamlit.*