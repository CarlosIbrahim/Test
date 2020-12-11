import streamlit as st
import  pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime


#Read all the tables
sales=pd.read_csv('201904 sales reciepts.csv')
customers=pd.read_csv('customer.csv')
products=pd.read_csv('product.csv')
generations=pd.read_csv('generations.csv')
staff=pd.read_csv('staff.csv')


#add a new column of total amount of each column (quantity of item * unit price)
sales['total'] = sales['quantity'] * sales['unit_price']
#add a new column (day_hour) in wich we only take the hour of the transaction
sales['day_hour']=sales['transaction_time'].str.split(':').str[0]

#Change to date time format
sales['transaction_date'] = pd.to_datetime(sales['transaction_date']).dt.floor('D')
customers['customer_since']=pd.to_datetime(customers['customer_since']).dt.floor('D')


st.title('Coffee Shop Analysis:')
st.markdown('---')

st.sidebar.subheader('Select the Date of the Analysis:')
#To filter based on a date
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=600)
start_date = st.sidebar.date_input('Start date', yesterday)
end_date = st.sidebar.date_input('End date', today)
#Change the date to datetime format
start_date=pd.to_datetime(start_date)
end_date =pd.to_datetime(end_date)

#Make the sales data based on the new filtered date
sales=sales.loc[(sales['transaction_date'] >= start_date) & (sales['transaction_date'] <= end_date) ]
#Merge the sales and the customers with a left join
sales_customers_left=pd.merge(sales, customers, how='left')

sales_products=pd.merge(sales,products, how='left')

sales_products['transaction_time_filtered'] = sales_products['transaction_time']
sales_products['transaction_time_filtered'] = pd.to_datetime(sales_products['transaction_time_filtered'])


#merge the sales and the customers with an inner join
sales_customers=pd.merge(sales,customers,how='inner')


#merge the sales and customers with generations
sales_customers_loyal_generations=pd.merge(sales_customers, generations, how='left')

#get the unique rows of customers
loyal_customers_Loyal_g_unique=sales_customers_loyal_generations.drop_duplicates(subset=['customer_id'])

#Add a year column to the customer to show from which year he is a cusyomer
loyal_customers_Loyal_g_unique['year'] = pd.DatetimeIndex(loyal_customers_Loyal_g_unique['customer_since']).year


#Create 3 data frames based on the 3 stores that we have (ID: 3;5;8)
sales_3=sales.loc[sales['sales_outlet_id']==3]
sales_5=sales.loc[sales['sales_outlet_id']==5]
sales_8=sales.loc[sales['sales_outlet_id']==8]



sales_customers_left_3=sales_customers_left.loc[sales_customers_left['sales_outlet_id']==3]
sales_customers_left_5=sales_customers_left.loc[sales_customers_left['sales_outlet_id']==5]
sales_customers_left_8=sales_customers_left.loc[sales_customers_left['sales_outlet_id']==8]

sales_customers_loyal_generations_3=sales_customers_loyal_generations.loc[sales_customers_loyal_generations['sales_outlet_id']==3]
sales_customers_loyal_generations_5=sales_customers_loyal_generations.loc[sales_customers_loyal_generations['sales_outlet_id']==5]
sales_customers_loyal_generations_8=sales_customers_loyal_generations.loc[sales_customers_loyal_generations['sales_outlet_id']==8]

loyal_customers_Loyal_g_unique_3=loyal_customers_Loyal_g_unique.loc[loyal_customers_Loyal_g_unique['sales_outlet_id']==3]
loyal_customers_Loyal_g_unique_5=loyal_customers_Loyal_g_unique.loc[loyal_customers_Loyal_g_unique['sales_outlet_id']==5]
loyal_customers_Loyal_g_unique_8=loyal_customers_Loyal_g_unique.loc[loyal_customers_Loyal_g_unique['sales_outlet_id']==8]

loyal_customers_Loyal_g_unique_home_3=loyal_customers_Loyal_g_unique.loc[loyal_customers_Loyal_g_unique['home_store']==3]
loyal_customers_Loyal_g_unique_home_5=loyal_customers_Loyal_g_unique.loc[loyal_customers_Loyal_g_unique['home_store']==5]
loyal_customers_Loyal_g_unique_home_8=loyal_customers_Loyal_g_unique.loc[loyal_customers_Loyal_g_unique['home_store']==8]

#Keep only the transaction date and the total amount of the DataSets
sales_dropped = sales[['transaction_date','sales_outlet_id','total']]
sales_3_dropped = sales_3[['transaction_date','total']]
sales_5_dropped = sales_5[['transaction_date','total']]
sales_8_dropped = sales_8[['transaction_date','total']]

#Calculate the total amount of sales for each day and for all the stores and for each one
sales_day_total=sales_dropped['total'].groupby(sales_dropped['transaction_date']).sum().reset_index()
sales_3_day_total=sales_3_dropped['total'].groupby(sales_3_dropped['transaction_date']).sum().reset_index()
sales_5_day_total=sales_5_dropped['total'].groupby(sales_5_dropped['transaction_date']).sum().reset_index()
sales_8_day_total=sales_8_dropped['total'].groupby(sales_8_dropped['transaction_date']).sum().reset_index()
sales_day_outlet=sales.groupby(['sales_outlet_id','transaction_date'])['total'].sum().reset_index()


#Calculate the sales if they are in stores or out of customers_card_stores
sales_y_n=sales.dropna(subset=['instore_yn'])
sales_y_n_3=sales_3.dropna(subset=['instore_yn'])
sales_y_n_5=sales_5.dropna(subset=['instore_yn'])
sales_y_n_8=sales_8.dropna(subset=['instore_yn'])

#count the number of transactions if they are in stores or not
sales_y_n_count=sales_y_n.groupby(['instore_yn']).size().reset_index(name='count')
sales_y_n_3_count=sales_y_n_3.groupby(['instore_yn']).size().reset_index(name='count')
sales_y_n_5_count=sales_y_n_5.groupby(['instore_yn']).size().reset_index(name='count')
sales_y_n_8_count=sales_y_n_8.groupby(['instore_yn']).size().reset_index(name='count')
sales_y_n_compare_count=sales_y_n.groupby(['sales_outlet_id','instore_yn']).size().reset_index(name='count')

#total sales in store vs takeaway
sales_y_n_total=sales_y_n['total'].groupby(sales_y_n['instore_yn']).sum().reset_index()
sales_y_n_3_total=sales_y_n_3['total'].groupby(sales_y_n_3['instore_yn']).sum().reset_index()
sales_y_n_5_total=sales_y_n_5['total'].groupby(sales_y_n_5['instore_yn']).sum().reset_index()
sales_y_n_8_total=sales_y_n_8['total'].groupby(sales_y_n_8['instore_yn']).sum().reset_index()
sales_y_n_compare_total=sales_y_n.groupby(['sales_outlet_id','instore_yn'])['total'].sum().reset_index()

#count the transactions if they are with promotion or no
sales_promo_all=sales.groupby(['promo_item_yn']).size().reset_index(name='count')
sales_promo_3=sales_3.groupby(['promo_item_yn']).size().reset_index(name='count')
sales_promo_5=sales_5.groupby(['promo_item_yn']).size().reset_index(name='count')
sales_promo_8=sales_8.groupby(['promo_item_yn']).size().reset_index(name='count')
sales_promo_compare=sales.groupby(['sales_outlet_id','promo_item_yn']).size().reset_index(name='count')


#Claculate the total of sales for each day for each store between in store and take away total
sales_day_total_y_n=sales_y_n.groupby(['instore_yn','transaction_date'])['total'].sum().reset_index()
sales_day_total_3_y_n=sales_y_n_3.groupby(['instore_yn','transaction_date'])['total'].sum().reset_index()
sales_day_total_5_y_n=sales_y_n_5.groupby(['instore_yn','transaction_date'])['total'].sum().reset_index()
sales_day_total_8_y_n=sales_y_n_8.groupby(['instore_yn','transaction_date'])['total'].sum().reset_index()
sales_day_total_y_n_compare=sales_y_n.groupby(['instore_yn','sales_outlet_id','transaction_date'])['total'].sum().reset_index()


#create a data frame that hae the total of sales for each hour and for each location
sales_day_total_hour=sales['total'].groupby(sales['day_hour']).sum().reset_index()
sales_3_day_total_hour=sales_3['total'].groupby(sales['day_hour']).sum().reset_index()
sales_5_day_total_hour=sales_5['total'].groupby(sales['day_hour']).sum().reset_index()
sales_8_day_total_hour=sales_8['total'].groupby(sales['day_hour']).sum().reset_index()
sales_day_total_hour_compare=sales.groupby(['day_hour','sales_outlet_id'])['total'].sum().reset_index()

#create a data frame that has the total of sales for each generation in each store
sales_customers_loyal_generations_sales=sales_customers_loyal_generations['total'].groupby(sales_customers_loyal_generations['generation']).sum().reset_index()
sales_customers_loyal_generations_3_sales=sales_customers_loyal_generations_3['total'].groupby(sales_customers_loyal_generations_3['generation']).sum().reset_index()
sales_customers_loyal_generations_5_sales=sales_customers_loyal_generations_5['total'].groupby(sales_customers_loyal_generations_5['generation']).sum().reset_index()
sales_customers_loyal_generations_8_sales=sales_customers_loyal_generations_8['total'].groupby(sales_customers_loyal_generations_8['generation']).sum().reset_index()
sales_customers_loyal_generations_sales_compare=sales_customers_loyal_generations.groupby(['sales_outlet_id','generation'])['total'].sum().reset_index()

#count the number of transactions based on the genration in each store
sales_customers_loyal_generations_year = loyal_customers_Loyal_g_unique.groupby(['year']).size().reset_index(name='count')
sales_customers_loyal_generations_year_3 = loyal_customers_Loyal_g_unique_3.groupby(['year']).size().reset_index(name='count')
sales_customers_loyal_generations_year_5 = loyal_customers_Loyal_g_unique_5.groupby(['year']).size().reset_index(name='count')
sales_customers_loyal_generations_year_8 = loyal_customers_Loyal_g_unique_8.groupby(['year']).size().reset_index(name='count')
sales_customers_loyal_generations_year_compare = loyal_customers_Loyal_g_unique.groupby(['sales_outlet_id','generation']).size().reset_index(name='count')

#count the number of loyal customers based on year of being loyal and in all Stores
sales_customers_loyal_generations_transaction = sales_customers_loyal_generations.groupby(['generation'], sort=False).size().reset_index(name='count')
sales_customers_loyal_generations_3_transaction = loyal_customers_Loyal_g_unique_home_3.groupby(['generation'], sort=False).size().reset_index(name='count')
sales_customers_loyal_generations_5_transaction = loyal_customers_Loyal_g_unique_home_5.groupby(['generation'], sort=False).size().reset_index(name='count')
sales_customers_loyal_generations_8_transaction = loyal_customers_Loyal_g_unique_home_8.groupby(['generation'], sort=False).size().reset_index(name='count')

