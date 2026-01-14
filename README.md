# About

A tool for automatic data collection from open scientific sources for material science analysis. 

It requires **Chrome** to be installed.

# Prepare repository for use

1. Clone repository

```bash
git clone https://github.com/philexfertich/ceramic-to-titanium-adhesion.git
```

or

```bash
git clone git@github.com:philexfertich/ceramic-to-titanium-adhesion.git
```

2. Go to the repository dir

```bash
cd ~/ceramic-to-titanium-adhesion
```

3. Create virtual environment

```bash
python -m venv .venv
```

4. Then activate

```bash
source .venv/bin/activate
```

5. Install dependencies

```bash
pip install -r requirements.txt
```

6. Run process with 

```bash
python -m provide_cta <ARGS> 
```

# Arguments

- `-u`, `--url`: Required. Takes url collect data from.

- `-r`, `--raw`: Optional. Path for raw data output. File must be in `.html` format. If not provided, saves to `./var/prep/tables.html`

- `-f`, `--formatted`: Optional. Path for formatted data output. File must be in `.xlsx` format. If not provided saves to `./var/tables/adhesion.xlsx`

- `-H`, `--headless`: Sets headless option **SeleniumBase** to True

- `-s`, `--use-selenium`: Allows not to bypass `scrape` step.

# Showcase

![Screenshot](/screenshots/Screenshot_2026-01-14_22-36-43.png)

# Credits

[Oxford Academic. Adhesion of dental ceramic materials to titanium and titanium alloys: a review](https://academic.oup.com/ooms/article/3/1/itad011/7211653)