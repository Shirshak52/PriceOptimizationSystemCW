# **OptiPrice**  
**(NOTE: The name 'OptiPrice' is used in this project solely for academic and demonstration purposes.)**

This is a full-stack Flask web application **designed for supermarkets** to empower them with data-driven decision-making. It provides core functionalities for:
* **Optimizing Product Prices**
* **Predicting Sales**
* **Segmenting Customers** using machine learning.

---

## **Core Features**

OptiPrice offers a variety of functionalities to enhance supermarket operations:

* **Intelligent Pricing Suggestions:** Leveraging data analysis to recommend optimal product prices.
* **Sales Forecasting:** Predicting future sales trends to aid in inventory management and strategic planning.
* **Customer Segmentation:** Categorizing customers based on their behavior for targeted marketing and personalized experiences.
* **User-Friendly Interface:** A robust Flask web application providing a seamless experience for supermarket administrators.
* **Secure Data Handling:** Utilizing PostgreSQL for reliable data storage and management.

---

## **Machine Learning Models: Detailed Analysis**

This project's core intelligence is driven by powerful machine learning models, thoroughly explored and trained in a dedicated Colab notebook. This notebook covers:

* **Customer Segmentation:** In-depth analysis and application of **K-Means Clustering** to identify distinct customer groups based on purchasing patterns.
* **Sales Prediction:** Development and training of robust sales forecasting models using **XGBoost Regressor**, designed to predict weekly, monthly, and quarterly sales. This section details comprehensive feature engineering, hyperparameter tuning with Optuna, and model evaluation.

The full detailed analysis, code, and model performance metrics can be viewed in the notebook here:  
[**View Notebook (FYP_ModelTraining.ipynb)**](FYP_ModelTraining.ipynb)

---

## **Technologies Used**

This project leverages a modern tech stack to deliver its features:

* **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, etc.
* **Database:** PostgreSQL, pgAdmin
* **Machine Learning:** Scikit-learn, XGBoost, Optuna, Pandas, NumPy, SciPy
* **Data Visualization:** Matplotlib, Seaborn
* **Frontend:** HTML, TailwindCSS, Flowbite (via CDN for speed and simplicity)
* **Version Control:** Git, GitHub

---

## **Getting Started (Local Setup)**

Follow these steps carefully to set up and run OptiPrice on your local device.

**(Before proceeding, ensure that PostgreSQL and pgAdmin are installed and running on your system.)**

### 1. **Clone the Repository**
Open your terminal or command prompt and run:
```
git clone https://github.com/Shirshak52/PriceOptimizationSystemCW.git
```




### 2. **Open the Project**  
Navigate to the cloned folder and open it in Visual Studio Code.


### 3. **Set Up Virtual Environment**  
Open the integrated terminal in VSCode and run these commands one after the other:

* Windows (Command Prompt, NOT Powershell):  
```
python -m venv venv 
venv\Scripts\activate
```  

* Mac/Linux:  
```
python3 -m venv venv
source venv/bin/activate
```

Alternatively, if python3 doesn't work directly, replace it with the full path to your Python installation:
```
full_path_to_your_python_executable -m venv venv
source venv/bin/activate
```


### 4. **Install all dependencies**  
With the virtual environment activated, run this command in the VSCode terminal:  
```
pip install -r requirements.txt
```


### 5. **Create `.env` file**  
At the root of the project folder, create a new file named EXACTLY `.env`.  
Copy all contents from the provided `.env.example file` and paste them into the `.env` file.

#### **Important Replacements in `.env`:**  
- Replace the `SECRET_KEY` value with any random, long string  
- Update the `SQLALCHEMY_DATABASE_URI` value with your actual PostgreSQL credentials

**Note**:
* `.env` variables MUST NOT have spaces around the `=` and MUST be all capital letters. The convention MUST be `VARNAME=value`.
* Ensure PostgreSQL is installed and running and that the user and database you specify in `SQLALCHEMY_DATABASE_URI` actually exist ***(if not, create them)*** and have all privileges.


### 6. **Restart Terminal**  
Close the current VSCode terminal and open a new one.  
If you're on Windows, ensure that you are using CMD (NOT PowerShell).


### 7. **Reset migrations**  
Delete the entire `migrations` folder. Then, in the VSCode terminal, run these commands one after another:  
```
flask db init
flask db migrate -m "Initial database setup"
flask db upgrade
```

**Confirm via pgAdmin that the tables have been successfully created.**


### 8. **Insert dummy data**  
Open `pgAdmin`, connect to your database, go to the Query Tool, paste the following SQL `INSERT` statements, and execute them:  