#count the gender of the customers
customers_gender=loyal_customers_Loyal_g_unique.groupby(['gender','generation']).size().reset_index(name='count')
customers_gender_3=loyal_customers_Loyal_g_unique_3.groupby(['gender','generation']).size().reset_index(name='count')
customers_gender_5=loyal_customers_Loyal_g_unique_5.groupby(['gender','generation']).size().reset_index(name='count')
customers_gender_8=loyal_customers_Loyal_g_unique_8.groupby(['gender','generation']).size().reset_index(name='count')

#get the total sales for each customer
sales_customers_loyal_generations_total=sales_customers_loyal_generations.groupby(['customer_first-name'])['total'].sum().reset_index()
sales_customers_loyal_generations_3_total=sales_customers_loyal_generations_3.groupby(['customer_first-name'])['total'].sum().reset_index()
sales_customers_loyal_generations_5_total=sales_customers_loyal_generations_5.groupby(['customer_first-name'])['total'].sum().reset_index()
sales_customers_loyal_generations_8_total=sales_customers_loyal_generations_8.groupby(['customer_first-name'])['total'].sum().reset_index()

#add a new column to describe if it is a loyal customers or not
sales_customers_left['customer type'] = np.where(sales_customers_left['customer_id']==0, 'No Loyalty Card', 'With Loyalty Card')
sales_customers_left_3['customer type'] = np.where(sales_customers_left_3['customer_id']==0, 'No Loyalty Card', 'With Loyalty Card')
sales_customers_left_5['customer type'] = np.where(sales_customers_left_5['customer_id']==0, 'No Loyalty Card', 'With Loyalty Card')
sales_customers_left_8['customer type'] = np.where(sales_customers_left_8['customer_id']==0, 'No Loyalty Card', 'With Loyalty Card')

#count the number of transactions done by each customer type in each store
sales_customers_left_type_count=sales_customers_left.groupby(['customer type']).size().reset_index(name='count')
sales_customers_left_3_type_count=sales_customers_left_3.groupby(['customer type']).size().reset_index(name='count')
sales_customers_left_5_type_count=sales_customers_left_5.groupby(['customer type']).size().reset_index(name='count')
sales_customers_left_8_type_count=sales_customers_left_8.groupby(['customer type']).size().reset_index(name='count')
sales_customers_left_compare_type_count= sales_customers_left.groupby(['sales_outlet_id','customer type']).size().reset_index(name='count')


#total of sales of each customer type in each store
sales_customers_left_type_total=sales_customers_left.groupby(['customer type'])['total'].sum().reset_index()
sales_customers_left_3_type_total=sales_customers_left_3.groupby(['customer type'])['total'].sum().reset_index()
sales_customers_left_5_type_total=sales_customers_left_5.groupby(['customer type'])['total'].sum().reset_index()
sales_customers_left_8_type_total=sales_customers_left_8.groupby(['customer type'])['total'].sum().reset_index()
sales_customers_left_compare_type_total=sales_customers_left.groupby(['sales_outlet_id','customer type'])['total'].sum().reset_index()

#Divide the Sales_Products in 3 data frame based on the Stores
sales_products_3=sales_products.loc[sales_products['sales_outlet_id']==3]
sales_products_5=sales_products.loc[sales_products['sales_outlet_id']==5]
sales_products_8=sales_products.loc[sales_products['sales_outlet_id']==8]

#Count the quantity sold of each item based based on the quantity column and in each store
sales_products_quantity=sales_products.groupby(['product'])['quantity'].sum().reset_index()
sales_products_3_quantity=sales_products_3.groupby(['product'])['quantity'].sum().reset_index()
sales_products_5_quantity=sales_products_5.groupby(['product'])['quantity'].sum().reset_index()
sales_products_8_quantity=sales_products_8.groupby(['product'])['quantity'].sum().reset_index()

#Merge the sales data with the staff data
sales_staff=pd.merge(sales,staff, how='inner')

#Divide the sales_staff dataset based on the stores
sales_staff_3=sales_staff.loc[sales_staff['sales_outlet_id']==3]
sales_staff_5=sales_staff.loc[sales_staff['sales_outlet_id']==5]
sales_staff_8=sales_staff.loc[sales_staff['sales_outlet_id']==8]

#Calculate the total sales for each employee
sales_staff_total=sales_staff.groupby(['first_name','position'])['total'].sum().reset_index()
sales_staff_3_total=sales_staff_3.groupby(['first_name','position'])['total'].sum().reset_index()
sales_staff_5_total=sales_staff_5.groupby(['first_name','position'])['total'].sum().reset_index()
sales_staff_8_total=sales_staff_8.groupby(['first_name','position'])['total'].sum().reset_index()




button=st.sidebar.radio('Select what you want to see:',
                            ('Sales Description','Customers Description','Loyal Customers Description', 'Products Description', 'Staff Description', 'Loyal Customer Machine Learning'))

