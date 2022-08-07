#!/bin/bash
curl 'https://stcharles.heyawellness.com/graphql?operationName=FilteredProducts&variables=%7B%22includeEnterpriseSpecials%22%3Afalse%2C%22includeCannabinoids%22%3Atrue%2C%22productsFilter%22%3A%7B%22dispensaryId%22%3A%225f5fae36c702e000fb457605%22%2C%22pricingType%22%3A%22med%22%2C%22strainTypes%22%3A%5B%5D%2C%22subcategories%22%3A%5B%5D%2C%22Status%22%3A%22Active%22%2C%22types%22%3A%5B%22Flower%22%5D%2C%22useCache%22%3Afalse%2C%22sortDirection%22%3A1%2C%22sortBy%22%3Anull%2C%22isDefaultSort%22%3Atrue%2C%22bypassOnlineThresholds%22%3Afalse%2C%22isKioskMenu%22%3Afalse%2C%22removeProductsBelowOptionThresholds%22%3Atrue%7D%2C%22page%22%3A0%2C%22perPage%22%3A50%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22aca5bbf9093bf1ccd28d3d9f010de5cd18e50dcbe96e4ddcda1e530fc0eabe2b%22%7D%7D' >results.json
cat results.json |jq .data[].products[].Status >status
cat results.json |jq .data[].products[].Prices[] >prices
cat results.json |jq .data[].products[].strainType >strains
cat results.json |jq .data[].products[].Image >images
cat results.json |jq .data[].products[].Name >names
cat results.json |jq .data[].products[].POSMetaData.children[].quantityAvailable >quantity
cat results.json |jq .data[].products[].type >types
cat results.json |jq .data[].products[].POSMetaData.canonicalBrandName >brands
cat results.json |jq .data[].products[].POSMetaData.children[].option >grams

echo "[" >final.json

for i in {1..50}
do
        brand="\"brand\":"$(head -q -n$i brands |tail -n1)
        gram="\"gram\":"$(head -q -n$i grams |tail -n1)
        image="\"image\":"$(head -q -n$i images |tail -n1)
        name="\"name\":"$(head -q -n$i names |tail -n1)
        price="\"price\":"$(head -q -n$i prices |tail -n1)
        quantity="\"quantity\":"$(head -q -n$i quantity |tail -n1)
        status="\"status\":"$(head -q -n$i status |tail -n1)
        strain="\"strain\":"$(head -q -n$i strains |tail -n1)
        type="\"type\":"$(head -q -n$i types |tail -n1)

        line="{${brand},${gram},${image},${name},${price},${quantity},${status},${strain},${type}},"
        echo $line >>final.json
done

echo "]" >>final.json