```
INSERT INTO supermarket (id, name, phone_number, email, password, role)
VALUES 
  ('53d10155-7b61-4464-9ed8-054b3f7d36e3', 'Supermarket3', '333-333-3333', 'supermarket3@example.com', 'scrypt:32768:8:1$wXgPNoVkvMDpdRnf$3594136b3a30e9354115021b4dd03e467c6c4a4d00d7fd8ef86353787badd87ede1802b6c15248dd10109708442322fd08971c92108ed2a580923bbd679dfd68', 'admin'),
  ('87d9f307-6933-4960-a9d3-7dc49edbddfe', 'Supermarket1', '111-111-1111', 'supermarket1@example.com', 'scrypt:32768:8:1$gzkjzEZIH2SFD7YJ$5cd82f886d7095225a9c22dbc28948c07f97f8a53456ee4b4b4bc4cd69adab9e6adf8c7f4baa81f0f8ac883fef1ce80bb71455467cf366a6445ee032085690b1', 'admin'),
  ('beff7094-f85e-4afc-ade0-d51450613dae', 'Supermarket2', '222-222-2222', 'supermarket2@example.com', 'scrypt:32768:8:1$EMyDEL9aLPnyfcxx$ab418277fadb6ee1e9978621e507af3efaf46806f6d6b85ea688a62eefa2ecfd0c730eeda6025aaa8e11cd58a3fd1ca4a478ac05d3c04d5e1efb98b4d0f9d7c1', 'admin');
commit;

INSERT INTO branch (id, name, location, phone_number, email, password, supermarket_id, role) 
VALUES
('20f3a341-917b-46a3-b46b-ade29b7ad708', 'Branch3', 'Bhaktapur', '333-333-3333', 'branch3@example.com', 'scrypt:32768:8:1$BDNOReH1dj6qb3IC$62c84219200eaae2873046d8915ed7e53fdf71e58dd9dad984a1c71b38b01796a2edd56ae31bac81e4fa9f73c4ae824d38ea4a1ddb967ba80772f19e699985ad', 'beff7094-f85e-4afc-ade0-d51450613dae', 'user'),
('26210f86-8d2d-4efd-9787-c4258824885f', 'Branch5', 'Lalitpur', '555-555-5555', 'branch5@example.com', 'scrypt:32768:8:1$Ri6H91mMU5HrtThm$0d773424568fad84b351b0aaa9e6ec442ecf6237df76fefd9446992d3bbc286fa704e6dc8df08f6ba50ff0d5493124e7c31954f5208e3929bb081bfefda7d776', '53d10155-7b61-4464-9ed8-054b3f7d36e3', 'user'),
('50f56a9c-a78f-40e1-897b-4529e7782ca9', 'Branch4', 'Kathmandu', '444-444-4444', 'branch4@example.com', 'scrypt:32768:8:1$uExbxaJvqRefIyWU$e92f94822de6d5f71d6ed4fab98d094badaf63cf4ec959f8e9970b90a46d9ca939f5266fa0b6ffea398d58224059ce2b60a88558d7fff843aee154a96bfba46a', 'beff7094-f85e-4afc-ade0-d51450613dae', 'user'),
('a2e64d9f-1ac9-4e83-917e-c66c2c897d69', 'Branch1', 'Kathmandu', '111-111-1111', 'branch1@example.com', 'scrypt:32768:8:1$kkPU17Ibw48NpAOJ$c47e2e7ec191e42c15c831333f0602bd19e6441b1a891131a4db764ad7ba370d961841f7c3ce9bada90ab8dd0ee5c8ce47f3441d29f71ee951fec14e0165509d', '87d9f307-6933-4960-a9d3-7dc49edbddfe', 'user'),
('b9a229a1-e13b-438e-a6ed-709c0a73969f', 'Branch2', 'Lalitpur', '222-222-2222', 'branch2@example.com', 'scrypt:32768:8:1$5EakG94FDCwcMJkg$e41fbf9a5465619ce2518301abb1ae280f1c430e38d1d02f4a1017e38492b4b68abd62e8c191ca60c54e956aade3e78f9e779d658fec49ce365dbeb35501a581', '87d9f307-6933-4960-a9d3-7dc49edbddfe', 'user'),
('fee8e835-18f7-4036-b4c2-83015aeff027', 'Branch6', 'Bhaktapur', '666-666-6666', 'branch6@example.com', 'scrypt:32768:8:1$X5Blp7HGKOEKAGAh$38b598866452ed72bda3198d9e6d017ed9f2efc5e162d51ca7e538fd59f409dbb3e4f923239ce0a9e949d5a1c0bdb7f2bc9b81d1b80efc49db2f4180bbcb04b5', '53d10155-7b61-4464-9ed8-054b3f7d36e3', 'user');
commit;
```

----------------------------------------

Done! The app is now ready to run locally.  
**To run the app**, run this command in the VSCode terminal:  
```
flask run
```


**Login Credentials**  
To log in, you can enter any one of the emails provided in the dummy data above. The corresponding passwords are straightforward:  
* The password for `branch1@example.com` is `branch1`  
* The password for `branch2@example.com` is `branch2`
* The password for `supermarket1@example.com` is `supermarket1`
and so on.

**Note**: Ensure you have internet access while running the project, as it uses CDN links to various resources.

**Demo Dataset**: Sample datasets have been included in the `/demo_data/` folder for testing and demonstration purposes. The names of the files are self-explanatory.

**P.S.** The application does NOT have the following features due to some reasons/assumptions made during development:
- **No account registration/management features** (**assumption:** sales data is sensitive, so supermarkets directly pay the developer for account registration/management, ensuring trust and security as well as a source of income for the developer)
- **No feature to access past reports** (**reason:** time and scope constraints, possible future enhancement)

