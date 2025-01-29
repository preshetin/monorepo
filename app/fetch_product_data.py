import aiohttp


async def fetch_product_data(artikul: int):
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={artikul}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()

                # Extract the product information
                product = data['data']['products'][0]

                # Extract the required fields
                product_name = product['name']
                article_number = product['id']
                price = product['salePriceU'] / 100  # Assuming the price is in cents
                rating = product['rating']
                
                # Calculate the total quantity across all stocks
                total_quantity = sum(stock['qty'] for stock in product['sizes'][0]['stocks'])                

                product_data = {
                    'name': product_name,
                    'artikul': article_number,
                    'price': price,
                    'rating': rating,
                    'total_quantity': total_quantity
                }

                return product_data
    return None