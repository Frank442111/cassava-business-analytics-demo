"""Public portfolio entry point. Fictional inputs only; deliberately no private-app imports."""
import altair as alt
import pandas as pd
import streamlit as st

from demo_data import fictional_transactions, FICTIONAL_OPENING_KG, FICTIONAL_PURCHASE_RWF_PER_KG
from demo_analytics import scenario_summary, daily_quantities, fictional_csv


def main():
    st.set_page_config(page_title='Simulated Cassava Portfolio Demo', page_icon='🌱', layout='wide')
    st.title('Cassava Analytics — SIMULATED Portfolio Demo')
    st.warning('SIMULATED DATA ONLY. Every transaction, date, price and stock figure is entirely fictional. '
               'This is a read-only portfolio demonstration, not a real business report.')
    st.caption('No real records, files, secrets or personal information are used. Controls affect only this view. '
               'There are no uploads, file browsers, entry forms or persistent writes.')
    try:
        rows = fictional_transactions()
        if not rows:
            raise ValueError('Empty fictional scenario')
    except Exception:
        st.error('The fictional scenario is unavailable. The demo has stopped; no alternative data source is used.')
        st.stop()

    st.sidebar.header('SIMULATED scenario filters')
    start = st.sidebar.date_input('SIMULATED start date', value=rows[0]['date'], key='demo_start')
    end = st.sidebar.date_input('SIMULATED end date', value=rows[-1]['date'], key='demo_end')
    zero_expenses = st.sidebar.checkbox('SIMULATED assumption: zero additional transaction expenses',
                                       value=False, key='demo_zero_expenses')
    st.sidebar.caption('Unchecked means expenses are unknown. These controls never change records.')
    if start > end:
        st.error('Choose a start date on or before the end date.')
        st.stop()
    selected = [row for row in rows if start <= row['date'] <= end]
    summary = scenario_summary(rows, selected, zero_expenses)
    overview, analytics, inventory, forecasting, reports = st.tabs([
        'SIMULATED Overview', 'SIMULATED Sales Analytics', 'SIMULATED Inventory',
        'SIMULATED Forecasting', 'SIMULATED Reports'])
    with overview:
        st.header('SIMULATED overview')
        cards = st.columns(3)
        cards[0].metric('SIMULATED revenue (RWF)', f"{summary['revenue_rwf']:,.2f}")
        cards[1].metric('SIMULATED quantity sold (kg)', f"{summary['quantity_kg']:,.2f}")
        profit = summary['transaction_profit_rwf']
        cards[2].metric('SIMULATED transaction profit (RWF)', f'{profit:,.2f}' if profit is not None else 'Unknown')
        st.caption(f"SIMULATED COGS: RWF {summary['cogs_rwf']:,.2f}; gross profit: RWF {summary['gross_profit_rwf']:,.2f}. "
                   f'Fictional purchase price: RWF {FICTIONAL_PURCHASE_RWF_PER_KG:,.2f}/kg, assumed 1:1 resale. '
                   'Transaction profit excludes shared overhead, tax and financing; unknown expenses are never zero-filled.')
    with analytics:
        st.header('SIMULATED sales analytics')
        if selected:
            chart = pd.DataFrame(daily_quantities(selected))
            chart['date'] = pd.to_datetime(chart.date).dt.strftime('%Y-%m-%d')
            st.altair_chart(alt.Chart(alt.Data(values=chart.to_dict('records'))).mark_bar().encode(
                x=alt.X('date:T', title='SIMULATED date'), y=alt.Y('quantity_kg:Q', title='SIMULATED quantity (kg)'),
                tooltip=['date:T', alt.Tooltip('quantity_kg:Q', format=',.2f')],
            ).properties(title='SIMULATED daily quantities', height=280).interactive(), width='stretch')
        else:
            st.info('No fictional transactions in this range. Select dates in the fictional scenario.')
        display = [{'SIMULATED date': row['date'].isoformat(), 'SIMULATED quantity (kg)': float(row['quantity_kg']),
                    'SIMULATED price (RWF/kg)': float(row['selling_price_per_kg']),
                    'SIMULATED revenue (RWF)': float(row['revenue'])} for row in selected]
        st.dataframe(display, hide_index=True, width='stretch')
    with inventory:
        st.header('SIMULATED inventory and assumptions')
        st.metric('SIMULATED remaining stock — full scenario (kg)', f"{summary['remaining_kg']:,.2f}")
        st.write(f'SIMULATED opening stock: {FICTIONAL_OPENING_KG:,.2f} kg. Fictional purchases and losses: 0 kg. '
                 'Remaining stock subtracts all fictional sales, independently of the selected dates. '
                 'This is an invented scenario, not a physical stock count or replenishment recommendation.')
    with forecasting:
        st.header('SIMULATED forecasting comparison')
        st.info('A short real sales history is insufficient for reliable business forecasting. This demo uses only '
                'invented observations and gives no real business forecast or purchasing recommendation.')
        try:
            from demo_forecasting import compare_models
            train, test, scores, _ = compare_models(pd.DataFrame(daily_quantities(rows)))
        except Exception:
            st.info('The simulated comparison is unavailable. No private dataset is loaded as a replacement.')
        else:
            st.write(f'SIMULATED training: first {len(train)} days; testing: last {len(test)} days. '
                     'All models predict the same held-out dates from one training cutoff, without actual test updates. '
                     'The sales date filter does not change this comparison.')
            plot = test.rename(columns={'quantity_kg': 'SIMULATED actual'}).melt(
                id_vars='date', value_vars=['SIMULATED actual', 'Moving Average', 'Linear Regression', 'Enhanced Ridge'],
                var_name='SIMULATED series', value_name='SIMULATED kg')
            plot['date'] = plot.date.dt.strftime('%Y-%m-%d')
            st.altair_chart(alt.Chart(alt.Data(values=plot.to_dict('records'))).mark_line(point=True).encode(
                x=alt.X('date:T', title='SIMULATED held-out date'),
                y=alt.Y('SIMULATED kg:Q', title='SIMULATED quantity (kg)', scale=alt.Scale(zero=True)),
                color='SIMULATED series:N', strokeDash='SIMULATED series:N',
                tooltip=['date:T', 'SIMULATED series:N', alt.Tooltip('SIMULATED kg:Q', format=',.2f')],
            ).properties(title='SIMULATED actual vs predicted', height=300).interactive(), width='stretch')
            st.table(scores)
            st.caption('MAE is average absolute error in kg/day; smaller is better on these fictional test dates only. '
                       'Moving Average repeats the final 7-day training mean. Linear Regression uses day number. '
                       'Ridge adds weekly calendar features, lag 1/7 and the strictly earlier 7-day mean; '
                       'scaling fits training rows only, alpha=10 is fixed, and test lags use earlier predictions. '
                       'Negative regression outputs are clipped to zero before scoring. Features may help or hurt. '
                       'Overfitting learns noise; regularization limits feature weights but may underfit. '
                       'Repeated test-set tuning is unreliable; no uncertainty or real-business validity is established.')
    with reports:
        st.header('SIMULATED report download')
        st.caption('In-memory fictional CSV only. Every row contains a SIMULATED_FICTIONAL label. No server file is saved.')
        st.download_button('Download SIMULATED fictional CSV', fictional_csv(selected),
                           file_name='SIMULATED_fictional_cassava.csv', mime='text/csv', key='demo_download')


if __name__ == '__main__':
    main()
