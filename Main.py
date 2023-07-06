import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

"""
Nike_URL = "https://www.nike.com/w/mens-shoes-nik1zy7ok"
Nike = requests.get(Nike_URL)

with open("Nike.html","w") as file:
    file.write(str(Nike.content))
file.close()
"""

#Open and read the local html file
with open("Nike.html",'r',encoding="utf8") as html_file: 
    Nike_page = html_file.read()

#Use lxml as parser for the html Nike page
Nike_Soup = bs(Nike_page,"lxml")

#SHOW THE PAGE CONTENT
#print(Nike_Soup.prettify())

#Extract all the whole shoes from Nike
All_Shoes = Nike_Soup.findAll('div',class_="product-grid__items css-hvew4t")

#Get the web link for the first 20 shoes
Link_Shoes = []
for shoe in All_Shoes:
    for link in shoe.find_all('a',class_="product-card__link-overlay",href = True,limit = 20):
        if link['href'] not in Link_Shoes:
            Link_Shoes.append(link['href'])  #Add the link to the link list
        
#Gather information about each shoe and place them in the shoes list
ShoesList = []
max_widths = [4,3,5,7,6,5]
for link in Link_Shoes:
    ll = requests.get(link)  #Request to enter the website for each shoe then parse it to extract information using beautiful soup
    ss = bs(ll.content,'lxml')
    
    #Attribute Name
    name = ss.find('h1',id = 'pdp_product_title').text
    if(len(name)>max_widths[0]):
        max_widths[0] = len(name)
    
    #Attributes Price - Sale
    if ss.find('div',class_ = "product-price css-11s12ax is--current-price css-tpaepq") is None:
        price = ss.find('div',class_ ="product-price is--current-price css-s56yt7 css-xq7tty").text
        sale = "YES"
    else:
        price = ss.find('div',class_ = "product-price css-11s12ax is--current-price css-tpaepq").text
        sale = "NO"
    if(len(price)>max_widths[2]):
        max_widths[2] = len(price)
    
    
    #Attributes Use - Review - Rating
    use = ss.find('h2',class_="headline-5 pb1-sm d-sm-ib").text
    if(len(use)>max_widths[1]):
        max_widths[1] = len(use)
    
    reviews = ss.find('h3',class_="headline-4 css-xd87ek").text
    if(len(reviews)>max_widths[3]):
        max_widths[3] = len(reviews)
    
    rating = ss.find('p',class_ = "d-sm-ib pl4-sm").text
    if(len(rating)>max_widths[4]):
        max_widths[4] = len(rating)
    
    
    #Place the attributes in a dictionary to add to the list
    shoes = {
        'NAME' : name,
        'USE' : use,
        'PRICE': price,
        'REVIEWS': reviews,
        'RATING': rating,
        'SALE' : sale
    }
    print(name,"was added.")  
    ShoesList.append(shoes)

#Turn the list into a dataframe
Df = pd.DataFrame(ShoesList)

#Initiate a writer to turn the dataframe into an excel file
writer = pd.ExcelWriter('Nike_Shoes.xlsx')
Df.to_excel(writer , index=False, sheet_name= "Shoes")

#Better visualization of the excel file
worksheet = writer.sheets["Shoes"]
columns = ['A:A','B:B','C:C','D:D','E:E','F:F']
for index,value in enumerate(columns):
    worksheet.set_column(value, max_widths[index])  

#Save the excel file
writer.close()

#Read and Print the excel file
a = pd.read_excel('Nike_Shoes.xlsx')
print(a)

