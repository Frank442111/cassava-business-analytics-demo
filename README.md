# Simulated Cassava Analytics Portfolio Demo
## Live Demo

🚀 [Launch Cassava Business Analytics Dashboard](https://cassava-business-analytics-demo-7gfspdy2l8nuab3pxdxw9f.streamlit.app/)

Explore my interactive Cassava Business Analytics Dashboard built with Python, Pandas, Streamlit, and Machine Learning.

**Note:** This public demo uses fictional business data to protect real business information.
This read-only Streamlit demonstration uses **entirely fictional data** generated
by arithmetic in demo_data.py. No real transactions are copied, anonymized or
transformed. It generates 112 fictional transactions over 56 days beginning
2032-04-01 and invents opening stock of 12,000 kg. There are no data files,
credentials, private imports, file uploads, entry forms or persistent writes.

Features: simulated RWF sales/cost analysis, date filters, unknown-expense
handling, full-scenario stock, interactive charts, an in-memory labeled fictional
CSV download, and chronological Moving Average / Linear Regression / Ridge
comparison. All figures and predictions are simulated, not business advice.

From this directory in a compatible Python environment:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.address localhost --browser.gatherUsageStats false
```

Python 3.11+ with compatible package wheels is expected; test the exact Python
version offered by the intended host before publishing. The original local
verification environment was Python 3.15.1 on Windows. Installation on a cloud
host is a separate check, not a completed deployment.

No secrets or data-upload configuration is needed. If the fictional generator
fails, the demo stops; it never falls back to another dataset. Filters and the
fictional zero-expense toggle affect only the current view. There is no save path.
The server-side demo config hides detailed exception displays and disables static
file serving; this is not an operating-system sandbox. The deployable repository
must contain only reviewed demo code, not private files.

Forecasting uses the final 14 fictional days as a chronological holdout. Ridge
uses prior-only lag/rolling features and training-only scaling, then recursively
feeds predictions into later lags. None of the models receives actual test sales.
MAE is average absolute error in kg/day. One invented scenario cannot establish
real forecasting quality. A short real sales history is insufficient for reliable
forecasts; no purchasing recommendations or real inventory claims are made.

This app has no authentication and is intended only for fictional public content.
An unlisted URL is not private authentication. Keep any real application and its
records on a separate, protected system. Only reviewed fictional content belongs in this repository. The operational
application and its records are not included.