if button=='Sales Description':

    st.header('Sales Analysis:')
    st.subheader('Select the Store to see the Sales Analysis:')

    sns.set_context('talk')

    transaction_category=['Y','N',' ']
    promotion_category=['Y','N']

    sales_description=st.selectbox(
            '',
            ('All','Outlet 3','Outlet 5','Outlet 8','Comparaison between the Outlets'))

    if sales_description == 'All':

        st.subheader('Total Daily Sales combined in All the Stores:')
        plt.rcParams['figure.figsize'] = [13, 10]
        sales_day_total_line = sns.lineplot(x="transaction_date", y="total", data=sales_day_total)
        sales_day_total_line.set(ylim=(0, 10000))
        sales_day_total_line.set(xlabel='Transaction Date',ylabel='Total Sales')
        sales_day_total_line.set_title('Total Sales In All Stores:',y=1.02)
        plt.xticks(rotation=10)
        st.pyplot(sales_day_total_line)

        st.subheader('Total Daily Sales combined in All the Stores based on In Store Sales and Take-away Sales:')
        plt.rcParams['figure.figsize'] = [13, 10]
        sales_y_n_line=sns.lineplot(x="transaction_date", y="total", hue='instore_yn', data=sales_day_total_y_n)
        sales_y_n_line.set(ylim=(0, 6000))
        sales_y_n_line.set(xlabel='Transaction Date',ylabel='Total Sales')
        sales_y_n_line.set_title('In Store Sales (Y) Vs Take-away (N) Sales',y=1.02)
        plt.xticks(rotation=10)
        st.pyplot()

        st.subheader('Total Sales in All the Stores based on the Hour of the Day:')
        sales_day_total_hour_bar = sns.barplot(x="day_hour", y="total", palette="Blues_d", data=sales_day_total_hour)
        sales_day_total_hour_bar.set(xlabel='Hours of the Day',ylabel='Total Sales')
        sales_day_total_hour_bar.set_title('Total Sales in each Hour',y=1.02)
        st.pyplot()

        st.subheader('Total In Store Vs Take-away Transactions done in All Stores:')
        sales_y_n_count_bar=sns.barplot(x='instore_yn', y='count', palette="Blues_d", data=sales_y_n_count, order=transaction_category)
        sales_y_n_count_bar.set(xlabel='In Stores Vs Take-away Vs Not Specified',ylabel='Total Transactions')
        sales_y_n_count_bar.set_title('In Store Transactions (Y) Vs Take-away Transactions (N) Sales',y=1.02)
        st.pyplot()

        st.subheader('Total In Store Vs Take-away Sales done in All Stores:')
        sales_y_n_total_bar=sns.barplot(x='instore_yn', y='total', palette='Blues_d', data=sales_y_n_total, order=transaction_category)
        sales_y_n_total_bar.set(xlabel='In Stores Vs Take-away Vs Not Specified',ylabel='Total Sales')
        sales_y_n_total_bar.set_title('In Store Sales (Y) Vs Take-away Sales (N) Sales',y=1.02)
        st.pyplot()

        st.subheader('Total Transactions with Promotion or Without Promotions in All Stores:')
        sales_promo_all_bar=sns.barplot(x='promo_item_yn', y='count', palette='Blues_d', data=sales_promo_all, order=promotion_category)
        sales_promo_all_bar.set(xlabel='Promotion Transactions Vs Without Promotion Trasactions',ylabel='Total Transactions')
        sales_promo_all_bar.set_title('Promotion Transactions (Y) Vs Without Promotion Trasactions (N)',y=1.02)
        st.pyplot()


    elif sales_description == 'Outlet 3':

        st.subheader('Total Daily Sales in Store 3:')
        plt.rcParams['figure.figsize'] = [13, 10]
        sales_3_day_total_line = sns.lineplot(x="transaction_date", y="total", data=sales_3_day_total)
        sales_3_day_total_line.set(ylim=(0, 5000))
        sales_3_day_total_line.set(xlabel='Transaction Date',ylabel='Total Sales')
        sales_3_day_total_line.set_title('Total Sales In Store 3:',y=1.02)
        plt.xticks(rotation=10)
        st.pyplot()

        st.subheader('Total Daily Sales combined in Store 3 based on In Store Sales and Take-away Sales:')
        plt.rcParams['figure.figsize'] = [13, 10]
        sales_y_n_3_line=sns.lineplot(x="transaction_date", y="total", hue='instore_yn', data=sales_day_total_3_y_n)
        sales_y_n_3_line.set(ylim=(0, 3000))
        sales_y_n_3_line.set(xlabel='Transaction Date',ylabel='Total Sales')
        sales_y_n_3_line.set_title('In Store Sales (Y) Vs Take-away (N) Sales',y=1.02)
        plt.xticks(rotation=10)
        st.pyplot()

        st.subheader('Total Sales in Store 3 based on the Hour of the Day:')
        sales_3_day_total_hour_bar = sns.barplot(x="day_hour", y="total", palette="Blues_d", data=sales_3_day_total_hour)
        sales_3_day_total_hour_bar.set(xlabel='Hours of the Day',ylabel='Total Sales')
        sales_3_day_total_hour_bar.set_title('Total Sales in each Hour',y=1.02)
        st.pyplot()

        st.subheader('Total In Store Vs Take-away Transactions done in Store 3:')
        sales_y_n_3_count_bar=sns.barplot(x='instore_yn', y='count', palette="Blues_d", data=sales_y_n_3_count,order=transaction_category)
        sales_y_n_3_count_bar.set(xlabel='In Stores Vs Take-away Vs Not Specified',ylabel='Total Transactions')
        sales_y_n_3_count_bar.set_title('In Store Transactions (Y) Vs Take-away Transactions (N) Sales',y=1.02)
        st.pyplot()

        st.subheader('Total In Store Vs Take-away Sales done in Store 3:')
        sales_y_n_3_total_bar=sns.barplot(x='instore_yn', y='total', palette='Blues_d', data=sales_y_n_3_total, order=transaction_category)
        sales_y_n_3_total_bar.set(xlabel='In Stores Vs Take-away Vs Not Specified',ylabel='Total Sales')
        sales_y_n_3_total_bar.set_title('In Store Sales (Y) Vs Take-away Sales (N) Sales',y=1.02)
        st.pyplot()

        st.subheader('Total Transactions with Promotion or Without Promotions in Store 3:')
        sales_promo_3_bar=sns.barplot(x='promo_item_yn', y='count', palette='Blues_d', data=sales_promo_3, order=promotion_category)
        sales_promo_3_bar.set(xlabel='Promotion Transactions Vs Without Promotion Trasactions',ylabel='Total Transactions')
        sales_promo_3_bar.set_title('Promotion Transactions (Y) Vs Without Promotion Trasactions (N)',y=1.02)
        st.pyplot()


    elif sales_description == 'Outlet 5':

        st.subheader('Total Daily Sales in Store 5:')
        plt.rcParams['figure.figsize'] = [13, 10]
        sales_5_day_total_line = sns.lineplot(x="transaction_date", y="total", data=sales_5_day_total)
        sales_5_day_total_line.set(ylim=(0, 5000))
        sales_5_day_total_line.set(xlabel='Transaction Date',ylabel='Total Sales')
        sales_5_day_total_line.set_title('Total Sales In Store 5:',y=1.02)
        plt.xticks(rotation=10)
        st.pyplot()

        st.subheader('Total Daily Sales combined in Store 5 based on In Store Sales and Take-away Sales:')
        plt.rcParams['figure.figsize'] = [13, 10]
        sales_y_n_5_line=sns.lineplot(x="transaction_date", y="total", hue='instore_yn', data=sales_day_total_5_y_n)
        sales_y_n_5_line.set(ylim=(0, 3000))
        sales_y_n_5_line.set(xlabel='Transaction Date',ylabel='Total Sales')
        sales_y_n_5_line.set_title('In Store Sales (Y) Vs Take-away (N) Sales',y=1.02)
        plt.xticks(rotation=10)
        st.pyplot()

        st.subheader('Total Sales in Store 5 based on the Hour of the Day:')
        sales_5_day_total_hour_bar = sns.barplot(x="day_hour", y="total", palette="Blues_d", data=sales_5_day_total_hour)
        sales_5_day_total_hour_bar.set(xlabel='Hours of the Day',ylabel='Total Sales')
        sales_5_day_total_hour_bar.set_title('Total Sales in each Hour',y=1.02)
        st.pyplot()

        st.subheader('Total In Store Vs Take-away Transactions done in Store 5:')
        sales_y_n_5_count_bar=sns.barplot(x='instore_yn', y='count', palette="Blues_d", data=sales_y_n_5_count,order=transaction_category)
        sales_y_n_5_count_bar.set(xlabel='In Stores Vs Take-away Vs Not Specified',ylabel='Total Transactions')
        sales_y_n_5_count_bar.set_title('In Store Transactions (Y) Vs Take-away Transactions (N) Sales',y=1.02)
        st.pyplot()

        st.subheader('Total In Store Vs Take-away Sales done in Store 5:')
        sales_y_n_5_total_bar=sns.barplot(x='instore_yn', y='total', palette='Blues_d', data=sales_y_n_5_total, order=transaction_category)
        sales_y_n_5_total_bar.set(xlabel='In Stores Vs Take-away Vs Not Specified',ylabel='Total Sales')
        sales_y_n_5_total_bar.set_title('In Store Sales (Y) Vs Take-away Sales (N) Sales',y=1.02)
        st.pyplot()

        st.subheader('Total Transactions with Promotion or Without Promotions in Store 5:')
        sales_promo_5_bar=sns.barplot(x='promo_item_yn', y='count', palette='Blues_d', data=sales_promo_5, order=promotion_category)
        sales_promo_5_bar.set(xlabel='Promotion Transactions Vs Without Promotion Trasactions',ylabel='Total Transactions')
        sales_promo_5_bar.set_title('Promotion Transactions (Y) Vs Without Promotion Trasactions (N)',y=1.02)
        st.pyplot()


    elif sales_description == 'Outlet 8':

        st.subheader('Total Daily Sales in Store 8:')
        plt.rcParams['figure.figsize'] = [13, 10]
        sales_8_day_total_line = sns.lineplot(x="transaction_date", y="total", data=sales_8_day_total)
        sales_8_day_total_line.set(ylim=(0, 5000))
        sales_8_day_total_line.set(xlabel='Transaction Date',ylabel='Total Sales')
        sales_8_day_total_line.set_title('Total Sales In Store 8:',y=1.02)
        plt.xticks(rotation=10)
        st.pyplot()

        st.subheader('Total Daily Sales combined in Store 8 based on In Store Sales and Take-away Sales:')
        plt.rcParams['figure.figsize'] = [13, 10]
        sales_y_n_8_line=sns.lineplot(x="transaction_date", y="total", hue='instore_yn', data=sales_day_total_8_y_n)
        sales_y_n_8_line.set(ylim=(0, 3000))
        sales_y_n_8_line.set(xlabel='Transaction Date',ylabel='Total Sales')
        sales_y_n_8_line.set_title('In Store Sales (Y) Vs Take-away (N) Sales',y=1.02)
        plt.xticks(rotation=10)
        st.pyplot()

        st.subheader('Total Sales in Store 8 based on the Hour of the Day:')
        sales_8_day_total_hour_bar = sns.barplot(x="day_hour", y="total", palette="Blues_d", data=sales_8_day_total_hour)
        sales_8_day_total_hour_bar.set(xlabel='Hours of the Day',ylabel='Total Sales')
        sales_8_day_total_hour_bar.set_title('Total Sales in each Hour',y=1.02)
        st.pyplot()

        st.subheader('Total In Store Vs Take-away Transactions done in Store 5:')
        sales_y_n_8_count_bar=sns.barplot(x='instore_yn', y='count', palette="Blues_d", data=sales_y_n_8_count,order=transaction_category)
        sales_y_n_8_count_bar.set(xlabel='In Stores Vs Take-away Vs Not Specified',ylabel='Total Transactions')
        sales_y_n_8_count_bar.set_title('In Store Transactions (Y) Vs Take-away Transactions (N) Sales',y=1.02)
        st.pyplot()

        st.subheader('Total In Store Vs Take-away Sales done in Store 8:')
        sales_y_n_8_total_bar=sns.barplot(x='instore_yn', y='total', palette='Blues_d', data=sales_y_n_8_total, order=transaction_category)
        sales_y_n_8_total_bar.set(xlabel='In Stores Vs Take-away Vs Not Specified',ylabel='Total Sales')
        sales_y_n_8_total_bar.set_title('In Store Sales (Y) Vs Take-away Sales (N) Sales',y=1.02)
        st.pyplot()

        st.subheader('Total Transactions with Promotion or Without Promotions in Store 8:')
        sales_promo_8_bar=sns.barplot(x='promo_item_yn', y='count', palette='Blues_d', data=sales_promo_8, order=promotion_category)
        sales_promo_8_bar.set(xlabel='Promotion Transactions Vs Without Promotion Trasactions',ylabel='Total Transactions')
        sales_promo_8_bar.set_title('Promotion Transactions (Y) Vs Without Promotion Trasactions (N)',y=1.02)
        st.pyplot()


    elif sales_description == 'Comparaison between the Outlets':

        compare = st.radio('',('All Stores', 'Select Specific Stores'))

        if compare == 'All Stores':

            st.subheader('Comparaison in the Total Daily Sales between the Stores:')
            plt.rcParams['figure.figsize'] = [13, 10]
            sales_day_outlet_line = sns.lineplot(x="transaction_date", y="total",  style='sales_outlet_id', data=sales_day_outlet)
            sales_day_outlet_line.set(ylim=(0, 5000))
            sales_day_outlet_line.set(xlabel='Transaction Date',ylabel='Total Sales')
            sales_day_outlet_line.set_title('Total Sales In The Stores:',y=1.02)
            plt.xticks(rotation=10)
            st.pyplot()

            st.subheader('Total Daily Sales combined in All the Stores based on In Store Sales and Take-away Sales:')
            plt.rcParams['figure.figsize'] = [13, 10]
            sales_day_total_y_n_compare_line=sns.lineplot(x="transaction_date", y="total", hue='instore_yn', style='sales_outlet_id', data=sales_day_total_y_n_compare)
            sales_day_total_y_n_compare_line.set(ylim=(0, 3000))
            sales_day_total_y_n_compare_line.set(xlabel='Transaction Date',ylabel='Total Sales')
            sales_day_total_y_n_compare_line.set_title('In Store Sales (Y) Vs Take-away (N) Sales',y=1.02)
            plt.xticks(rotation=10)
            st.pyplot()

            st.subheader('Total Sales in All the Stores based on the Hour of the Day:')
            sales_day_total_hour_compare_bar = sns.barplot(x="day_hour", y="total", palette="Blues_d", hue='sales_outlet_id', data=sales_day_total_hour_compare)
            sales_day_total_hour_compare_bar.set(xlabel='Hours of the Day',ylabel='Total Sales')
            sales_day_total_hour_compare_bar.set_title('Total Sales in each Hour',y=1.02)
            st.pyplot()


            st.subheader('Total In Store Vs Take-away Transactions done in All the Stores:')
            sales_y_n_compare_count_bar=sns.barplot(x='instore_yn', y='count', hue='sales_outlet_id', palette="Blues_d", data=sales_y_n_compare_count,order=transaction_category)
            sales_y_n_compare_count_bar.set(xlabel='In Stores Vs Take-away Vs Not Specified',ylabel='Total Transactions')
            sales_y_n_compare_count_bar.set_title('In Store Transactions (Y) Vs Take-away Transactions (N) Sales',y=1.02)
            st.pyplot()

            st.subheader('Total In Store Vs Take-away Sales done in All the Stores:')
            sales_y_n_compare_total_bar=sns.barplot(x='instore_yn', y='total', hue='sales_outlet_id' , palette='Blues_d', data=sales_y_n_compare_total, order=transaction_category)
            sales_y_n_compare_total_bar.set(xlabel='In Stores Vs Take-away Vs Not Specified',ylabel='Total Sales')
            sales_y_n_compare_total_bar.set_title('In Store Sales (Y) Vs Take-away Sales (N) Sales',y=1.02)
            st.pyplot()

            st.subheader('Total Transactions with Promotion or Without Promotions All the Stores:')
            sales_promo_compare_bar=sns.barplot(x='promo_item_yn', y='count', hue= 'sales_outlet_id', palette='Blues_d', data=sales_promo_compare, order=promotion_category)
            sales_promo_compare_bar.set(xlabel='Promotion Transactions Vs Without Promotion Trasactions',ylabel='Total Transactions')
            sales_promo_compare_bar.set_title('Promotion Transactions (Y) Vs Without Promotion Trasactions (N)',y=1.02)
            st.pyplot()

        elif compare == 'Select Specific Stores':
            sales_day_outlet_name=sales_day_outlet.copy()
            sales_day_outlet_name_unique=sales_day_outlet_name.drop_duplicates(subset=['sales_outlet_id'])
            list = sales_day_outlet_name_unique['sales_outlet_id'].to_numpy()
            options = st.multiselect('Select Outlet:', list)
            options_df=pd.DataFrame(options,columns = ['sales_outlet_id'])
            sales_day_outlet_name_selected=pd.merge(sales_day_outlet_name, options_df, how='inner' )
            sales_day_total_hour_compare_selected=pd.merge(sales_day_total_hour_compare, options_df, how='inner')
            sales_day_total_y_n_compare_selected=pd.merge(sales_day_total_y_n_compare, options_df, how='inner')
            sales_y_n_compare_count_selected=pd.merge(sales_y_n_compare_count, options_df, how='inner' )
            sales_y_n_compare_total_selected=pd.merge(sales_y_n_compare_total, options_df, how='inner' )
            sales_promo_compare_selected=pd.merge(sales_promo_compare, options_df, how='inner' )
            if not options:
                st.warning('Please add products above.')
            elif options:
                st.subheader('Comparaison in the Total Daily Sales between the Stores:')
                plt.rcParams['figure.figsize'] = [13, 10]
                g=sns.lineplot(x="transaction_date", y="total",  style='sales_outlet_id', data=sales_day_outlet_name_selected)
                g.set(ylim=(0, 5000))
                g.set(xlabel='Transaction Date',ylabel='Total Sales')
                g.set_title('Total Sales In Store 3:',y=1.02)
                plt.xticks(rotation=10)
                st.pyplot()

                st.subheader('Total Daily Sales combined in Stores selected based on In Store Sales and Take-away Sales:')
                plt.rcParams['figure.figsize'] = [13, 10]
                sales_day_total_y_n_compare_selected_line=sns.lineplot(x="transaction_date", y="total", hue='instore_yn', style='sales_outlet_id', data=sales_day_total_y_n_compare_selected)
                sales_day_total_y_n_compare_selected_line.set(ylim=(0, 3000))
                sales_day_total_y_n_compare_selected_line.set(xlabel='Transaction Date',ylabel='Total Sales')
                sales_day_total_y_n_compare_selected_line.set_title('In Store Sales (Y) Vs Take-away (N) Sales',y=1.02)
                plt.xticks(rotation=10)
                st.pyplot()

                st.subheader('Total Sales in Stores selected based on the Hour of the Day:')
                sales_day_total_hour_compare_selected_bar = sns.barplot(x="day_hour", y="total", palette="Blues_d", hue='sales_outlet_id', data=sales_day_total_hour_compare_selected)
                sales_day_total_hour_compare_selected_bar.set(xlabel='Hours of the Day',ylabel='Total Sales')
                sales_day_total_hour_compare_selected_bar.set_title('Total Sales in each Hour',y=1.02)
                st.pyplot()

                st.subheader('Total In Store Vs Take-away Transactions done in the selected Stores:')
                sales_y_n_compare_count_selected_bar=sns.barplot(x='instore_yn', y='count', hue='sales_outlet_id', palette="Blues_d", data=sales_y_n_compare_count_selected,order=transaction_category)
                sales_y_n_compare_count_selected_bar.set(xlabel='In Stores Vs Take-away Vs Not Specified',ylabel='Total Transactions')
                sales_y_n_compare_count_selected_bar.set_title('In Store Transactions (Y) Vs Take-away Transactions (N) Sales',y=1.02)
                st.pyplot()

                st.subheader('Total In Store Vs Take-away Sales done in the selected Stores:')
                sales_y_n_compare_total_selected_bar=sns.barplot(x='instore_yn', y='total', hue='sales_outlet_id' , palette='Blues_d', data=sales_y_n_compare_total_selected, order=transaction_category)
                sales_y_n_compare_total_selected_bar.set(xlabel='In Stores Vs Take-away Vs Not Specified',ylabel='Total Sales')
                sales_y_n_compare_total_selected_bar.set_title('In Store Sales (Y) Vs Take-away Sales (N) Sales',y=1.02)
                st.pyplot()

                st.subheader('Total Transactions with Promotion or Without Promotions the selected Stores:')
                sales_promo_compare_selected_bar=sns.barplot(x='promo_item_yn', y='count', hue= 'sales_outlet_id', palette='Blues_d', data=sales_promo_compare_selected, order=promotion_category)
                sales_promo_compare_selected_bar.set(xlabel='Promotion Transactions Vs Without Promotion Trasactions',ylabel='Total Transactions')
                sales_promo_compare_selected_bar.set_title('Promotion Transactions (Y) Vs Without Promotion Trasactions (N)',y=1.02)
                st.pyplot()


