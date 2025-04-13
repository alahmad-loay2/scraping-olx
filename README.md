# Scraping OLX to Assess Secondhand Product Resale Potential

---

## Table of contents 

- [installation](#installation)
- [about](#about)
- [technologies](#technologies)
---

## installation

- #### clone
   
```html
    https://github.com/alahmad-loay2/scraping-olx.git
````

- #### frontend
  
```html
    cd project
```

```html
    npm install
```

```html
    npm run dev
```

- #### backend

```html
    cd scraping
```

```html
    pip install -r requirements.txt
```

```html
    python server.py
```

push changes on github and in Workflow permissions <br/>
turn on Read and write permissions

---

## about

Fullstack Webapp to scrape data from dubizzle lebanon, track products and analyze them. <br/>
uses NLP tokenization and lemmatization of names, and ML Logistic Regression classifier  <br/>
to check resalability of tracked products trained on original price, listing price, names, <br/>
and how many days the product has been up for listing.

### 📦 Product Tracking Page
---
![Tracking Page](https://github.com/alahmad-loay2/scraping-olx/blob/main/project-screenshots/tracking.jpg?raw=true)

### 📊 Graph Analysis Page
---
![Analyzing Page](https://github.com/alahmad-loay2/scraping-olx/blob/main/project-screenshots/visual-analysis.jpg?raw=true)

### Prediction
---
![Prediction Page](https://github.com/alahmad-loay2/scraping-olx/blob/main/project-screenshots/ml.jpg?raw=true)


---

## technologies

- vite.js
- selenium/beautifulSoup
- pandas
- Flask
- Logistic Regression ML 
- NLP 

--- 

[Back To The Top](#Scraping-OLX-to-Assess-Secondhand-Product-Resale-Potential)
