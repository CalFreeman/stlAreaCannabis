#!/bin/bash

#pass dispensary_id as argument, 
#fetch url text field and curl it.
#scrap 2nd page if exist
#clean up extra files created
declare -a scrap_url
declare DISP_ID=$1

#dispensary_id passed when running script
echo "depo_id: $DISP_ID"

SCRAP_URL=( $(psql -d testdb -U myuser -t -h 0.0.0.0 -p 5432 -c "SELECT url FROM dispensaries WHERE id = '28a2786e-7741-40ca-98d2-07ea464f4950';"))
echo "SCRAP_URL: $SCRAP_URL"
curl $SCRAP_URL >results.json
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