elif button=='Customers Description':

    sns.set_context('talk')

    customer_type=['With Loyalty Card','No Loyalty Card']

    st.header('Customers Analysis:')
    st.subheader('Select the Store to see the Customers Analysis:')

    customers_card_stores=st.selectbox(' ',
            ('All','Outlet 3','Outlet 5','Outlet 8', 'Compare the 3 Stores'))

    if customers_card_stores == 'All':

        st.subheader('Total Transactions in All Stores based on Customer Type:')
        st.write('Note that the same customer can be repeated more than once in this count')
        sales_customers_left_type_count_bar=sns.barplot(x="customer type", y="count", palette="Blues_d", data=sales_customers_left_type_count, order=customer_type)
        sales_customers_left_type_count_bar.set(xlabel='Customer Type',ylabel='Total Transactions')
        sales_customers_left_type_count_bar.set_title('Total Transactions based on Customer Type',y=1.02)
        st.pyplot()

        st.subheader('Total Sales in All Stores based on Customer Type:')
        st.write('Note that the same customer can be repeated more than once in this count')
        sales_customers_left_type_total_bar=sns.barplot(x='customer type', y='total', palette='Blues_d', data=sales_customers_left_type_total, order=customer_type)
        sales_customers_left_type_total_bar.set(xlabel='Customer Type',ylabel='Total Sales')
        sales_customers_left_type_total_bar.set_title('Total Sales based on Customer Type',y=1.02)
        st.pyplot()

    elif customers_card_stores == 'Outlet 3':

        st.subheader('Total Transactions in Store 3 based on Customer Type:')
        st.write('Note that the same customer can be repeated more than once in this count')
        sales_customers_left_3_type_count_bar=sns.barplot(x="customer type", y="count", palette="Blues_d", data=sales_customers_left_3_type_count, order=customer_type)
        sales_customers_left_3_type_count_bar.set(xlabel='Customer Type',ylabel='Total Transactions')
        sales_customers_left_3_type_count_bar.set_title('Total Transactions based on Customer Type',y=1.02)
        st.pyplot()

        st.subheader('Total Sales in Store 3 based on Customer Type:')
        st.write('Note that the same customer can be repeated more than once in this count')
        sales_customers_left_3_type_total_bar=sns.barplot(x='customer type', y='total', palette='Blues_d', data=sales_customers_left_3_type_total, order=customer_type)
        sales_customers_left_3_type_total_bar.set(xlabel='Customer Type',ylabel='Total Sales')
        sales_customers_left_3_type_total_bar.set_title('Total Sales based on Customer Type',y=1.02)
        st.pyplot()

    elif customers_card_stores == 'Outlet 5':

        st.subheader('Total Transactions in Store 5 based on Customer Type:')
        st.write('Note that the same customer can be repeated more than once in this count')
        sales_customers_left_5_type_count_bar=sns.barplot(x="customer type", y="count", palette="Blues_d", data=sales_customers_left_5_type_count, order=customer_type)
        sales_customers_left_5_type_count_bar.set(xlabel='Customer Type',ylabel='Total Transactions')
        sales_customers_left_5_type_count_bar.set_title('Total Transactions based on Customer Type',y=1.02)
        st.pyplot()

        st.subheader('Total Sales in Store 5 based on Customer Type:')
        st.write('Note that the same customer can be repeated more than once in this count')
        sales_customers_left_5_type_total_bar=sns.barplot(x='customer type', y='total', palette='Blues_d', data=sales_customers_left_5_type_total, order=customer_type)
        sales_customers_left_5_type_total_bar.set(xlabel='Customer Type',ylabel='Total Sales')
        sales_customers_left_5_type_total_bar.set_title('Total Sales based on Customer Type',y=1.02)
        st.pyplot()

    elif customers_card_stores == 'Outlet 8':

        st.subheader('Total Transactions in Store 5 based on Customer Type:')
        st.write('Note that the same customer can be repeated more than once in this count')
        sales_customers_left_8_type_count_bar=sns.barplot(x="customer type", y="count", palette="Blues_d", data=sales_customers_left_8_type_count, order=customer_type)
        sales_customers_left_8_type_count_bar.set(xlabel='Customer Type',ylabel='Total Transactions')
        sales_customers_left_8_type_count_bar.set_title('Total Transactions based on Customer Type',y=1.02)
        st.pyplot()

        st.subheader('Total Sales in Store 8 based on Customer Type:')
        st.write('Note that the same customer can be repeated more than once in this count')
        sales_customers_left_8_type_total_bar=sns.barplot(x='customer type', y='total', palette='Blues_d', data=sales_customers_left_8_type_total, order=customer_type)
        sales_customers_left_8_type_total_bar.set(xlabel='Customer Type',ylabel='Total Sales')
        sales_customers_left_8_type_total_bar.set_title('Total Sales based on Customer Type',y=1.02)
        st.pyplot()

    elif customers_card_stores == 'Compare the 3 Stores':

        compare = st.radio('',('All Stores', 'Select Specific Stores'))

        if compare == 'All Stores':

            st.subheader('Total Transactions in All Stores based on Customer Type:')
            st.write('Note that the same customer can be repeated more than once in this count')
            sales_customers_left_compare_type_count_bar=sns.barplot(x="customer type", y="count", palette="Blues_d", hue='sales_outlet_id', data=sales_customers_left_compare_type_count, order=customer_type)
            sales_customers_left_compare_type_count_bar.set(xlabel='Customer Type',ylabel='Total Transactions')
            sales_customers_left_compare_type_count_bar.set_title('Total Transactions based on Customer Type',y=1.02)
            st.pyplot()

            st.subheader('Total Sales All the Stores based on Customer Type:')
            st.write('Note that the same customer can be repeated more than once in this count')
            sales_customers_left_compare_type_total_bar=sns.barplot(x='customer type', y='total', palette='Blues_d', hue='sales_outlet_id', data=sales_customers_left_compare_type_total, order=customer_type)
            sales_customers_left_compare_type_total_bar.set(xlabel='Customer Type',ylabel='Total Sales')
            sales_customers_left_compare_type_total_bar.set_title('Total Sales based on Customer Type',y=1.02)
            st.pyplot()

        elif compare == 'Select Specific Stores':
            sales_customers_left_unique=sales_customers_left.drop_duplicates(subset=['sales_outlet_id'])
            list = sales_customers_left_unique['sales_outlet_id'].to_numpy()
            options = st.multiselect('Select Outlet:', list)
            options_df=pd.DataFrame(options,columns = ['sales_outlet_id'])
            sales_customers_left_compare_type_count_selected=pd.merge(sales_customers_left_compare_type_count, options_df, how='inner' )
            sales_customers_left_compare_type_total_selected=pd.merge(sales_customers_left_compare_type_total, options_df, how='inner' )
            if not options:
                st.warning('Please add products above.')
            elif options:

                st.subheader('Total Transactions in the selected Stores based on Customer Type:')
                st.write('Note that the same customer can be repeated more than once in this count')
                sales_customers_left_compare_type_count_selected_bar=sns.barplot(x="customer type", y="count", palette="Blues_d", hue='sales_outlet_id', data=sales_customers_left_compare_type_count_selected, order=customer_type)
                sales_customers_left_compare_type_count_selected_bar.set(xlabel='Customer Type',ylabel='Total Transactions')
                sales_customers_left_compare_type_count_selected_bar.set_title('Total Transactions based on Customer Type',y=1.02)
                st.pyplot()

                st.subheader('Total Sales the selected Stores based on Customer Type:')
                st.write('Note that the same customer can be repeated more than once in this count')
                sales_customers_left_compare_type_total_selected_bar=sns.barplot(x='customer type', y='total', palette='Blues_d', hue='sales_outlet_id', data=sales_customers_left_compare_type_total_selected, order=customer_type)
                sales_customers_left_compare_type_total_selected_bar.set(xlabel='Customer Type',ylabel='Total Sales')
                sales_customers_left_compare_type_total_selected_bar.set_title('Total Sales based on Customer Type',y=1.02)
                st.pyplot()


elif button == 'Loyal Customers Description':

    sns.set_context('talk')
    category_order=['Baby Boomers','Gen X','Older Millennials','Younger Millennials','Gen Z']
    gender_order=['F','M','N']

    st.header('Loyal Customers Analysis:')
    st.subheader('Select the Store to see the Loyal Customers Analysis:')

    customers_loyal_stores=st.selectbox(' ',
            ('All','Outlet 3','Outlet 5','Outlet 8','Compare the 3 Stores'))


    if customers_loyal_stores == 'All':

        st.subheader('Total Transactions by each Generation in All the Stores:')
        sales_customers_loyal_generations_transaction_bar=sns.barplot(x="generation", y="count", palette="Blues_d", data=sales_customers_loyal_generations_transaction, order=category_order)
        sales_customers_loyal_generations_transaction_bar.set(xlabel='Generation',ylabel='Total Transactions')
        sales_customers_loyal_generations_transaction_bar.set_title('Total Transactions based on Generation',y=1.02)
        plt.xticks(rotation=10)
        st.pyplot()

        st.subheader('Total Sales by each Generation in All the Stores:')
        sales_customers_loyal_generations_sales_bar=sns.barplot(x="generation", y="total", palette="Blues_d", data=sales_customers_loyal_generations_sales, order=category_order)
        sales_customers_loyal_generations_sales_bar.set(xlabel='Generation',ylabel='Total Sales')
        sales_customers_loyal_generations_sales_bar.set_title('Total Sales based on Generation',y=1.02)
        plt.xticks(rotation=10)
        st.pyplot()

        st.subheader('Gender of loyal customers based on their Generation in All the Stores:')
        customers_gender_bar=sns.barplot(x='gender', y='count',palette="Blues_d", hue='generation', data=customers_gender, order=gender_order)
        customers_gender_bar.set(xlabel='Gender',ylabel='Number of Customers')
        customers_gender_bar.set_title('Number of Customers based on Gender and Generation',y=1.02)
        st.pyplot()

        st.subheader('Number of Loyal Customer from each Year in All the Stores:')
        sales_customers_loyal_generations_year_bar=sns.barplot(x="year", y="count", palette="Blues_d", data=sales_customers_loyal_generations_year)
        sales_customers_loyal_generations_year_bar.set(xlabel='Year',ylabel='Number of Customers')
        sales_customers_loyal_generations_year_bar.set_title('Number of Customers based on the Year of being Loyal',y=1.02)
        st.pyplot()

        st.subheader('The most Profitable Customers to our Business in All the Stores:')
        x = st.number_input('Enter the number of customers you want to see:',min_value=5,)
        x=int(x)
        sales_customers_loyal_generations_total=sales_customers_loyal_generations_total.nlargest(x, ['total'])
        sales_customers_loyal_generations_total_bar=sns.barplot(x="customer_first-name", y="total", palette="Blues_d",  data=sales_customers_loyal_generations_total)
        sales_customers_loyal_generations_total_bar.set(xlabel='Customer First Name',ylabel='Total Sales')
        sales_customers_loyal_generations_total_bar.set_title('Most Profitable Customers',y=1.02)
        plt.xticks(rotation=50)
        st.pyplot()



    elif customers_loyal_stores == 'Outlet 3':

        st.subheader('Total Transactions by each Generation in Store 3:')
        sales_customers_loyal_generations_3_transaction_bar=sns.barplot(x="generation", y="count", palette="Blues_d", data=sales_customers_loyal_generations_3_transaction, order=category_order)
        sales_customers_loyal_generations_3_transaction_bar.set(xlabel='Generation',ylabel='Total Transactions')
        sales_customers_loyal_generations_3_transaction_bar.set_title('Total Transactions based on Generation',y=1.02)
        plt.xticks(rotation=10)
        st.pyplot()

        st.subheader('Total Sales by each Generation in Store 3:')
        sales_customers_loyal_generations_3_sales_bar=sns.barplot(x="generation", y="total", palette="Blues_d", data=sales_customers_loyal_generations_3_sales, order=category_order)
        sales_customers_loyal_generations_3_sales_bar.set(xlabel='Generation',ylabel='Total Sales')
        sales_customers_loyal_generations_3_sales_bar.set_title('Total Sales based on Generation',y=1.02)
        plt.xticks(rotation=10)
        st.pyplot()

        st.subheader('Gender of loyal customers based on their Generation in Store 3:')
        customers_gender_3_bar=sns.barplot(x='gender', y='count',palette="Blues_d", hue='generation', data=customers_gender_3, order=gender_order)
        customers_gender_3_bar.set(xlabel='Gender',ylabel='Number of Customers')
        customers_gender_3_bar.set_title('Number of Customers based on Gender and Generation',y=1.02)
        st.pyplot()

        st.subheader('Number of Loyal Customer from each Year in Store 3:')
        sales_customers_loyal_generations_year_3_bar=sns.barplot(x="year", y="count", palette="Blues_d", data=sales_customers_loyal_generations_year_3)
        sales_customers_loyal_generations_year_3_bar.set(xlabel='Year',ylabel='Number of Customers')
        sales_customers_loyal_generations_year_3_bar.set_title('Number of Customers based on the Year of being Loyal',y=1.02)
        st.pyplot()

        st.subheader('The most Profitable Customers to our Business in Store 3:')
        x = st.number_input('Enter the number of customers you want to see:',min_value=5,)
        x=int(x)
        sales_customers_loyal_generations_3_total=sales_customers_loyal_generations_3_total.nlargest(x, ['total'])
        sales_customers_loyal_generations_3_total_bar=sns.barplot(x="customer_first-name", y="total", palette="Blues_d",  data=sales_customers_loyal_generations_3_total)
        sales_customers_loyal_generations_3_total_bar.set(xlabel='Customer First Name',ylabel='Total Sales')
        sales_customers_loyal_generations_3_total_bar.set_title('Most Profitable Customers',y=1.02)
        plt.xticks(rotation=50)
        st.pyplot()


    elif customers_loyal_stores == 'Outlet 5':

        st.subheader('Total Transactions by each Generation in Store 5:')
        sales_customers_loyal_generations_5_transaction_bar=sns.barplot(x="generation", y="count", palette="Blues_d", data=sales_customers_loyal_generations_5_transaction, order=category_order)
        sales_customers_loyal_generations_5_transaction_bar.set(xlabel='Generation',ylabel='Total Transactions')
        sales_customers_loyal_generations_5_transaction_bar.set_title('Total Transactions based on Generation',y=1.02)
        plt.xticks(rotation=10)
        st.pyplot()

        st.subheader('Total Sales by each Generation in Store 5:')
        sales_customers_loyal_generations_5_sales_bar=sns.barplot(x="generation", y="total", palette="Blues_d", data=sales_customers_loyal_generations_5_sales, order=category_order)
        sales_customers_loyal_generations_5_sales_bar.set(xlabel='Generation',ylabel='Total Sales')
        sales_customers_loyal_generations_5_sales_bar.set_title('Total Sales based on Generation',y=1.02)
        plt.xticks(rotation=10)
        st.pyplot()

        st.subheader('Gender of loyal customers based on their Generation in Store 5:')
        customers_gender_5_bar=sns.barplot(x='gender', y='count',palette="Blues_d", hue='generation', data=customers_gender_5, order=gender_order)
        customers_gender_5_bar.set(xlabel='Gender',ylabel='Number of Customers')
        customers_gender_5_bar.set_title('Number of Customers based on Gender and Generation',y=1.02)
        st.pyplot()

        st.subheader('Number of Loyal Customer from each Year in Store 5:')
        sales_customers_loyal_generations_year_5_bar=sns.barplot(x="year", y="count", palette="Blues_d", data=sales_customers_loyal_generations_year_5)
        sales_customers_loyal_generations_year_5_bar.set(xlabel='Year',ylabel='Number of Customers')
        sales_customers_loyal_generations_year_5_bar.set_title('Number of Customers based on the Year of being Loyal',y=1.02)
        st.pyplot()

        st.subheader('The most Profitable Customers to our Business in Store 5:')
        x = st.number_input('Enter the number of customers you want to see:',min_value=5,)
        x=int(x)
        sales_customers_loyal_generations_5_total=sales_customers_loyal_generations_5_total.nlargest(x, ['total'])
        sales_customers_loyal_generations_5_total_bar=sns.barplot(x="customer_first-name", y="total", palette="Blues_d",  data=sales_customers_loyal_generations_5_total)
        sales_customers_loyal_generations_5_total_bar.set(xlabel='Customer First Name',ylabel='Total Sales')
        sales_customers_loyal_generations_5_total_bar.set_title('Most Profitable Customers',y=1.02)
        plt.xticks(rotation=50)
        st.pyplot()



    elif customers_loyal_stores == 'Outlet 8':

        st.subheader('Total Transactions by each Generation in Store 8:')
        sales_customers_loyal_generations_8_transaction_bar=sns.barplot(x="generation", y="count", palette="Blues_d", data=sales_customers_loyal_generations_8_transaction, order=category_order)
        sales_customers_loyal_generations_8_transaction_bar.set(xlabel='Generation',ylabel='Total Transactions')
        sales_customers_loyal_generations_8_transaction_bar.set_title('Total Transactions based on Generation',y=1.02)
        plt.xticks(rotation=10)
        st.pyplot()

        st.subheader('Total Sales by each Generation in Store 8:')
        sales_customers_loyal_generations_8_sales_bar=sns.barplot(x="generation", y="total", palette="Blues_d", data=sales_customers_loyal_generations_8_sales, order=category_order)
        sales_customers_loyal_generations_8_sales_bar.set(xlabel='Generation',ylabel='Total Sales')
        sales_customers_loyal_generations_8_sales_bar.set_title('Total Sales based on Generation',y=1.02)
        plt.xticks(rotation=10)
        st.pyplot()

        st.subheader('Gender of loyal customers based on their Generation in Store 8:')
        customers_gender_8_bar=sns.barplot(x='gender', y='count',palette="Blues_d", hue='generation', data=customers_gender_8, order=gender_order)
        customers_gender_8_bar.set(xlabel='Gender',ylabel='Number of Customers')
        customers_gender_8_bar.set_title('Number of Customers based on Gender and Generation',y=1.02)
        st.pyplot()

        st.subheader('Number of Loyal Customer from each Year in Store 8:')
        sales_customers_loyal_generations_year_8_bar=sns.barplot(x="year", y="count", palette="Blues_d", data=sales_customers_loyal_generations_year_8)
        sales_customers_loyal_generations_year_8_bar.set(xlabel='Year',ylabel='Number of Customers')
        sales_customers_loyal_generations_year_8_bar.set_title('Number of Customers based on the Year of being Loyal',y=1.02)
        st.pyplot()

        st.subheader('The most Profitable Customers to our Business in Store 8:')
        x = st.number_input('Enter the number of customers you want to see:',min_value=5,)
        x=int(x)
        sales_customers_loyal_generations_8_total=sales_customers_loyal_generations_8_total.nlargest(x, ['total'])
        sales_customers_loyal_generations_8_total_bar=sns.barplot(x="customer_first-name", y="total", palette="Blues_d",  data=sales_customers_loyal_generations_8_total)
        sales_customers_loyal_generations_8_total_bar.set(xlabel='Customer First Name',ylabel='Total Sales')
        sales_customers_loyal_generations_8_total_bar.set_title('Most Profitable Customers',y=1.02)
        plt.xticks(rotation=50)
        st.pyplot()


    elif customers_loyal_stores == 'Compare the 3 Stores':

        compare = st.radio('',('All Stores', 'Select Specific Stores'))

        if compare == 'All Stores':

            st.subheader('Total Transactions by each Generation in All the Stores:')
            sales_customers_loyal_generations_year_compare_bar=sns.barplot(x="generation", y="count",hue='sales_outlet_id', palette="Blues_d", data=sales_customers_loyal_generations_year_compare, order=category_order)
            sales_customers_loyal_generations_year_compare_bar.set(xlabel='Generation',ylabel='Total Transactions')
            sales_customers_loyal_generations_year_compare_bar.set_title('Total Transactions based on Generation',y=1.02)
            plt.xticks(rotation=10)
            st.pyplot()

            st.subheader('Total Sales by each Generation in All the Stores:')
            sales_customers_loyal_generations_sales_compare_bar=sns.barplot(x="generation", y="total",hue='sales_outlet_id', palette="Blues_d", data=sales_customers_loyal_generations_sales_compare, order=category_order)
            sales_customers_loyal_generations_sales_compare_bar.set(xlabel='Generation',ylabel='Total Sales')
            sales_customers_loyal_generations_sales_compare_bar.set_title('Total Sales based on Generation',y=1.02)
            plt.xticks(rotation=10)
            st.pyplot()



        elif compare == 'Select Specific Stores':
            sales_customers_loyal_generations_year_compare_unique=sales_customers_loyal_generations_year_compare.drop_duplicates(subset=['sales_outlet_id'])
            list = sales_customers_loyal_generations_year_compare_unique['sales_outlet_id'].to_numpy()
            options = st.multiselect('Select Outlet:', list)
            options_df=pd.DataFrame(options,columns = ['sales_outlet_id'])
            sales_customers_loyal_generations_year_compare_selected=pd.merge(sales_customers_loyal_generations_year_compare, options_df, how='inner' )
            sales_customers_loyal_generations_sales_compare_selected=pd.merge(sales_customers_loyal_generations_sales_compare, options_df, how='inner' )
            if not options:
                st.warning('Please add products above.')
            elif options:

                st.subheader('Total Transactions by each Generation in the selected Stores:')
                sales_customers_loyal_generations_year_compare_selected_bar=sns.barplot(x="generation", y="count",hue='sales_outlet_id', palette="Blues_d", data=sales_customers_loyal_generations_year_compare_selected, order=category_order)
                sales_customers_loyal_generations_year_compare_selected_bar.set(xlabel='Generation',ylabel='Total Transactions')
                sales_customers_loyal_generations_year_compare_selected_bar.set_title('Total Transactions based on Generation',y=1.02)
                plt.xticks(rotation=10)
                st.pyplot()

                st.subheader('Total Sales by each Generation in the selected Stores:')
                sales_customers_loyal_generations_sales_compare_selected_bar=sns.barplot(x="generation", y="total",hue='sales_outlet_id', palette="Blues_d", data=sales_customers_loyal_generations_sales_compare_selected, order=category_order)
                sales_customers_loyal_generations_sales_compare_selected_bar.set(xlabel='Generation',ylabel='Total Sales')
                sales_customers_loyal_generations_sales_compare_selected_bar.set_title('Total Sales based on Generation',y=1.02)
                plt.xticks(rotation=10)
                st.pyplot()



elif button == 'Products Description':

    st.header('Products Analysis:')
    st.subheader('Select the Store to see the Products Analysis:')

    product_description=st.selectbox(
            '',
            ('All','Outlet 3','Outlet 5','Outlet 8'))

    if product_description == 'All':

        st.subheader('Select what you want to see:')

        smallest_largest=st.radio(' ',
                                    ('Most Products Sold in All the Stores','Least Products Sold in All the Stores'))

        if smallest_largest=='Most Products Sold in All the Stores':

            x = st.number_input('Enter the number of products you want to see:',min_value=4,)
            x=int(x)
            sales_products_quantity_largest=sales_products_quantity.nlargest(x, ['quantity'])
            st.subheader('Most Products sold in All the Stores:')
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_products_quantity_largest_bar=sns.barplot(x='product', y='quantity', palette='Blues_d', data=sales_products_quantity_largest)
            sales_products_quantity_largest_bar.set(xlabel='Products',ylabel='Quantity Sold')
            sales_products_quantity_largest_bar.set_title('Most Products Sold',y=1.02)
            plt.xticks(rotation=30)
            st.pyplot()


            st.subheader('Select the Hour of the Day to see the Most Products Sold at this time in All the Stores:')
            hour_to_filter = st.slider('Hour of the Day:', 0, 23, 17)
            filtered_data = sales_products[sales_products['transaction_time_filtered'].dt.hour == hour_to_filter]
            sales_products_quantity_hour=filtered_data.groupby(['product'])['quantity'].sum().reset_index()
            sales_products_quantity_hour_largest=sales_products_quantity_hour.nlargest(x, ['quantity'])
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_products_quantity_hour_largest_bar=sns.barplot(x='product', y='quantity', palette='Blues_d', data=sales_products_quantity_hour_largest)
            sales_products_quantity_hour_largest_bar.set(xlabel='Products',ylabel='Quantity Sold')
            sales_products_quantity_hour_largest_bar.set_title('Most Products Sold at the chosen time',y=1.02)
            plt.xticks(rotation=30)
            st.pyplot()

        elif smallest_largest=='Least Products Sold in All the Stores':

            y = st.number_input('Enter the number of products you want to see:',min_value=4,)
            y=int(y)
            sales_products_quantity_smallest=sales_products_quantity.nsmallest(y, ['quantity'])
            st.subheader('Least Products sold in All the Stores:')
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_products_quantity_smallest_bar=sns.barplot(x='product', y='quantity', palette='Blues_d', data=sales_products_quantity_smallest)
            sales_products_quantity_smallest_bar.set(xlabel='Products',ylabel='Quantity Sold')
            sales_products_quantity_smallest_bar.set_title('Least Products Sold',y=1.02)
            plt.xticks(rotation=30)
            st.pyplot()

            st.subheader('Select the Hour of the Day to see the Least Products Sold at this time in ALl the Stores:')
            hour_to_filter = st.slider('Hour of the Day:', 0, 23, 17)
            filtered_data = sales_products[sales_products['transaction_time_filtered'].dt.hour == hour_to_filter]
            sales_products_quantity_hour=filtered_data.groupby(['product'])['quantity'].sum().reset_index()
            sales_products_quantity_hour_smallest=sales_products_quantity_hour.nsmallest(y, ['quantity'])
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_products_quantity_hour_smallest_bar=sns.barplot(x='product', y='quantity', palette='Blues_d', data=sales_products_quantity_hour_smallest)
            sales_products_quantity_hour_smallest_bar.set(xlabel='Products',ylabel='Quantity Sold')
            sales_products_quantity_hour_smallest_bar.set_title('Least Products Sold at the chosen time',y=1.02)
            plt.xticks(rotation=30)
            st.pyplot()


        st.markdown('***')
        st.subheader('Select Products to see the Quantity sold in All the Stores:')
        sales_products_unique=sales_products.drop_duplicates(subset=['product'])
        list = sales_products_unique['product'].to_numpy()
        options = st.multiselect('Select Products:', list)
        options_df=pd.DataFrame(options,columns = ['product'])
        sales_products_unique_selected=pd.merge(sales_products, options_df, how='inner')
        sales_products_unique_selected_quantity=sales_products_unique_selected.groupby(['product'])['quantity'].sum().reset_index()
        if not options:
            st.warning('Please add products above.')
        elif options:
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_products_unique_selected_quantity_bar=sns.barplot(x='product', y='quantity', palette='Blues_d', data=sales_products_unique_selected_quantity)
            sales_products_unique_selected_quantity_bar.set(xlabel='Products',ylabel='Quantity Sold')
            sales_products_unique_selected_quantity_bar.set_title('Quantity Sold of the selected Products',y=1.02)
            plt.xticks(rotation=30)
            st.pyplot()


    elif product_description == 'Outlet 3':

        st.subheader('Select what you want to see:')

        smallest_largest_3=st.radio(' ',
                                    ('Most Products Sold in Store 3','Least Products Sold in Store 3'))

        if smallest_largest_3=='Most Products Sold in Store 3':

            x = st.number_input('Enter the number of products you want to see:',min_value=4,)
            x=int(x)
            sales_products_3_quantity_largest=sales_products_3_quantity.nlargest(x, ['quantity'])
            st.subheader('Most Products sold in Store 3:')
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_products_3_quantity_largest_bar=sns.barplot(x='product', y='quantity', palette='Blues_d', data=sales_products_3_quantity_largest)
            sales_products_3_quantity_largest_bar.set(xlabel='Products',ylabel='Quantity Sold')
            sales_products_3_quantity_largest_bar.set_title('Most Products Sold',y=1.02)
            plt.xticks(rotation=30)
            st.pyplot()

            st.subheader('Select the Hour of the Day to see the Most Products Sold at this time in Store 3:')
            hour_to_filter = st.slider('Hour of the Day:', 0, 23, 17)
            filtered_data = sales_products_3[sales_products_3['transaction_time_filtered'].dt.hour == hour_to_filter]
            sales_products_3_quantity_hour=filtered_data.groupby(['product'])['quantity'].sum().reset_index()
            sales_products_3_quantity_hour_largest=sales_products_3_quantity_hour.nlargest(x, ['quantity'])
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_products_3_quantity_hour_largest_bar=sns.barplot(x='product', y='quantity', palette='Blues_d', data=sales_products_3_quantity_hour_largest)
            sales_products_3_quantity_hour_largest_bar.set(xlabel='Products',ylabel='Quantity Sold')
            sales_products_3_quantity_hour_largest_bar.set_title('Most Products Sold at the chosen time',y=1.02)
            plt.xticks(rotation=30)
            st.pyplot()

        elif smallest_largest_3=='Least Products Sold in Store 3':

            y=st.number_input('Enter the number of products you want to see:', min_value=4,)
            y=int(y)
            sales_products_3_quantity_smallest=sales_products_3_quantity.nsmallest(y, ['quantity'])
            st.subheader('Least Products sold in Store 3:')
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_products_3_quantity_smallest_bar=sns.barplot(x='product', y='quantity', palette='Blues_d', data=sales_products_3_quantity_smallest)
            sales_products_3_quantity_smallest_bar.set(xlabel='Products',ylabel='Quantity Sold')
            sales_products_3_quantity_smallest_bar.set_title('Least Products Sold',y=1.02)
            plt.xticks(rotation=30)
            st.pyplot()

            st.subheader('Select the Hour of the Day to see the Least Products Sold at this time in Store 3:')
            hour_to_filter = st.slider('Hour of the Day:', 0, 23, 17)
            filtered_data = sales_products_3[sales_products_3['transaction_time_filtered'].dt.hour == hour_to_filter]
            sales_products_3_quantity_hour=filtered_data.groupby(['product'])['quantity'].sum().reset_index()
            sales_products_3_quantity_hour_smallest=sales_products_3_quantity_hour.nsmallest(y, ['quantity'])
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_products_3_quantity_hour_smallest_bar=sns.barplot(x='product', y='quantity', palette='Blues_d', data=sales_products_3_quantity_hour_smallest)
            sales_products_3_quantity_hour_smallest_bar.set(xlabel='Products',ylabel='Quantity Sold')
            sales_products_3_quantity_hour_smallest_bar.set_title('Least Products Sold at the chosen time',y=1.02)
            plt.xticks(rotation=30)
            st.pyplot()

        st.markdown('***')
        st.subheader('Select Products to see the Quantity sold in Store 3:')
        sales_products_unique=sales_products.drop_duplicates(subset=['product'])
        list = sales_products_unique['product'].to_numpy()
        options = st.multiselect('Select Products:', list)
        options_df=pd.DataFrame(options,columns = ['product'])
        sales_products_3_unique_selected=pd.merge(sales_products_3, options_df, how='inner')
        sales_products_3_unique_selected_quantity=sales_products_3_unique_selected.groupby(['product'])['quantity'].sum().reset_index()
        if not options:
            st.warning('Please add products above.')
        elif options:
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_products_3_unique_selected_quantity_bar=sns.barplot(x='product', y='quantity', palette='Blues_d', data=sales_products_3_unique_selected_quantity)
            sales_products_3_unique_selected_quantity_bar.set(xlabel='Products',ylabel='Quantity Sold')
            sales_products_3_unique_selected_quantity_bar.set_title('Quantity Sold of the selected Products',y=1.02)
            plt.xticks(rotation=30)
            st.pyplot()


    elif product_description == 'Outlet 5':

        st.subheader('Select what you want to see:')

        smallest_largest_5=st.radio(' ',
                                    ('Most Products Sold in Store 5','Least Products Sold in Store 5'))

        if smallest_largest_5=='Most Products Sold in Store 5':

            x = st.number_input('Enter the number of products you want to see:',min_value=4,)
            x=int(x)
            sales_products_5_quantity_largest=sales_products_5_quantity.nlargest(x, ['quantity'])
            st.subheader('Most Products sold in Store 5:')
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_products_5_quantity_largest_bar=sns.barplot(x='product', y='quantity', palette='Blues_d', data=sales_products_5_quantity_largest)
            sales_products_5_quantity_largest_bar.set(xlabel='Products',ylabel='Quantity Sold')
            sales_products_5_quantity_largest_bar.set_title('Most Products Sold',y=1.02)
            plt.xticks(rotation=30)
            st.pyplot()

            st.subheader('Select the Hour of the Day to see the Most Products Sold at this time in store 5:')
            hour_to_filter = st.slider('Hour of the Day:', 0, 23, 17)
            filtered_data = sales_products_5[sales_products_5['transaction_time_filtered'].dt.hour == hour_to_filter]
            sales_products_5_quantity_hour=filtered_data.groupby(['product'])['quantity'].sum().reset_index()
            sales_products_5_quantity_hour_largest=sales_products_5_quantity_hour.nlargest(x, ['quantity'])
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_products_5_quantity_hour_largest_bar=sns.barplot(x='product', y='quantity', palette='Blues_d', data=sales_products_5_quantity_hour_largest)
            sales_products_5_quantity_hour_largest_bar.set(xlabel='Products',ylabel='Quantity Sold')
            sales_products_5_quantity_hour_largest_bar.set_title('Most Products Sold at the chosen time',y=1.02)
            plt.xticks(rotation=30)
            st.pyplot()

        elif smallest_largest_5=='Least Products Sold in Store 5':

            y=st.number_input('Enter the number of products you want to see:', min_value=4,)
            y=int(y)
            sales_products_5_quantity_smallest=sales_products_5_quantity.nsmallest(y, ['quantity'])
            st.subheader('Least Products sold in Store 5:')
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_products_5_quantity_smallest_bar=sns.barplot(x='product', y='quantity', palette='Blues_d', data=sales_products_5_quantity_smallest)
            sales_products_5_quantity_smallest_bar.set(xlabel='Products',ylabel='Quantity Sold')
            sales_products_5_quantity_smallest_bar.set_title('Least Products Sold',y=1.02)
            plt.xticks(rotation=30)
            st.pyplot()

            st.subheader('Select the Hour of the Day to see the Least Products Sold at this time in Store 5:')
            hour_to_filter = st.slider('Hour of the Day:', 0, 23, 17)
            filtered_data = sales_products_5[sales_products_5['transaction_time_filtered'].dt.hour == hour_to_filter]
            sales_products_5_quantity_hour=filtered_data.groupby(['product'])['quantity'].sum().reset_index()
            sales_products_5_quantity_hour_smallest=sales_products_5_quantity_hour.nsmallest(y, ['quantity'])
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_products_5_quantity_hour_smallest_bar=sns.barplot(x='product', y='quantity', palette='Blues_d', data=sales_products_5_quantity_hour_smallest)
            sales_products_5_quantity_hour_smallest_bar.set(xlabel='Products',ylabel='Quantity Sold')
            sales_products_5_quantity_hour_smallest_bar.set_title('Least Products Sold at the chosen time',y=1.02)
            plt.xticks(rotation=30)
            st.pyplot()

        st.markdown('***')
        st.subheader('Select Products to see the Quantity sold in Store 5:')
        sales_products_unique=sales_products.drop_duplicates(subset=['product'])
        list = sales_products_unique['product'].to_numpy()
        options = st.multiselect('Select Products:', list)
        options_df=pd.DataFrame(options,columns = ['product'])
        sales_products_5_unique_selected=pd.merge(sales_products_5, options_df, how='inner')
        sales_products_5_unique_selected_quantity=sales_products_5_unique_selected.groupby(['product'])['quantity'].sum().reset_index()
        if not options:
            st.warning('Please add products above.')
        elif options:
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_products_5_unique_selected_quantity_bar=sns.barplot(x='product', y='quantity', palette='Blues_d', data=sales_products_5_unique_selected_quantity)
            sales_products_5_unique_selected_quantity_bar.set(xlabel='Products',ylabel='Quantity Sold')
            sales_products_5_unique_selected_quantity_bar.set_title('Quantity Sold of the selected Products',y=1.02)
            plt.xticks(rotation=30)
            st.pyplot()


    elif product_description == 'Outlet 8':

        st.subheader('Select what you want to see:')

        smallest_largest_8=st.radio(' ',
                                    ('Most Products Sold in Store 8','Least Products Sold in Store 8'))

        if smallest_largest_8=='Most Products Sold in Store 8':

            x = st.number_input('Enter the number of products you want to see:',min_value=4,)
            x=int(x)
            sales_products_8_quantity_largest=sales_products_8_quantity.nlargest(x, ['quantity'])
            st.subheader('Most Products sold in Store 8:')
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_products_8_quantity_largest_bar=sns.barplot(x='product', y='quantity', palette='Blues_d', data=sales_products_8_quantity_largest)
            sales_products_8_quantity_largest_bar.set(xlabel='Products',ylabel='Quantity Sold')
            sales_products_8_quantity_largest_bar.set_title('Most Products Sold',y=1.02)
            plt.xticks(rotation=30)
            st.pyplot()

            st.subheader('Select the Hour of the Day to see the Most Products Sold at this time in store 8:')
            hour_to_filter = st.slider('Hour of the Day:', 0, 23, 17)
            filtered_data = sales_products_8[sales_products_8['transaction_time_filtered'].dt.hour == hour_to_filter]
            sales_products_8_quantity_hour=filtered_data.groupby(['product'])['quantity'].sum().reset_index()
            sales_products_8_quantity_hour_largest=sales_products_8_quantity_hour.nlargest(x, ['quantity'])
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_products_8_quantity_hour_largest_bar=sns.barplot(x='product', y='quantity', palette='Blues_d', data=sales_products_8_quantity_hour_largest)
            sales_products_8_quantity_hour_largest_bar.set(xlabel='Products',ylabel='Quantity Sold')
            sales_products_8_quantity_hour_largest_bar.set_title('Most Products Sold at the chosen time',y=1.02)
            plt.xticks(rotation=30)
            st.pyplot()

        elif smallest_largest_8=='Least Products Sold in Store 8':

            y=st.number_input('Enter the number of products you want to see:', min_value=4,)
            y=int(y)
            sales_products_8_quantity_smallest=sales_products_8_quantity.nsmallest(y, ['quantity'])
            st.subheader('Least Products sold in Store 8:')
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_products_8_quantity_smallest_bar=sns.barplot(x='product', y='quantity', palette='Blues_d', data=sales_products_8_quantity_smallest)
            sales_products_8_quantity_smallest_bar.set(xlabel='Products',ylabel='Quantity Sold')
            sales_products_8_quantity_smallest_bar.set_title('Least Products Sold',y=1.02)
            plt.xticks(rotation=30)
            st.pyplot()

            st.subheader('Select the Hour of the Day to see the Least Products Sold at this time in Store 8:')
            hour_to_filter = st.slider('Hour of the Day:', 0, 23, 17)
            filtered_data = sales_products_8[sales_products_8['transaction_time_filtered'].dt.hour == hour_to_filter]
            sales_products_8_quantity_hour=filtered_data.groupby(['product'])['quantity'].sum().reset_index()
            sales_products_8_quantity_hour_smallest=sales_products_8_quantity_hour.nsmallest(y, ['quantity'])
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_products_8_quantity_hour_smallest_bar=sns.barplot(x='product', y='quantity', palette='Blues_d', data=sales_products_8_quantity_hour_smallest)
            sales_products_8_quantity_hour_smallest_bar.set(xlabel='Products',ylabel='Quantity Sold')
            sales_products_8_quantity_hour_smallest_bar.set_title('Least Products Sold at the chosen time',y=1.02)
            plt.xticks(rotation=30)
            st.pyplot()

        st.markdown('***')
        st.subheader('Select Products to see the Quantity sold in Store 8:')
        sales_products_unique=sales_products.drop_duplicates(subset=['product'])
        list = sales_products_unique['product'].to_numpy()
        options = st.multiselect('Select Products:', list)
        options_df=pd.DataFrame(options,columns = ['product'])
        sales_products_8_unique_selected=pd.merge(sales_products_8, options_df, how='inner')
        sales_products_8_unique_selected_quantity=sales_products_8_unique_selected.groupby(['product'])['quantity'].sum().reset_index()
        if not options:
            st.warning('Please add products above.')
        elif options:
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_products_8_unique_selected_quantity_bar=sns.barplot(x='product', y='quantity', palette='Blues_d', data=sales_products_8_unique_selected_quantity)
            sales_products_8_unique_selected_quantity_bar.set(xlabel='Products',ylabel='Quantity Sold')
            sales_products_8_unique_selected_quantity_bar.set_title('Quantity Sold of the selected Products',y=1.02)
            plt.xticks(rotation=30)
            st.pyplot()


elif button =='Staff Description':

    st.header('Staff Analysis:')
    st.subheader('Select the Store to see the Staff Analysis:')

    staff_description=st.selectbox(
            '',
            ('All','Outlet 3','Outlet 5','Outlet 8'))

    if staff_description == 'All':

        staff=st.radio('',('See All the Staff members:','Choose the Staff members to see:'))

        if staff == 'See All the Staff members:':

            st.subheader('Total Sales by each Staff Member in All the Stores:')
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_staff_total_bar=sns.barplot(x="first_name", y="total", palette="Blues_d", hue='position', order=sales_staff_total.sort_values('total', ascending=False).first_name, data=sales_staff_total)
            sales_staff_total_bar.set(xlabel='Employee Name' ,ylabel='Total Sales')
            sales_staff_total_bar.set_title('Total Sales by each Employee',y=1.02)
            plt.xticks(rotation=90)
            st.pyplot()

        elif staff == 'Choose the Staff members to see:':
            list = sales_staff_total['first_name'].to_numpy()
            options = st.multiselect('Select Staff members:', list)
            options_df=pd.DataFrame(options,columns = ['first_name'])
            sales_staff_total_selected=pd.merge(sales_staff_total, options_df, how='inner' )
            if not options:
                st.warning('Please add products above.')
            elif options:
                st.subheader('Total Sales by the selected Staff Members in All the Stores:')
                plt.rcParams['figure.figsize'] = [16, 13]
                sales_staff_total_selected_bar=sns.barplot(x='first_name', y='total', palette='Blues_d',hue='position',order=sales_staff_total_selected.sort_values('total', ascending=False).first_name, data=sales_staff_total_selected)
                sales_staff_total_selected_bar.set(xlabel='Employee Name' ,ylabel='Total Sales')
                sales_staff_total_selected_bar.set_title('Total Sales by each Employee',y=1.02)
                plt.xticks(rotation=90)
                st.pyplot()


    elif staff_description == 'Outlet 3':

        staff=st.radio('',('See All the Staff members:','Choose the Staff members to see:'))

        if staff == 'See All the Staff members:':

            st.subheader('Total Sales by each Staff Member in Store 3:')
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_staff_3_total_bar=sns.barplot(x="first_name", y="total", palette="Blues_d", hue='position', order=sales_staff_3_total.sort_values('total', ascending=False).first_name, data=sales_staff_3_total)
            sales_staff_3_total_bar.set(xlabel='Employee Name' ,ylabel='Total Sales')
            sales_staff_3_total_bar.set_title('Total Sales by each Employee',y=1.02)
            plt.xticks(rotation=90)
            st.pyplot()

        elif staff == 'Choose the Staff members to see:':
            list = sales_staff_3_total['first_name'].to_numpy()
            options = st.multiselect('Select Staff members:', list)
            options_df=pd.DataFrame(options,columns = ['first_name'])
            sales_staff_3_total_selected=pd.merge(sales_staff_3_total, options_df, how='inner' )
            if not options:
                st.warning('Please add products above.')
            elif options:
                st.subheader('Total Sales by the selected Staff Members in Store 3:')
                plt.rcParams['figure.figsize'] = [16, 13]
                sales_staff_3_total_selected_bar=sns.barplot(x='first_name', y='total', palette='Blues_d',hue='position',order=sales_staff_3_total_selected.sort_values('total', ascending=False).first_name, data=sales_staff_3_total_selected)
                sales_staff_3_total_selected_bar.set(xlabel='Employee Name' ,ylabel='Total Sales')
                sales_staff_3_total_selected_bar.set_title('Total Sales by each Employee',y=1.02)
                plt.xticks(rotation=90)
                st.pyplot()

    elif staff_description == 'Outlet 5':

        staff=st.radio('',('See All the Staff members:','Choose the Staff members to see:'))

        if staff == 'See All the Staff members:':

            st.subheader('Total Sales by each Staff Member in Store 5:')
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_staff_5_total_bar=sns.barplot(x="first_name", y="total", palette="Blues_d", hue='position', order=sales_staff_5_total.sort_values('total', ascending=False).first_name, data=sales_staff_5_total)
            sales_staff_5_total_bar.set(xlabel='Employee Name' ,ylabel='Total Sales')
            sales_staff_5_total_bar.set_title('Total Sales by each Employee',y=1.02)
            plt.xticks(rotation=90)
            st.pyplot()

        elif staff == 'Choose the Staff members to see:':
            list = sales_staff_5_total['first_name'].to_numpy()
            options = st.multiselect('Select Staff members:', list)
            options_df=pd.DataFrame(options,columns = ['first_name'])
            sales_staff_5_total_selected=pd.merge(sales_staff_5_total, options_df, how='inner' )
            if not options:
                st.warning('Please add products above.')
            elif options:
                st.subheader('Total Sales by the selected Staff Members in Store 5:')
                plt.rcParams['figure.figsize'] = [16, 13]
                sales_staff_5_total_selected_bar=sns.barplot(x='first_name', y='total', palette='Blues_d',hue='position',order=sales_staff_5_total_selected.sort_values('total', ascending=False).first_name, data=sales_staff_5_total_selected)
                sales_staff_5_total_selected_bar.set(xlabel='Employee Name' ,ylabel='Total Sales')
                sales_staff_5_total_selected_bar.set_title('Total Sales by each Employee',y=1.02)
                plt.xticks(rotation=90)
                st.pyplot()

    elif staff_description == 'Outlet 8':

        staff=st.radio('',('See All the Staff members:','Choose the Staff members to see:'))

        if staff == 'See All the Staff members:':

            st.subheader('Total Sales by each Staff Member in Store 8:')
            plt.rcParams['figure.figsize'] = [16, 13]
            sales_staff_8_total_bar=sns.barplot(x="first_name", y="total", palette="Blues_d", hue='position', order=sales_staff_8_total.sort_values('total', ascending=False).first_name, data=sales_staff_8_total)
            sales_staff_8_total_bar.set(xlabel='Employee Name' ,ylabel='Total Sales')
            sales_staff_8_total_bar.set_title('Total Sales by each Staff',y=1.02)
            plt.xticks(rotation=90)
            st.pyplot()

        elif staff == 'Choose the Staff members to see:':
            list = sales_staff_8_total['first_name'].to_numpy()
            options = st.multiselect('Select Staff members:', list)
            options_df=pd.DataFrame(options,columns = ['first_name'])
            sales_staff_8_total_selected=pd.merge(sales_staff_8_total, options_df, how='inner' )
            if not options:
                st.warning('Please add products above.')
            elif options:
                st.subheader('Total Sales by the selected Staff Members in Store 8:')
                plt.rcParams['figure.figsize'] = [16, 13]
                sales_staff_8_total_selected_bar=sns.barplot(x='first_name', y='total', palette='Blues_d',hue='position',order=sales_staff_8_total_selected.sort_values('total', ascending=False).first_name, data=sales_staff_8_total_selected)
                sales_staff_8_total_selected_bar.set(xlabel='Employee Name' ,ylabel='Total Sales')
                sales_staff_8_total_selected_bar.set_title('Total Sales by each Employee',y=1.02)
                plt.xticks(rotation=90)
                st.pyplot()
